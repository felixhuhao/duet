# Escalation 协议

## 触发条件

命中任何一条即出循环，通知 owner：

1. round 2/2 结束仍有未关闭 P0/P1 或双方争议（protocol/verdict.md）；
2. open-decision 触发条件命中（roles/codex.md，产品选择类立即触发，不等轮次）；
3. 任一方认为继续会撞 redline 或需要 owner 显式接受风险。

## Escalate 必附推荐判定（校准的核心）

**没有这一栏，磨合就没有信号。** 每次 escalate，发起方必须写下
"如果没有 owner，我本来会怎么判"，owner 裁决后双双记入
`calibration/decision-log.md`：

```text
| 日期 | 类型 | 上下文（文件+行） | agent 建议 | owner 裁决 | 一致? |
```

类型取值：`round-cap` / `P0P1-dispute` / `open-decision` / `redline-risk` / `baton-confirm`。

## 争议格式

双方立场各 **≤10 行**：主张 / 依据 / 采纳的代价。owner 只看这两段拍板，
不重读全部上下文。这是对 owner 注意力的保护，超长立场视为无效。

## 通知方式

- `herdr notification show "<类型>: <一句话>" --body "<文件路径>"`；
- pane 转入 blocked 状态（sidebar 可见）。

## Open decision 的落点路由（2026-08-15 拍板）

| OD 作用域 | 真源 |
|---|---|
| 轨内（产品选择、batch 边界、存量账目） | 本 batch review 文件 OD 节 / plan 待拍板节 |
| 跨轨结构性（不属于任何单轨） | migration ROADMAP「尚未拍板且影响排期」节 |
| 跨 owner（要别人的仓改东西） | 对方仓需求分析文档（如 `Agent/docs/plans/`） |
| owner 收件箱 | decision-log 中 ⬜ 行（escalate 必记，天然聚合） |

kanban 建卡不强制，owner 需要排期跟踪时自建。判错路由不算 finding，
由 escalate 时纠正。

## 不对称原则

- **stop 从严，永不放松**：疑似 P0 一律先停受影响 slice，宁可 owner 按一次继续，
  不可让带 P0 的增量滑过去；
- **escalate 的误报随磨合调低**：某类型在 decision-log 中达到毕业条件后转自动
  （见 calibration/stage.md），但 open-decision 类设计上永不毕业。
