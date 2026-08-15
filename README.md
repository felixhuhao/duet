# duet

Claude × Codex 双角色开发流程的**定义仓库**。管流程本身，不管任何一批具体开发的实例文件。

> 前身：`~/Workspace/docs/Claude-Codex双角色开发模式-待拍板草案.md`（保留作历史稿）。
> 状态：Stage 0。宪法首批条款已拍定（2026-08-15，见文末拍板记录）；
> 待 herdr 本地验证与 D track 首个试运行 batch。

## 三层架构

```text
运行时层   herdr workspace，两个 agent 各占一个 pane，owner 旁观并随时介入
状态层     md 文件。定义住本仓库；实例（plan/devlog/review）住各工作仓库
决策层     dg-kanban。open decisions 建卡，owner 在看板拍板
```

**定义与实例分家**：实例文件里全是 commit SHA、baseline 和 diff 证据，必须与它管的代码同仓库。
唯一例外是跨仓库积累的校准数据，住本仓库 `calibration/`。

## 核心原则

1. **每阶段一个交付 owner，另一方独立 review。** Plan 由 Claude 主笔、Codex review；
   Implementation 由 Codex 主写、Claude 验收。Reviewer 指出可证明的问题，不遥控实现细节。
2. **Plan 要 decision-complete，不要 implementation-complete。** 说清 outcome、scope、
   redlines、AC；不预定类名、目录和测试落点。
3. **技术选择归实现者，产品选择归 owner。** 产品选择必须走 open-decision 通道，
   触发条件见 [roles/codex.md](roles/codex.md)。
4. **Finding 必须绑定依据**：已放行 outcome/AC、redline/authority、可复现 regression、
   P0/P1 运行时边界、或证据未覆盖的关键路径。"我会换种写法"不构成 blocker。
5. **每个增量最多两轮 review**（substantive + closure），超限强制 escalate。
   规则见 [protocol/verdict.md](protocol/verdict.md)。
6. **传话走文件，消息只是门铃。** 任何一轮都必须能只凭落盘文件冷启动。
   见 [protocol/baton.md](protocol/baton.md)。
7. **Escalate 必附 agent 自己的推荐判定**，用于校准自动判定规则。
   见 [protocol/escalation.md](protocol/escalation.md)。

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
track ⊃ batch ⊃ increment ⊃ slice
```

- **track**：一条产品线/迁移线（如 D track）；
- **batch**：一份 frozen plan 覆盖的范围，plan baseline 的单位；
- **increment**：一轮 review 的 commits 集合，两轮上限的作用对象；
- **slice**：可独立暂停的最小工作单元，open decision 只暂停受影响的 slice。

## 仓库结构

```text
roles/        claude.md / codex.md —— 两张角色卡，各自工作时唯一需要读的执行面
protocol/     baton / verdict / escalation —— 传棒、结论块、升级的机制规范
calibration/  decision-log（校准记录）+ stage（阶段梯子与毕业状态）
templates/    plan / devlog / review 三件套模板，实例化到工作仓库
scripts/      herdr workspace 搭建等（待 herdr 本地验证后补）
```

工作仓库接入方式：`CLAUDE.md` / `AGENTS.md` 各加一行指向对应角色卡；实例文件按
`templates/` 落在工作仓库约定目录（建议 `docs/duet/`）。

## 拍板记录

**已定（2026-08-15 brainstorm）：**

- 运行时用 herdr，两个 agent 平级，接力棒模型，无 driver；
- 状态层用 md 三件套 + decision log，暂不引入 loopx（升级判据：出现无人值守需求，
  或手写状态文件出现漂移）；
- open decisions 走 dg-kanban 建卡；
- 自主性走三阶段梯子，当前 Stage 0，毕业靠 decision-log 一致率（见 calibration/stage.md）；
- stop 从严、escalate 误报随磨合调低的不对称原则。

**已定（2026-08-15 拍板会）：**

- **Owner 触点钉在不可逆时刻**：Stage 1+ 时 plan 冻结前 decision core（outcome/scope/
  redlines/AC/open decisions 一页）必过 owner 的眼；增量级 pass 不经 owner；batch 标 Done
  前 owner ack 一次。Stage 0 不受影响（棒全经 owner）。
- **Plan errata 机制采用**：实现暴露的 plan 缺陷记 errata、不算实现者 finding；立 errata
  必须引用 plan 具体条款 + 暴露它的代码证据；Claude 质疑是包装的走争议通道；免责不免修；
  影响 scope/AC 时局部重开。
- **三层分工**：duet 只管 agent 间的权力与循环机制（角色/传棒/verdict/轮次/escalation/校准/
  errata），机制条款项目不可覆盖（否则校准跨项目不可比），修订须经 owner；工件规范归
  `AI_AGENT_DEV_SPEC.md`，域内容（门禁命令、产品红线、文档落点）归各项目。duet 的
  templates/ 仅是必备字段契约 + 新项目起步默认，不取代项目现有格式。
- **两轮上限采用**：每 increment 最多 substantive + closure 两轮；新 diff/新事实可开新
  finding 但须写明"新在哪里"；closure 中发现修复引入的新 P0/P1 → 开新增量而非 round 3；
  round 2 后仍有未关闭 P0/P1 或争议强制 escalate。细则见 protocol/verdict.md。

- **P2 默认不阻塞合并**：登记到期点进 watchlist；仅 owner 明确升级或实证 outcome 不成立
  时升 P1。
- **全量门禁仅 Done / 合并前跑一次**：门禁内容由项目层定义，duet 只定时机；普通增量靠
  定向证据；re-review 不自动重跑。

- **试运行**：D track 下一个边界清楚的 batch 起跑；判据四条全过才算成功——①每增量轮数≤2
  守住 ②无 P0/P1 逃逸（pass 后才被发现的算逃逸）③owner 被打断次数中「真该 owner 决定」
  占比 ≥80%（从 decision-log 算）④owner 主观愿意跑下一批。跑完 1 个 batch 拍「继续用」，
  2 个拍「推广到 B/C/E」。

**待拍板：** 无——首批 7 条已于 2026-08-15 全部拍定。机制条款的后续修订经 owner 拍板。
