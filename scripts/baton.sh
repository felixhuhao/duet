#!/usr/bin/env bash
# 门铃 helper：传棒 / 等待 / 读 pane / escalate 通知。协议见 protocol/baton.md。
#
# 用法：
#   baton.sh send <to-pane> <from-role> <message>
#       组装 "[peer:<from-role>] <message>" 注入对方输入框并回车。
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
    to="${1:?to-pane}"; from="${2:?from-role}"; shift 2
    msg="[peer:$from] $*"
    herdr pane send-text "$to" "$msg"
    # 状态感知投递（单次查询，非监听）：忙碌的 codex 用 Tab 入 runtime 队列
    # （实测 2026-08-15：turn 结束才投递，零 steering 污染）；其余 Enter 直投。
    # stop 类要打断 → 别用本脚本，直接 herdr send-keys enter（steering 是 stop 特权）。
    st=$(herdr agent list 2>/dev/null | python3 -c "import json,sys; a=[x for x in json.load(sys.stdin)['result']['agents'] if x['pane_id']=='$to']; print(a[0]['agent']+':'+a[0]['agent_status'] if a else 'none')" 2>/dev/null)
    sleep 1   # 实测坑：send-text 后立刻发按键会丢（TUI 未渲染完）
    case "$st" in
      codex:working) herdr pane send-keys "$to" tab; echo "baton ⇥ 入队 → $to : $msg" ;;
      *) herdr pane send-keys "$to" enter; echo "baton → $to : $msg" ;;
    esac
    ;;
  wait)
    pane="${1:?pane}"; state="${2:-idle}"
    herdr agent wait "$pane" --until "$state"
    ;;
  read)
    pane="${1:?pane}"; lines="${2:-40}"
    herdr pane read "$pane" --source visible --lines "$lines"
    ;;
  escalate)
    type="${1:?type}"; summary="${2:?summary}"; path="${3:-}"
    herdr notification show "duet escalate [$type]: $summary" --body "$path"
    echo "已通知 owner。勿忘: decision-log 记一行（含 agent 建议），open-decision 类另建看板卡。"
    ;;
  *)
    echo "未知命令: $cmd（send|wait|read|escalate）" >&2; exit 2
    ;;
esac
