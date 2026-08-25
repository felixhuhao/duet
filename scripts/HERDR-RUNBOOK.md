# Herdr solo runbook

Herdr 负责统一 terminal 面板、进程保活和可见运行态；Goal 文件与 Git 负责工作事实。

## 1. 打开与切换

```bash
herdr
herdr agent list
```

裸 `herdr` 进入长期 `default` session。用方向键或鼠标选择 workspace；`q` 只退出当前 UI client，不结束
里面的 agent。

## 2. 固定布局

```text
default
├── canonical repo workspace
├── wt1 workspace · dev1 agent
├── wt2 workspace · dev2 agent
└── wt3 workspace · dev3 agent
```

workspace/worktree/agent name 长期复用。idle 分支使用 `wt1/wt2/wt3`；换 Goal 再切 Goal branch，不按任务
创建或删除 workspace/worktree。

## 3. 看状态

```bash
herdr agent list
herdr agent get dev1
herdr agent read dev1 --source recent-unwrapped --lines 80
```

- `working`：正在执行；
- `blocked`：等待输入或审批；
- `idle/done`：可接收输入，`done` 只是后台完成后尚未查看；
- `unknown`：进入 pane 人工核实。

Herdr 状态不等于 Goal 完成。Goal 是否 DONE 仍看 AC、验证、Git 与是否合入 canonical 主线。

## 4. 启动和 resume

只在现存 shell pane 中启动：

```bash
scripts/herdr-agent-start.sh dev1 codex <pane-id>
scripts/herdr-agent-start.sh dev1 codex <pane-id> \
  resume <native-session-id> --disable network_proxy
```

默认使用 PATH 上的 `codex`。事故恢复时可显式指定已验证 binary：

```bash
CODEX_BIN=/absolute/path/to/codex \
  scripts/herdr-agent-start.sh dev1 codex <pane-id> \
  resume <native-session-id> --disable network_proxy
```

helper 校验 pane cwd、Codex binary、truecolor 环境和 agent ready。启动后再核 native session ID、branch/HEAD
与一次普通 prompt 回复。

## 5. Goal 切换

1. 当前 Goal 完成并合入 canonical 主线；
2. 席位 worktree clean；
3. owner 指定基于最新 main 的下一 Goal branch；没有下一项则切回同名 idle branch；
4. agent 在原 workspace/cwd/native session 继续，不重建席位；
5. 新 Goal 开工前读取项目规则与 Goal，并确认 base 可达。

## 6. 安全退出与迁移

确认 agent 为 `idle/done` 且没有在途 turn；`Ctrl+U` 清 composer，再 `Ctrl+D`。`herdr agent list` 中名称
消失且 pane 回 shell后，才能在别的 runtime resume 同一 native session。

迁回 Herdr 时：

1. 记录 native session ID、cwd、branch/HEAD；
2. 安全退出旧 runtime；
3. 确认固定 Herdr pane cwd 正确且在 shell；
4. 使用 helper resume 原 session；
5. 核对 agent list、状态、cwd、session ID 和回复。

不要 stop Herdr server，不要为关一个 agent 删除 workspace，也不要双开同一 native session。

## 7. 验收

```bash
bash -n scripts/herdr-agent-start.sh
herdr agent list
scripts/worktree-audit.py /absolute/repo/root
```

最终只检查：三个 agent 都在 `default`、名称与固定 worktree 对应、状态可识别、native session 无重复、
worktree clean 或有明确恢复指针。
