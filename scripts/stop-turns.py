#!/usr/bin/env python3
"""提取「loop 停下来找 owner」的完整现场：agent 停机前最后的话 + owner 的回复。"""
import json
import sys


def text_of(msg):
    c = msg.get("message", {}).get("content")
    if isinstance(c, list):
        return " ".join(b.get("text", "") for b in c
                        if isinstance(b, dict) and b.get("type") == "text").strip()
    return str(c or "").strip()


for path in sys.argv[1:]:
    last_assistant = ""
    pairs = []
    for line in open(path):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = d.get("type")
        if t == "assistant":
            txt = text_of(d)
            if txt:
                last_assistant = txt
        elif t == "user":
            txt = text_of(d)
            if not txt or txt.startswith(("[peer:", "[owner-relay]", "<")):
                continue
            pairs.append((last_assistant, txt))
    name = path.rsplit("/", 1)[-1][:8]
    print(f"\n{'#' * 70}\n# {name}: {len(pairs)} 个 owner 推动回合\n{'#' * 70}")
    for i, (ask, reply) in enumerate(pairs, 1):
        tail = ask[-600:] if ask else "（无 agent 前文——session 首条或纯工具轮）"
        print(f"\n----- 回合 {i} -----")
        print(f"[agent 停机前] …{tail}")
        print(f"[owner 回复] {reply[:400]}")
