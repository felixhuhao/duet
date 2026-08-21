# Herdr 0.8.0 owner 轨操作手册

> 适用：本机 `herdr 0.8.0`、duet owner/runtime orchestrator、Codex/Claude Code/OpenCode。
> Herdr 上游真源固定到 `v0.8.0@346411fa`；安装二进制的 `herdr --skill` 与该 tag 一致。
> 本页只写操作顺序；角色、传棒语义和五态仍以 `protocol/runtime.md`、`protocol/baton.md` 为准。

## 1. 先记住四个对象

| 对象 | 是什么 | 生命周期 |
|---|---|---|
| session | 独立 Herdr server namespace、socket 和持久布局 | 可跨项目长期存在 |
| workspace/tab/pane | terminal 布局；pane 是真实 PTY | detach 后进程继续；server stop 后进程消失 |
| agent name | 当前 pane 中活 agent 进程的路由别名 | 进程退出即清除；不是 conversation identity |
| native agent session ID | Codex/Claude/OpenCode 自己的 conversation identity | `resume` 的连续性真源 |

`instance_id` 是 duet 从 Herdr session + agent name + terminal ID + 前台进程组计算的本次进程
incarnation。resume 后 native session ID 应不变，`instance_id` 必须变化。

Herdr 原始状态中，`done` 是“后台完成、尚未被看过”，`idle` 是同一可输入状态已被看过；duet 对外都
归一为 `idle`。`unknown` 只表示无法可信分类，不表示完成或死亡。

## 2. owner 轨与上游 skill 的边界

上游 skill 默认要求 `HERDR_ENV=1`，防止普通 agent 从 Herdr 外部控制用户当前焦点。本项目 owner 轨
从 VS Code/Codex extension 运行，属于 owner 明确授权的外部 orchestrator 例外，必须额外满足：

1. 所有 mutation 都显式写 `herdr --session <name> ...`，不依赖 default/focus；
2. 跨 session 查找和通信优先用 `herdr-federation.py` / `baton.sh`；
3. 不运行裸 `herdr`，它会启动/attach TUI；
4. 不关闭自己未创建或 owner 未明确要求清理的 workspace/pane/session；
5. 不用生产 session 试命令；不确定先查 `herdr <group> --help` 和本页。

## 3. 每次操作的固定 preflight

```bash
target_session=mobile-solo-pilot

herdr --version
herdr --session "$target_session" status
herdr --session "$target_session" integration status
scripts/baton.sh peers
```

- 本机当前 client/server 都必须是 `0.8.0`、protocol `19`、compatible `yes`；
- 当前 integration：Codex v7、Claude v7、OpenCode v9；native session ID 来自 integration；
- `baton.sh peers` 聚合所有 running sessions，输出 name/session/workspace/kind/status/instance/pane/cwd；
- 对 agent 投递前后都重新 resolve + verify instance，禁止缓存 pane、instance 或状态。

只查看一个 session 时仍把全局参数放在 subcommand 前，形成唯一写法：

```bash
herdr --session "$target_session" workspace list
herdr --session "$target_session" agent list
```

## 4. 通信：只走 baton，raw prompt 只用于诊断

```bash
scripts/baton.sh send <全局唯一agent名> <from-role> \
  "事件 · 真源路径 · 轮次/verdict/下一动作"
```

`baton.sh send` 的成功条件是：

1. 全局 resolve 唯一 agent；
2. 取得非空 `instance_id`，投递前验证未变化；
3. 按 runtime/status 使用已 qualification 的传输面；
4. 投递后再次验证同一 instance；
5. Codex/Claude 从 terminal 读回 delivery ID；OpenCode 使用 prompt 状态确认 fallback。

状态路由：

| runtime/status | 本机做法 |
|---|---|
| Codex idle/done | `agent prompt --wait` 先观察生命周期变化，再读回 delivery ID |
| Codex working | `pane send-text` + `Tab`，进入 Codex 下一 turn 队列 |
| OpenCode idle/done | prompt API + 状态变化确认；alternate-screen 不强求读回 |
| OpenCode working | 先 event-driven settle，再作为独立 turn prompt |
| Claude working/idle | `agent prompt`；仍需 delivery ID 读回 |
| blocked | 普通门铃 deferred，不往批准/问题 UI 写字 |
| unknown/dead | 拒绝投递，先诊断或恢复 |

`DELIVERY FAILED` 表示职责棒仍在发送方。不得口头说“已发送”；先 `agent read` / `agent explain` 判断，
确认消息没有消费后才能重投。不要用 `agent prompt --wait` 等整个长任务结束；送达确认只等首次状态变化。

`agent wait` 不是监听循环。只在 owner 点名排查 blocked 或一次性迁移验证时使用，并始终带 timeout。

## 5. 建立新的 agent

### 5.1 先创建正确的 terminal topology

已有普通目录、不是 Git worktree：

```bash
created=$(herdr --session "$target_session" workspace create \
  --cwd /absolute/project/path --label task-label --no-focus)
pane_id=$(printf '%s\n' "$created" | jq -r '.result.root_pane.pane_id')
```

创建新 Git worktree并打开为 workspace：

```bash
created=$(herdr --session "$target_session" worktree create \
  --cwd /absolute/repo/root \
  --branch goal/example --base v2 \
  --path /absolute/worktree/path --label example --no-focus)
pane_id=$(printf '%s\n' "$created" | jq -r '.result.root_pane.pane_id')
```

打开已经存在的 Git worktree：

```bash
opened=$(herdr --session "$target_session" worktree open \
  --cwd /absolute/repo/root \
  --path /absolute/worktree/path --label example --no-focus)
pane_id=$(printf '%s\n' "$opened" | jq -r '.result.root_pane.pane_id')
```

已有 worktree 必须用 `worktree open`，不能用 `workspace create --cwd` 代替；后者能启动 shell，但会丢
Herdr 的 linked-worktree provenance、父子分组和原子 remove 路径。

创建命令会同时创建 workspace、首个 tab 和 root pane。必须从 JSON 读取 ID，不能猜 `wN:p1`。

### 5.2 准备 pane 环境并启动

```bash
herdr --session "$target_session" pane run "$pane_id" \
  "unset NO_COLOR CODEX_CI CODEX_INTERNAL_ORIGINATOR_OVERRIDE CODEX_PERMISSION_PROFILE CODEX_THREAD_ID; export TERM=xterm-256color COLORTERM=truecolor; printf '__DUET_ENV_READY__\\n'"
herdr --session "$target_session" pane wait-output "$pane_id" \
  --match "__DUET_ENV_READY__" --timeout 5000

herdr --session "$target_session" agent start mobile-solo \
  --kind codex --pane "$pane_id" --timeout 120000 -- --disable network_proxy
```

OpenCode 额外传 `-- --auto`。批量建职责 pair 时优先调用：

```bash
HERDR_SESSION="$target_session" scripts/pair-setup.sh <spec-dir> <delivery-dir> <label> codex opencode
```

成功启动后立即记录：agent name、Herdr session、workspace/pane、cwd、kind、native session ID、
instance ID。再用 `baton.sh send` 投初始任务；不要绕过 readback。

## 6. Resume：换 worktree，不换 conversation

先区分四件事：

| 场景 | 正确动作 |
|---|---|
| detach/reattach client | 直接 attach；原进程一直活着，不 resume |
| Herdr server restart | 官方 integration 可自动 native resume；任意普通进程不会保留 |
| Goal 更换 worktree | 手动退出旧前台 agent，在新 pane 用同一 native session ID resume |
| session 无法恢复/owner 明确要求 | 才冷启动新 conversation |

Codex Goal 迁移固定顺序：

1. 旧 agent 到安全停点且为 idle；取实时 route、旧 pane、native session ID；
2. 用 `worktree create/open` 准备新 workspace，解析新 root pane；
3. 准备新 pane 环境；旧 worktree/workspace仍保留；
4. `agent send-keys <name> ctrl+d` 正常退出 Codex；
5. 退出是异步的：必须确认旧 pane 前台已是 shell，且旧 agent name 已释放；未确认不得 start；
6. 在新 pane 启动同名 agent，并把 resume 参数放到 `--` 后；
7. 核对新 cwd、native session ID 不变、instance ID 已变化；
8. 发送 `RESUME-OK CHECK`，要求复述上一 delivery/commit/Goal 和新 cwd；读回 delivery ID；
9. 只有上下文连续性确认后，才清旧 workspace/worktree。

Codex 示例：

```bash
herdr --session "$target_session" agent start followup-solo \
  --kind codex --pane "$new_pane" --timeout 120000 -- \
  resume <codex-session-id> --disable network_proxy
```

官方 native resume 参数：

| runtime | 参数 |
|---|---|
| Codex | `codex resume <id>` |
| Claude Code | `claude --resume <id>` |
| OpenCode | `opencode --session <id>` |
| Cursor Agent | `cursor-agent --resume <id>` |
| Kimi | `kimi --session <id>` |
| Hermes | `hermes --resume <id>` |

完整 runtime 表见上游 session-state 文档。模型切换而 native session ID 不变，不算冷启动。

## 7. Worktree 清理

优先使用 Herdr 的原子路径：

```bash
herdr --session "$target_session" worktree remove --workspace <old-workspace-id>
```

它关闭 workspace并执行 `git worktree remove`，但**不会删除 branch**。默认不加 `--force`；Git 因 dirty
拒绝时立即停止并保留现场。普通 `workspace close` 只关闭 Herdr 状态，不删除 checkout。

清理前必须同时满足：

- 新 worktree已就绪；
- 同一 native session已在新 cwd恢复；
- 新 instance和上下文连续性已确认；
- 旧 worktree clean；
- 旧 commit有 branch/新 branch/已合主线中的可恢复指针。

下一 Goal 未确定时保留 idle agent和旧 clean worktree。agent生命周期不跟随 worktree生命周期。

## 8. 诊断顺序

| 症状 | 先查 | 判定/动作 |
|---|---|---|
| agent not found | `baton.sh peers` | 名字是否已随进程退出清除；跨 session 是否重名 |
| 状态可疑 | `agent get` + `agent explain --verbose` | Codex/Claude状态来自 screen manifest；integration主要给 session ID |
| prompt无消费 | `agent read` recent-unwrapped，再看 visible | delivery ID不存在则未交棒；存在则禁止重发 |
| start name_taken | 旧进程尚未退出 | 查旧 pane process-info；不要换名字制造第二 context |
| start timeout/blocked | `agent read` + `agent explain` | 处理启动 UI；不要盲重启 |
| cwd错误 | `agent get` 的 `foreground_cwd` | 停止写仓；恢复到正确 pane/worktree |
| instance变化 | federation resolve/verify | 视为新进程；重新做 RESUME-OK，不沿用旧投递结论 |
| server/client版本不一 | `herdr --session <name> status` | 先处理兼容；不要 server stop，除非 owner明确接受 pane进程退出 |

日志：`~/.config/herdr/herdr.log`、`herdr-client.log`、`herdr-server.log`。需要详细诊断时临时使用
`HERDR_LOG=herdr=debug`；不得把包含 token/prompt 的日志整屏贴给 owner。

## 9. 禁止的捷径

- 不把 worktree、workspace、pane、agent name、native session ID 当成同一个对象；
- 不因 `done` 退出 agent；不因 Goal 完成冷启动；
- 不在没确认旧 agent已退出时抢同名 start；
- 不对现有 worktree用 `workspace create`；
- 不用 `workspace close` + raw `git worktree remove` 替代 `herdr worktree remove`；
- 不直接向 blocked UI投普通任务；
- 不把 prompt API success 当送达；必须状态确认 + delivery读回；
- 不运行无 timeout 的 wait，不做 heartbeat/轮询；
- 不在 owner 外部轨省略 `--session`，不依赖 focused workspace/pane；
- 不自动升级、stop server、push、删除 branch或使用 `--force`。

## 10. 版本差异

本机保持 `0.8.0`，未经 owner 指令不升级。上游 `0.8.2` 已修复与本流程直接相关的两项：

- `agent start` 等待新 shell/first-run prompt 真正 ready，降低 premature readiness；
- `agent prompt` 在 blocked UI前拒绝写入，并改进输入后延迟 Enter。

升级应单独做 runtime qualification，不能把 release note 当成本机已具备能力。

## 11. 上游真源

- [Herdr v0.8.0 release](https://github.com/herdrdev/herdr/releases/tag/v0.8.0)
- [v0.8.0 agent automation](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/agent-automation.mdx)
- [v0.8.0 CLI reference](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/cli-reference.mdx)
- [v0.8.0 agent states](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/agents.mdx)
- [v0.8.0 session restore](https://github.com/herdrdev/herdr/blob/v0.8.0/website/src/content/docs/session-state.mdx)
- [v0.8.0 bundled skill](https://github.com/herdrdev/herdr/blob/v0.8.0/skills/herdr/SKILL.md)
- [Herdr v0.8.2 release notes](https://github.com/herdrdev/herdr/releases/tag/v0.8.2)

