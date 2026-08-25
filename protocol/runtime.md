# Runtime 绑定与资格协议

默认运行形态是 solo Goal：一个 `goal_owner` 从 Contract 到 Completion Package 负责到底。职责角色与客户端
仍解耦，但 `spec_owner/delivery_owner` 只在独立 review 例外中绑定，不再为每个 Goal 常驻成 pair。tmux
的具体创建、resume、固定 worktree 与事故恢复命令见
[`scripts/TMUX-RUNBOOK.md`](../scripts/TMUX-RUNBOOK.md)。

## 唯一默认拓扑

一个产品域使用一个稳定 tmux session，例如 `mobile`；canonical 主树占 `main` window，owner 预置的长期
worktree 各占 `dev1/dev2/...` window。terminal 关闭只 detach，Goal 切换只换 branch，不换 cwd、window
或 native session。worktree 创建、移动、删除只由 owner 安排；worker/reviewer/orchestrator 禁止为任务
临时建树。

tmux 只提供 PTY、布局和进程保活，不提供 agent identity、语义状态、消息送达或审批检测。日常不以
`send-keys/capture-pane` 建 agent-to-agent 自动通信；owner 直接切 window 调度，跨席位事实写 Goal、review、
handoff 与 Git commit。需要可靠门铃的双角色例外必须由 owner 明确启用并按
[`protocol/baton.md`](baton.md) qualification，不能扩写 tmux wrapper 造状态机。

## 每个 solo 席位必须声明

```text
goal_owner: <stable name> · tmux=<session>:<window>.0 · <kind> · <native-session-id> · <cwd>
```

名字只负责 owner 认知与 window 路由；native session ID 是 conversation 连续性的真源。启动记录与
Goal Context Receipt 同时记 frozen BASE、branch/HEAD 与 cwd。下一 Goal 未确定时进程留在原 window idle；
只有原 session 无法恢复或 owner 明确要求时才 cold start。

## 状态与新上下文

对 Goal 只使用 `QUEUED / ACTIVE / READY_FOR_REVIEW / DEV_DONE / BLOCKED / NEEDS_REFRESH / CANCELLED`；
tmux 的 `pane_current_command` 不是 Goal 状态。owner 需要运行态时直接看目标 TUI，不做 heartbeat、轮询或
自动唤醒。

模型切换但 session/context 未变，不重做冷启动。context reset、进程重启或换 terminal 后，若继续同一
Goal，先读项目规则、Goal Contract、Resume Capsule、当前 HEAD 与未验证面；若领取新 Goal，无论 native
session 是否复用，都必须按 Pickup Context 只读装载并落盘 Context Receipt，`ACCEPTED` 前禁止生产写。

## Runtime 资格

新 terminal/client 组合进入产品 Goal 前只验五件事：

1. `tmux-solo-setup.sh` 只打开 owner 已有树，同名 window/cwd 不一致时拒绝；
2. `tmux-codex-start.sh` 能在精确 pane 启动并 resume 同一 native session，且显式固定 cwd；
3. detach/attach 后进程与 TUI 连续，机器重启后能由文件、Git 与 session ID 冷恢复；
4. 从真实工作目录读取项目规则、Goal 与所需 authority，并验证 writable scope；
5. 人工 prompt 能得到完整回复；若依赖 MCP，`/mcp verbose` 显示目标服务可用。

失败只降级对应能力，不把“Codex 进程存在”伪装成 session、上下文或消息链路已恢复。Herdr 保留为显式
兼容路径；同一 native session 禁止跨 runtime 双开。

## 独立 review 例外

P0/P1、安全/权限/金额/数据删除、共享契约、owner 点名或 worker 主动请求时加 reviewer。启动记录额外声明：

```text
reviewer: <name> · <runtime target> · <kind> · <native-session-id> · roles/<role>.md
```

reviewer 只消费冻结 `BASE..HEAD` 并写 verdict，不接管 Goal ownership。旧 spec/delivery qualification 证据
继续有效，但不构成默认 pair 或自动门铃授权。
