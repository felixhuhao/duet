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

写 verdict 前重读当前文件与本地 git log，冻结本轮 `COVERS`；若改过被引用的条款，先搜索并
同步所有命中处。fetch 只在 README 规定的三个边界做，轮次中不追新。

## 分支语义

- **PASS**：本增量通过，baseline 前移，棒传给下一阶段；
- **FINDINGS**：存在需关闭的 P0/P1（或被 owner 升级的 P2），棒传回实现者；
- **ESCALATE**：出循环，走 protocol/escalation.md。

## Plan review 特化

- 只查角色卡四项，使用 `templates/plan-review.md`；PASS 不做全量事实审计，列 coverage、
  最多三个关键锚与未验证面即可；没有生产 diff，不跑项目测试或 analyze；
- 硬 finding 必须针对 plan 声明的精确快照；mutable HEAD、过期 checkout、记忆中的 runtime
  状态不能支撑 P0/P1。快照不可得时写 `not-verified`，只有其本身使开工不安全才阻塞；
- **FINDINGS** 用于正确答案唯一的修订（如误引已接受 authority、漏写关键 AC）；
  **ESCALATE** 只用于两个合理选项会改变产品结果、authority 真冲突、需接受风险或 round-cap；
- closure PASS 后活文件折叠为 coverage + 关票矩阵 + 最终 verdict，长证据留在 git 历史。

## 轮次上限

- 每个 increment 最多两轮：round 1 = substantive（发现并固定 findings），
  round 2 = closure（只核对固定验收条件）；
- 轮次计数写在 review 文件头和 verdict 块里，不放在任何一方记忆里；
- round 2 结束仍有未关闭或新出现的 P0/P1、或双方争议，统一 **ESCALATE**；不得自动开
  round 3 或换一个 increment 继续循环。owner 决定接受风险、收窄范围或追加一次固定条件复验；
- 新 diff、新生产证据、新 authority 变化必须写明“新在哪里”，不得换措辞重开旧 finding。

## 终止条件（closure 后满足即终止本增量）

- 所有 P0/P1 已关闭或由 owner 显式接受风险；
- 新 diff 中无新 P0/P1；
- P2 已登记到期点；
- reviewer baseline 前移到本轮 HEAD；
- 已通过范围不再重审；
- 终止时本增量的详细段落折叠为关票矩阵行（全文永在 git 历史）——活文件只保留活状态。
