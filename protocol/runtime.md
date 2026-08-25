# Runtime 协议

默认 runtime 是 Herdr `default` session + 长期 worktree。一个 solo Goal owner 使用一个固定 agent 席位。

## 固定拓扑

- canonical 主树独立 workspace，负责规划、合并和真源维护；
- `dev1/dev2/...` 各绑定 owner 预置的 `wt1/wt2/...` workspace 和长期 worktree；
- idle 时使用同名分支 `wt1/wt2/...`，换 Goal 只换 branch，不换 workspace 或 cwd；
- worktree 的创建、移动和删除只由 owner 安排；
- 同一 native session 禁止跨 Herdr、tmux 或其他 terminal 双开。

## 两种状态不要混

Herdr 的 `working/blocked/idle/done/unknown` 只描述 agent 当前是否可交互。`done` 与 `idle` 都表示可接收
下一 turn；`unknown` 必须进入 pane 核实。

Goal 的 `QUEUED/ACTIVE/BLOCKED/DONE/CANCELLED` 由 Goal 文件和 Git 裁决。agent 显示 `done` 不代表代码
已合并，也不代表 AC 已满足。

## 席位记录

每个 active Goal 记录一行即可：

```text
owner=<name> · herdr=default/<agent> · pane=<id> · native_session=<id> · cwd=<path> · branch=<branch>
```

native session ID 用于恢复 conversation；Goal 文件与 Git 用于冷恢复工作。两者都要留，不能互相替代。

## 启动与恢复

只使用 `scripts/herdr-agent-start.sh` 新建或 resume。完成后确认：

1. agent name、pane 和 cwd 正确；
2. native session ID 正确；
3. branch/HEAD 与 Goal 一致；
4. Herdr 状态可识别且 agent 能正常回复。

原 session 无法恢复时才 cold start，并先从项目规则、Goal、当前 HEAD 和未验证面恢复上下文。

## 通信边界

owner 通过 Herdr 面板直接进入目标 pane，或发送明确的人工消息。默认不启用 agent-to-agent 自动传棒、
baton、heartbeat 或 delivery acknowledgement。独立 reviewer 只检查冻结 diff，不与 Goal owner 组成常驻 pair。

tmux 仅作为事故兼容路径；迁移 runtime 前必须等 agent 可接收输入、安全退出旧进程，再 resume 原 session。
