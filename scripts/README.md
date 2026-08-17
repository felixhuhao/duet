# scripts

薄封装，只固化已验证的运行时命令（herdr 0.8.0）。职责角色与客户端绑定见
`../protocol/runtime.md`。

- `pair-setup.sh <spec-dir> [delivery-dir] [label] [spec-kind] [delivery-kind]` —— 建命名 pair；
  默认 `<session>-spec=codex`、`<session>-delivery=opencode`，也可通过 kind 参数替换客户端；
- `herdr-setup.sh <work-repo> [codex-dir] [label]` —— 旧 Claude/Codex 组合的兼容入口；
- `herdr-federation.py peers|resolve` —— 聚合 running sessions，不缓存、不轮询；
- `baton.sh peers|send|wait|read|escalate` —— 全局名称路由与门铃 helper。
- `owner-turns.py` / `stop-turns.py` —— Claude/Codex JSONL 复盘；OpenCode 先经
  `opencode-turns.py <session-id>` 归一后从 stdin 输入。

每个 pair 使用独立命名 session，实例名须全局唯一（推荐 `<pair>-spec/delivery`）。恢复时保留名字：
Codex 用 `herdr agent start ... -- resume <session-id>`；
OpenCode 用 `herdr agent start ... -- --session <session-id>`。恢复后必须用上一轮 delivery id
做一次上下文连续性检查。

Codex 通过 `workspace-full` permission profile 访问 Herdr；每新增命名 session，须把它的
`herdr.sock` 精确加入该 profile 的 `network.unix_sockets` allowlist，再启动/恢复 Codex。

送达验证由 `baton.sh send` 自动完成：Codex 读回 delivery id；OpenCode alternate-screen
无法稳定读回，使用 prompt API 成功 + 状态转移。runtime working 队列只允许已完成
qualification 的组合。通知开关在
`~/.config/herdr/config.toml`（`ui.toast.delivery`，默认 off，本机已设 system）。

原则：只放薄封装。开始想写调度器/状态机时，先按 README 当前治理重评是否真的需要 loopx。
不提供 idle heartbeat/backstop：空闲 pair 保持静默，仅由真实消息或 blocked 事件唤醒。
