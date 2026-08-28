# Herdr solo runbook

Herdr 保存长期 terminal 和可见运行态；Goal 文件与 Git 保存交付事实。

## 打开与查看

```bash
herdr
herdr agent list
herdr agent get <agent-name>
herdr agent read <agent-name> --source recent-unwrapped --lines 80
```

裸 `herdr` 进入长期 `default` session。`q` 只退出当前 UI client，不结束其中的 agent。

Herdr `working/blocked/idle/done/unknown` 只说明 agent 是否可交互，不等于 Goal 完成。`unknown` 时进入 pane
核实，不从状态名猜测进程或交付结果。

## 固定 workspace

owner 预先建立 canonical workspace 和需要的长期 Goal owner workspace。workspace、agent name、cwd 和 worktree
长期复用；换 Goal 只按项目规则切 branch，不为任务临时创建或删除 workspace/worktree。

## 启动与 resume

只在目标 workspace 已存在的 shell pane 中运行：

```bash
scripts/herdr-agent-start.sh <agent-name> <kind> <pane-id>
scripts/herdr-agent-start.sh <agent-name> <kind> <pane-id> \
  resume <native-session-id> --disable network_proxy
```

默认使用 PATH 中与 `<kind>` 对应的 binary。事故恢复时可以显式提供已验证的 Codex binary：

```bash
CODEX_BIN=/absolute/path/to/codex \
  scripts/herdr-agent-start.sh <agent-name> codex <pane-id> \
  resume <native-session-id> --disable network_proxy
```

helper 会校验 pane cwd、binary、终端颜色环境和 agent ready。启动后人工核对：agent/pane、cwd、native session、
branch/HEAD 和一次普通 prompt 回复。

## Goal 切换

1. 当前 Goal 达到项目定义的交付状态；
2. worktree clean，或 Goal 留有明确恢复指针；
3. owner 指定下一 Goal、branch/base；没有下一项则保持 idle；
4. agent 在原 workspace/cwd/native session 继续；
5. 新 Goal 重新读取项目规则和 Goal，不把旧上下文当作已完成 pickup。

## 安全退出与恢复

确认 agent 没有在途 turn；清空 composer 后安全退出进程。只有 Herdr 中 agent 名称消失且 pane 回到 shell，才可
在另一处 resume 同一 native session。不要为退出一个 agent 停止整个 Herdr server 或删除 workspace。

## 验证

```bash
bash -n scripts/herdr-agent-start.sh
python3 scripts/test-herdr-agent-start.py
python3 scripts/test-worktree-audit.py
scripts/worktree-audit.py /absolute/repo/root
```

检查 agent 名称与 owner 预置 worktree 对应、状态可识别、native session 无重复，以及 worktree clean 或有明确
恢复指针。
