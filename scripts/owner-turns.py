#!/usr/bin/env python3
"""复盘工具：从 Claude Code / Codex JSONL transcript 提取 owner 亲手输入的回合。

用法: owner-turns.py <transcript.jsonl> [...]
      Claude: ~/.claude/projects/<项目目录>/<session-id>.jsonl
      Codex:  ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl
过滤掉 [peer:*] / [owner-relay] / 系统块，剩下的就是 owner 推动的回合。
复盘时逐条问：这条是 决策 / 传棒推动 / 环境故障 / 规则过严 / 信息问答？
非决策占比就是校准判据 ③ 的分母来源（打断有效率 ≥80%）。
"""
import json, sys


def content_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            b.get("text", b.get("input_text", b.get("output_text", "")))
            for b in content if isinstance(b, dict)
        )
    return ""


def role_text(d):
    """Return normalized (role, text) for Claude or Codex transcript rows."""
    if d.get("type") in ("user", "assistant"):
        return d["type"], content_text(d.get("message", {}).get("content"))
    if d.get("type") == "response_item":
        p = d.get("payload", {})
        if p.get("type") == "message" and p.get("role") in ("user", "assistant"):
            return p["role"], content_text(p.get("content"))
    return "", ""

for path in sys.argv[1:]:
    rows = []
    source = sys.stdin if path == "-" else open(path)
    for line in source:
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        role, t = role_text(d)
        if role != 'user':
            continue
        t = t.strip()
        if not t or t.startswith(('[peer:', '[owner-relay]', '<')):
            continue
        rows.append(t[:120].replace('\n', ' ⏎ '))
    name = "stdin" if path == "-" else path.rsplit('/',1)[-1]
    print(f"== {name}: {len(rows)} 条 owner 输入 ==")
    for i, r in enumerate(rows, 1):
        print(f"{i:3}. {r}")
