# Runtime 绑定与资格协议

职责角色固定，客户端可换：`spec_owner` = Plan 主笔 + Acceptance Reviewer；
`delivery_owner` = Plan Reviewer + Implementation Owner。Herdr 活实例按 `<pair>-<role>` 唯一命名。

## 多 pair 拓扑

一个 pair 独占一个命名 Herdr session，因此多个 terminal 可分别显示完整 pair，互不争抢
active workspace。`scripts/herdr-federation.py` 每次从所有 running session 实时聚合 agent；
`baton.sh peers/send/read/wait` 据此跨 session 路由，不缓存状态、不发送 heartbeat。原生 TUI
sidebar 只显示本 session，跨 pair 状态由 `baton.sh peers` 按需查询。

## 每个 pair 必须声明

```text
spec_owner:     <global herdr name> · <session> · <kind> · <cwd> · roles/spec-owner.md
delivery_owner: <global herdr name> · <session> · <kind> · <cwd> · roles/delivery-owner.md
```

plan 或启动记录须保存这些项；calibration 同时记职责角色与 runtime，不能把客户端表现归因给角色。

## Runtime 资格

新客户端组合在进入产品 batch 前必须完成空载 qualification：

1. 两端均由 `herdr agent start <name> --kind <kind>` 启动并能恢复会话；
2. 冷启动能读项目 `AGENTS.md`、自己的角色卡和 baton/verdict/escalation；
   OpenCode pane 须设 `OPENCODE_DISABLE_CLAUDE_CODE=1`，避免目录中的兼容 `CLAUDE.md`
   或历史 `claude.md` 被隐式加载成另一职责；
3. idle / working / blocked 三态识别可信；
4. working 时的普通门铃不 steering，按 FIFO 只消费一次；stop 类可以显式打断；
5. 发送命令成功且以 delivery id 从目标 pane 读回；失败必须报 `DELIVERY FAILED`；
6. owner gate、escalation 中继和一轮 FINDINGS→closure PASS 能走完；
7. runtime 缺通知、看板或外部目录权限时，capability fallback 能把动作交给 peer/owner。

未通过的组合只能做 qualification，不得进入产品 batch。已通过组合出现一次坏 case，立即降级重验。

## 已有证据

- `spec_owner=Claude Code / delivery_owner=Codex`：2026-08-15~16 四批试运行通过；
- `spec_owner=Codex / delivery_owner=OpenCode 1.18`：2026-08-17 空载 qualification 通过；
  working 直接 prompt 实测会并入当前 turn，故只允许 settle-then-deliver adapter；通知无前台
  客户端时必须走 capability fallback。细节见当日 qualification 记录；
- 其他组合：以最新 qualification 记录为准，不从“herdr 能识别进程”推断流程已通过。
