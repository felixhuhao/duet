# duet

一套简单的 Goal 开发约定：**一个人负责一个 Goal，从理解问题做到可交付。**

tmux 只把多个长期 terminal 放在一起；Goal 文件和 Git 保存事实。没有自动传棒、agent 状态机或默认双角色。

## 默认流程

1. 写一个 Goal：结果、范围、验收标准、必要约束。
2. 把 Goal 交给一个固定 tmux 席位和 worktree。
3. owner 读项目规则与 Goal，确认 branch/base 后开始工作。
4. 同一个 owner 实施、验证、自检，并在 Goal 文件记录结果和证据。
5. 需要独立 review 时再叫 reviewer；否则直接交付并由 main 席位合并。

默认只需要一个 Goal 文件。Goal 多到需要排序时再加 roadmap；昂贵的跨 Goal 验证需要集中管理时再加
validation ledger。不要为可能发生的协作预先建流程。

## 五条规则

1. **一个 Goal，一个 owner。** 不在 spec/delivery 之间来回传棒。
2. **Goal 写决定，不写教程。** 写清要达到什么、不能破坏什么、怎样算完成；实现方式由执行者决定。
3. **文件和 Git 是真源。** tmux 只负责 terminal 布局与进程保活，不负责消息和状态。
4. **风险决定 review 强度。** 普通改动自检；安全、权限、金额、数据删除、共享契约、P0/P1 或 owner
   点名时加独立 review。
5. **只上报需要注意的事。** 产品选择、重大风险、真实阻塞立即找 owner；正常过程不 ping、不写流水账。

## Done 的最低标准

- Goal 的验收标准已满足；
- 相关验证已执行并记录结果；未验证面写明；
- branch/HEAD 和主要改动可定位；
- 风险、后续事项和需要 owner 决定的内容写清；
- 代码已合入 canonical 主线（非代码 Goal 则已交付），或仍保持 `ACTIVE/BLOCKED` 并说明差什么。

## tmux 布局

```text
mobile
├── main   主树：规划、合并、真源维护
├── dev1   固定 worktree：solo Goal owner
├── dev2   固定 worktree：solo Goal owner
└── dev3   固定 worktree：solo Goal owner
```

window 和 worktree 长期复用；换 Goal 只换 branch。owner 直接进入相应 window 沟通，不用 `send-keys`
做 agent-to-agent 自动消息。运行命令见 [tmux runbook](scripts/TMUX-RUNBOOK.md)。

## 日常只读这些

- [Goal 协议](protocol/goal.md)：Goal 怎么开始、停止和完成；
- [Goal 模板](templates/goal.md)：复制到工作仓，按需删掉空项；
- [Runtime 协议](protocol/runtime.md)：tmux、worktree 与 native session 的边界；
- [tmux runbook](scripts/TMUX-RUNBOOK.md)：setup、resume 和恢复命令。

其余 `roles/`、`protocol/baton.md`、Herdr 文档和旧 batch 模板是兼容/历史资料，**不是默认流程，
日常无需阅读**。具体项目规则、产品红线、文档落点和 Git 约定始终以工作仓自己的 `AGENTS.md` 为准。
