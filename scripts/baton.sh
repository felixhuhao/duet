#!/usr/bin/env bash
# 门铃 helper：传棒 / 等待 / 读 pane / escalate 通知。协议见 protocol/baton.md。
#
# 用法：
#   baton.sh send <to-pane> <from-role> <message>
#       组装 "[peer:<from-role>] <message>" 注入对方输入框并回车。
#       message 只放：事件 · 文件路径 · 轮次 · verdict。不放内容摘要。
#   baton.sh wait <pane> [state]
#       阻塞等待对方状态（默认 idle；可 blocked/done）。放后台跑，翻转即返回。
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
    herdr pane send-keys "$to" enter
    echo "baton → $to : $msg"
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
