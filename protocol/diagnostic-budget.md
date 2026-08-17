# 超时与无进展诊断预算

本协议处理测试挂死、命令超时、进程不退出和“换一种写法再跑一次”但没有信息增量的循环。
目标是用最少执行次数取得可判别证据；不是禁止诊断。

## 同症状如何计数

计数单位是**可观察失败签名**，由 pair 共享，不按命令字符串、agent 或临时文件名重置。
以下变化仍算同一症状：

- 只把 30 秒改成 60/90 秒；
- 只换 probe 文件、日志文件、测试过滤器或并发参数；
- 每次都停在同一阶段，且新输出不能排除任何候选原因；
- 强杀后原样重跑。

OpenCode 的 doom-loop 只能抓完全相同的 tool input，不能替代这里的语义计数。

## 预算：首次观察 + 一次判别性重试

1. **首次观察**：保存完整命令、真实墙钟耗时、最后有效输出、卡住阶段和相关进程身份；
2. **唯一一次重试**：执行前必须写出一个可证伪假设，以及 A/B 两种结果分别排除什么。
   只能改变与该假设直接相关的一个变量；
3. 第二次仍是同一失败签名，或重试不能产生判别结果，立即标记
   `DIAGNOSTIC_BUDGET_EXHAUSTED`，停止受影响 slice。继续执行需要新外部证据或 owner 明确追加预算。

不能先跑再补假设。代码静态阅读、查看既有日志、读取进程栈等非执行型调查不消耗次数，
但不得借此启动等价测试。

## timeout 必须是真墙钟边界

- test runner 的 `--timeout` 默认只算测试体，不得宣称它能限制编译、启动、发现测试或 teardown；
- 需要墙钟上限时，必须由外层 supervisor 覆盖整条命令及其进程组；环境没有可靠 supervisor 时，
  明说“无墙钟边界”，不要用内部参数伪装；
- 到期先终止本次启动的**精确 PID/进程组**，必要时再升级强杀。多 agent 工作区禁止
  `pkill -f flutter_tester`、`killall` 等宽泛清场，它们可能杀掉别人的并行门禁；
- agent 正在 TUI 中运行 tool 时，不用 pane 级 `Ctrl+C` 代替子进程终止：终端前台控制可能让
  runtime 自身一并退出。必须由启动命令的 supervisor 持有并终止子进程组；若做不到，停在
  Incident，不能靠反复重启 TUI 清场；
- 到期后的 cleanup 只清本次创建的 probe、日志和进程，不扩大到仓库或其他 worktree。

## 预算耗尽后的交接

Delivery Owner 把以下短账写进当前 devlog/review 后传给 Spec Owner，并结束 turn：

```text
DIAGNOSTIC_BUDGET_EXHAUSTED
symptom: <失败签名与卡住阶段>
attempt-1: <命令/墙钟/最后输出>
attempt-2: <假设/唯一变量/结果/排除了什么>
cleanup: <精确处理了哪些本轮进程与 probe>
recommendation: <静态修复、隔离验证或请求追加预算；必须给自己的推荐>
```

Spec Owner 只做三件事：核对两次是否同症状、检查推荐是否有新判别力、决定静态收窄或向 owner
报告 Incident。不得把“再多跑几次看看”作为 closure。该 slice 停止不占住 pair；其他已授权且
不依赖它的 slice 按 baton 的 `dependency parked / pair released` 规则处理。
