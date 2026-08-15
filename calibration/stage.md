# 阶段梯子

当前阶段：**Stage 0**（2026-08-15 起）
> 同日修订：机械传棒先通电（送审/回修/重验/续行直接 send-text + 旁观通报），
> gate 传棒仍经 owner——见 protocol/baton.md「传棒分级」。

## 阶段定义

| 阶段 | 传棒 | escalate/stop |
|---|---|---|
| Stage 0 | 全部经过 owner：完成阶段只发 notification，owner 看完产物手动放行 | 全部到 owner |
| Stage 1 | 已毕业的传棒类型 agent 间直接 send-text，owner 旁观 sidebar | 全部到 owner |
| Stage 2 | 同 Stage 1 | 已毕业的 escalation 类型转自动，decision-log 留痕供抽查 |

## 毕业规则

- 某决策类型在 `decision-log.md` 中**连续 10 次** agent 建议与 owner 裁决一致 → 毕业；
- **owner 可对无判断含量的类型直批毕业**（记日期，🧪 试行制复核点照设）；
- 毕业后出现一次坏 case → 立即降回上一档，坏 case 记入 decision-log；
- 阶段切换由 owner 确认，本文件更新记录。

## 决策类型毕业状态

| 类型 | 状态 | 连续一致次数 |
|---|---|---|
| baton-confirm·机械（送审/回修/重验/续行） | **已毕业**（owner 直批 2026-08-15，🧪 D3b Done 复核） | — |
| baton-confirm·放行（冻结/开工/Done ack） | 未毕业 | 2 |
| round-cap（轮次上限后的处置） | 未毕业 | 0 |
| P0P1-dispute（定级争议） | 未毕业 | 0 |
| redline-risk | 未毕业 | 0 |
| open-decision（产品选择） | **设计上永不毕业** | — |

## 终点

磨合的终点不是全自动，是**只有真正属于 owner 的决定才到 owner 手里**。
