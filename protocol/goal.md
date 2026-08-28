# Goal 协议

Goal 是一个可独立验收的用户或工程结果，也是 ownership 和交付的最小单位。

## 1. 创建

Goal 只需写清：

- **Outcome**：完成后谁能得到什么结果；
- **Scope / Non-goals**：这次做什么、不做什么；
- **Acceptance Criteria**：可观察、可验证的完成条件；
- **Constraints**：不能破坏的产品、数据、权限或契约边界；
- **Context**：必要真源、base、repo/branch/worktree；
- **Stop conditions**：遇到什么必须暂停并找 owner。

控制在一页内。文件、类、实现步骤和命令属于执行记录，不属于合同。

## 2. 开始

状态只用 `QUEUED / ACTIVE / BLOCKED / DONE / CANCELLED`。

开工前，Goal owner 必须读工作仓规则、Goal 和列出的真源，确认 cwd、branch、base 与可写范围。发现文件
缺失、上下文冲突、base 不可达或 Goal 仍有产品二选一时，不写生产代码：标记 `BLOCKED` 并给出推荐方案。

一个席位同一时间只做一个 `ACTIVE` Goal。Goal 切换时更新 Goal 文件中的 branch/HEAD 和下一动作，确保任何
人都能从文件与 Git 接手。

## 3. 执行

执行者自行决定技术方案，并持续记录：已完成、关键选择、验证证据、风险和下一动作。

局部、可逆且不改变 Goal 的问题可以直接处理。以下情况必须暂停：

- Outcome、Scope、AC 或产品语义需要改变；
- 触及未授权的共享 API、数据、安全、权限或金额边界；
- 发现可能影响其他 Goal/仓的重大事实；
- 继续会覆盖他人工作或丢失现场。

报告阻塞时写：事实、影响、已查证据、可选方案和自己的推荐。

## 4. Review 与完成

普通 Goal 由 Goal owner 自检。安全、权限、金额、数据删除、共享契约或 P0/P1 要加强验证并在合并前报告
owner，由 owner 决定是否需要独立 review；风险类别和优先级不自动占用其他席位。只有 Goal 合同已记录
owner 预授权，或 owner 在执行中明确指派 reviewer/目标席位时，Goal owner 才可发起 review。执行者可以请求，
但请求不是授权；reviewer 空闲也不是授权。reviewer 只检查冻结的 `BASE..HEAD`，不接管 Goal。

完成时在同一 Goal 文件写四项：结果、证据、未验证/风险、下一步。代码合入 canonical 主线后标记
`DONE`（非代码 Goal 在约定产物交付后标记）；仍待 review、合并、集中集成或真机验证时保持
`ACTIVE/BLOCKED` 并写清下一步，不要假装已经交付或验证。

Goal 文件是唯一必需工件。只有多个 Goal 排序或集中验证确实需要共享视图时，才增加 roadmap 或 ledger。
