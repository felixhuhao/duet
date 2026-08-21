# 阶段梯子

当前阶段：**Stage 1 · Goal v1 pilot**（Goal 模式 2026-08-20 owner 拍板）
> owner 触点收缩为：roadmap grooming 批量授权 2–3 个 Goal、产品/open decision、Q4 级大问题、
> 队列补充与 pilot review。普通 Goal readiness、review、merge 与 DEV_DONE 不逐项等 owner ack；
> Completion Package 始终落盘，推送频率由 owner 指定。
> 依据：owner-turns 复盘（D 轨 58 条 vs B 轨全规则下 4 条）+ decision-log 一致率。
>
> Stage 0 记录（2026-08-15）：机械传棒先通电（送审/回修/重验/续行直接 send-text +
> 旁观通报），gate 传棒经 owner——见 protocol/baton.md「传棒分级」。

## 当前试行

- **Plan review 紧凑契约**（2026-08-17 起）：从下两个新 plan review 起使用
  `templates/plan-review.md`；完成后复核是否仍有因错误快照撤回的硬 finding、是否误跑项目门禁，
  以及无 finding 的 PASS 能否保持一屏可读，再由 owner 决定保留、调整或撤回。
- **Pre-Done Code Review**（2026-08-21 起）：先在一个 Goal 试行一轮静态 feedback。实现者冻结
  `BASE..HEAD` 后留在当前 Goal；reviewer 不跑 test/analyze/build、不做 signoff 或 closure，只把一轮
  feedback 写进 Goal 的 `Code Review`。实现者处理一次后自行标 `DEV_DONE`；P0/P1 必须修复或
  escalate，P2/Suggestion 进 follow-up。试行完成后由 owner 决定转正、调整或撤回，现行通用 review
  契约不标 legacy。

## 阶段定义

| 阶段 | 传棒 | escalate/stop |
|---|---|---|
| Stage 0 | 全部经过 owner：完成阶段只发 notification，owner 看完产物手动放行 | 全部到 owner |
| Stage 1 | 已毕业的传棒类型 agent 间直接 send-text；按 owner-report 作旁观通报，不等放行 | 全部到 owner |
| Stage 2 | 同 Stage 1 | 已毕业的 escalation 类型转自动，decision-log 留痕供抽查 |

## 毕业规则

- 某决策类型在 `decision-log.md` 中**连续 10 次** agent 建议与 owner 裁决一致 → 毕业；
- **owner 可对无判断含量的类型直批毕业**（记日期，🧪 试行制复核点照设）；
- 毕业后出现一次坏 case → 立即降回上一档，坏 case 记入 decision-log；
- 阶段切换由 owner 确认，本文件更新记录。

## 决策类型毕业状态

| 类型 | 状态 | 连续一致次数 |
|---|---|---|
| baton-confirm·机械（送审/回修/重验/续行） | **已毕业**（owner 直批 2026-08-15，✅ 转正 2026-08-16） | — |
| baton-confirm·放行·增量级（增量 PASS 续行确认） | **已毕业**（Stage 1 语义，owner 直批 2026-08-16） | — |
| goal-queue·批量授权 / pilot 推广 | **设计上不毕业** | — |
| baton-confirm·旧 batch 冻结 / Done ack | **历史模式，不用于新 Goal** | — |
| round-cap（轮次上限后的处置） | 未毕业 | 2 |
| P0P1-dispute（定级争议） | 未毕业 | 0 |
| redline-risk | 未毕业 | 0 |
| open-decision（产品选择） | **设计上永不毕业** | — |

## 终点

磨合的终点不是全自动，是**只有真正属于 owner 的决定才到 owner 手里**。
