# Plan：<batch 名>

```text
status:  draft | frozen（冻结日期）
batch:   <track>-<批次号>
BASE:    <冻结时的 repository commit SHA>
owner:   goal_owner=<name>/<runtime> · tmux=<session:window.0> · cwd=<worktree>
review:  <none | reviewer=<name>/<runtime> + trigger>
```

## Outcome

<用户或业务 outcome，一段话>

## Scope / Out-of-scope

- in：
- out：

<能被 reviewer 独立批准/拒绝且不破坏同一 outcome 的 slice，应拆成独立 batch>

## Authority

<只列会改变 decision core 的关键事实；代码/跨仓事实注明 repo + 精确 SHA + 文件，
无法取得声明快照的写进未验证面，不用 mutable HEAD 代替>

## Redlines

<不可突破项：旧路径兼容、金额、权限、持久化边界等，每条注明来源>

## Acceptance Criteria

<每条必须可在 UI、状态、请求或持久化层被观察>

- [ ] AC1：
- [ ] AC2：

## Frozen decisions

<本批已定的产品/方向选择>

## Open decisions

<仍待 owner 拍板项；每项注明是否阻塞开工、影响哪些 slice、看板卡链接>

## 依赖与到期点

## Watchlist（继承或新增，必须有到期点）

## Errata（冻结后追加，不改动上文）

<实现暴露的 plan 缺陷记在此；影响 scope/AC 时走局部重开>
