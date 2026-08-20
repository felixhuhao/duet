# Validation Ledger

## 当前策略

- frozen HEAD：默认同日累计 3 个 `DEV_DONE` 则当日一次，否则每累计 3 个 Goal 请求一次；owner 可调整
- integration debt 上限：未完成 I1/I2 最多 2 项或 48h；先到者触发。

## Goal 状态

| Goal | Tier | DEV | Integration | Device | 自动化/QA Goal | 债务起点 | 下一验证 |
|---|---|---|---|---|---|---|---|

## Frozen HEAD Runs

| Run | Repo@SHA | Goal 集合 | 环境/命令 | 结果 | Integration owner | 证据 |
|---|---|---|---|---|---|---|

## Device / 真环境残余

| Goal/场景 | 平台 | 依赖 | 状态 | 唯一唤醒事件 | 证据 |
|---|---|---|---|---|---|

## Defect Links

| 来源 Goal | Validation 失败 | Defect Goal | 影响范围 | 状态 |
|---|---|---|---|---|
