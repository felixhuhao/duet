# duet

Goal 开发流程的**定义仓库**。管流程本身，不管任何一批具体开发的实例文件；默认由一个 solo Goal
owner 从合同到交付负责到底，原 spec/delivery 双职责卡保留为高风险或 owner 点名的独立 review 模式。

> 前身：`~/Workspace/docs/Claude-Codex双角色开发模式-待拍板草案.md`（保留作历史稿）。
> 状态：**Stage 1 · Goal v1 pilot**（2026-08-20 owner 确认，见
> [Goal 运行协议](protocol/goal.md) 与 calibration/stage.md）。旧 batch 工件保留历史，
> 新工作映射为用户结果 Goal 后才可执行。

## 三层架构

```text
运行时层   一个产品域一个 tmux session；长期 solo 席位各占一个 window/工作树；owner 直接调度
状态层     md 文件。定义住本仓库；实例（roadmap/Goal/validation ledger）住各工作仓库
决策层     OD 分层路由：真源就地；owner 轨同步 decision-log，⬜ 行兼任收件箱；建卡自选
```

**定义与实例分家**：实例文件里全是 commit SHA、baseline 和 diff 证据，必须与它管的代码同仓库。
唯一例外是跨仓库积累的校准数据，住本仓库 `calibration/`。

## 核心原则

**Simple and effective：默认路径只保留一种。** 一个 tmux session、长期 solo 席位、固定 worktree、
文件真源和人工可见的 owner 调度。新规则只有在替换旧分支并减少 owner/agent 的认知负担时才进入
主流程；兼容路径留在故障说明，不得反向污染日常操作。

1. **每个 Goal 一个 solo owner。** 同一 worker 从 Goal Contract、实施、定向验证、自检到 Completion
   Package 负责到底；P0/P1、安全/权限/金额/数据删除、共享契约或 owner 点名时才加独立 reviewer。
2. **Goal Contract 要 decision-complete，不要 implementation-complete。** 一页说清 outcome、Core、
   non-goals、invariants、AC、stop/validation/fallback；文件、类、命令进 Execution Notes。
3. **技术选择归实现者，产品选择归 owner。** 产品选择必须走 open-decision 通道，
   触发条件见 [roles/delivery-owner.md](roles/delivery-owner.md)。
4. **Finding 必须绑定依据**：已放行 outcome/AC、redline/authority、可复现 regression、
   P0/P1 运行时边界、或证据未覆盖的关键路径。"我会换种写法"不构成 blocker。
5. **每个增量最多两轮 review**（substantive + closure），超限强制 escalate。
   规则见 [protocol/verdict.md](protocol/verdict.md)。
6. **状态与交付走文件，tmux 不做消息总线；owner 汇报必须做摘要。** 任何一轮都必须能只凭
   落盘文件冷启动；跨席位协作由 owner 直接调度，双角色例外才使用旧
   [baton](protocol/baton.md)。汇报见 [owner-report](protocol/owner-report.md)。
7. **Escalate 必附 agent 自己的推荐判定**，用于校准自动判定规则。
   见 [protocol/escalation.md](protocol/escalation.md)。
8. **验证按 I0/I1/I2 分层并限频。** `DEV_DONE` 与 Integration/Device 分开；昂贵测试通常只跑
   基线一次 + 相关修复后一次，frozen HEAD 集中验，债务上限见 protocol/goal.md。

## Finding 分级

| 级别 | 示例 | 阻塞？ |
|---|---|---|
| P0 | 数据破坏、安全/权限绕过、严重金额错误、核心路径不可用 | 立即停止受影响 slice |
| P1 | 已放行 outcome 不成立、明确 regression、竞态错误状态、关键错误被吞 | 合并/Done 前必须关闭 |
| P2 | 非关键边界、维护性、证据或文档缺口 | 不阻塞，登记到期点 |
| Suggestion | 风格、替代设计、未来优化 | 不阻塞，不进强制 closure |

约束：implementation finding 不自动重开 plan；已关闭 finding 不得换表述重开；
watchlist 必须有核销时刻，没有到期点的 watchlist 等于噪声。

## 术语层级

```text
canonical outcome roadmap ⊃ Goal ⊃ increment
```

- **Goal**：完整用户结果的调度、ownership 与交付单位；
- **increment**：一轮 review 的冻结 commits 集合，两轮上限仍作用于它；
- **slice**：只在大问题影响分析时使用的最小暂停面；
- **track / batch**：历史工件术语，不再作为新工作的固定队列或 owner gate。

## 仓库结构

```text
roles/        spec-owner / delivery-owner —— 独立 review 例外使用的职责卡
protocol/     goal / verdict / escalation / owner-report / runtime —— Goal、结论、升级、汇报、运行时
calibration/  decision-log（校准记录）+ stage（阶段梯子与毕业状态）
templates/    Goal / outcome roadmap / validation ledger + review 模板，实例化到工作仓库
scripts/      tmux solo 布局与 Codex resume 薄封装；Herdr 只保留兼容工具
```

工作仓库接入方式：项目 `AGENTS.md` 声明 duet 入口；每个 Goal 在启动记录中声明 solo owner、tmux target、
worktree 与 native session ID。需要独立 review 时再把 reviewer 绑定到对应角色卡。**工件（plan/评审/
devlog/移交单）按宿主仓的功能/类型惯例归档与命名，不以流程名建目录或命名文件**——流程
只活在角色卡、脚本与 commit 纪律里，不在仓里留品牌；文内首次提及流程时一句话自述；
多人仓落点遵仓 owner 惯例。`templates/` 是字段契约，不是落点约定。

## 当前治理

- 当前是 **Stage 1 · Goal v1 pilot**：owner 在 roadmap grooming 批量授权 2–3 个 Goal；普通
  readiness/review/merge 自行闭环，只有产品拍板、Q4 级风险、队列补充和 pilot review 到 owner。
- duet 只管 Goal、职责边界、review 与升级；门禁内容、产品红线和仓库操作写在项目自己的规则里。
- 实现中发现 Contract 缺陷，追加 Addendum；影响 Outcome/Core/AC 时局部重开，不包装成实现 finding。
- P2 默认不阻塞，只登记到期点；P0/P1 与两轮上限见 `protocol/verdict.md`。
- 纯调查/scout 不开 batch、不走两轮 review，报告交付即结束。
- 所有 agent 默认住产品域的稳定 tmux session，`tmux attach -t <session>` 即可查看；agent 是跨 Goal
  续用的长期 solo 席位，不按任务创建或删除；每个 window 绑定 owner 预置的长期 worktree，换 Goal
  只换 branch。tmux 不提供语义状态或可靠门铃，禁止用自动 `send-keys` 冒充 agent 通信。
  worktree 创建、移动、删除严格由 owner 安排，agent/orchestrator 不得临时建树。canonical 主树承载
  grilling、规划、merge 与真源回写，开发席位只写自己的树；下一 Goal 未定时原地 idle。启动、resume、
  维护与迁移只走 [tmux owner runbook](scripts/TMUX-RUNBOOK.md)。
- 顺手动作必须同时满足：结果唯一或可逆、不占他人决策权、留痕可 review；AC/scope/契约/
  金额权限/verdict 不得顺手改。
- fetch 只在定 BASE、实施开工、Done 门禁三个边界做；轮次中不追新。无冲突可自行追平，
  有冲突立即停止并保留现场。
- 角色卡 ≤70 行、protocol 单文件 ≤80 行。新增规则必须置换旧规则；历史理由留在 git 与
  `calibration/`，活文件只保留当前行为。
- 机制变更由 owner 拍板；当前无待拍板项。
