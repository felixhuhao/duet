#!/usr/bin/env python3
"""把 OpenCode session 归一成 Claude/Codex 风格的 user/assistant JSONL。

用法: opencode-turns.py <ses_id> [<ses_id> ...]
示例: opencode-turns.py ses_xxx | owner-turns.py -
"""
import json
import re
import subprocess
import sys


for session_id in sys.argv[1:]:
    if not re.fullmatch(r"ses_[A-Za-z0-9]+", session_id):
        raise SystemExit(f"invalid OpenCode session id: {session_id}")
    sql = f"""
select m.id, m.time_created,
       json_extract(m.data, '$.role') as role,
       coalesce((select group_concat(json_extract(p.data, '$.text'), ' ')
                 from part p
                 where p.message_id=m.id
                   and json_extract(p.data, '$.type')='text'), '') as text
from message m
where m.session_id='{session_id}'
order by m.time_created, m.id
"""
    result = subprocess.run(
        ["opencode", "db", sql, "--format", "json"],
        check=True, capture_output=True, text=True,
    )
    for row in json.loads(result.stdout):
        role = row.get("role")
        if role not in ("user", "assistant"):
            continue
        print(json.dumps({
            "type": role,
            "timestamp": row.get("time_created"),
            "message": {"content": row.get("text", "")},
        }, ensure_ascii=False))
