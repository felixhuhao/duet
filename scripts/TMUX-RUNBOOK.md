# tmux solo runbook

tmux 只做两件事：把多个 terminal 放在一个 session，关闭 terminal app 后继续保活。

## 1. 布局

```text
<product>
├── main   canonical 主树
├── dev1   固定 worktree 1
├── dev2   固定 worktree 2
└── dev3   固定 worktree 3
```

window/worktree 长期复用；换 Goal 只换 branch。不要按任务创建 window 或 worktree。

## 2. 第一次 setup

先确认 owner 已准备好所有 worktree：

```bash
git -C /absolute/repo worktree list --porcelain
```

再创建 tmux 布局：

```bash
scripts/tmux-solo-setup.sh mobile /absolute/repo \
  dev1=/absolute/repo-wt1 \
  dev2=/absolute/repo-wt2 \
  dev3=/absolute/repo-wt3
```

已有同名 window 但 cwd 不一致时 helper 会拒绝；先查清，不要覆盖。

## 3. 启动 Codex

新 session：

```bash
scripts/tmux-codex-start.sh mobile dev1 /absolute/repo-wt1
```

恢复原 conversation：

```bash
scripts/tmux-codex-start.sh mobile dev1 /absolute/repo-wt1 \
  resume <native-session-id>
```

如果 PATH 上的 Codex 不可用，可以临时指定已验证的 binary：

```bash
CODEX_BIN=/absolute/path/to/codex \
  scripts/tmux-codex-start.sh mobile dev1 /absolute/repo-wt1 \
  resume <native-session-id>
```

进入 TUI 后人工核对 `/status`、cwd、branch/HEAD，并发一次普通 prompt 确认能完整回复。看到进程存在不等于
上下文已经恢复。

## 4. 日常操作

```bash
tmux attach -t mobile
tmux switch-client -t mobile:dev2
tmux list-windows -t mobile -F '#{window_name} · #{pane_current_command} · #{pane_current_path}'
tmux detach-client
```

常用键：`Ctrl-b n/p` 切 window，`Ctrl-b w` 看列表，`Ctrl-b d` detach。

owner 直接进入目标 window 沟通。不要用自动 `send-keys` 投递 Goal，不做 heartbeat、消息回执或 agent
状态推断；任务和证据写入工作仓文件与 Git。

## 5. 安全退出与恢复

退出 Codex 前确认没有在途 turn，`Ctrl+U` 清空 composer，再 `Ctrl+D`。pane 回到 shell 后，才可以在别处
resume 同一 native session。不要为关闭一个 worker 而 kill 整个 tmux session。

恢复时按这个顺序：

1. 核对 worktree、dirty 状态、branch/HEAD 和 native session ID；
2. 核对精确 tmux target 和 cwd；
3. 旧进程确已退出后，用 helper resume；
4. 核对 `/status` 并完成一次人工 prompt；
5. 回报 `RESUME/COLD START · session ID · target · cwd · branch/HEAD`。

Herdr 迁移同样必须等旧 agent idle 并安全退出后再 resume。是否清理 Herdr server/workspace 是另一项 owner
决策，不是迁移步骤。

## 6. 验收

```bash
bash -n scripts/tmux-solo-setup.sh scripts/tmux-codex-start.sh
tmux list-panes -s -t mobile \
  -F '#{session_name}:#{window_name}.#{pane_index} · #{pane_current_command} · #{pane_current_path}'
```

最终只检查：window 对应正确 worktree、没有 native session 双开、main 不被开发 worker 写、每个 Goal 能从
Goal 文件和 Git 冷恢复。
