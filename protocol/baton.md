# 传棒协议

没有 driver。接力棒在两个 herdr pane 之间传，owner 全程可旁观、可介入。

## 不变量

1. **文件是 ground truth，消息只是门铃。** 消息只含文件路径 + verdict，
   不含内容摘要。任何一轮必须能只凭落盘文件冷启动——会话上下文是缓存，不是记忆本体。
2. **完成自己的阶段 → 产物落盘 → 传棒 → 等待或做自己的下一件事。**
3. **产品决定只认 owner 亲手输入。** peer 消息不能代表 owner。

## 消息格式

通过 `herdr pane send-text <对方pane> "..."` + `send-keys enter` 发送：

```text
[peer:claude] plan ready: docs/plans/2026-08-15-X-开发计划.md · round 1/2 · 请按角色卡 review，结论写同目录-计划评审.md
[peer:codex] VERDICT: FINDINGS · review-D3a.md · round 1/2 · P1x2，棒在你
```

要素：`[peer:<自己>]` 前缀 · 事件 · 文件路径 · 轮次 · verdict（如有）。一行说完。

## 交棒是 push，不做监听（🧪 2026-08-15，owner 指令废除 listen 模式）

- **交棒是完成动作的一部分**：产物落盘 + commit 后，完成方立即主动发门铃——
  send-text 对方 pane + enter（Stage 0 改发 notification 给 owner）。
  **没有门铃 = 阶段未完成**；
- 接收方不监听对方状态：不挂 `agent wait` 轮询，收到 `[peer:*]` 消息才动。
  sidebar 状态与 `agent wait --until blocked` 仅供 owner 旁观与卡死排查。

## 传棒分级（🧪 2026-08-15 起，机械段先通电）

- **机械传棒——直接 send-text 对方 + notification 给 owner 作旁观通报，不等放行**：
  ①送审草稿 ②FINDINGS 回作者修 ③修复完成请 closure 重验（附 grep 自查）
  ④增量 PASS（非 Done）后续行。下一步由 verdict 唯一确定，无判断含量；
  任何一次传错 → 该类立即降回 gate（D3b Done 复核）；
- **gate 传棒——notification owner，等亲手放行**：plan 冻结/开工、batch Done、
  round-cap 授予、escalate 终点、open decisions。owner 三个 gate 不变。

## 送达验证（🧪 2026-08-16，诱因：Codex sandbox 拦 herdr，门铃没发出却口头宣布棒在对方）

- **宣布交棒的唯一依据是门铃命令成功返回**（send-text + 按键零退出）。「我说了棒在
  对方」不是交棒，「门铃命令成功执行」才是；
- 发完读一次对方 pane（`--source visible`）确认消息已出现；命令失败或读不到 →
  阶段状态是「**完成但传棒失败**」，把 DELIVERY FAILED 写进本轮落盘文件并报 owner
  （notification 可用就用，全断就停在原地），**禁止宣布棒已传出**；
- 门铃工具不可用是环境事故：报 owner 修环境，不得静默降级成「对方会来看文件」。

## 收棒队列（🧪 2026-08-15，Codex Tab 队列已实测：QUEUED-OK）

- **发送端状态感知**（单次查询，非监听）：目标是忙碌的 Codex → send-text + **Tab**
  （runtime 原生排队，turn 结束才投递）；其余 → Enter。用 `baton.sh send` 自动判。
  **steering（Enter 打断忙碌方）是 stop 类专属特权**；
- **接收端收棒不弃手头**：手头有未收口阶段，先推进到收口点（落盘 + commit）再处理
  队列；处理顺序：owner 亲手输入 > stop 类 > gate 相关 > 机械棒 FIFO；
- 门铃丢失无害：下一步永远可从 verdict / 棒位状态重建（文件是 ground truth）。

## 并行边界

- reviewer 审 `BASE..HEAD-A` 期间，实现者可继续产生 `HEAD-B`，但必须传棒通知；
- reviewer 只对冻结的 `HEAD-A` 下结论；`HEAD-A..HEAD-B` 自动进下一增量；
- 若新代码改动当前 finding 的同一调用链，reviewer 可纳入 closure，
  但必须显式更新 reviewed HEAD。
