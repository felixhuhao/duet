#!/usr/bin/env bash
# 门铃 helper：传棒 / 等待 / 读 pane / escalate 通知。协议见 protocol/baton.md。
#
# 用法：
#   baton.sh send <to-agent-or-pane> <from-role> <message>
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

cmd="${1:?用法见文件头}"; shift
case "$cmd" in
  send)
    to="${1:?to-agent-or-pane}"; from="${2:?from-role}"; shift 2
    delivery_id="d$(date +%s)-$$"
    msg="[peer:$from] [delivery:$delivery_id] $*"
    info=$(herdr agent list 2>/dev/null | python3 -c '
import json,sys
t=sys.argv[1]; xs=json.load(sys.stdin)["result"]["agents"]
a=[x for x in xs if t in (x.get("pane_id"),x.get("name"),x.get("agent_name"))]
if not a: raise SystemExit(1)
x=a[0]; print("|".join((x.get("agent","unknown"),x.get("agent_status","unknown"),x["pane_id"])))' "$to")
    kind="${info%%|*}"; rest="${info#*|}"; status="${rest%%|*}"; pane="${rest##*|}"
    case "$kind:$status" in
      *:blocked)
        echo "DELIVERY DEFERRED: $to 正在等待批准/回答；普通门铃不得写入交互 UI" >&2
        exit 5
        ;;
      codex:working)
        herdr pane send-text "$pane" "$msg"
        sleep 1
        herdr pane send-keys "$pane" tab
        ;;
      opencode:working)
        # OpenCode 1.18 的 working prompt 会并入当前 turn（温和 steering），不是下一 turn。
        # 因此把一次 event-driven settle wait 作为 push 送达动作的一部分；不做轮询。
        herdr agent wait "$to" --until idle --until done \
          --timeout "${DUET_DELIVERY_TIMEOUT_MS:-300000}" >/dev/null
        herdr agent prompt "$to" "$msg"
        ;;
      claude:working)
        herdr agent prompt "$to" "$msg"
        ;;
      *:working)
        echo "runtime '$kind' 的 working 投递未 qualification；拒绝普通门铃" >&2
        exit 3
        ;;
      *)
        herdr agent prompt "$to" "$msg"
        ;;
    esac
    sleep 1
    seen="$(herdr agent read "$to" --source recent-unwrapped --lines 200 2>/dev/null || true)"
    if ! printf '%s\n' "$seen" | grep -Fq "$delivery_id"; then
      seen="$(herdr agent read "$to" --source visible --lines 200 2>/dev/null || true)"
    fi
    if ! printf '%s\n' "$seen" | grep -Fq "$delivery_id"; then
      echo "DELIVERY FAILED: $delivery_id 未从目标读回；禁止宣布交棒" >&2
      exit 4
    fi
    echo "baton delivered → $to ($kind/$status) · $delivery_id"
    ;;
  wait)
    target="${1:?agent-or-pane}"; state="${2:-idle}"
    herdr agent wait "$target" --until "$state"
    ;;
  read)
    target="${1:?agent-or-pane}"; lines="${2:-40}"
    herdr agent read "$target" --source recent-unwrapped --lines "$lines"
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
    echo "已通知 owner。勿忘: decision-log 记一行（含 agent 建议），open-decision 类另建看板卡。"
    ;;
  *)
    echo "未知命令: $cmd（send|wait|read|escalate）" >&2; exit 2
    ;;
esac
