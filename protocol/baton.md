# 传棒协议

没有 driver，也没有 idle watchdog。每个 pair 独占一个 workspace/工作树，可独占或共用
Herdr session；每个 Goal 独立传棒，pair 最多同时持有一个 ACTIVE + 一个 READY_FOR_REVIEW，接力棒按全局唯一 agent 名在 session 内外传递。

## 不变量

1. **文件是 ground truth，peer 消息只是门铃。** peer 消息只含文件路径 + verdict，
   不含内容摘要；owner 汇报另按 owner-report.md 做摘要投影。任何一轮必须能只凭落盘文件冷启动。
2. **完成自己的阶段 → Goal 文件落盘 → 传棒 → 结束当前 turn。** 成功送达即转移该 Goal 棒权；
   writer 可按 protocol/goal.md 领取下一已授权 Goal，不得自行扩队列。
3. **产品决定只认 owner 亲手输入。** peer 消息不能代表 owner。

## 消息格式

统一通过 `scripts/baton.sh send <对方agent或pane> <from-role> "..."` 发送；脚本按
runtime qualification 选择传输方式并做 delivery-id 读回：

```text
[peer:spec_owner] [delivery:d...] [to-instance:i-...] plan ready: docs/plans/2026-08-15-X-开发计划.md · round 1/2 · 请按角色卡 review
[peer:delivery_owner] [delivery:d...] [to-instance:i-...] VERDICT: FINDINGS · review-D3a.md · round 1/2 · P1x2，棒在你
```

要素：脚本生成的 peer/delivery/instance 前缀 · 事件 · 文件路径 · 轮次 · verdict（如有）。一行说完。
目标必须取 runtime 启动记录里的**全局唯一实例名**（如 `b-spec`）；`baton.sh peers` 可实时
查看所有 session 的状态。pane id 只在 session 内唯一，职责名也不能直接当目标。

## 交棒是 push，不做监听（✅ 2026-08-15，owner 指令废除 listen 模式）

- **交棒是完成动作的一部分**：产物落盘 + commit 后，完成方立即主动发门铃——
  调用门铃脚本。**没有门铃 = 阶段未完成**；
- 接收方不监听对方状态：不挂 `agent wait` 轮询，收到 `[peer:*]` 消息才动。
  sidebar 状态与 `agent wait --until blocked` 仅供 owner 主动排查卡死；不得定时调用；
- **idle 就是静默**：不设 heartbeat/backstop，不按分钟 ping agent，也不要求 orchestrator 常驻。
  Herdr integration 只被动上报状态；下一次动作只能由 peer/owner 消息或真实 blocked 事件触发。
- 门铃送达后发送方立即结束当前 turn；不得用 `sleep`、Git 或 Herdr 状态命令观察对方是否完成。

## 传棒分级（✅ 2026-08-15 起，机械段先通电）

- **机械传棒——直接调用门铃脚本 + 按 owner-report.md 给 owner 作旁观通报，不等放行**：
  ①送审草稿 ②FINDINGS 回作者修 ③修复完成请 closure 重验（附 grep 自查）
  ④增量 PASS 后续行 ⑤READY_FOR_REVIEW 后领取下一已授权 Goal。下一步由 verdict/Ready Queue 唯一确定；
  任何一次传错 → 该类立即降回 gate（D3b Done 复核）；
- **gate 传棒——按 owner-report.md 通知 owner，等亲手放行**：Ready Queue 批量授权、Contract
  实质变更、大问题影响面、round-cap、escalate 终点、open decisions 与 pilot 推广。

## 送达验证（✅ 2026-08-16，诱因：Codex sandbox 拦 herdr，门铃没发出却口头宣布棒在对方）

- **宣布交棒的唯一依据是门铃脚本成功返回**（Codex 用 delivery-id 读回；OpenCode 因
  alternate-screen 不可稳定读回，使用 prompt API 成功 + 状态转移）。「我说了」不算交棒；
- 发完按 runtime qualification 验证送达；命令失败或证据不足 →
  阶段状态是「**完成但传棒失败**」，把 DELIVERY FAILED 写进本轮落盘文件并报 owner
  （notification 可用就用，全断就停在原地），**禁止宣布棒已传出**；
- 门铃工具不可用是环境事故：报 owner 修环境，不得静默降级成「对方会来看文件」。
- 名字只定位 agent，instance 才定位本次进程；复验不一致或为 `unknown/dead` 均按送达失败处理。

## 停机条件（✅ 2026-08-17，明确交棒后的 turn 边界）

- **只在自己持有某 Goal 棒时跑到底**：做完交棒前无需 owner 的动作后传棒。合法停机只有两种：①交棒送达后结束 turn；②撞 gate 并主动发出具体 gate 门铃。停机后的 idle 静默是正常状态；
- 只剩外部依赖时，把 slice 标为 parked、记录唯一唤醒事件并报告 `pair available`，然后结束 turn。
  不挂 wait、不轮询；有已授权且不依赖该事件的 Ready Goal 时可领取，否则报告 `pair available`。

## 收棒队列（✅ 2026-08-15，Codex Tab 队列已实测：QUEUED-OK）

- **发送端状态感知**（单次查询，非监听）：职责消息与 runtime 投递分开；由
  `scripts/baton.sh` 按目标 agent kind 选择已验证的提交方式。Codex working 使用 Tab 入队；
  OpenCode 1.18 的 prompt 会并入当前 turn，因此 adapter 先做一次 server-owned settle wait，
  再作为新 turn 投递（这是 push 送达动作的一部分，不是接收方 listen）；其他 kind 只有通过
  protocol/runtime.md qualification 后才能在 working 状态接普通门铃；
  **steering 是 stop 类专属特权**；
- **接收端收棒不弃手头**：手头有未收口阶段，先推进到收口点（落盘 + commit）再处理
  队列；处理顺序：owner 亲手输入 > stop 类 > gate 相关 > 机械棒 FIFO；
- 门铃丢失无害：下一步永远可从 verdict / 棒位状态重建（文件是 ground truth）。

## 并行边界

- reviewer 审 `BASE..HEAD-A` 期间，实现者可继续产生 `HEAD-B`，但必须传棒通知；
- reviewer 只对冻结的 `HEAD-A` 下结论；`HEAD-A..HEAD-B` 自动进下一增量；
- 若新代码改动当前 finding 的同一调用链，reviewer 可纳入 closure，
  但必须显式更新 reviewed HEAD。
