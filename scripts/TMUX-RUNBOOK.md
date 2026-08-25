# tmux solo Goal owner 操作手册

> 原则：simple and effective。tmux 只负责把长期 terminal 放在一起并在 detach 后保活；
> Goal、上下文、状态与交付证据仍由工作仓文件和 Git 承担。默认不做 agent 间自动通信。

## 1. 只记四个对象

| 对象 | 含义 | 生命周期 |
|---|---|---|
| tmux session | 一个产品域的 terminal 集合，如 `mobile` | 长期存在；`tmux attach -t mobile` 进入 |
| window | 一个固定席位，如 `main/dev1/dev2` | 长期存在；不按 Goal 创建/删除 |
| worktree | 席位唯一可写目录 | owner 预置；换 Goal 只换 branch |
| native session ID | Codex conversation identity | resume 连续性的真源 |

tmux pane 只知道前台进程和 cwd，不知道 agent 是 `idle/working/blocked`。不得从
`pane_current_command=codex` 推断工作完成、消息送达或上下文已装载。

## 2. 唯一默认拓扑

```text
tmux session: <product>
├── main   canonical 主树：grilling / planning / merge / 真源回写
├── dev1   owner 预置 wt1：一个 solo Goal owner
├── dev2   owner 预置 wt2：一个 solo Goal owner
└── dev3   owner 预置 wt3：一个 solo Goal owner
```

每个 window 默认一个 Codex pane；需要普通 shell 时人工 split，不把测试 runner、watcher 或第二 agent
固化进启动脚本。session 名、window 名和 cwd 是路由真源，不另建运行时 registry。

## 3. 只打开 owner 已准备的树

先核路径、branch 与 dirty 状态，再创建 terminal 布局：

```bash
git -C /absolute/repo/root worktree list --porcelain
scripts/tmux-solo-setup.sh mobile /absolute/repo/root \
  dev1=/absolute/worktree/wt1 \
  dev2=/absolute/worktree/wt2 \
  dev3=/absolute/worktree/wt3
```

helper 只创建 tmux session/window，不运行 `git worktree add/move/remove`，也不切 branch。若同名 window
已经存在但 cwd 不同则拒绝，不能用现有名字覆盖别的 terminal。

## 4. 启动和 resume 只走一个入口

新 Codex：

```bash
scripts/tmux-codex-start.sh mobile dev1 /absolute/worktree/wt1 \
  --disable network_proxy
```

resume 同一 conversation：

```bash
scripts/tmux-codex-start.sh mobile dev1 /absolute/worktree/wt1 \
  resume <native-session-id> --disable network_proxy
```

helper 要求目标 pane 正停在 shell、pane cwd 与参数目录一致；它清除 `NO_COLOR/CODEX_CI` 等宿主变量，
保留 tmux 自己的 `TERM`，设置 truecolor，并给 Codex 补 `--cd <pane-cwd>`。默认使用 PATH 上的 `codex`；
事故恢复可显式传 `CODEX_BIN=/absolute/path/to/codex`，但必须在回执中披露。

启动成功只证明 Codex 进程进入目标 pane。进入 TUI 后人工核对：

```text
/status        native session ID
/mcp verbose   本 Goal 依赖的 MCP（如有）
```

随后发一次普通 recovery prompt 并看到完整回复。没有回复就不宣布恢复，不用 `tmux send-keys` 重投。

## 5. Solo Goal pickup

1. owner 在 canonical 主树完成 roadmap grooming、Goal Contract 与冻结 BASE；
2. 指定一个固定席位和 branch；该 branch 必须包含 BASE，并通过 ancestor 检查；
3. owner 在对应 window 直接投递 Goal 文件路径与 commit，不向其他 agent 自动转发；
4. worker 只读 Launch Capsule，落盘 Context Receipt；`ACCEPTED` 前禁止生产写；
5. 同一 worker 从 Contract/Execution Notes 到实现、定向验证、自检和 Completion Package 负责到底；
6. DEV_DONE 后 owner/main 串行并轨；下一 Goal 仍复用同一 window/worktree/native session。

默认不设 spec/delivery pair。只有 P0/P1、安全/权限/金额/数据删除、共享契约、owner 点名或 worker 主动
请求时才加独立 review；reviewer 消费冻结 `BASE..HEAD`，不接管 Goal ownership。

## 6. 通信边界

- tmux 是显示与进程保活工具，不是消息总线；日常不使用 `tmux send-keys` 给另一个 Codex 注入任务；
- owner 直接切换 window 输入，或让 worker 读取已提交的 Goal/handoff/review 文件；
- 跨仓/跨席位事实仍写发送方仓 `docs/handoffs/`，Git commit 是可恢复指针；
- 不做 heartbeat、自动轮询、状态归一、instance registry 或 delivery acknowledgement；需要这些能力时
  必须重新拍板是否启用 Herdr 兼容路径，不能在 tmux wrapper 中悄悄重建。

## 7. 日常命令

```bash
tmux attach -t mobile
tmux switch-client -t mobile:dev2
tmux list-windows -t mobile -F '#{window_name} · #{pane_current_command} · #{pane_current_path}'
tmux detach-client
```

常用默认键：`Ctrl-b n/p` 切前后 window，`Ctrl-b w` 列表，`Ctrl-b d` detach。关闭 terminal app 不影响
tmux 内进程；重启机器会结束 tmux server，之后按第 3、4 节重建布局并 resume native session。

## 8. 维护与事故恢复

正常退出某个 Codex 前先确认没有在途 turn，`Ctrl+U` 清 composer，再 `Ctrl+D`；确认 pane 回到 shell
后才能 resume。不能直接 kill tmux server，也不能为关一个 worker 使用 session 级命令。

恢复顺序固定：

1. 核 worktree dirty/branch/HEAD 与 native session ID；
2. `tmux list-windows` 确认精确目标；
3. pane 已丢才由 setup helper 补同名 window；已有错误 cwd 则停止，不覆盖；
4. 走 start helper resume 原 session；只有原 session 无法恢复或 owner 明确要求才 cold start；
5. 核 `/status`、必要 MCP、颜色与一次人工 prompt 回答；
6. 报 `RESUME/COLD START · session ID · tmux target · cwd · branch/HEAD`。

Herdr → tmux 的自然迁移必须先让旧 agent 到 idle，记录 native session ID，安全退出并确认进程消失，
再在 tmux resume；禁止同一 native session 双开。Herdr server/workspace 的清理由 owner另行决定，不是迁移前置。

## 9. 验收

```bash
bash -n scripts/tmux-solo-setup.sh scripts/tmux-codex-start.sh
scripts/worktree-audit.py /absolute/repo/root  # 只读审计；Herdr ownership 字段在 tmux 模式下不作成功条件
tmux list-panes -s -t mobile -F '#{session_name}:#{window_name}.#{pane_index} · #{pane_pid} · #{pane_current_command} · #{pane_current_path}'
```

最终必须满足：一个稳定 session、每个固定 worktree 一个同名 window、无重复 Codex native session、
canonical 主树不被开发 worker 写、所有 worker 能从文件与 Git 冷恢复。
