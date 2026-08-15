#!/usr/bin/env bash
# 搭建一个 duet 试运行 workspace：两个 pane（Claude Code / Codex），平级接力棒。
#
# 用法：
#   ./herdr-setup.sh <work-repo> [codex-dir] [label]
#     work-repo   Claude pane 的工作目录（工作仓库，如 ~/Workspace/byteme_mobile-D）
#     codex-dir   Codex pane 的工作目录（默认同 work-repo；建议给 Codex 独立 worktree）
#     label       workspace 标签（默认 duet-<repo 名>）
#
# 验证记录（2026-08-15，herdr 0.8.0）：
#   - pane read 用 --source visible / detection；--source recent 不稳，勿用；
#   - codex 首次启动有目录 trust 提示（状态 blocked），owner attach 后确认；
#   - 通知需 ~/.config/herdr/config.toml 设 ui.toast.delivery（本机已设 system）。
set -euo pipefail

WORK_REPO="${1:?用法: herdr-setup.sh <work-repo> [codex-dir] [label]}"
CODEX_DIR="${2:-$WORK_REPO}"
LABEL="${3:-duet-$(basename "$WORK_REPO")}"

WORK_REPO="$(cd "$WORK_REPO" && pwd)"
CODEX_DIR="$(cd "$CODEX_DIR" && pwd)"

# 1. server 不在就拉起
if ! herdr status server 2>/dev/null | grep -q "status: running"; then
  nohup herdr server >/dev/null 2>&1 &
  sleep 2
fi

# 2. 同名 workspace 已存在则拒绝重建（幂等保护）
if herdr workspace list 2>/dev/null | python3 -c "
import json,sys
ws=json.load(sys.stdin)['result']['workspaces']
sys.exit(0 if any(w.get('label')=='$LABEL' for w in ws) else 1)" 2>/dev/null; then
  echo "workspace '$LABEL' 已存在；attach 用: herdr" >&2
  exit 1
fi

# 3. 建 workspace（p1=Claude）并 split（p2=Codex）
CREATE_JSON="$(herdr workspace create --cwd "$WORK_REPO" --label "$LABEL")"
P1="$(echo "$CREATE_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')"
SPLIT_JSON="$(herdr pane split "$P1" --direction right)"
P2="$(echo "$SPLIT_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')"

# 4. 启动两个 agent（trust/权限提示留给 attach 的 owner 处理）
herdr pane send-text "$P1" "claude" && herdr pane send-keys "$P1" enter
herdr pane send-text "$P2" "cd $CODEX_DIR && codex" && herdr pane send-keys "$P2" enter

cat <<DONE
workspace: $LABEL
  $P1  claude  @ $WORK_REPO
  $P2  codex   @ $CODEX_DIR
旁观: 任意终端运行 herdr
传棒: scripts/baton.sh send <对方pane> <自己角色> "<事件 · 路径 · 轮次>"
DONE
