# Runtime 绑定与资格协议

职责角色固定，客户端可换：`spec_owner` = Plan 主笔 + Acceptance Reviewer；
`delivery_owner` = Plan Reviewer + Implementation Owner。Herdr 活实例按 `<pair>-<role>` 唯一命名。

## 多 pair 拓扑

运行隔离单位是 pair 的 workspace + 工作树，不强绑 session。默认一个 pair 独占一个命名
Herdr session，适合多个 terminal 各看一对；owner 要在同一 sidebar 监控时，也可让多个 pair
共用一个命名 session，但必须一 pair 一 workspace、实例名全局唯一，且不得跨工作树写入。
`scripts/herdr-federation.py` 每次从所有 running session 实时聚合 agent；
`baton.sh peers/send/read/wait` 对同 session 和跨 session 使用同一名称路由，不缓存状态、不发送
heartbeat。原生 TUI sidebar 显示本 session 的所有 workspace；其他 session 状态按需查 `peers`。

pair 是持续协作上下文，不是一次性任务容器。相邻的 scout、规划与 review 默认续用原 pair，直接
发送带 authority、当前 HEAD 与明确 scope 的新任务；不要仅因 batch/编号变化重启 runtime。只有进入
生产实现且需要独立提交边界、BASE 变化不能安全沿用当前工作树，或确有并行写入需求时，才新建
worktree/pair。runtime 或模型异常优先恢复原 session；重建 pair 是恢复失败后的手段，不是清上下文。

## 每个 pair 必须声明

```text
spec_owner:     <global name> · <session> · <kind> · <instance_id> · <cwd> · roles/spec-owner.md
delivery_owner: <global name> · <session> · <kind> · <instance_id> · <cwd> · roles/delivery-owner.md
```

名字只负责路由；`instance_id` 由 terminal + 本次前台进程实时计算，重启即变化。门铃提交前后必须
复验并带目标 instance，变化则按送达失败处理。plan 或启动记录须保存这些项；calibration 同时
记职责角色与 runtime，不能把客户端表现归因给角色。

## 状态与新上下文

对外状态只用 `working / idle / blocked / unknown / dead`；未知 runtime 状态或无法确认本次进程
一律归 `unknown`。`unknown/dead` 禁止普通门铃，且任何状态都不触发 heartbeat、自动唤醒或重启。
Herdr 的 `done` 表示本 turn 完成且进程仍在，归一为 `idle`，不能据此宣告 agent 丢失。

模型切换但 session/context 未变，不重做冷启动。context reset、进程重启或换 session 后，先读项目
规则、角色卡、frozen plan、最新 devlog/review、当前 HEAD 与棒位；回报新 instance 和下一动作后
再收产品棒。恢复只重建上下文，不自行选下一任务、不启动自动 loop。

## Runtime 资格

新客户端组合进入产品 batch 前只验五件事：

1. 用 `herdr agent start <name> --kind <kind>` 启动，重启后名字与原会话都能恢复；
2. 从真实工作目录读取项目规则与角色卡，并验证该 batch 所需目录权限；
3. 五态可归一，跨 session 门铃有 delivery-id + target-instance 回执；
4. working 时普通门铃不会 steering 或丢失，stop 类能安全停止受影响工作；
5. 跑通一次 plan review → implementation review → owner gate，并生成一屏自含摘要。

失败只降级对应能力，修好后复验该项；不因单点问题停掉无关能力或在途 batch。

## 已有证据

- `spec_owner=Claude Code / delivery_owner=Codex`：2026-08-15~16 四批试运行通过；
- `spec_owner=Codex / delivery_owner=OpenCode 1.18`：基础路由通过；已知限制是 working 消息需
  settle 后投递、手工重启会丢 Herdr 名字、Workspace 外部目录权限尚未完成 qualification；
- 其他组合：以最新 qualification 记录为准，不从“herdr 能识别进程”推断流程已通过。
