# templates

**这里是必备字段契约 + 新项目起步默认，不取代项目现有格式。**（2026-08-15 拍板）

新工作默认采用 `goal.md` + `outcome-roadmap.md` + `validation-ledger.md` 三份真源；旧项目的
plan/devlog/review 工件保留历史，不批量重写。已有格式只要能一一映射下列字段即可：

- **Goal**：稳定 Contract + 可更新 Execution Notes/Resume Capsule + Completion Package + 条件式
  Retrospective；具体字段见 `goal.md`；
- **Outcome Roadmap**：用户结果、Priority、依赖、状态与已授权 Ready Queue；
- **Validation Ledger**：I0/I1/I2、DEV/Integration/Device、frozen HEAD 与 defect links；

以下为旧 plan/batch 兼容字段，未映射到 Goal 的旧未完成项不得继续执行：

`plan-review.md`、`review.md`、`devlog.md` 仅为旧 batch 兼容入口；Goal v1 的 readiness、review、
执行记录和完成包全部写在同一 Goal 文件，避免再造第四类状态文档。

- **plan**：outcome / scope 与 out-of-scope / redlines+authority 来源 / 可观察 AC /
  open decisions / Errata 节（追加式）/ 冻结状态与 BASE；
  活跃 Goal 另须声明 goal_owner、tmux target、runtime kind、native session ID 与固定 cwd；独立 review
  例外再声明 reviewer 与角色卡；
  跨仓 batch（仅限同 owner 多仓的声明式例外）另须声明：仓清单 + 各仓 writable scope +
  各仓 BASE；跨仓特性的子 batch 须链接父需求文档（authority 仓）；
- **devlog（或等价实施记录）**：本轮自含摘要（owner-report 五项，链接可选）/ 增量 commits 范围 /
  证据块（cmd·scope·result·noise）/ 已知限制 / 被暂停 slice；
- **plan review**：用 `plan-review.md`；四项 coverage / plan HEAD + code BASE + authority
  snapshot / not-verified / finding 的精确依据、影响与固定关闭条件 / VERDICT；
- **code review**：用 `review.md`；round 计数 / BASE 与 reviewed HEAD / blockers（绑定依据）/ **OD 节
  （OD 完整语境与争议立场的真源）** / watchlist+到期点 / VERDICT 块（见
  protocol/verdict.md）/ 本轮自含摘要（owner-report 五项，链接可选）。工作仓文档须对没有 duet 访问权的读者自含。

- **message（跨界消息）**：from+commit / to / type / 到期点 / 事实（自含）/ 请求 /
  回执。落点与路由见 protocol/inbox.md。

字段缺失 = reviewer 可拒收，不是 finding。
