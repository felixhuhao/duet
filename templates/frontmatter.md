# 状态头（YAML frontmatter）· 第一轮格式

> 🧪 试行 2026-08-16。目的：把散在各工件 `text` 块里的状态字段抽成机器可读的
> 文件头，供 `scripts/dashboard.py` 渲染态势板。**真源仍是 md 文件本身**——
> frontmatter 是文件自己的一部分，不是第二真源；页面是纯渲染层，随时可整页重生成。

## 规则

1. 放在文件**最顶部**（`# 标题` 之前），`---` 包围的扁平 YAML；
2. **谁改状态谁顺手更新**（顺手总则适用：机械同步，无判断含量）；
   正文里的状态叙述仍照写，frontmatter 只是它的机器可读投影，两者不一致以正文为准并当场修头；
3. 时间与现状断言遵守**时刻级 as-of**：`as_of` 写到分钟，或写 `repo@sha（本地/已fetch）`；
4. 只加下面的字段，别发明新键；缺的字段直接省略，不写空值。

## 字段表

| 键 | 取值 | 适用 |
|---|---|---|
| `doc` | `plan` `review` `devlog` `decision-pack` `handoff` `handoff-index` `roadmap` | 全部 |
| `track` | `全局` `B钱` `D对话` `E分身` `C经营` `AGT` `跨仓` … | 全部 |
| `batch` | `B8` `D4` `D3b` … | batch 级工件 |
| `status` | `draft` `frozen` `in-progress` `pending-owner` `paused` `done` `archived` `open` | 全部 |
| `baton` | `claude` `codex` `owner` `none` | 活跃 batch |
| `round` | `1/2` 等（照 verdict 块抄） | review |
| `base` / `covers` | 短 SHA | plan / review |
| `blocked_on` | 列表：`["B4 ← D2b", "owner: 拍板"]` | 有阻塞时 |
| `next` | 一行：**承担者 + 动作**；等 owner 的一律以 `owner:` 开头（态势板据此聚合「等你」队列） | 未完结工件 |
| `as_of` | `2026-08-16 21:40` 或 `Agent/main@f3199778（本地）` | 有现状断言时 |
| `updated` | 分钟级时间 | 全部 |

## 示例

```yaml
---
doc: review
track: D对话
batch: D4
status: done
round: 1/2
covers: dba2f7d5
updated: 2026-08-16 21:40
---
```
