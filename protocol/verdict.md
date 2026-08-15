# Verdict 块规范

每轮 review（plan review 与 code review 同用）的结论必须以此块收尾，
机器可读，杜绝"理解自然语言来决定循环走向"。

## 格式

```text
VERDICT: PASS | FINDINGS | ESCALATE
ROUND: <n>/2
COVERS: <本 verdict 已消化的最新 commit>
P0: <列表或无>
P1: <列表或无>
P2: <列表或无>
SUGGESTION: <列表或无>
ESCALATE_REASON: <仅 ESCALATE 时，一句话>
```

写入对应的 review 文件末尾；传棒消息里只复述 `VERDICT` 和 P0/P1 计数。

**写 verdict 前的两个动作**（🧪 试行 · D3b Done 复核）：
① 重读目标文件现状 + 自己上次读取之后的 git log，消化所有并发落盘（诱因：D3b
的 PASS 没读到早 3 分钟的 §8）；② 本轮改过被引用的条款 → 先 grep 其名字，
命中处置逐处列入 errata（诱因：E-7 修定义漏两处引用，烧掉一整轮 closure）。

## 分支语义

- **PASS**：本增量通过，baseline 前移，棒传给下一阶段；
- **FINDINGS**：存在需关闭的 P0/P1（或被 owner 升级的 P2），棒传回实现者；
- **ESCALATE**：出循环，走 protocol/escalation.md。

## 轮次上限

- 每个 increment 最多两轮：round 1 = substantive（发现并固定 findings），
  round 2 = closure（只核对固定验收条件）；
- 轮次计数写在 review 文件头和 verdict 块里，不放在任何一方记忆里；
- round 2 结束仍有未关闭 P0/P1 或双方争议 → **必须 ESCALATE；未经 owner 授权不得进
  round 3**（2026-08-15 修订：禁止的是「未经 owner 看见的 round 3」，不是结果本身）。
  owner 的裁决选项包含「**授予一轮 closure 重验**」：重验只判原固定验收条件，
  **不得新增 findings**——门柱冻结语义继承自旧流程「修复复审只判固定验收条件」；
  授予可连续多次，每次记 decision-log 的 round-cap 类；该类型毕业后转
  自动授予 + 通知，owner 只在想介入时介入；
- closure 轮在修复代码中发现新 P0/P1 → 不开 round 3：**该修复作为新 increment 开出**，
  带自己的两轮预算，范围锁定在该修复；
- 新 diff、新生产证据、新 authority 变化可开新 finding，但必须写明"新在哪里"，
  不得用新措辞延续旧循环。

## 终止条件（closure 后满足即终止本增量）

- 所有 P0/P1 已关闭或由 owner 显式接受风险；
- 新 diff 中无新 P0/P1；
- P2 已登记到期点；
- reviewer baseline 前移到本轮 HEAD；
- 已通过范围不再重审；
- 终止时本增量的详细段落折叠为关票矩阵行（全文永在 git 历史）——活文件只保留活状态。
