# Runtime qualification · Codex × OpenCode（2026-08-17）

绑定：`role1=spec_owner/codex 0.147.0` · `role2=delivery_owner/opencode 1.18.15` ·
Herdr 0.8.0，workspace `pair-codex-opencode`。全程只读/空载，无产品开发。

| 检查 | 结果 | 证据/处置 |
|---|---|---|
| Herdr integration | ✅ | codex v7 · opencode v9 current；两端均有 native session id |
| 命名启动 | ✅ | `herdr agent start role1/role2` 均 interactive ready |
| 角色冷启动 | ✅ | 两端读各自角色卡并报 READY，无 blocker |
| OpenCode 角色隔离 | ✅ | pane 注入 `OPENCODE_DISABLE_CLAUDE_CODE=1` 后不再隐式加载 `roles/claude.md` |
| idle 双向门铃 | ✅ | 两向均附 delivery id，命令成功且目标 readback 命中 |
| OpenCode working 直接 prompt | ❌ | 未中断工具，但并入当前 turn，属于温和 steering，不是下一 turn FIFO |
| OpenCode settle adapter | ✅ | primary `sleep 6` 完整结束并输出后，门铃作为独立下一 turn 消费一次 |
| blocked 识别 | ✅ | 外部 `/etc` 只读请求被识别为 blocked；Esc 拒绝后回 done |
| transcript 复盘 | ✅ | Claude/Codex JSONL 统一；OpenCode 从本地 DB 经 `opencode-turns.py` 归一 |
| session restart/restore | ✅ | 两端退出后用原 session id 恢复，均准确回忆 closure delivery `d1786930948-7043` |
| FINDINGS→closure + escalation | ✅ | synthetic 一轮闭环 PASS；两跳均读回 delivery id，全程无文件改动 |
| 职责→实例映射 | ✅ | role2 首次误投 `spec_owner` 后从 agent list 自纠为 `role1`；协议已显式禁止混用 |
| capability fallback | ✅ | notification 返回 `shown:false/no_foreground_client`，role2 改由 peer 门铃代达；helper 已改为显式失败 |

演练期间还发现并修复了 `baton.sh` agent-list 参数引号回归；失败未被误报为送达。

结论：该 pair 的空载 qualification 已完成，达到**待 owner gate 后进入产品 batch**的条件。
当前保持 `done/done`，未开始任何具体开发。

## 多 session federation 补验（2026-08-17）

- 拓扑：`btrack`（`b-spec` Codex + `b-delivery` OpenCode）与 `etrack`（`e-spec` Codex +
  `e-delivery` OpenCode）独立 session；两个完整 TUI 不共享 active workspace；
- `baton.sh peers` 从 running sessions 实时聚合四个 agent，无缓存、heartbeat 或 watchdog；
- Codex B→E→B：`d1786949589-36091` / `d1786949602-36404`，两端均看见四 agent 且
  delivery-id 读回，PASS；
- OpenCode B→E→B：`d1786949649-37263` / `d1786949679-37939`（重试
  `d1786949864-41425`），目标数据库确认三条均消费，PASS；Herdr 对 OpenCode alternate-screen
  的 `recent-unwrapped` / `visible` 不可靠，adapter 改用 prompt API 成功 + 状态转移；
- 权限：Codex `workspace-full` 精确 allow Herdr Unix sockets；OpenCode 只 allow 外部
  `~/Workspace/duet/scripts/**` 且 edit deny。新增 session 必须先补 Codex socket allowlist。

## Owner 汇报补验（2026-08-17）

`protocol/owner-report.md` 在原空载 qualification 后新增，不推翻既有门铃/恢复结论。
Codex×OpenCode 现役 pair 在下一次自然 Milestone / Decision 汇报时补验；不为补验中断或重启 agent。
