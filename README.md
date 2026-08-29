# duet v2

duet 是一套可版本化、可迁移的个人 AI 工作方法：用一个 Goal owner 从理解问题走到可交付，用 Herdr 保存
长期运行现场，用 skills 携带跨项目可复用的方法。

duet **不是业务仓依赖**。共享项目必须凭自己的 `AGENTS.md`、代码和文档自含；项目不需要引用、安装或知道
duet。个人开发环境可以安装 duet skills，CI 也不需要它。

## 默认流程

1. 用一个 Goal 写清 outcome、scope、验收标准、约束和停止条件。
2. owner 把 Goal 交给 Herdr `default` session 中一个固定席位与 worktree。
3. 同一个 Goal owner 读取项目规则，确认 cwd、branch、base 和写入权限。
4. owner 实施、验证、自检，在 Goal 中记录结果、证据、未验证面和下一步。
5. 只有 Goal 预授权或 owner 明确指派时才调用独立 reviewer；否则直接交付。
6. 是否合并、push、部署或删除，始终服从目标项目和用户当前授权。

## 知识边界

duet 可以保存：

- 跨项目稳定的方法、判断边界和验收纪律；
- owner 自己的多仓工作站 bootstrap / 机器生命周期操作手册；其中可以列出项目安装步骤，但不得取代
  项目仓内的实时工具链、验证、Release 或 CI authority；
- 第一方 skills 及其必要 reference/script；
- Herdr solo runtime 和可复用 Goal 模板；
- 已知来源的第三方 skill 清单，不复制同一依赖的多份安装结果。

duet 不保存：

- 产品/API/支付/隐私等业务真源；
- 项目工具链、branch、release 或 CI 私有约定；
- token、账号、session、浏览器状态、签名私钥、机器审批记录或绝对用户路径；
- Codex 系统 skills、plugin cache 或来源/许可证不明的第三方大包。

## v2 内容

```text
protocol/   Goal 与 Herdr runtime 的最小协议
templates/  Goal；仅在确有共享排序/验证需要时使用 roadmap/ledger
skills/     第一方可移植 skills 与第三方来源清单
scripts/    Herdr 启动和只读 worktree 审计
docs/       机器生命周期 runbook 与跨项目 playbooks
```

- [Goal 协议](protocol/goal.md)
- [Runtime 协议](protocol/runtime.md)
- [Herdr runbook](scripts/HERDR-RUNBOOK.md)
- [机器生命周期 runbook](docs/machine-lifecycle.md) ·
  [ByteMe Mobile 三端开发机 bootstrap](docs/byteme-mobile-three-platform-bootstrap.md) ·
  [playbooks](docs/playbooks.md)
- [Goal 模板](templates/goal.md)
- [`duet-goal-workflow`](skills/duet-goal-workflow/SKILL.md)
- [`mobile-ui-audit`](skills/mobile-ui-audit/SKILL.md)

v2 之前的现场由 Git tag `v1-final` 保存，不在当前工作树维护兼容副本。
