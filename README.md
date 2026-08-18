# duet

双职责角色开发流程的**定义仓库**。管流程本身，不管任何一批具体开发的实例文件；
职责角色与运行时客户端解耦，同一张角色卡可以由 Codex、Claude Code、OpenCode 等客户端承担。

> 前身：`~/Workspace/docs/Claude-Codex双角色开发模式-待拍板草案.md`（保留作历史稿）。
> 状态：**Stage 1**（2026-08-16 起，见 calibration/stage.md）。宪法 2026-08-15 拍定；
> 试运行已完成（D3b/AGT-1/B8/D4 四批 + 三轨并轨），试行条款全部转正。

## 三层架构

```text
运行时层   每 pair 一个独立 workspace；可独占 session，也可多 pair 共用 session；owner 按需介入
状态层     md 文件。定义住本仓库；实例（plan/devlog/review）住各工作仓库
决策层     OD 分层路由：真源就地；owner 轨同步 decision-log，⬜ 行兼任收件箱；建卡自选
```

**定义与实例分家**：实例文件里全是 commit SHA、baseline 和 diff 证据，必须与它管的代码同仓库。
唯一例外是跨仓库积累的校准数据，住本仓库 `calibration/`。

## 核心原则

1. **每阶段一个交付 owner，另一方独立 review。** Plan 由 Spec Owner 主笔、Delivery Owner review；
   Implementation 由 Delivery Owner 主写、Spec Owner 验收。Reviewer 指出可证明的问题，不遥控实现细节。
2. **Plan 要 decision-complete，不要 implementation-complete。** 说清 outcome、scope、
   redlines、AC；不预定类名、目录和测试落点。
3. **技术选择归实现者，产品选择归 owner。** 产品选择必须走 open-decision 通道，
   触发条件见 [roles/delivery-owner.md](roles/delivery-owner.md)。
4. **Finding 必须绑定依据**：已放行 outcome/AC、redline/authority、可复现 regression、
   P0/P1 运行时边界、或证据未覆盖的关键路径。"我会换种写法"不构成 blocker。
5. **每个增量最多两轮 review**（substantive + closure），超限强制 escalate。
   规则见 [protocol/verdict.md](protocol/verdict.md)。
6. **传话走文件，peer 消息只是门铃；owner 汇报必须做摘要。** 任何一轮都必须能只凭
   落盘文件冷启动；给 owner 的消息负责信息压缩与注意力路由。见
   [baton](protocol/baton.md) 与 [owner-report](protocol/owner-report.md)。
7. **Escalate 必附 agent 自己的推荐判定**，用于校准自动判定规则。
   见 [protocol/escalation.md](protocol/escalation.md)。
8. **验证要有触发条件。** 没有相关代码/配置变化就复用新鲜结果；稳定增量跑一次定向，
   最终冻结 HEAD 跑一次项目门禁；同一失败最多执行两次，第二次仍无新证据就停。

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
roles/        spec-owner / delivery-owner —— 两张职责角色卡，与 runtime 客户端无关
protocol/     baton / verdict / escalation / owner-report / runtime —— 传棒、结论、升级、汇报、运行时
calibration/  decision-log（校准记录）+ stage（阶段梯子与毕业状态）
templates/    plan / devlog / review 三件套模板，实例化到工作仓库
scripts/      已验证的 herdr pair 启动、门铃与态势工具
```

工作仓库接入方式：项目 `AGENTS.md` 声明 duet 入口；每次 pair 启动由 runtime manifest 和
冷启动 prompt 把当前客户端绑定到对应角色卡。**工件（plan/评审/
devlog/移交单）按宿主仓的功能/类型惯例归档与命名，不以流程名建目录或命名文件**——流程
只活在角色卡、脚本与 commit 纪律里，不在仓里留品牌；文内首次提及流程时一句话自述；
多人仓落点遵仓 owner 惯例。`templates/` 是字段契约，不是落点约定。

## 当前治理

- 当前是 **Stage 1**：owner 只在 plan 冻结与 batch Done 前确认；增量 review 由 pair 自行闭环。
- duet 只管角色、交棒、review 与升级；门禁内容、产品红线和仓库操作写在项目自己的规则里。
- plan 冻结后发现计划缺陷，追加 Errata；影响 scope/AC 时局部重开，不把它包装成实现 finding。
- P2 默认不阻塞，只登记到期点；P0/P1 与两轮上限见 `protocol/verdict.md`。
- 纯调查/scout 不开 batch、不走两轮 review，报告交付即结束。
- 多 pair 可按 owner 的监控需求共用一个 Herdr session，但必须保持一 pair 一 workspace/工作树、
  实例名全局唯一；需要 terminal 完全隔离时仍用一 pair 一 session。
- 顺手动作必须同时满足：结果唯一或可逆、不占他人决策权、留痕可 review；AC/scope/契约/
  金额权限/verdict 不得顺手改。
- fetch 只在定 BASE、实施开工、Done 门禁三个边界做；轮次中不追新。无冲突可自行追平，
  有冲突立即停止并保留现场。
- 角色卡 ≤70 行、protocol 单文件 ≤80 行。新增规则必须置换旧规则；历史理由留在 git 与
  `calibration/`，活文件只保留当前行为。
- 机制变更由 owner 拍板；当前无待拍板项。
