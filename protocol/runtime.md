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

新客户端组合进入产品 batch 前只验五件事：

1. 用 `herdr agent start <name> --kind <kind>` 启动，重启后名字与原会话都能恢复；
2. 从真实工作目录读取项目规则与角色卡，并验证该 batch 所需目录权限；
3. idle/working/blocked 可识别，跨 session 门铃有 delivery-id 回执；
4. working 时普通门铃不会 steering 或丢失，stop 类能安全停止受影响工作；
5. 跑通一次 plan review → implementation review → owner gate，并生成一屏自含摘要。

失败只降级对应能力，修好后复验该项；不因单点问题停掉无关能力或在途 batch。

## 已有证据

- `spec_owner=Claude Code / delivery_owner=Codex`：2026-08-15~16 四批试运行通过；
- `spec_owner=Codex / delivery_owner=OpenCode 1.18`：基础路由通过；已知限制是 working 消息需
  settle 后投递、手工重启会丢 Herdr 名字、Workspace 外部目录权限尚未完成 qualification；
- 其他组合：以最新 qualification 记录为准，不从“herdr 能识别进程”推断流程已通过。
