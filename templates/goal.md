---
doc: goal
goal: <GOAL-ID>
process_version: goal-v1
priority: <P0|P1|P2|enablement>
size: <S|M|L>
status: <queued|active|ready-for-review|dev-done|blocked|needs-refresh|cancelled>
owner: <delivery owner>
blocked_by: []
integration: <NOT_RUN|PASS|FAIL|BLOCKED|N/A>
device: <NOT_RUN|PASS|FAIL|BLOCKED|N/A>
base: <repo@sha；跨仓逐项列出>
updated: <YYYY-MM-DD HH:mm>
---

# <GOAL-ID> · <用户结果>

## Goal Contract · 稳定层（目标一页内）

### Outcome

<一个完整、可观察的用户结果。>

### Core / Non-goals

- Core：
- Non-goals：

### 产品边界与 Invariants

- <用户可见、金额、权限、隐私、数据、平台红线；注明 authority。>

### Acceptance Criteria（3–7 条）

- [ ] AC-1：Given / When / Then，能在 UI、状态、请求或持久化层观察。

### Dependencies / Stop Conditions

- `blocked_by`：
- 必须停止讨论：<会改变 Contract 或污染后续 Goal 的条件。>

### Validation / Fallback Boundary

- tier：`I0 | I1 | I2`
- 开发证据：
- Integration 责任：<复用既有测试 | 关联 QA Goal | N/A + 理由>
- Device residual：
- Fallback boundary：<Core 外自动回队列的扩展项。>

### Contract Addenda（只追加）

<只有 Contract 字段实质改变时追加：日期 / 原条款 / 新条款 / authority / 影响。>

## Readiness Review

- reviewer / Contract HEAD：
- coverage：decision / acceptance / authority / start-risk / not-verified
- findings：无；或固定关闭条件
- verdict：`PASS | FINDINGS | ESCALATE`（最多 substantive + closure 两轮）

## Execution Notes / Resume Capsule · 可更新层

- branch / HEAD / worktree：
- 当前 checkpoint：
- 已完成：
- 关键技术选择：
- 已执行证据：`cmd / scope / result / noise`
- 小问题与 follow-up：
- 下一动作：
- 大问题 / 受影响依赖：无

## Code Review

- reviewer / BASE / reviewed HEAD / round：
- coverage：reviewed / spec / risk / evidence / not-verified
- P0/P1：无；或 finding + 固定关闭条件
- P2/Suggestion：<进入 follow-up，不阻塞>
- verdict：`PASS | FINDINGS | ESCALATE`
- merge：`PENDING | <merge commit>`

## Completion Package · DEV_DONE 时填写

- **结论**：Outcome 是否成立；当前 lifecycle 状态。
- **用户现在能做什么**：
- **实际修改及影响**：
- **意外发现及意义**：无；或 <事实 → 意义>。
- **证据状态**：Development / Integration / Device 分别列明。
- **Follow-up / 风险**：
- **需 owner 拍板**：无；或题面 + 选项代价 + 推荐。
- **下一步**：review / merge / QA Goal / Ready Queue。

## Retrospective · 条件触发

<只在 >2 天、反复 review、昂贵测试异常或 owner 点名时填写；从对话与执行记录提取，
说明时间/token 花在哪里、根因、下次保留/删除/改变什么。>
