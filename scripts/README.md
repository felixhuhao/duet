# scripts

薄封装，只固化已验证的运行时命令（herdr 0.8.0）。职责角色与客户端绑定见
`../protocol/runtime.md`。

- `pair-setup.sh <spec-dir> [delivery-dir] [label] [spec-kind] [delivery-kind]` —— 建命名 pair；
  默认 `<session>-spec=codex`、`<session>-delivery=opencode`，也可通过 kind 参数替换客户端；
  OpenCode 默认带官方 `--auto`，自动批准所有非显式 deny 的 permission request；
- `herdr-setup.sh <work-repo> [codex-dir] [label]` —— 旧 Claude/Codex 组合的兼容入口；
- `herdr-federation.py peers|resolve|verify` —— 聚合 running sessions，并从 terminal + 前台进程
  计算本次 incarnation；不缓存、不轮询；
- `baton.sh peers|send|wait|read|escalate` —— 全局名称路由与门铃 helper。
- `owner-turns.py` / `stop-turns.py` —— Claude/Codex JSONL 复盘；OpenCode 先经
  `opencode-turns.py <session-id>` 归一后从 stdin 输入。

每个 pair 使用独立 workspace/工作树；可独占命名 session，也可在 owner 需要统一 sidebar 时与
其他 pair 共用 session。实例名始终须全局唯一（推荐 `<pair>-spec/delivery`）。名字是路由，
`instance_id` 才标识本次进程；`baton.sh send` 会在提交前后校验并把它写入门铃。恢复时保留名字：
Codex 用 `herdr agent start ... -- resume <session-id>`；
OpenCode 用 `herdr agent start ... -- --session <session-id> --auto`。恢复后必须用上一轮 delivery id
做一次上下文连续性检查，并用 `baton.sh peers` 取得新的 instance_id。

Codex 权限由用户级配置统一提供；本机采用 `:danger-full-access` + `approval_policy=never`，
无需再按 Herdr session 维护 socket allowlist。OpenCode 除全局 permission 外仍在启动时带
`--auto`，避免存量 `ask` 或项目级规则让非交互 pair 停在确认框；显式 `deny` 仍生效。

送达验证由 `baton.sh send` 自动完成：Codex 读回 delivery id；OpenCode alternate-screen
无法稳定读回，使用 prompt API 成功 + 状态转移。runtime working 队列只允许已完成
qualification 的组合。通知开关在
`~/.config/herdr/config.toml`（`ui.toast.delivery`，默认 off，本机已设 system）。

原则：只放薄封装。开始想写调度器/状态机时，先按 README 当前治理重评是否真的需要 loopx。
不提供 idle heartbeat/backstop：空闲 pair 保持静默，仅由真实消息或 blocked 事件唤醒。
