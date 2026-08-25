# scripts

薄封装，只固化已验证的运行时命令。默认 solo runtime 与客户端绑定见
`../protocol/runtime.md`。

- `tmux-solo-setup.sh <session> <canonical> [seat=worktree ...]` —— 打开一个 canonical window 与 owner
  已准备的长期 worktree windows；不创建/移动/删除 Git worktree；
- `tmux-codex-start.sh <session> <window> <cwd> [codex args...]` —— 在精确 shell pane 启动或 resume Codex，
  校验 cwd、清禁色变量并固定 `--cd`；
- [TMUX-RUNBOOK.md](TMUX-RUNBOOK.md) —— 当前默认的 tmux + solo Goal owner 操作手册；
- 以下 Herdr/pair 工具只保留为 owner 明确启用的双角色兼容路径：
- `pair-setup.sh <spec-dir> [delivery-dir] [label] [spec-kind] [delivery-kind]` —— 建命名 pair；
  默认 `<session>-spec=codex`、`<session>-delivery=opencode`，也可通过 kind 参数替换客户端；
  OpenCode 默认带官方 `--auto`，自动批准所有非显式 deny 的 permission request；
- `herdr-setup.sh <work-repo> [codex-dir] [label]` —— 旧 Claude/Codex 组合的兼容入口；
- `herdr-agent-start.sh <name> <kind> <pane> [runtime args...]` —— 新建和 resume 的唯一启动入口；
  准备 truecolor pane 环境，把 Codex `--cd` 固定到 pane 的现存 worktree，并对活进程做禁色变量断言；
- `herdr-federation.py peers|resolve|verify` —— `baton.sh` 的实时 instance 计算器；正常只看当前 session，
  无缓存、无轮询，跨-session 仅保留为事故兼容；
- `baton.sh peers|send|wait|read|escalate` —— 当前 session 内的名称路由与门铃 helper；默认 `default`。
- `worktree-audit.py <repo-root>` —— 一次性对账 linked worktree 与全部活 agent cwd；出现
  `CLEAN_UNOWNED` 或 `DIRTY_UNOWNED` 返回 3，迁移/关闭 agent 后必须清零或升级，不轮询；
- `owner-turns.py` / `stop-turns.py` —— Claude/Codex JSONL 复盘；OpenCode 先经
  `opencode-turns.py <session-id>` 归一后从 stdin 输入。
- [HERDR-RUNBOOK.md](HERDR-RUNBOOK.md) —— Herdr 0.8.0 兼容手册；不用临场试错学习 Herdr。

所有长期 solo 席位使用产品域的稳定 tmux session，各自绑定 owner 预置的 window/worktree；Goal 切换只换
branch。tmux 不做状态检测、门铃或 agent-to-agent 自动通信；恢复后由 owner 人工核 native session、cwd、
必要 MCP 与一次完整 prompt 回复。

Codex 权限由用户级配置统一提供；本机采用 `:danger-full-access` + `approval_policy=never`。
tmux helper 清除宿主禁色变量、固定 cwd；Herdr 兼容 helper 另做活进程环境断言。Codex 同时关闭当前
会打断内置 `codex_apps` MCP 的实验 `network_proxy`；普通网络能力不受影响。OpenCode 兼容路径除全局 permission 外仍在启动时带
`--auto`，避免存量 `ask` 或项目级规则让非交互 pair 停在确认框；显式 `deny` 仍生效。

送达验证由 `baton.sh send` 自动完成：idle Codex 先观察 prompt 生命周期变化，再读回 delivery id；
working Codex 使用已 qualification 的 Tab 队列；OpenCode alternate-screen 无法稳定读回，使用
prompt API 成功 + 状态转移。runtime working 队列只允许已完成 qualification 的组合。通知开关在
`~/.config/herdr/config.toml`（`ui.toast.delivery`，默认 off，本机已设 system）。

原则：只放薄封装。开始想写调度器、状态机、tmux 自动注入消息或 delivery ack 时，先按 README 当前治理
重评是否真的需要 Herdr 兼容路径。不提供 idle heartbeat/backstop。
