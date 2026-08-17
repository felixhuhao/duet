# 跨界消息协议（inbox）

2026-08-15 拍板。跨轨（B/D/E worktree 之间）与跨仓消息的唯一标准信道，
取代「写进 Workspace 层无主 docs、指望各仓 agent 跑去看」。

## 设计不变量

1. **真源在发送方仓**：消息按 `templates/message.md` 写成文件，commit 在发送方
   自己分支的移交单目录（默认 `docs/handoffs/`，落点归项目层）。谁也不写别人的树——
   「任何 batch 只写本仓」红线无例外。
2. **kanban 只做路由**：inbox 卡上只有指针与状态（标题前缀 `[→<目标repo>]` +
   一行摘要 + payload 锚 + 到期点）。卡上信息可全丢而不损失任何事实。
3. **真源转移**：接收方读文件后在**自己仓**登账处置（去向语义同 watchlist 核销：
   核销/展期/移交，写明剩余缺口由谁承担），**关卡即回执**；发送方账上只留链接，
   不存第二份内容。

## 流程

1. 发送方写 outbox 文件并 commit；当前 runtime 无 kanban 能力时，写完文件传棒给
   有该能力的 peer，或报 owner 代建卡——能力缺失不是跳过建卡的理由；
2. 建 inbox 卡：标题 `[→<repo或worktree>] <一行摘要>`；description 填
   payload 锚（`仓:分支:路径 @ commit`）、类型、到期点；
3. 接收方 pane 正在跑时补一记 herdr 门铃（push 兜底 pull）；
4. 接收方读文件 → 自己仓登账 → 处置 → 关卡。

## 兜底与边界

- closure 轮 checklist 固定动作：按标题前缀过滤查一次本仓的 inbox 卡；
- 跨 owner：目标是对方 owner 的仓时，**格式管内容、落点跟随对方约定**
  （如 Agent 仓的需求分析文档），卡照建；
- Workspace 层 `docs/` 不再承担信道职能，只放真正无主的历史稿。
