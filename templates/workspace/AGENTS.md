# Workspace 总目录

多仓工作区的根。此处启动的 session 是 **owner 轨**（跨仓 lookup、编排、复盘）。

**硬规则：写任何仓之前，必读该仓根目录的 AGENTS.md（无则 CLAUDE.md）。只读不受限。**

## 仓库地图（稳定拓扑 + 所有权）

| 仓 | 是什么 | Owner |
|---|---|---|
| `Agent/` | 后端主仓：`apps/api`（API/OpenAPI 契约 authority）+ `apps/web`（当前 Web）；`AI_AGENT_DEV_SPEC.md` 上游 | 后端 owner |
| `byteme_mobile/` | Flutter App 主仓，唯一开发主线 `main`。`byteme_mobile-*` 是席位 worktree，由 owner 运行时安排：现役清单看 `git worktree list` | 我 |
| `bytemeweb/` | legacy 老 Web：仅历史迁移、视觉来源与事故证据；不是当前 Web，不参与契约与实现决策 | 后端 owner |
| `byteme-platform-backend/` | 老平台后端，迁移退役方向 | 后端 owner |
| `duet/` | 个人 AI 工作方法仓：Goal 协议 + Herdr solo runtime + 可移植 skills；不是业务仓依赖 | 我 |
| `ai-byteme-frontend/` `byteme-taro/` `docs/` `tools/` | 其他前端 / 跨仓文档与工具 | — |

**任何 batch/session 只写自己所在的仓**；改别的仓 = 去那个仓内遵其 AGENTS.md 工作。
跨仓特性用父需求文档（authority 仓，通常 `Agent/docs/plans/` 需求分析，先查 `prds/`）
+ 每仓子 batch 组织，默认先后端后消费端。

## 路由表：找什么 → 去哪

| 找什么 | 真源 |
|---|---|
| 跨仓产品需求 / 体系设计 | `Agent/docs/prds/` |
| 向后端提需求 | `Agent/docs/plans/` 需求分析文档 |
| 迁移进度、跨轨阻塞 | `byteme_mobile/docs/migration/ROADMAP.md` |
| 端点契约（Web/Mobile 共用） | `Agent/apps/api` 生成的 OpenAPI（`Agent/docs/refer/api-operations/`：`openapi.json` 全量、`openapi-mobile.json` Mobile 消费面）。一份契约两端消费，消费端只能证明"正在怎样调用"，不得反推契约；Mobile 侧解读见 `byteme_mobile/docs/migration/` 集成边界 |
| 长期架构决策 | 各仓 `docs/adr/` |
| 轨内拍板与 open decisions | 该轨 plan 待拍板节 / duet review 的 OD 节 |
| 跨轨/跨仓消息（移交单、需求、契约变更） | 发送方仓 `docs/handoffs/`（真源） |
| 协作机制 | `duet/`：协议见 `protocol/`，Herdr runbook 见 `scripts/HERDR-RUNBOOK.md` |
