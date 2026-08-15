# Verdict 块规范

每轮 review（plan review 与 code review 同用）的结论必须以此块收尾，
机器可读，杜绝"理解自然语言来决定循环走向"。

## 格式

```text
VERDICT: PASS | FINDINGS | ESCALATE
ROUND: <n>/2
P0: <列表或无>
P1: <列表或无>
P2: <列表或无>
SUGGESTION: <列表或无>
ESCALATE_REASON: <仅 ESCALATE 时，一句话>
```

写入对应的 review 文件末尾；传棒消息里只复述 `VERDICT` 和 P0/P1 计数。

## 分支语义

- **PASS**：本增量通过，baseline 前移，棒传给下一阶段；
- **FINDINGS**：存在需关闭的 P0/P1（或被 owner 升级的 P2），棒传回实现者；
- **ESCALATE**：出循环，走 protocol/escalation.md。

## 轮次上限

- 每个 increment 最多两轮：round 1 = substantive（发现并固定 findings），
  round 2 = closure（只核对固定验收条件）；
- 轮次计数写在 review 文件头和 verdict 块里，不放在任何一方记忆里；
- round 2 结束仍有未关闭 P0/P1 或双方争议 → **必须 ESCALATE，禁止 round 3**；
- closure 轮在修复代码中发现新 P0/P1 → 不开 round 3：**该修复作为新 increment 开出**，
  带自己的两轮预算，范围锁定在该修复；
- 新 diff、新生产证据、新 authority 变化可开新 finding，但必须写明"新在哪里"，
  不得用新措辞延续旧循环。

## 终止条件（closure 后满足即终止本增量）

- 所有 P0/P1 已关闭或由 owner 显式接受风险；
- 新 diff 中无新 P0/P1；
- P2 已登记到期点；
- reviewer baseline 前移到本轮 HEAD；
- 已通过范围不再重审。
