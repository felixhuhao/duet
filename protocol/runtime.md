# Runtime 协议

默认 runtime 是 Herdr `default` session + owner 预置的长期 workspace/worktree。一个 Goal owner 使用一个固定
agent 席位；换 Goal 不靠重建 terminal 获取“干净上下文”。

## 固定现场

- workspace、agent name、cwd 和 worktree 由 owner 预置并长期复用；
- worktree 的创建、移动和删除只由 owner 安排；
- Goal 开始前确认 branch/HEAD/base，结束后按项目规则合并或保留恢复指针；
- 同一 native session 不得在两个 runtime 或 pane 同时运行。

## 两种状态

Herdr 的 `working/blocked/idle/done/unknown` 只说明 agent 是否可交互。Goal lifecycle、AC、验证、Git 和是否已
交付由目标项目的文件与仓库裁决。`idle/done` 不等于 Goal 完成，`unknown` 必须进入 pane 核实。

每个 active Goal 至少记录：

```text
owner=<name> · herdr=default/<agent> · pane=<id> · native_session=<id>
cwd=<path> · branch=<branch> · base=<sha>
```

## 启动与恢复

只使用 `scripts/herdr-agent-start.sh` 在现存 shell pane 新建或 resume。恢复后核对 agent、pane、cwd、native
session、branch/HEAD 和一次普通回复。原 session 无法恢复时才 cold start，并从项目规则、Goal、Git 和
未验证面恢复上下文。

## 通信与权限

agent 存在或显示 `idle/done` 不表示可被其他 Goal owner 占用。没有 Goal 预授权或 owner 对目标席位的明确
指派时，Goal owner 不得发送 agent-to-agent task、follow-up 或 review 请求；需要协助先报告 owner。

Herdr 只保存运行现场，不扩大 Git、网络、发布、删除、跨仓或外部系统权限。
