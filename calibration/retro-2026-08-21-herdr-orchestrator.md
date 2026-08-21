# 事故复盘 · Mobile solo Herdr 编排学习成本（2026-08-21）

> 范围：本轮 owner 轨接管 Mobile solo agents、Goal worktree迁移和 Integration续派。
> 结论：错误主体是 orchestrator 未先读上游 Herdr 操作真源，把运行时对象混为一谈并用生产 session
> 临场试错；不是 agent、Herdr 或 owner 的责任。

## 事故与成本

| 事件 | 错误 | 可核实成本/影响 | 永久处置 |
|---|---|---|---|
| 旧 `mobile-solo` 提前退出 | 把 Goal/worktree结束误当 agent生命周期结束，未先迁移同一 session | 丢失一个仍可续用的活 context；旧 transcript仍在，但不能再以原进程连续工作 | `runtime.md`、Mobile AGENTS 已固化“agent长命、worktree短命”和迁移顺序 |
| 冷启动代价被低估 | 先按 agent-per-Goal思路调度，后补算 overhead | CASH strict boot约 1m40、8.7万有效 token；同-session换树实测约1–4min、3.7%–7.8%有效 token | Goal放大为 outcome + increments；默认 resume，冷启动必须显式说明 |
| default session空 workspace | 当时同时维护 default 与多个 named session，raw mutation 路由错误 | 在 default创建一个空 `wD`，随即关闭；无 agent、无仓库写入 | 正常拓扑收敛为唯一 `default` session；旧 named session只在自然迁移时兼容 |
| 现有 worktree用 `workspace create` 打开 | 未区分普通 workspace与linked-worktree workspace | 新 `w6` 可工作但缺 Herdr worktree provenance/父子分组；本 Goal运行中不为修显示再次迁移 | runbook规定已有树用 `worktree open`，新树用 `worktree create` |
| resume启动竞态 | `ctrl+d` 后立即同名 `agent start`，未等旧名字释放 | 一次 `agent_name_taken`，多一次恢复命令；没有第二agent、没有新context | 退出后同时核旧 pane前台shell + agent name消失，再start |
| 首次 Integration投递假成功风险 | resume后用不等待状态变化的 `agent prompt`；API返回但delivery未读回 | `d1787283733-96605` 失败，多一轮诊断和重投；`d1787283773-97761` 成功 | Codex idle prompt改为先观察生命周期变化，再做instance与delivery双验证 |
| resume 后终端无颜色 | 手工执行 `agent start ... resume`，漏掉 pair setup 中的 pane 环境准备 | `followup-solo` 活进程继承 `NO_COLOR=1`、`CODEX_CI=1`；用户可见颜色回归 | 新建/resume统一走 `herdr-agent-start.sh`；活 Codex 进程禁色变量断言进入自动测试 |
| MCP startup 后首次门铃未读回 | resume ready早于内置 MCP 完成启动，prompt API进入状态变化但屏幕无delivery | `d1787285903-51712` 明确失败；启动完成后 `d1787285932-52534` 单次重投成功 | 保持“无读回=未送达”；resume check在MCP ready后投递，最多确认后重投一次 |
| 旧 worktree清理绕过Herdr原语 | 先 `workspace close`，再raw `git worktree remove` | checkout成功删除、branch `cbff38b1` 保留，无数据损失；但绕过Herdr原子remove路径 | 后续统一 `herdr worktree remove --workspace`，默认不用force |
| 校验脚本覆盖zsh特殊变量 | GitHub链接循环误用变量名 `path`，覆盖zsh的命令搜索数组 | 一次只读校验报 `gh: command not found`，无运行态或文件影响 | shell变量使用任务专用名；不复用 `path`/`HOME` 等系统语义名 |

## 量化边界

- 本轮直接出现：1个错误session空workspace、1次name_taken、2次delivery readback失败、1次颜色回归；均未造成仓库数据
  丢失、重复agent或重复任务消费。
- 最大不可逆损失是旧 `mobile-solo` 活进程连续性。其 transcript累计约181万有效 token；该数字不是
  “需要全部重做”的成本，只表示被放弃的上下文规模，不能伪装成精确损失额。
- 正确 resume 对照：`followup-solo` 原 native session `01a021e6-…` 在新pane启动约3秒，约59秒完成
  cwd/基线/上下文复验；context连续。
- 颜色修复对照：旧进程环境含 `NO_COLOR=1/CODEX_CI=1`；同 native session resume 后仅保留
  `TERM=xterm-256color/COLORTERM=truecolor`，visible snapshot 实测 247 个 SGR 序列。
- 当前 runtime drift：`integration-p0/w6` 是普通workspace方式打开的既有worktree，缺worktree分组元数据。
  不打断正在工作的agent修复；下次自然Goal迁移时按runbook进入正确worktree workspace。

## 根因

1. 开工只读了 duet wrapper说明，没有完整阅读 Herdr `agent-automation`、CLI reference、session-state和
   内置 skill；
2. 把“Herdr能检测进程”误当成“已掌握agent identity、session restore和worktree topology”；
3. raw CLI 与本仓wrapper混用，没有先固定“何时必须使用哪一层”；
4. 对成功条件定义过低：命令exit 0不等于agent已退出、prompt API success不等于消息已消费。
5. 默认拓扑和操作手册提供太多 session/启动分支，正确性依赖 orchestrator 临场记住隐含环境步骤。

## 修正与验收

- 新增 `scripts/HERDR-RUNBOOK.md`，以本机0.8.0和上游tag为双真源；
- `baton.sh` 的idle Codex投递复用状态变化确认，再做delivery-id读回；
- 新增统一 `herdr-agent-start.sh`，启动与resume共用颜色环境准备和活进程断言；
- 日常拓扑收敛为单一 `default` session、长期 agent 席位；跨-session只保留为自然迁移/事故兼容；
- `scripts/README.md`把runbook设为raw CLI编排前置；
- 静态验收：`bash -n scripts/baton.sh`、federation unittest、fake-Herdr Codex idle delivery测试、
  文档链接与命令help对账；
- 动态验收不新开测试agent、不打断现役agent；Codex新投递路径在下一次自然门铃中事件驱动补验；
- `0.8.2`包含start readiness与blocked prompt修复，但本轮不擅自升级；升级另走qualification。

## Owner注意力结论

以后汇报必须明确写 `COLD START` 或 `RESUME`、native session ID是否保持、instance是否变化、worktree
是否由Herdr provenance管理。没有这四项，不得宣称“agent已迁移”或“handoff已完成”。
