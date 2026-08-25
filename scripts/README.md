# scripts

当前默认只需要：

- `herdr-agent-start.sh <name> <kind> <pane> [runtime args...]`：在固定 Herdr pane 启动或 resume agent；
- [HERDR-RUNBOOK.md](HERDR-RUNBOOK.md)：默认 Herdr + solo Goal 操作手册；
- `worktree-audit.py <repo-root>`：需要时做一次只读拓扑对账。

`baton.sh`、`pair-*` 和 `herdr-federation.py` 是旧双角色兼容工具；tmux helper/runbook 是事故兼容路径。
除非 owner 明确要求，不要启动、修改或扩展这些兼容机制。
