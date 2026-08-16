#!/usr/bin/env python3
"""复盘工具：从 pane Claude 的 transcript 提取 owner 亲手输入的全部回合。

用法: owner-turns.py <transcript.jsonl> [...]
      transcript 在 ~/.claude/projects/<项目目录>/<session-id>.jsonl
过滤掉 [peer:*] / [owner-relay] / 系统块，剩下的就是 owner 推动的回合。
复盘时逐条问：这条是 决策 / 传棒推动 / 环境故障 / 规则过严 / 信息问答？
非决策占比就是校准判据 ③ 的分母来源（打断有效率 ≥80%）。
"""
import json, sys

for path in sys.argv[1:]:
    rows = []
    for line in open(path):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get('type') != 'user':
            continue
        c = d.get('message', {}).get('content')
        if isinstance(c, list):
            t = ' '.join(b.get('text', '') for b in c
                         if isinstance(b, dict) and b.get('type') == 'text')
        else:
            t = str(c or '')
        t = t.strip()
        if not t or t.startswith(('[peer:', '[owner-relay]', '<')):
            continue
        rows.append(t[:120].replace('\n', ' ⏎ '))
    print(f"== {path.rsplit('/',1)[-1]}: {len(rows)} 条 owner 输入 ==")
    for i, r in enumerate(rows, 1):
        print(f"{i:3}. {r}")
