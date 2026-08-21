# Herdr 0.8.0 owner 操作手册

> 原则：simple and effective。正常路径只有一个 Herdr `default` session、长期 agent 席位、
> 每席位一个 workspace/工作树。跨-session 只用于迁移或事故恢复。

## 1. 只记四个对象

| 对象 | 含义 | 生命周期 |
|---|---|---|
| Herdr `default` session | 全部 agent 与 terminal 布局 | 长期存在；终端直接 `herdr` 进入 |
| workspace/pane/worktree | 一个席位固定的隔离目录和 PTY | 长期存在；Goal 只换 branch |
| agent name | 稳定席位名，如 `dev1/dev2` | 跨 Goal 复用；不是任务名 |
| native session ID | Codex/Claude/OpenCode conversation identity | resume 连续性的真源 |

`instance_id` 标识这一次前台进程，重启后必须变化；native session ID 在 resume 后必须保持。
Herdr 的 `done` 与 `idle` 都表示 agent 可接收下一 turn；对外统一为 `idle`。

## 2. 日常只用这些命令

```bash
herdr
herdr agent list
scripts/baton.sh peers
scripts/baton.sh send <agent-name> <from-role> "事件 · 真源路径 · verdict/下一动作"
```

- `herdr` 直接 attach `default` session，统一查看所有 workspace；
- `baton.sh` 默认同样只操作 `default`；临时迁移旧 named session 时才显式设置
  `HERDR_SESSION=<old-name>`；
- 不 heartbeat、不轮询；只有 owner/peer 消息或真实 blocked 事件唤醒 agent；
- agent 是 `dev1/dev2` 一类长期席位，Goal 只是当前工作，不按 Goal 创建/删除 agent。

worktree 创建、移动、删除只由 owner 安排；agent、reviewer、orchestrator 禁止临时建树。事故恢复也只能
打开 owner 已准备的树，不能以“恢复”为由创建 checkout。

## 3. 只打开 owner 已准备的工作树

`herdr worktree create` 与 `git worktree add` 不进入日常命令面。owner 准备好长期树后，只用 open：

```bash
opened=$(herdr worktree open \
  --cwd /absolute/repo/root --path /absolute/worktree/path \
  --label wt1 --no-focus)
pane_id=$(printf '%s\n' "$opened" | jq -r '.result.root_pane.pane_id')
```

必须确认路径、branch 与 owner 分配一致；用 `worktree open`，不能用 `workspace create --cwd` 冒充；
从 JSON 读取 pane ID，不能猜 `wN:p1`。

## 4. 启动和 resume 只走一个入口

新 Codex：

```bash
scripts/herdr-agent-start.sh dev1 codex "$pane_id" --disable network_proxy
```

resume 同一 Codex conversation：

```bash
scripts/herdr-agent-start.sh dev1 codex "$pane_id" \
  resume <native-session-id> --disable network_proxy
```

OpenCode resume：

```bash
scripts/herdr-agent-start.sh dev2 opencode "$pane_id" \
  --session <native-session-id> --auto
```

helper 在启动前清除 `NO_COLOR/CODEX_CI` 等宿主变量，固定
`TERM=xterm-256color`、`COLORTERM=truecolor`，并检查活 Codex 进程确实继承。出现
`color preflight` 失败时不得继续交棒；先修环境并 resume 同一 native session。
helper 同时从 pane 实时读取 cwd，自动给 Codex 加 `--cd`；pane cwd 不存在或显式参数与 pane 不一致时
拒绝启动。否则 Codex resume 会复用旧 session cwd，使 SessionStart hook 和 MCP 在旧树删除后一起失败。

不要手写 `pane run` + `agent start`；这正是 2026-08-21 无颜色 regression 的入口。

## 5. Goal 切换不迁 cwd

固定顺序：

1. agent 在固定 `wt1/wt2` 完成当前 Goal、提交并回报 branch/HEAD；
2. owner/merge-owner 在 canonical 主树把 branch 合入 `v2`；
3. owner 指定下一 Goal branch 与 BASE，agent 在同一席位树切 branch；
4. 核对 cwd、workspace、agent 名与 native session 都未变化，再走 Pickup Context/Receipt；
5. 没有下一 Goal 时保持原 branch idle，不退出、不清 worktree。

只有进程退出、workspace 丢失或 owner 指定拓扑变更才 resume。此时先 `worktree open` 固定树，再按第 4 节
恢复原 native session；禁止创建替代树。恢复后核 cwd/session/instance/color/MCP，并发一次回验门铃。

MCP 启动阶段可能让第一次 prompt API 返回但屏幕尚无 delivery ID。此时判定“未送达”，等启动完成，
确认消息没有消费后最多重投一次；API success 不是交棒成功。

只有 native session 无法恢复或 owner 明确要求时才 cold start，并在汇报中明确写 `COLD START`。

### Goal pickup：迁移成功不等于上下文已装载

新 Goal 的 worktree/agent ready 后，用 `baton.sh send` 投递一条指针，不在 prompt 里重新口述合同：

```text
[GOAL PICKUP] <GOAL-ID> · role=<role> · goal=<repo@sha:path> · target=<cwd/branch>
先只读完成 Launch Capsule 并落盘 Context Receipt；ACCEPTED 前禁止生产写。
```

接收者必须核对 Goal commit、逐项必读 authority 与 target cwd，再在本仓 Goal child 写 Context Receipt。
Receipt commit + 门铃读回才表示 pickup 完成；Herdr delivery success、agent `working` 或 worktree 已创建都
只证明消息/进程存在。Receipt 缺文件、SHA 漂移或结论冲突时标 `REJECTED/NEEDS_REFRESH` 并停在只读边界，
不得重新 discovery 或自行补产品决定。复用旧 native session 只省冷启动，不豁免新 Goal receipt。

## 6. 门铃验收

`baton.sh send` 成功必须同时满足：目标 instance 在提交前后没变、runtime 状态允许投递、delivery ID
从 terminal 读回（OpenCode 使用已 qualification 的状态确认 fallback）。返回 `DELIVERY FAILED` 时棒仍在
发送方；先 `agent read` 判断消息是否消费，禁止口头宣布送达。

Codex working 时门铃用 `Tab` 排入下一 turn。普通消息不得写入 blocked approval UI；`unknown/dead`
也拒绝投递。`agent wait` 只用于 owner 点名诊断或一次迁移验证，必须带 timeout。

## 7. Worktree 拓扑审计

```bash
scripts/worktree-audit.py /absolute/repo/root
```

最终拓扑只允许 canonical 主树与 owner 声明的长期席位树。`ACTIVE` 表示 agent 正绑定；维护窗口中固定
席位可暂时 unowned，resume 后必须回到 `ACTIVE`。除此以外的 `CLEAN_UNOWNED/DIRTY_UNOWNED` 都是 legacy，
只报告 branch、HEAD、dirty 文件与可恢复指针；不得自行处置。audit 是事件后的单次验收，不是 heartbeat。

只有 owner 明确给出目标后，才可在维护窗口执行移动/删除；不删 branch、不使用 `--force`：

```bash
git -C <repo-root> worktree move <old-path> <owner-approved-path>
git -C <repo-root> worktree remove <owner-approved-legacy-path>
```

执行前必须确认目标树 clean 或已保存、commit 有 branch/其他恢复指针、无 agent 进程占用；执行后重新
open 固定树并 resume 原 session。普通 Goal 收尾只处理 branch，永不触发这里的 worktree 命令。

## 8. 最短诊断表

| 症状 | 先查 | 动作 |
|---|---|---|
| agent not found | `herdr agent list` | 进程是否退出、名字是否变化；不要直接新建 context |
| 状态可疑 | `agent get` + `agent explain --verbose` | `done` 归 idle；证据不足归 unknown |
| prompt 没消费 | `agent read` recent-unwrapped/visible | 找 delivery ID；存在则禁止重发 |
| `name_taken` | `pane process-info` | 等旧进程退出和名字释放，不换名字 |
| cwd 错 | `agent get` 的 foreground cwd | 立即停写，resume 到正确 worktree |
| 无颜色 | 活 Codex 进程的 `NO_COLOR/CODEX_CI/TERM/COLORTERM` | 同 session 安全退出，再走唯一启动 helper |
| MCP startup interrupted | `agent read` | 若是等待则等启动；若 hook/MCP 同报 `No such file`，核 Codex `--cd` 与 pane cwd |

需要深查再看 `~/.config/herdr/herdr*.log`，只摘取已脱敏的信号。未经 owner 指令不升级 Herdr、
不 stop server、不 push、不删 branch、不使用 `--force`。

## 9. 上游真源

- [Herdr v0.8.0 release](https://github.com/herdrdev/herdr/releases/tag/v0.8.0)
- [agent automation](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/agent-automation.mdx)
- [CLI reference](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/cli-reference.mdx)
- [agent states](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/agents.mdx)
- [session restore](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/session-state.mdx)
- [bundled skill](https://github.com/herdrdev/herdr/blob/v0.8.0/skills/herdr/SKILL.md)
