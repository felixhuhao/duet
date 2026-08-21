# Runtime 绑定与资格协议

职责角色固定，客户端可换：`spec_owner` = Plan 主笔 + Acceptance Reviewer；
`delivery_owner` = Plan Reviewer + Implementation Owner。Herdr agent 是长期开发席位，不是 Goal 容器；
使用稳定名字（如 `dev1/dev2` 或 `<pair>-<role>`），换 Goal 不换 identity。Herdr 0.8.0 的具体启动、
通信、resume、固定 worktree 绑定与故障恢复命令见
[`scripts/HERDR-RUNBOOK.md`](../scripts/HERDR-RUNBOOK.md)；raw CLI 编排不得靠试错发现语义。

## 唯一默认拓扑

所有 agent 放在 Herdr `default` session，因此 owner 在 terminal 直接运行 `herdr` 就能看到全部席位。
每个活 agent 独占一个长期 workspace/pane/worktree 席位，名字在该 session 内唯一，且只能写自己的树。
`baton.sh peers/send/read/wait` 默认只操作这个 session，不缓存状态、不发送 heartbeat。旧命名 session
只在自然 Goal 迁移时搬入 `default`；不得为了统一显示中断在途工作。跨-session federation 仅是事故
恢复兼容面，不进入正常调度或文档主路径。

agent/pair 与其 worktree 是跨 Goal 续用的长期席位，不是一次性任务容器；换 Goal 只换 branch，不换
cwd、workspace、identity 或 native session。worktree 的创建、移动、删除只由 owner 安排；agent、pair、
orchestrator 严禁运行创建命令或为任务临时加树。规划/grilling 在宿主仓 canonical 主树进行，开发席位
只消费已授权 Goal；每次领取前先让目标 branch 包含冻结的 canonical BASE，再验 ancestor/Receipt。
下一 Goal 未确定时原地 idle；只有原 native session 无法恢复时才冷启动。

## 每个 pair 必须声明

```text
spec_owner:     <stable name> · default · <kind> · <instance_id> · <cwd> · roles/spec-owner.md
delivery_owner: <stable name> · default · <kind> · <instance_id> · <cwd> · roles/delivery-owner.md
```

名字只负责路由；`instance_id` 由 terminal + 本次前台进程实时计算，重启即变化。门铃提交前后必须
复验并带目标 instance，变化则按送达失败处理。plan 或启动记录须保存这些项；calibration 同时
记职责角色与 runtime，不能把客户端表现归因给角色。

## 状态与新上下文

对外状态只用 `working / idle / blocked / unknown / dead`；未知 runtime 状态或无法确认本次进程
一律归 `unknown`。`unknown/dead` 禁止普通门铃，且任何状态都不触发 heartbeat、自动唤醒或重启。
Herdr 的 `done` 表示本 turn 完成且进程仍在，归一为 `idle`，不能据此宣告 agent 丢失。

模型切换但 session/context 未变，不重做冷启动。context reset、进程重启或换 session 后，若继续同一
Goal，先读项目规则、角色卡、Goal Contract、Resume Capsule、最新 review、当前 HEAD 与棒位；回报
新 instance 和下一动作后继续。若领取新 Goal，无论 native session 是否复用，都必须按 Goal 文件的
Pickup Context 做只读装载并落盘 Context Receipt；`ACCEPTED` 前禁止生产写。恢复/领取都不自行扩大
Ready Queue、不启动自动 loop。

## Runtime 资格

新客户端组合进入产品 batch 前只验五件事：

1. 用 `herdr agent start <name> --kind <kind>` 启动，重启后名字与原会话都能恢复；
2. 从真实工作目录读取项目规则与角色卡，并验证该 batch 所需目录权限；
3. 五态可归一，门铃有 delivery-id + target-instance 回执；
4. working 时普通门铃不会 steering 或丢失，stop 类能安全停止受影响工作；
5. 跑通一次 plan review → implementation review → owner gate，并生成一屏自含摘要。

失败只降级对应能力，修好后复验该项；不因单点问题停掉无关能力或在途 batch。

## 已有证据

- `spec_owner=Claude Code / delivery_owner=Codex`：2026-08-15~16 四批试运行通过；
- `spec_owner=Codex / delivery_owner=OpenCode 1.18`：基础路由通过；已知限制是 working 消息需
  settle 后投递、手工重启会丢 Herdr 名字、Workspace 外部目录权限尚未完成 qualification；
- 其他组合：以最新 qualification 记录为准，不从“herdr 能识别进程”推断流程已通过。
