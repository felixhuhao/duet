# Workspace 本机附加规则

此文件只属于当前机器，不进入 duet 或任何业务仓。由 owner 按本机用途填写；新机 bootstrap 时复制为
workspace 根目录的 `AGENTS.local.md`，后续同步共享 `AGENTS.md` 时保留。

可记录：

- 本机 worker 数量、canonical worktree 与是否允许额外 seat；
- CPU、内存、模拟器、Docker、端口等资源限制；
- 已由 owner 授权的正常 commit/push 同步节奏；
- 仅本机适用的恢复、驻留或串行执行约束。

不得记录：

- token、账号、绝对用户路径或其它秘密；
- 产品/API/支付/隐私、测试门禁、Release authority 等项目真源；
- 试图放宽目标仓安全规则或外部动作授权的覆盖。
