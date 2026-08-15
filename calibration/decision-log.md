# Decision Log（校准记录 · owner 收件箱）

每次 escalate（及 Stage 0 的传棒放行）记一行。类型定义见 protocol/escalation.md，
毕业规则见 stage.md。追加写入，不修改历史行——**例外**：「owner 裁决」「一致?」两列
从 ⬜ 填成结论属于完成记录，不算改历史。

**⬜ 行 = owner 收件箱**：owner 扫本文件即知全轨有什么等拍。closure 轮逐条重提
悬置 ⬜ 或显式搁置（搁置也要写进裁决列）。

**行 = 索引级摘要**（2026-08-15 起）：一句话上下文 + 建议结论 + 裁决结论 +
工作仓真源路径。完整语境、可选方案、依据长文一律写工作仓 review 文件——本仓私有，
团队看不见；两处长文必漂移。首跑（D3b OD-1~6）的历史行按当时写法保留，不改。

| 日期 | 类型 | 仓库/batch | 上下文（文件+行） | agent 建议 | owner 裁决 | 一致? |
|---|---|---|---|---|---|---|
| 2026-08-15 | open-decision | byteme_mobile / D3b | `docs/duet/review-D3b.md` OD-1 · 一页历史里单个 run 的 steps 取失败时用户看到什么 | **A**：整页失败给显式错误+重试；单 run 失败给「这一轮没读回来」占位，其余照常。不跟 web 的静默降级——本仓已为「空列表=没历史」这个无声错付过一次代价（实施记录 §3.9） | ⬜ | ⬜ |
| 2026-08-15 | open-decision | byteme_mobile / D3b | `docs/duet/review-D3b.md` OD-2 · 历史翻页的用户形态 | **①滚到顶自动加载**，与 D1a 已交付的会话列表无限滚动同形。把握不足：③「本轨不做翻页」也是诚实选项 | ⬜ | ⬜ |
| 2026-08-15 | open-decision | byteme_mobile / D3b | `docs/duet/review-D3b.md` OD-3 · D3 Done 的边界 | D3 Done ≡ D3-W1 + D3-W2 关闭 + AC-16/17/18 通过；D3-W3 留在 D4 开工不动 | ⬜ | ⬜ |
| 2026-08-15 | open-decision | byteme_mobile / 存量交接 | `docs/duet/review-D3b.md` OD-4 · 存量收藏账目 D-L1 的到期点 | **②改挂到期点 = D1b 开工**，不核销：`loadFavorites` + 收藏页确实还没做，核销等于让真实缺口从账上消失 | ⬜ | ⬜ |
| 2026-08-15 | baton-confirm | byteme_mobile / D2a 在飞 | `docs/duet/review-D3b.md` OD-5 · `2cb9f95e` / `4bac7b01` 走哪个流程收尾 | **①按旧流程在实施记录里收尾 D2a**，D3b 只审 D3 diff。混账会毁掉补充卡第 4 步要保的「两个时代不混算」 | ⬜ | ⬜ |
| 2026-08-15 | open-decision | byteme_mobile / 存量交接 | `docs/duet/review-D3b.md` OD-6 · endpoint audit 抽取债的归属 | 移出 D 账目，登记到 `tool/endpoint-audit/README`，到期点「下一次并行轨合并前」——它不该由某条轨的批次进度决定生死 | ⬜ | ⬜ |
| 2026-08-15 | baton-confirm | byteme_mobile / D3b | Stage 0 传棒：交接仪式 + plan errata 已落盘，请求放行传棒给 Codex 做 plan review | **暂不传棒**：门槛 #2/#5 未过（根因 OD-1），plan 未达冻结条件。先拍 OD-1～OD-3，再传 | ⬜ | ⬜ |
