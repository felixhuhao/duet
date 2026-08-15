# Decision Log（校准记录 · owner 收件箱）

每次 escalate（及 Stage 0 的传棒放行）记一行。类型定义见 protocol/escalation.md，
毕业规则见 stage.md。追加写入，不修改历史行——**例外**：「owner 裁决」「一致?」两列
从 ⬜ 填成结论属于完成记录，不算改历史。

**⬜ 行 = owner 收件箱**：owner 扫本文件即知全轨有什么等拍。closure 轮逐条重提
悬置 ⬜ 或显式搁置（搁置也要写进裁决列）。

**单写者 = Claude**（🧪 2026-08-15，诱因：round-cap 双账）：一次 escalation 只记一行，
由 Claude 记；发起方是 Codex 时「agent 建议」列**原样摘录**其 verdict 文本，不改写。

**行 = 索引级摘要**（2026-08-15 起）：一句话上下文 + 建议结论 + 裁决结论 +
工作仓真源路径。完整语境、可选方案、依据长文一律写工作仓 review 文件——本仓私有，
团队看不见；两处长文必漂移。首跑（D3b OD-1~6）的历史行按当时写法保留，不改。

| 日期 | 类型 | 仓库/batch | 上下文（文件+行） | agent 建议 | owner 裁决 | 一致? |
|---|---|---|---|---|---|---|
| 2026-08-15 | open-decision | byteme_mobile / D3b | `docs/duet/review-D3b.md` OD-1 · 一页历史里单个 run 的 steps 取失败时用户看到什么 | **A**：整页失败给显式错误+重试；单 run 失败给「这一轮没读回来」占位，其余照常。不跟 web 的静默降级——本仓已为「空列表=没历史」这个无声错付过一次代价（实施记录 §3.9） | **A**（owner huh · 2026-08-15；查明为纯前端决定，零后端依赖） | ✅ 一致 |
| 2026-08-15 | open-decision | byteme_mobile / D3b | `docs/duet/review-D3b.md` OD-2 · 历史翻页的用户形态 | **①滚到顶自动加载**，与 D1a 已交付的会话列表无限滚动同形。把握不足：③「本轨不做翻页」也是诚实选项 | **①**（owner huh · 2026-08-15；纯前端，游标现成） | ✅ 一致 |
| 2026-08-15 | open-decision | byteme_mobile / D3b | `docs/duet/review-D3b.md` OD-3 · D3 Done 的边界 | D3 Done ≡ D3-W1 + D3-W2 关闭 + AC-16/17/18 通过；D3-W3 留在 D4 开工不动 | **六条 Done 条件**（owner huh · 2026-08-15）：W1+W2+AC 六条+全量门禁+交付索引+**新开 testcases 一份**；真机手感转 D3-W4 | ✅ 一致 |
| 2026-08-15 | open-decision | byteme_mobile / 存量交接 | `docs/duet/review-D3b.md` OD-4 · 存量收藏账目 D-L1 的到期点 | **②改挂到期点 = D1b 开工**，不核销：`loadFavorites` + 收藏页确实还没做，核销等于让真实缺口从账上消失 | **①′ 核销并写明去向**（owner huh · 2026-08-15）：剩余缺口已被 plan §4 D1b 行 + X-1 覆盖，改挂到期点会造第三份账 | ❌ **不一致**（首判 ②；Claude 补查后自行改判 ①′，owner 采纳 ①′）|
| 2026-08-15 | baton-confirm | byteme_mobile / D2a 在飞 | `docs/duet/review-D3b.md` OD-5 · `2cb9f95e` / `4bac7b01` 走哪个流程收尾 | **①按旧流程在实施记录里收尾 D2a**，D3b 只审 D3 diff。混账会毁掉补充卡第 4 步要保的「两个时代不混算」 | **①**（owner huh · 2026-08-15）：D2a 按旧流程在实施记录 §3.15 收尾；并进 duet 会因两轮上限当场 escalate | ✅ 一致（结论同；理由在补查后由「统计不混算」换成「轮次上限冲突」）|
| 2026-08-15 | open-decision | byteme_mobile / 存量交接 | `docs/duet/review-D3b.md` OD-6 · endpoint audit 抽取债的归属 | 移出 D 账目，登记到 `tool/endpoint-audit/README`，到期点「下一次并行轨合并前」——它不该由某条轨的批次进度决定生死 | **移出 D，登 tool/endpoint-audit/README**（owner huh · 2026-08-15），到期点「下一次并行轨合并前」；补查发现 45 个调用点整类不可见，同形状第二次 | ✅ 一致 |
| 2026-08-15 | redline-risk | byteme_mobile / D3b plan review R1 | `docs/duet/review-D3b.md` §8 · 新 authority 证据推翻 OD-2/OD-3 的翻页与请求预算前提 | 保留完整回读 outcome：分叉 runs 游标修复列为 Agent 子 batch / D3 Done 前置；AC-18 保留有界预算与并发，但不写死与 steps 分页互斥的 `1+N` | **一次做对**（owner huh · 2026-08-15）：PR1 保留完整回读 outcome，分叉游标列 Agent 跨仓前置、不接受降级；PR2 AC-18 改写，空页探针判性能项不作前置。正文 plan E-6/E-7 | ✅ 一致 |
| 2026-08-15 | baton-confirm | byteme_mobile / D3b | Stage 0 传棒放行：交接仪式 + decision core + 门槛六项全过，请求冻结 plan 并传棒 Codex 做 plan review | 门槛已全过，建议放行并传棒 | **放行**（owner huh · 2026-08-15）；plan 冻结于 `710a898b`，棒已传 w3:p2 | ✅ 一致 |
| 2026-08-15 | round-cap | byteme_mobile / D3b plan review R2 | `docs/duet/plan-review-D3b.md` round 2/2 结束 PR2 仍开——缺口是作者只修了 AC 定义、漏了 E-3 Scope #4 与 E-5 Done #2 两处引用 | 补 errata 后请 owner 授权一轮窄范围 closure 重验（不建议 owner 直接判关闭：第一次撞上限就绕过去，这条上限以后不会再拦住任何东西）| **批准第三轮**（owner huh · 2026-08-15），范围锁定该缺口 ⇒ round 3 PASS，两条 P1 全关 | ✅ 一致 |
| 2026-08-15 | baton-confirm | byteme_mobile / D3b acceptance R1 | `docs/duet/review-D3b.md` §10 · VERDICT FINDINGS(P1x1, D3b-A1)，请求把棒传回 Codex 修 | 传棒（常规：verdict 已落盘、固定条件已写死，无产品选择、无争议）| **放行传棒**（owner huh · 2026-08-15）| ✅ 一致 |
| 2026-08-15 | baton-confirm | Agent / AGT-1 | Agent:docs/duet/plan-AGT-1.md · 跨仓首批 plan 送审 → review 两轮已闭（round1 四条 P1 全关，round2 PASS @901cf96b），请求冻结 | **冻结放行**（owner hao · 2026-08-15，plan `fb6bdcd8`）；rebase 追平亦经 owner 授权 | ✅ 一致 |
| 2026-08-15 | open-decision | Agent / AGT-1 | plan-AGT-1 AGT1-OD-1 · Agent/CLAUDE.md 要不要加 duet 接入指针 | **不自行处理**：该文件是 ale 的约定面，hao 代行的是 batch owner 角色、不含它；建议由 ale 决定 | ⬜ | ⬜ |
| 2026-08-15 | open-decision | Agent / AGT-1 | plan-AGT-1 AGT1-OD-3 · GET /conversations 要不要下发 fork 标识 | 本 batch 不做——分页修好后该需求即消失；若要给消费端识别分叉会话的能力，单开 | ⬜ | ⬜ |

| 2026-08-15 | baton-confirm | Agent / AGT-1 | Agent:docs/plans/2026-08-15-对话历史分页-开发计划.md §9 · AGT1-G1 开工硬闸第 1 步未过（三个在途未提交文件属他人），但 owner 已令传棒进实现阶段 | 传棒但在门铃里显式标明 G1 未过、不得写代码、不许代管或 stash 他人改动——冻结与开工是两道独立的闸 | ⬜ | ⬜ |
| 2026-08-15 | baton-confirm | byteme_mobile / D2a | `docs/devlogs/2026-08-12-D对话-迁移实施记录.md` §3.17 · D2a 实现/验证/交付工件三样齐备，请求 owner ack 标 Done | ack（无未关闭 finding、无未到期 watchlist、无缺失工件；reviewer 已在 ack HEAD 87207b08 亲跑全量门禁）| **ack**（owner hao · 2026-08-15）⇒ D2a Done，旧流程账目全部收尾 | ✅ 一致 |
| 2026-08-15 | redline-risk | Agent / AGT-1 | Agent:docs/plans/2026-08-15-对话历史分页-验收评审.md §2.1 · 验收开出 AGT1-A1：实现停在 /private/tmp/Agent-AGT1 游离 HEAD，无 ref 指向，且与 main 分叉（各 9/23 笔独有）| 判 P1 阻塞验收——代码全过但交付未发生，/private/tmp 会被系统清理；**两线怎么收敛不代判**，merge/cherry-pick/快进属 owner 裁决面 | ⬜ | ⬜ |
> 📌 **路径口径（2026-08-15，随「工件去品牌化」拍板）**：**后续行一律写迁移后的新路径**。
> 历史行按本文件「不修改历史行」的规则**原样保留**，但其中的落点已经变了，冷启动时按下表换算：
>
> | 历史行里的写法 | 现落点 |
> |---|---|
> | `Agent:docs/duet/plan-AGT-1.md` | `Agent:docs/plans/2026-08-15-对话历史分页-开发计划.md` |
> | `Agent:docs/duet/plan-review-AGT-1.md` | `Agent:docs/plans/2026-08-15-对话历史分页-计划评审.md` |
> | `byteme_mobile-D:docs/duet/*` · `docs/duet/outbox/*` | ⏳ **尚未迁移**——挂在 D3b 收口（`D3b-W6`），迁完再补进本表 |
>
> 迁移依据：duet `d5efef2`（工件按宿主仓类型惯例归档命名，禁以流程名建目录/文件；
> 移交单默认落点 `docs/handoffs/`）· Agent `9f9e76a6`（该仓存量已迁）。
