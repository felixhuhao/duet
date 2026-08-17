# Review：<batch 名> · 增量 <n>

```text
round:         <1|2>/2
BASE:          <reviewer baseline SHA>
COVERS:        <本轮覆盖的 commit / range>
reviewed HEAD: <本轮冻结的 HEAD SHA>
```

## 本轮摘要

<按 protocol/owner-report.md 填：结论 / 完成 / 发现 / 值得看 / 需拍板 / 下一步；作为汇报真源>

## Current blockers

<P0/P1，每条绑定依据：outcome/AC、redline/authority、regression、运行时边界、未覆盖关键路径>

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
P0: 无
P1: 无
P2: 无
SUGGESTION: 无
ESCALATE_REASON:
```
