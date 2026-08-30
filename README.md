# duet v2

duet 是一套可版本化、可迁移的个人 AI 工作方法：用一个 Goal owner 从理解问题走到可交付，用 Herdr 保存
长期运行现场，用 skills 携带跨项目可复用的方法。

duet **不是业务仓依赖**。共享项目必须凭自己的 `AGENTS.md`、代码和文档自含；项目不需要引用、安装或知道
duet。个人开发环境可以安装 duet skills，CI 也不需要它。

## 默认流程

一个 Goal owner 在 Herdr 固定席位上，从合同（outcome/scope/AC/停止条件）走到带证据的诚实交付；
review 与外发动作的授权边界见协议。细节以 [Goal 协议](protocol/goal.md)与
[Runtime 协议](protocol/runtime.md)为准，本文件不复述。

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
templates/  Goal、workspace 共享 hand files 与 host-local overlay 示例；仅在确有共享排序/验证
            需要时使用 roadmap/ledger
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
