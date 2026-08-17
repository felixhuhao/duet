#!/usr/bin/env python3
"""从 Claude Code / Codex JSONL 提取 agent 停机前最后的话 + owner 回复。"""
import json
import sys


def content_text(content):
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return " ".join(
            b.get("text", b.get("input_text", b.get("output_text", "")))
            for b in content if isinstance(b, dict)
        ).strip()
    return ""


def role_text(d):
    if d.get("type") in ("user", "assistant"):
        return d["type"], content_text(d.get("message", {}).get("content"))
    if d.get("type") == "response_item":
        p = d.get("payload", {})
        if p.get("type") == "message" and p.get("role") in ("user", "assistant"):
            return p["role"], content_text(p.get("content"))
    return "", ""


for path in sys.argv[1:]:
    last_assistant = ""
    pairs = []
    source = sys.stdin if path == "-" else open(path)
    for line in source:
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        role, txt = role_text(d)
        if role == "assistant":
            if txt:
                last_assistant = txt
        elif role == "user":
            if not txt or txt.startswith(("[peer:", "[owner-relay]", "<")):
                continue
            pairs.append((last_assistant, txt))
    name = ("stdin" if path == "-" else path.rsplit("/", 1)[-1])[:8]
    print(f"\n{'#' * 70}\n# {name}: {len(pairs)} 个 owner 推动回合\n{'#' * 70}")
    for i, (ask, reply) in enumerate(pairs, 1):
        tail = ask[-600:] if ask else "（无 agent 前文——session 首条或纯工具轮）"
        print(f"\n----- 回合 {i} -----")
        print(f"[agent 停机前] …{tail}")
        print(f"[owner 回复] {reply[:400]}")
