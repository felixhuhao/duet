# 机器生命周期 runbook · 新开发机 bootstrap 与旧机退役

方法与顺序，不含任何机器私有值（token、账号、审批记录、绝对用户路径）。owner 自己的完整
ByteMe Mobile 工作站安装步骤见 [三端开发机 bootstrap](byteme-mobile-three-platform-bootstrap.md)；
项目的实时工具链、验证、Release 与 CI authority 仍归 `byteme_mobile/docs/dev/本地开发测试说明.md`
等项目仓文档，本文件不重复、不覆盖。

## 新开发机 bootstrap

1. 基础：git、herdr（官方 release 二进制或包管理器任一）。tmux 是 legacy，不需要。
2. 建 workspace 根目录。**根目录不是 git 仓**：把 duet `templates/workspace/` 的
   `AGENTS.md` / `CLAUDE.md` 拷到根目录——它们是「写仓前必读 + 路由表」的唯一入口；
   规则变更先改 duet，再同步拷贝。
3. 克隆各业务仓；写任何仓之前先读该仓根目录 AGENTS.md（workspace 硬规则，只读不受限）。
4. clone duet，安装需要的 skills。
5. owner 建 canonical 主树与席位 worktree（拓扑 owner 管理，agent 不建树）；跑
   `scripts/worktree-audit.py` 确认 clean。
6. `scripts/herdr-agent-start.sh` 起各席位 agent；核对 Context Receipt：
   owner/herdr/pane/native_session + cwd/branch/base。
7. 按个人 bootstrap 完成软件安装，再回各仓执行该仓实时工具链自检；全绿后席位进入 idle 待命。

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
