# duet

一套简单的 Goal 开发约定：**一个人负责一个 Goal，从理解问题做到可交付。**

Herdr 把长期 terminal 集中到一个面板并显示 agent 状态；Goal 文件和 Git 保存工作事实。没有默认双角色、
自动传棒或复杂状态机。

## 默认流程

1. 写一个 Goal：结果、范围、验收标准、必要约束。
2. 把 Goal 交给 Herdr `default` session 中的一个固定席位和 worktree。
3. Goal owner 读项目规则与 Goal，确认 branch/base 后开始工作。
4. 同一个 owner 实施、验证、自检，并在 Goal 文件记录结果和证据。
5. 需要独立 review 时再叫 reviewer；否则交付并由 canonical 主树合并。

默认只需要一个 Goal 文件。Goal 多到需要排序时再加 roadmap；昂贵的跨 Goal 验证需要集中管理时再加
validation ledger。不要为可能发生的协作预先建流程。

## 五条规则

1. **一个 Goal，一个 owner。** 不在 spec/delivery 之间来回传棒。
2. **Goal 写决定，不写教程。** 写清要达到什么、不能破坏什么、怎样算完成；实现方式由执行者决定。
3. **Herdr 显示运行态，文件和 Git 裁决交付态。** 面板告诉你 agent 是否在工作；它不代替验收证据。
4. **风险决定 review 强度。** 普通改动自检；安全、权限、金额、数据删除、共享契约、P0/P1 或 owner
   点名时加独立 review。
5. **只上报需要注意的事。** 产品选择、重大风险、真实阻塞立即找 owner；正常过程不 ping、不写流水账。

## 面板状态

| Herdr 状态 | 含义 | owner 动作 |
|---|---|---|
| `working` | agent 正在执行 turn | 等待或查看 pane |
| `blocked` | 等待审批或回答 | 进入 pane 处理 |
| `idle` / `done` | 可接收下一条消息；`done` 表示后台完成后尚未查看 | 查看回复或派下一项 |
| `unknown` | Herdr 无法可靠判断 | 进入 pane 核实 |

这些是 agent 运行态，不是 Goal lifecycle。只有代码合入 canonical 主线（或非代码产物已交付）后，Goal
才标 `DONE`。

## 默认布局

```text
Herdr session: default
├── byteme_mobile   canonical 主树：规划、合并、真源维护
├── wt1 / dev1      固定 worktree：solo Goal owner
├── wt2 / dev2      固定 worktree：solo Goal owner
└── wt3 / dev3      固定 worktree：solo Goal owner
```

打开统一面板只需运行 `herdr`。workspace、worktree 和 agent name 长期复用；idle 分支使用
`wt1/wt2/wt3`，换 Goal 再切 Goal branch。

## 日常只读这些

- [Goal 协议](protocol/goal.md)：Goal 怎么开始、停止和完成；
- [Goal 模板](templates/goal.md)：复制到工作仓，按需删掉空项；
- [Runtime 协议](protocol/runtime.md)：Herdr 状态、worktree 与 native session 的边界；
- [Herdr runbook](scripts/HERDR-RUNBOOK.md)：打开、resume 和恢复命令。

其余双角色、baton、旧 batch 模板和 tmux 工具是兼容/历史资料，**不是默认流程，日常无需阅读**。
具体项目规则、产品红线、文档落点和 Git 约定始终以工作仓自己的 `AGENTS.md` 为准。
