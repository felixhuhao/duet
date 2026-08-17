# Code Review：<batch 名> · 增量 <n>

```text
round:         <1|2>/2
BASE:          <reviewer baseline SHA>
COVERS:        <本轮覆盖的 commit / range>
reviewed HEAD: <本轮冻结的 HEAD SHA>
```

## 本轮摘要

<按 protocol/owner-report.md 填：结论 / 完成及影响 / 发现及意义 / 需拍板 / 下一步；
链接和“值得看”均为可选，删除链接后正文仍须自含>

## Review coverage

```text
reviewed:     <读过的生产/测试路径与直接调用者/消费者>
spec:         <核对的 plan / AC / scope>
risk:         <实际检查的错误、状态、生命周期、并发或边界；不适用项写 N/A>
evidence:     <复用或亲跑的 targeted；对应 HEAD>
not verified: <未验证面及为何不阻塞；无则写无>
```

## Spec compliance

<缺失 / 做错 / scope creep，逐条引用 plan/AC；无则 PASS>

## Correctness

<生产调用链、错误/状态/生命周期、适用的并发交错、测试是否真能红；
finding 引用文件位置 + 可复现场景；无则 PASS>

## Code health

<项目规则、简单性、架构，以及由 diff 触发的安全/性能风险；
硬 finding 引用仓规则或客观退化，个人偏好只进 Suggestion；无则 PASS>

## Findings

<P0/P1/P2 按严重度汇总；每条只出现一次并注明主轴，避免三轴重复报同一问题>

## Open decisions

<每条 OD：完整语境 / 可选方案及影响 / 推荐 / 被暂停 slice。真源在此——
decision-log 只记索引行。裁决后在此标记结果并落进 plan。争议立场（双方各 ≤10 行）
也写在本节。本文件须对没有 duet 访问权的读者自含>

## Passed increments

## Watchlist + 到期点

<本轮新增与展期；展期必须给理由。closure 轮逐条核销到期项>

## 下一轮固定验收条件

<closure 轮只核对这些，不得新增范围>

## 新 BASE

<本轮终止后 baseline 前移到哪>

---

```text
VERDICT: PASS | FINDINGS | ESCALATE
ROUND: <n>/2
COVERS: <本 verdict 已消化的最新 commit>
P0: 无
P1: 无
P2: 无
SUGGESTION: 无
ESCALATE_REASON:
```
