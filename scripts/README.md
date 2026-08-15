# scripts

待 herdr 在本机安装验证后补充。计划内容：

- `herdr-setup.sh`：建 duet workspace、两个 pane（Claude Code / Codex）、注入角色卡路径；
- 门铃 helper：封装 `pane send-text` + `send-keys enter` 的传棒消息格式。

原则：只放薄封装。开始想写调度器/状态机时，先重评 loopx（见 README 拍板记录）。
