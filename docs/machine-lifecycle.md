# 机器生命周期 runbook · 新开发机 bootstrap 与旧机退役

方法与顺序，不含任何机器私有值（token、账号、审批记录、绝对路径）。项目工具链细节归各仓
（例：byteme_mobile 的 `docs/dev/新MacBook-Air三端环境安装指南.md` 与
`docs/dev/本地开发测试说明.md`），本文件不重复。

## 新开发机 bootstrap

1. 基础：Homebrew、git、herdr。tmux 是 legacy，不需要。
2. 建 workspace 根目录。**根目录不是 git 仓**：`AGENTS.md` / `CLAUDE.md` 是两份手工文件，
   必须单独从旧机迁移或按最新内容重建——它们是「写仓前必读 + 路由表」的唯一入口。
3. 克隆各业务仓；写任何仓之前先读该仓根目录 AGENTS.md（workspace 硬规则，只读不受限）。
4. clone duet，安装需要的 skills。
5. owner 建 canonical 主树与席位 worktree（拓扑 owner 管理，agent 不建树）；跑
   `scripts/worktree-audit.py` 确认 clean。
6. `scripts/herdr-agent-start.sh` 起各席位 agent；核对 Context Receipt：
   owner/herdr/pane/native_session + cwd/branch/base。
7. 各仓工具链自检按该仓文档执行（如上例），全绿后席位进入 idle 待命。

## 旧开发机退役（转 CI appliance）

1. 逐仓确认无未 push 提交、无 stash、无有价值的 untracked；duet 与全部业务仓同步远端。
2. 席位按 [HERDR-RUNBOOK](../scripts/HERDR-RUNBOOK.md)「安全退出与恢复」退出；不复用的
   native session 记录后放弃。
3. `scripts/worktree-audit.py` 全仓过一遍：clean 或留明确恢复指针；席位表快照落目标项目的
   Goal/启动记录，不落 duet。
4. 秘密清理：`.env.local`、keychain、浏览器 session 按各仓规则移交或销毁，走安全渠道，
   不进任何仓；曾暴露过的长期凭据退役前轮换。
5. agent 记忆：跨项目方法先晋升进 [playbooks](playbooks.md)；项目级记忆不迁移——新机项目
   路径不同，自动记忆不跟随。
6. CI 化改造属于项目仓（如 byteme_mobile 的 CI Goal），不在本文件。

## 自检

- 新机：`herdr agent list` 席位齐全；每个远端做一次只读 fetch 验证凭据。
- 退役：各仓 `git status` 干净、无领先远端的提交；秘密清单逐项打勾（移交/销毁/轮换）。
