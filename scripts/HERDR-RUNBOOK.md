# Herdr 0.8.0 owner 操作手册

> 原则：simple and effective。正常路径只有一个 Herdr `default` session、长期 agent 席位、
> 每席位一个 workspace/工作树。跨-session 只用于迁移或事故恢复。

## 1. 只记四个对象

| 对象 | 含义 | 生命周期 |
|---|---|---|
| Herdr `default` session | 全部 agent 与 terminal 布局 | 长期存在；终端直接 `herdr` 进入 |
| workspace/pane/worktree | 一个席位当前工作的隔离目录和 PTY | Goal 切换时可更换 |
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

当前仍在旧 named session 中工作的 agent 不为统一显示而中断；在下一次自然 Goal/worktree 迁移时，
resume 到 `default`，确认上下文连续后再停旧 session。

## 3. 创建或打开工作树

新 worktree：

```bash
created=$(herdr worktree create \
  --cwd /absolute/repo/root --branch goal/example --base v2 \
  --path /absolute/worktree/path --label example --no-focus)
pane_id=$(printf '%s\n' "$created" | jq -r '.result.root_pane.pane_id')
```

已有 worktree：

```bash
opened=$(herdr worktree open \
  --cwd /absolute/repo/root --path /absolute/worktree/path \
  --label example --no-focus)
pane_id=$(printf '%s\n' "$opened" | jq -r '.result.root_pane.pane_id')
```

已有树必须用 `worktree open`，不能用 `workspace create --cwd` 冒充；必须从 JSON 读取 pane ID，
不能猜 `wN:p1`。

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

不要手写 `pane run` + `agent start`；这正是 2026-08-21 无颜色 regression 的入口。

## 5. Goal/worktree 迁移，不冷启动

固定顺序：

1. 让旧 agent 到安全停点，记录 agent 名、旧 pane/cwd、native session ID、当前 Goal/commit；
2. 用 `worktree create/open` 准备新 workspace，旧树先保留；
3. 对 Codex 清空未提交的 prompt 后发送 `ctrl+d`；
4. 同时确认旧 agent 名已释放、旧 pane 前台已回 shell；
5. 在新 pane 用 `herdr-agent-start.sh` 以同名、同 native session ID resume；
6. 核对新 cwd、native session ID 不变、instance ID 已变化、`color=ok`；
7. 用 `baton.sh send` 发 `RESUME-OK CHECK`，要求复述上一 Goal/commit/下一步，并读回 delivery ID；
8. 上下文连续后才清旧 workspace/worktree。

MCP 启动阶段可能让第一次 prompt API 返回但屏幕尚无 delivery ID。此时判定“未送达”，等启动完成，
确认消息没有消费后最多重投一次；API success 不是交棒成功。

只有 native session 无法恢复或 owner 明确要求时才 cold start，并在汇报中明确写 `COLD START`。

## 6. 门铃验收

`baton.sh send` 成功必须同时满足：目标 instance 在提交前后没变、runtime 状态允许投递、delivery ID
从 terminal 读回（OpenCode 使用已 qualification 的状态确认 fallback）。返回 `DELIVERY FAILED` 时棒仍在
发送方；先 `agent read` 判断消息是否消费，禁止口头宣布送达。

Codex working 时门铃用 `Tab` 排入下一 turn。普通消息不得写入 blocked approval UI；`unknown/dead`
也拒绝投递。`agent wait` 只用于 owner 点名诊断或一次迁移验证，必须带 timeout。

## 7. Worktree 收尾

```bash
herdr worktree remove --workspace <old-workspace-id>
```

它会关闭 workspace 并删除 checkout，但不删 branch。默认不用 `--force`。只有以下条件全满足才清：

- 同一 native session 已在新 cwd 恢复，instance 与上下文连续性已确认；
- 旧树 clean；
- 旧 commit 有 branch、已合主线或其他可恢复指针。

下一 Goal 未定时让 agent idle，并保留旧 clean worktree；不为目录整洁牺牲活 context。

## 8. 最短诊断表

| 症状 | 先查 | 动作 |
|---|---|---|
| agent not found | `herdr agent list` | 进程是否退出、名字是否变化；不要直接新建 context |
| 状态可疑 | `agent get` + `agent explain --verbose` | `done` 归 idle；证据不足归 unknown |
| prompt 没消费 | `agent read` recent-unwrapped/visible | 找 delivery ID；存在则禁止重发 |
| `name_taken` | `pane process-info` | 等旧进程退出和名字释放，不换名字 |
| cwd 错 | `agent get` 的 foreground cwd | 立即停写，resume 到正确 worktree |
| 无颜色 | 活 Codex 进程的 `NO_COLOR/CODEX_CI/TERM/COLORTERM` | 同 session 安全退出，再走唯一启动 helper |
| MCP startup interrupted | `agent read` | 等启动结束；不把 prompt API success 当送达 |

需要深查再看 `~/.config/herdr/herdr*.log`，只摘取已脱敏的信号。未经 owner 指令不升级 Herdr、
不 stop server、不 push、不删 branch、不使用 `--force`。

## 9. 上游真源

- [Herdr v0.8.0 release](https://github.com/herdrdev/herdr/releases/tag/v0.8.0)
- [agent automation](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/agent-automation.mdx)
- [CLI reference](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/cli-reference.mdx)
- [agent states](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/agents.mdx)
- [session restore](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/session-state.mdx)
- [bundled skill](https://github.com/herdrdev/herdr/blob/v0.8.0/skills/herdr/SKILL.md)
