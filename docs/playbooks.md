# 跨项目 playbooks

从席位工作记忆晋升的稳定方法。项目私有事实不进这里，以各仓文档为准。

## 共享 main 的 push race（跨仓单写者）

工作期间另一写者推进了 main 时：`git fetch` → `git merge origin/main` → 解冲突 → 复跑定向门禁
（不跑全量）→ push → `git status` 确认同步。回执必须含：冲突文件与解法、门禁读数（测试计数、
analyze、最终 SHA）。落后过多或冲突超纲时停下报告 owner，不 reset/rebase 覆盖现场。

## 跨仓 Goal 领取前置

领取会写多个仓的 Goal 前，先查**所有**目标仓的席位与 canonical 状态（席位在忙/待命、canonical
是否 clean）；建树/席位授权请求与首仓开发并行发出，不等全部批准才动工。

## owner 协作约定

- 拍板类问题用「选项 + 推荐」格式，不开放式抛问。
- 让 owner 拍板事实前先做一轮一手信源核实（官方文档/上游代码），把不确定性消化在 agent 侧。
- push 与一切外发动作逐次批准；收口与合并权限以各仓 AGENTS 为准。
- 回执带证据读数：测试 PASS/FAIL 计数、analyze 结果、commit SHA、跳过项与原因。
