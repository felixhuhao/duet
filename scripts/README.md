# scripts

当前默认只需要两个 helper：

- `tmux-solo-setup.sh <session> <canonical> [seat=worktree ...]`：为已有 worktree 创建固定 windows；
- `tmux-codex-start.sh <session> <window> <cwd> [codex args...]`：在精确 pane 启动或 resume Codex。

完整命令和恢复步骤见 [TMUX-RUNBOOK.md](TMUX-RUNBOOK.md)。helper 不创建/移动/删除 worktree，不切 branch，
也不发送 agent-to-agent 消息。

其余 `herdr-*`、`pair-*`、`baton.sh` 和 `HERDR-RUNBOOK.md` 是旧 Herdr/pair 的兼容工具。除非 owner
明确要求，不要启动、修改或扩展它们。`worktree-audit.py` 仍可用于只读对账。
