# Plan Review：<batch 名>

```text
round:              <1|2>/2
plan HEAD:          <被审 plan commit>
code BASE:          <plan 声明的代码基线>
authority snapshot: <跨仓/契约的精确 SHA；无则写 N/A>
```

## 本轮摘要

<按 protocol/owner-report.md：结论 / 完成及影响 / 发现及意义 / 需拍板 / 下一步。>

## Review coverage

```text
decision:     <Outcome、Scope、Frozen/Open decisions 是否 decision-complete>
acceptance:   <AC 是否可观察、无关键场景缺口>
authority:    <authority、依赖、迁移/跨仓边界是否一致>
start-risk:   <是否存在开工即撞的 P0/P1>
not-verified: <未核事实及为何不阻塞；无则写无>
```

PASS 默认到此即可：最多列三个会改变 decision core 的抽查锚，不复制 plan 事实表，
不审 testcase/测试落点，不运行项目门禁。

## Findings

| ID | 级别 | 违反哪项 | 精确依据 | 不修的影响 | 固定关闭条件 |
|---|---|---|---|---|---|
| PR-1 | P1 | AC / authority / … | `<repo>@<sha>:<path>` | <改变哪个 outcome/scope/AC/依赖> | <唯一可核条件> |

<只有 finding 需要展开自含证据。正确答案唯一走 FINDINGS；需要 owner 选择才走 ESCALATE。>

## Closure

<round 2 只放固定 finding 的 CLOSED / NOT CLOSED 矩阵；PASS 后压缩活文件，全文留 git 历史。>

---

```text
VERDICT: PASS | FINDINGS | ESCALATE
ROUND: <n>/2
COVERS: <本 verdict 已消化的 plan commit>
P0: 无
P1: 无
P2: 无
SUGGESTION: 无
ESCALATE_REASON:
```
