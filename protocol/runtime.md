# Runtime 协议

默认 runtime 是 tmux + 长期 worktree。一个 solo Goal owner 在一个固定 window 中工作。

## 固定拓扑

- 一个产品域一个 tmux session；
- `main` window 使用 canonical 主树，负责规划、合并和真源维护；
- `dev1/dev2/...` 各绑定一个 owner 预置的长期 worktree；
- 换 Goal 只换 branch，不换 window 或 cwd；
- worktree 的创建、移动和删除只由 owner 安排。

tmux 只提供 terminal 布局、PTY 和进程保活。它不知道 Goal 状态、agent identity、消息是否送达或上下文
是否正确；不要用 `pane_current_command`、`capture-pane` 或自动 `send-keys` 构造状态机。

## 席位记录

每个 active Goal 记录一行即可：

```text
owner=<name> · tmux=<session>:<window>.0 · native_session=<id> · cwd=<path> · branch=<branch>
```

native session ID 用于恢复 conversation；Goal 文件与 Git 用于冷恢复工作。两者都要留，不能互相替代。

## 启动与恢复

新进程或 resume 后人工确认四件事：

1. target window 和 cwd 正确；
2. native session ID 正确；
3. branch/HEAD 与 Goal 一致；
4. agent 能读到项目规则并正常回复一次 prompt。

只有旧进程已退出后才能在另一 runtime resume 同一 native session，禁止双开。原 session 无法恢复时才
cold start，并先从项目规则、Goal、当前 HEAD 和未验证面恢复上下文。

## 例外

独立 reviewer 可以临时使用另一个固定席位，但只 review 冻结 diff，不与 Goal owner 组成常驻 pair。
Herdr 仅用于 owner 明确要求的兼容场景；不要为了消息通知在 tmux 上重建 Herdr。
