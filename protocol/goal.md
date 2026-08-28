# Goal 协议

Goal 是一个可独立验收的用户或工程结果，也是 ownership 和交付的最小单位。

## 1. 合同

Goal 只需写清：

- **Outcome**：完成后谁能得到什么可观察结果；
- **Scope / Non-goals**：做什么、不做什么；
- **Acceptance Criteria**：怎样观察和验证完成；
- **Constraints / Stop conditions**：不能破坏什么，何时必须找 owner；
- **Context**：必要真源、repo/base/branch/worktree。

实现步骤、命令流水和教程不属于合同。项目已有自己的 Goal 格式或 lifecycle 时，以项目规则为准。

## 2. 开始

一个席位同时只拥有一个 active Goal。开工前必须读取目标项目规则和 Goal，确认 cwd、branch、base、可写范围
与授权边界。文件缺失、base 不可达、现场会被覆盖或仍有产品二选一时，停止生产写并报告事实、影响、选项和
推荐方案。

## 3. 执行

Goal owner 自行决定 Goal 范围内的技术方案，并持续保留可接手事实：当前 HEAD、已完成、关键选择、验证结果、
未验证风险和下一动作。

局部、可逆且不改变 Goal 的问题可以直接处理。以下情况必须暂停对应范围：

- Outcome、Scope、AC 或用户可见语义需要改变；
- 触及未授权的共享 API、数据、安全、权限、金额或外部状态；
- 可能覆盖他人工作、丢失现场或影响另一个 Goal/仓；
- 继续执行需要新的 push、部署、发布、删除或跨席位权限。

## 4. Review 与完成

普通 Goal 由 Goal owner 自检。风险提高验证强度，但不自动取得其他席位：只有 Goal 合同已记录 owner
预授权，或 owner 明确指派 reviewer/目标席位时，才能发起独立 review。执行者请求、优先级、风险类别或
reviewer 空闲都不是授权。

完成时在 Goal 记录：结果、证据、未验证/风险、下一步。代码是否必须合并、push 或完成集成/真机验证，由项目
自己的 lifecycle 裁决；不得把 Development 证据写成 Integration、Device 或 Release 已完成。
