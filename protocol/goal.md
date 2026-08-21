# Goal 运行协议 · v1

> 2026-08-20 owner 确认。新工作以 Goal 为调度与交付单位；旧 track/batch 工件只保留历史，
> 未完成项重新映射进 Goal 后才能继续。设计目标依次是：缩短日历时间、减少 owner 中断、提高交付
> 确定性、提高 agent 利用率。

## 1. 三份真源

1. **Canonical Outcome Roadmap**：用户结果、Priority、`blocked_by`、Ready Queue 与当前状态；
2. **Goal 文件**：稳定 Contract、可更新 Execution Notes、Readiness/Code Review、Completion Package、
   条件式 Retrospective；
3. **Validation Ledger**：frozen HEAD、Integration/Device 状态与测试债务。

时间、token、工具调用和等待问题不另建台账；异常复盘从对话/执行记录提取结论，追加到 Goal。

## 2. Goal Contract 与 Ready

- Contract 控制在一页：Outcome、Core、Non-goals、产品边界、3–7 条可观察 AC、invariants、
  dependencies、stop conditions、validation tier、fallback boundary；不预定文件、类和实现步骤；
- 实现方案、文件、命令、HEAD、checkpoint、发现和下一动作写 Execution Notes，可随执行更新；
- 只有 Outcome、Core/Non-goals、可观察行为、数据语义、产品边界、stop condition 或 validation tier
  改变才追加 Contract Addendum；普通实现发现不改合同；
- 产品选择在 roadmap grooming 时完成。仍有方向二选一时先做 Decision/Discovery Goal；
- Goal 只分 S（约半天）/M（约一天）/L（最多两天），超过 L 在 Ready 前拆分；
- owner 一次授权每对 2–3 个有序 Goal；降到一个 Ready 时请求补队列，开工不重复确认。

**Ready 不等于已领取。** `QUEUED → ACTIVE` 前，Goal 必须冻结 Pickup Context：目标仓/cwd/role、
可从目标 cwd 解析的精确 `repo@sha:path` 必读集、继承决定/禁止重开项、首个 increment 与 refresh/stop
条件。跨仓 Goal 各仓有同 Goal ID 的本地 child，链接 parent authority，不让接收者从另一仓零散文档拼合同。
投递只需携 Goal 文件路径与 commit；接收者先只读装载并把 Context Receipt 落盘：实际读取的路径/SHA、
Outcome/Core/Non-goals/invariants 复述、第一动作和冲突。Receipt `ACCEPTED` 前禁止生产写；缺文件、SHA
漂移或结论冲突则记 `REJECTED`、Goal 转 `NEEDS_REFRESH` 并升级，不得以重新 discovery 代替上下文。
新 Goal 领取前还必须冻结 canonical BASE（如本地 `v2@SHA`），让固定 worktree 的目标 branch 包含该
SHA，并以 `git merge-base --is-ancestor <SHA> HEAD` 通过为准；Receipt 记录命令与结果。不同步不 ACTIVE，
冲突则停止；不得用 reset/rebase 覆盖现场，也不把“同步本地 v2”解释成自动 fetch/pull。

## 3. 生命周期与并行

`QUEUED → ACTIVE → READY_FOR_REVIEW → DEV_DONE`；`BLOCKED/NEEDS_REFRESH/CANCELLED` 为旁路状态。
每对最多一个 ACTIVE + 一个 READY_FOR_REVIEW，不能同时开发两个 Goal。Goal 期间 ownership 固定；
完成后从全局 Ready Queue 领取，领域熟悉度只作优先项。跨仓用户结果共用 Goal ID，各仓独立 branch/
commit，由一个 delivery owner 汇总。共享热点遵守单写者。

两日是强制 checkpoint，不是停工线：Contract 与 stop condition 未变则继续；Core 外 extension 自动回队列。
同一 Goal 的模型/session/terminal 更换读 Resume Capsule；换 Goal 必须重新走 Pickup Context/Receipt，
不能把长期 agent 的旧上下文当作新 Goal 已装载。

## 4. 问题、Review 与 Merge

- 小问题：局部、可逆、不改 Contract/共享边界，记录后继续；
- 大问题：可能改变 AC、架构、共享 API、数据、安全或后续前提，暂停当前 Goal 与依赖项并报告；
  无法判断按大问题。无依赖的其他 pair 可继续；
- Code Review 只以 AC、正确性、安全、数据、兼容边界和明确高风险问题阻塞；P2/Suggestion 入 follow-up；
- 最多 substantive + closure 两轮；writer 等 review/merge 时可领取下一已授权 Goal；
- reviewer PASS 后由 merge-owner 候选池串行合并；frozen HEAD 验证已合入 Goal，不是日常 merge gate；
- Goal branch 到 merged、superseded 或 owner cancelled 后才删除；阻塞时保留 HEAD + Resume Capsule；
- worktree 是 owner 预置的长期席位，Goal 完成只合并/处置 branch，不删除或新建 checkout；席位下一 Goal
  继续在原 cwd 使用。任何创建、移动、删除 worktree 的动作都必须由 owner 明确安排。

## 5. Validation 成本模型

- `I0`：无外部行为变化，静态/unit/定向验证；
- `I1`：局部边界或行为变化，定向 contract/integration，可用 mock；
- `I2`：P0/P1 关键旅程或资金、账号、session、迁移、SSE 等，进入下一 frozen HEAD 端到端验证；
- P0/P1 Goal 必须交付 AC、测试数据需求、必要 mock seam，并说明复用测试或关联 QA Goal；
- `DEV_DONE` 不等待 Integration/Device。二者独立记 `NOT_RUN/PASS/FAIL/BLOCKED`；仅未完成 I1/I2
  计债，两项或 48h 强制清债；
- 同一昂贵测试通常只跑基线一次 + 相关修复后一次。frozen HEAD 默认自适应：同一自然日累计
  3 个 `DEV_DONE` 时当日集中一次，否则每累计 3 个 Goal 请求一次；债务上限可提前触发，owner
  可随时改频率。真机 smoke 随 frozen HEAD，完整矩阵在 milestone/RC。

## 6. 汇报、复盘与变更

每个 Goal 在 DEV_DONE 生成自含 Completion Package；发送频率由 owner 指定。需要产品拍板、Q4 级风险、
队列补充或有意义状态变化时立即报告；idle 不 ping、不 heartbeat。完整 Retrospective 仅在超过两日、
反复 review、昂贵测试异常或 owner 点名时追加。规则带版本号，只在 pilot review/frozen HEAD 后集中升级，
安全与数据紧急项除外。前三个 Goal 为 pilot；pilot review 经 owner 确认后才推广全 roadmap。
