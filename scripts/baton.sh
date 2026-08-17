#!/usr/bin/env bash
# 门铃 helper：跨 session 传棒 / 状态 / 等待 / 读 pane / escalate。协议见 protocol/baton.md。
#
# 用法：
#   baton.sh peers [--json]
#       实时列出所有 running Herdr session 中的命名 agent；不轮询、不缓存。
#   baton.sh send <to-agent-name> <from-role> <message>
#       组装 "[peer:<from-role>] <message>"，按目标 runtime 的已验证方式投递并读回。
#       message 只放：事件 · 文件路径 · 轮次 · verdict。不放内容摘要。
#   baton.sh wait <pane> [state]
#       阻塞等待对方状态。⚠️ 协议主循环不用它（交棒是 push,见 protocol/baton.md）;
#       仅供 owner 排查卡死（--until blocked）。
#   baton.sh read <pane> [lines]
#       读 pane 可见内容（--source visible；recent 不稳勿用）。
#   baton.sh escalate <type> <summary> <path>
#       系统通知 owner。type ∈ round-cap|P0P1-dispute|open-decision|redline-risk|baton-confirm
#       发完记得把 agent 建议写进 duet:calibration/decision-log.md（escalation 协议要求）。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FEDERATION="$SCRIPT_DIR/herdr-federation.py"

resolve_target() {
  python3 "$FEDERATION" resolve "$1"
}

route_field() {
  printf '%s\n' "$1" | python3 -c 'import json,sys; print(json.load(sys.stdin)[sys.argv[1]])' "$2"
}

hcmd() {
  local target_session_name="$1"; shift
  herdr --session "$target_session_name" "$@"
}

prompt_opencode() {
  prompt_response="$(hcmd "$target_session" agent prompt "$target_name" "$msg" --wait \
    --until working --until idle --until done --until blocked --timeout 10000)"
  if ! printf '%s\n' "$prompt_response" | python3 -c '
import json,sys
r=json.load(sys.stdin)
sys.exit(0 if "result" in r and "error" not in r else 1)'; then
    printf '%s\n' "$prompt_response" >&2
    echo "DELIVERY FAILED: OpenCode prompt 未观察到状态转移" >&2
    exit 4
  fi
  prompt_confirmed=true
}

cmd="${1:?用法见文件头}"; shift
case "$cmd" in
  peers)
    python3 "$FEDERATION" peers "$@"
    ;;
  send)
    to="${1:?to-agent-name}"; from="${2:?from-role}"; shift 2
    delivery_id="d$(date +%s)-$$"
    msg="[peer:$from] [delivery:$delivery_id] $*"
    route="$(resolve_target "$to")"
    target_name="$(route_field "$route" name)"
    target_session="$(route_field "$route" session)"
    kind="$(route_field "$route" kind)"
    status="$(route_field "$route" status)"
    pane="$(route_field "$route" pane)"
    prompt_confirmed=false
    case "$kind:$status" in
      *:blocked)
        echo "DELIVERY DEFERRED: $to 正在等待批准/回答；普通门铃不得写入交互 UI" >&2
        exit 5
        ;;
      codex:working)
        hcmd "$target_session" pane send-text "$pane" "$msg"
        sleep 1
        hcmd "$target_session" pane send-keys "$pane" tab
        ;;
      opencode:working)
        # OpenCode 1.18 的 working prompt 会并入当前 turn（温和 steering），不是下一 turn。
        # 因此把一次 event-driven settle wait 作为 push 送达动作的一部分；不做轮询。
        hcmd "$target_session" agent wait "$target_name" --until idle --until done \
          --timeout "${DUET_DELIVERY_TIMEOUT_MS:-300000}" >/dev/null
        prompt_opencode
        ;;
      claude:working)
        hcmd "$target_session" agent prompt "$target_name" "$msg"
        ;;
      *:working)
        echo "runtime '$kind' 的 working 投递未 qualification；拒绝普通门铃" >&2
        exit 3
        ;;
      opencode:*)
        prompt_opencode
        ;;
      *)
        hcmd "$target_session" agent prompt "$target_name" "$msg"
        ;;
    esac
    sleep 1
    seen="$(hcmd "$target_session" agent read "$target_name" --source recent-unwrapped --lines 200 2>/dev/null || true)"
    if ! printf '%s\n' "$seen" | tr -d '[:space:]' | grep -Fq "$delivery_id"; then
      seen="$(hcmd "$target_session" agent read "$target_name" --source visible --lines 200 2>/dev/null || true)"
    fi
    if ! printf '%s\n' "$seen" | tr -d '[:space:]' | grep -Fq "$delivery_id"; then
      if [ "$kind" = "opencode" ] && [ "$prompt_confirmed" = true ]; then
        echo "baton delivered → $target_session/$target_name ($kind/$status) · $delivery_id · state-confirmed"
        exit 0
      fi
      echo "DELIVERY FAILED: $delivery_id 未从目标读回；禁止宣布交棒" >&2; exit 4
    fi
    echo "baton delivered → $target_session/$target_name ($kind/$status) · $delivery_id"
    ;;
  wait)
    target="${1:?agent-name}"; state="${2:-idle}"
    route="$(resolve_target "$target")"
    hcmd "$(route_field "$route" session)" agent wait "$(route_field "$route" name)" --until "$state"
    ;;
  read)
    target="${1:?agent-name}"; lines="${2:-40}"
    route="$(resolve_target "$target")"
    hcmd "$(route_field "$route" session)" agent read "$(route_field "$route" name)" \
      --source recent-unwrapped --lines "$lines"
    ;;
  escalate)
    type="${1:?type}"; summary="${2:?summary}"; path="${3:-}"
    response="$(herdr notification show "duet escalate [$type]: $summary" --body "$path")"
    shown="$(printf '%s\n' "$response" | python3 -c '
import json,sys
r=json.load(sys.stdin).get("result", {})
print("false" if r.get("shown") is False else "true")')"
    if [ "$shown" = "false" ]; then
      printf '%s\n' "$response" >&2
      echo "ESCALATION DELIVERY FAILED: notification 未显示；按 capability fallback 交给 peer/owner" >&2
      exit 6
    fi
    echo "已通知 owner。勿忘: decision-log 记一行（含 agent 建议）；看板卡仅在 owner 需要排期跟踪时创建。"
    ;;
  *)
    echo "未知命令: $cmd（peers|send|wait|read|escalate）" >&2; exit 2
    ;;
esac
