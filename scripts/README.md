# scripts

薄封装，只固化已验证的运行时命令（herdr 0.8.0）。职责角色与客户端绑定见
`../protocol/runtime.md`。

- `pair-setup.sh <spec-dir> [delivery-dir] [label] [spec-kind] [delivery-kind]` —— 建命名 pair；
  默认 `role1=codex` 承担 spec_owner、`role2=opencode` 承担 delivery_owner；
- `herdr-setup.sh <work-repo> [codex-dir] [label]` —— 旧 Claude/Codex 组合的兼容入口；
- `baton.sh send|wait|read|escalate` —— 门铃 helper，协议见 `protocol/baton.md`。
- `owner-turns.py` / `stop-turns.py` —— Claude/Codex JSONL 复盘；OpenCode 先经
  `opencode-turns.py <session-id>` 归一后从 stdin 输入。

恢复已命名 pair 时保留原 pane 与名字：Codex 用 `herdr agent start ... -- resume <session-id>`；
OpenCode 用 `herdr agent start ... -- --session <session-id>`。恢复后必须用上一轮 delivery id
做一次上下文连续性检查。

送达验证由 `baton.sh send` 自动附 delivery id 并读回；runtime working 队列只允许已完成
qualification 的组合。通知开关在
`~/.config/herdr/config.toml`（`ui.toast.delivery`，默认 off，本机已设 system）。

原则：只放薄封装。开始想写调度器/状态机时，先重评 loopx（见 README 拍板记录）。
