# scripts

薄封装，只固化已验证的运行时命令（herdr 0.8.0，2026-08-15 验证）。

- `herdr-setup.sh <work-repo> [codex-dir] [label]` —— 建试运行 workspace：
  p1 Claude Code、p2 Codex，幂等保护，agent 的 trust/权限提示留给 attach 的 owner；
- `baton.sh send|wait|read|escalate` —— 门铃 helper，协议见 `protocol/baton.md`。

已知坑：`pane read --source recent` 不稳，一律用 `visible`；通知开关在
`~/.config/herdr/config.toml`（`ui.toast.delivery`，默认 off，本机已设 system）。

原则：只放薄封装。开始想写调度器/状态机时，先重评 loopx（见 README 拍板记录）。
