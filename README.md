# duet

Claude × Codex 双角色开发流程的**定义仓库**。管流程本身，不管任何一批具体开发的实例文件。

> 前身：`~/Workspace/docs/Claude-Codex双角色开发模式-待拍板草案.md`（保留作历史稿）。
> 状态：**Stage 1**（2026-08-16 起，见 calibration/stage.md）。宪法 2026-08-15 拍定；
> 试运行已完成（D3b/AGT-1/B8/D4 四批 + 三轨并轨），试行条款全部转正。

## 三层架构

```text
运行时层   herdr workspace，两个 agent 各占一个 pane，owner 旁观并随时介入
状态层     md 文件。定义住本仓库；实例（plan/devlog/review）住各工作仓库
决策层     OD 分层路由：真源就地，decision-log 的 ⬜ 行兼任 owner 收件箱；建卡自选
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

工作仓库接入方式：`CLAUDE.md` / `AGENTS.md` 各加一行指向对应角色卡。**工件（plan/评审/
devlog/移交单）按宿主仓的功能/类型惯例归档与命名，不以流程名建目录或命名文件**——流程
只活在角色卡、脚本与 commit 纪律里，不在仓里留品牌；文内首次提及流程时一句话自述；
多人仓落点遵仓 owner 惯例。`templates/` 是字段契约，不是落点约定。

## 拍板记录

**已定（2026-08-15 brainstorm）：**

- 运行时用 herdr，两个 agent 平级，接力棒模型，无 driver；
- 状态层用 md 三件套 + decision log，暂不引入 loopx（升级判据：出现无人值守需求，
  或手写状态文件出现漂移）；
- **open decisions 分层路由**（2026-08-15 修订，取代初版「一律建卡」）：真源就地
  （轨内 OD 住 review OD 节 / plan 待拍板节，证据不离上下文）；每次 escalate 必记的
  decision-log 行中「owner 裁决 = ⬜」即 owner 收件箱（零新增机制）；跨轨结构性 OD
  → migration ROADMAP「尚未拍板且影响排期」节；跨 owner → 对方仓需求分析文档；
  kanban 建卡降为 owner 自选。closure 轮逐条重提悬置 ⬜ 或显式搁置；
- **跨仓写边界**（同日二次修订，改为流程中心表述）：任何 batch 只写本仓；改其他仓 =
  去该仓开 batch 遵其流程（它的 AGENTS.md、门禁、验收人），或走需求单。跨仓特性用
  **父需求文档（authority 仓）+ 每仓子 batch** 组织，契约衔接，默认先后端后消费端；
  同 owner 多仓的声明式同批双写保留为例外（plan 声明仓清单 + writable scope + 各仓
  BASE，未声明即越界 escalate）；多人仓中 duet 的 owner 角色由仓 owner 担任或显式约定；
- **跨界消息走 inbox 协议**（protocol/inbox.md）：真源 = 发送方仓移交单目录（默认
  `docs/handoffs/`，落点归项目层）的文件（commit 在自己分支），dg-kanban 卡只做路由指针
  （标题前缀 `[→repo]`，可全丢），herdr 门铃兜底，接收方登账关卡即回执；
  Workspace 层 docs/ 不再当信道；
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
  round 2 后仍有未关闭 P0/P1 或争议强制 escalate。同日修订上限语义：**round 3 需
  owner 授权**——escalate 后 owner 可授予 closure 重验（门柱冻结、不得新增 findings，
  继承旧流程 §4.2 语义），授予走 round-cap 毕业梯子。细则见 protocol/verdict.md。

- **P2 默认不阻塞合并**：登记到期点进 watchlist；仅 owner 明确升级或实证 outcome 不成立
  时升 P1。
- **全量门禁仅 Done / 合并前跑一次**：门禁内容由项目层定义，duet 只定时机；普通增量靠
  定向证据；re-review 不自动重跑。

- **试运行**：D track 下一个边界清楚的 batch 起跑；判据四条全过才算成功——①每增量轮数≤2
  守住 ②无 P0/P1 逃逸（pass 后才被发现的算逃逸）③owner 被打断次数中「真该 owner 决定」
  占比 ≥80%（从 decision-log 算）④owner 主观愿意跑下一批。跑完 1 个 batch 拍「继续用」，
  2 个拍「推广到 B/C/E」。

- **防杂宪章**（2026-08-15 晚，针对规则与文档的膨胀本身）：
  ① **规则预算**——角色卡 ≤70 行、protocol 单文件 ≤80 行；超预算必须先合并/淘汰
  旧条款再进新条款，规则只许置换不许纯累加；
  ② **新机制条款默认试行制**——带 🧪 标签与复核点（默认下个 batch Done）；复核时
  没有实际 fire 过的条款默认撤销，规则用事故换永久资格（补充卡 #9 模式的推广）；
  ③ **活文件只保留活状态**——关闭的轮次/finding 折叠为关票矩阵行，全文靠 git 历史，
  review 文件不做档案馆。

- **顺手总则**（2026-08-16 由顺手单推广，置换原条目；✅ 转正 2026-08-16，试行期看全体顺手动作
  revert 率）：任何动作同时满足三条，**谁看见谁顺手做，不传棒不等待**——
  ①结果唯一确定或完全可逆（做错代价 ≈ 一次 revert）；②不占用他人决策权（产品归
  owner、技术归实现者、verdict 归 reviewer 的产权线不动）；③留痕——单独 commit 标
  `[顺手]` 或记录一行索引，自动进受影响方下轮 review 面（做和验不同手，原则 1 不破）。
  缺任何一条 → 走角色分工。**廉价否决**：受影响方无理由 revert，revert 即宣告该事有
  决策含量、自动转正常流程，不算任何人的错。黑名单永不顺手：AC/scope/契约/金额权限/
  verdict 本身/单写者文件；salami 红线：不许连串顺手拼出决策性改动。
  实例：reviewer 代实现者机械修正、他人在途文件的无损安置（stash 带标签附恢复命令，
  内容处置仍归原写者）、断链/typo/路径修正、无冲突 rebase。
  **剩余仍需报 owner 的情况，报告必须带查清的事实 + 实测结论 + 建议方案**（原则 7
  「escalate 必附推荐判定」的推广）——只报「有障碍」不算报告，不得把不确定性
  未经调查就外包给 owner（诱因：三文件安置同一障碍报三轮，零信息增量）。

- **工件去品牌化**（2026-08-15）：流程工件按宿主仓类型惯例归档命名（见「仓库结构」下
  接入方式段），禁以流程名建目录/文件。存量：Agent 仓已迁 `docs/plans/`（`9f9e76a6`）；
  byteme_mobile-D 的 `docs/duet/` 与 outbox → `docs/handoffs/` 在 D3b 收口折叠时迁。

- **现状 = fetch 后的现状**（2026-08-15 立，2026-08-16 修订时机与 rebase，同 ✅）：
  fetch 锚在**三个边界时刻**——定 BASE / 实现阶段开工 / Done 全量门禁前；轮次中间
  不 fetch 不追新（门柱冻结不变），写 verdict 只消化本地并发落盘。跨仓只读走
  `origin/<branch>` ref、不动对方工作树；对现状的断言一律标注 as-of SHA——
  **对活跃的对方仓，as-of 按时刻记而非按天记，立项时刻必须重验**（2026-08-16 修订，
  诱因：TC-1 在「仅 +2 docs」的校核写下一小时内就进了契约代码）。追平时本地有未推 commits：**无冲突可自行 rebase**（解冲突有判断含量，
  干净快进没有），一有冲突立即 `--abort` 报 owner；他人在途未提交文件 → 按顺手总则
  无损安置（内容处置归原写者）；rebase 改写的 SHA 已被文档引用（BASE/COVERS 锚）→
  随手补一行新旧映射。fetch 不可用 → 不装新鲜，标注 as-of 与已知落差。

- **并轨结算包**（2026-08-16）：①**合并模式预授权**——对外动作从逐次申请升级为
  owner 按仓/阶段设定模式（如「本地 merge 自主 + 回执，push 须批」），模式内自主执行、
  回执照旧；各仓具体模式是域内容，写各仓 AGENTS；②**scout 任务免仪式**——纯调查类
  （盘点/拍板包/预研）不开 batch、不走两轮 review，报告落盘即收口；③**Stage 1 生效**
  （owner 触点 = plan 冻结 decision core + Done ack，见 calibration/stage.md）；
  ④worktree 短命化为 mobile 仓域规则（写其 AGENTS）。试行条款已于 2026-08-16 全部转正，结算见
  calibration/trial-settlement.md。

**待拍板：** 无——首批 7 条已于 2026-08-15 全部拍定。机制条款的后续修订经 owner 拍板。
