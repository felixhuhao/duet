# scripts

薄封装，只固化已验证的运行时命令（herdr 0.8.0）。职责角色与客户端绑定见
`../protocol/runtime.md`。

- `pair-setup.sh <spec-dir> [delivery-dir] [label] [spec-kind] [delivery-kind]` —— 建命名 pair；
  默认 `<session>-spec=codex`、`<session>-delivery=opencode`，也可通过 kind 参数替换客户端；
  OpenCode 默认带官方 `--auto`，自动批准所有非显式 deny 的 permission request；
- `herdr-setup.sh <work-repo> [codex-dir] [label]` —— 旧 Claude/Codex 组合的兼容入口；
- `herdr-agent-start.sh <name> <kind> <pane> [runtime args...]` —— 新建和 resume 的唯一启动入口；
  准备 truecolor pane 环境，并对活 Codex 进程做禁色变量断言；
- `herdr-federation.py peers|resolve|verify` —— `baton.sh` 的实时 instance 计算器；正常只看当前 session，
  无缓存、无轮询，跨-session 仅保留为事故兼容；
- `baton.sh peers|send|wait|read|escalate` —— 当前 session 内的名称路由与门铃 helper；默认 `default`。
- `worktree-audit.py <repo-root>` —— 一次性对账 linked worktree 与全部活 agent cwd；出现
  `CLEAN_UNOWNED` 或 `DIRTY_UNOWNED` 返回 3，迁移/关闭 agent 后必须清零或升级，不轮询；
- `owner-turns.py` / `stop-turns.py` —— Claude/Codex JSONL 复盘；OpenCode 先经
  `opencode-turns.py <session-id>` 归一后从 stdin 输入。
- [HERDR-RUNBOOK.md](HERDR-RUNBOOK.md) —— Herdr 0.8.0 owner 轨操作手册：default session、
  agent 创建、跨 Goal resume、门铃、worktree 生命周期与故障恢复；
  不用临场试错学习 Herdr。

所有长期 agent 席位使用 Herdr `default` session，各自占独立 workspace/工作树；terminal 直接运行
`herdr` 即可统一查看。实例名在该 session 内唯一（推荐稳定的 `dev1/dev2` 或
`<pair>-spec/delivery`）。名字是路由，
`instance_id` 才标识本次进程；`baton.sh send` 会在提交前后校验并把它写入门铃。恢复时保留名字：
Codex 用 `herdr-agent-start.sh ... resume <session-id> --disable network_proxy`；
OpenCode 用 `herdr-agent-start.sh ... --session <session-id> --auto`。恢复后必须用上一轮 delivery id
做一次上下文连续性检查，并用 `baton.sh peers` 取得新的 instance_id。

Codex 权限由用户级配置统一提供；本机采用 `:danger-full-access` + `approval_policy=never`，
无需再按 Herdr session 维护 socket allowlist。唯一启动 helper 会清除宿主注入的 `NO_COLOR/CODEX_CI`、
固定 truecolor terminal，并检查 Codex 活进程确实继承；Codex 同时关闭当前会打断内置
`codex_apps` MCP 的实验 `network_proxy`；普通网络
能力不受影响。OpenCode 除全局 permission 外仍在启动时带
`--auto`，避免存量 `ask` 或项目级规则让非交互 pair 停在确认框；显式 `deny` 仍生效。

送达验证由 `baton.sh send` 自动完成：idle Codex 先观察 prompt 生命周期变化，再读回 delivery id；
working Codex 使用已 qualification 的 Tab 队列；OpenCode alternate-screen 无法稳定读回，使用
prompt API 成功 + 状态转移。runtime working 队列只允许已完成 qualification 的组合。通知开关在
`~/.config/herdr/config.toml`（`ui.toast.delivery`，默认 off，本机已设 system）。

原则：只放薄封装。开始想写调度器/状态机时，先按 README 当前治理重评是否真的需要 loopx。
不提供 idle heartbeat/backstop：空闲 pair 保持静默，仅由真实消息或 blocked 事件唤醒。
