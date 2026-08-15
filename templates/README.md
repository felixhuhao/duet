# templates

**这里是必备字段契约 + 新项目起步默认，不取代项目现有格式。**（2026-08-15 拍板）

已有自己文档规范的项目（如 byteme_mobile 的 `AI_AGENT_DEV_SPEC.md` + migration 文档约定）
继续用自己的格式，只要下列字段在某个真源里存在即可：

- **plan**：outcome / scope 与 out-of-scope / redlines+authority 来源 / 可观察 AC /
  open decisions / Errata 节（追加式）/ 冻结状态与 BASE；
  跨仓 batch（仅限同 owner 多仓的声明式例外）另须声明：仓清单 + 各仓 writable scope +
  各仓 BASE；跨仓特性的子 batch 须链接父需求文档（authority 仓）；
- **devlog（或等价实施记录）**：增量 commits 范围 / 证据块（cmd·scope·result·noise）/
  已知限制 / 被暂停 slice；
- **review**：round 计数 / BASE 与 reviewed HEAD / blockers（绑定依据）/ watchlist+到期点 /
  VERDICT 块（见 protocol/verdict.md）。

字段缺失 = reviewer 可拒收，不是 finding。
