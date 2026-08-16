#!/usr/bin/env bash
# 停机 backstop：把「停机条件」从纪律降为机制（学 firstmate 的 turn-end backstop）。
# 轮询各 session 的 agent 状态；某 pane 连续 idle 超过阈值 → 踢它一脚做停机自查，
# 每个 idle 周期只踢一次（转回 working 后重置）。owner 不参与。
#
# 用法：backstop.sh [session ...]   # 无参 = default session；"default" 字面量表示默认
# 依赖：herdr ≥0.8（agent list 的 socket API）
set -u
SESSIONS=("${@:-default}")
INTERVAL=300         # 轮询间隔（秒）
IDLE_THRESHOLD=900   # 连续 idle 多久算可疑（秒）
STATE_DIR="${TMPDIR:-/tmp}/duet-backstop"; mkdir -p "$STATE_DIR"
PING='[backstop] 你已闲置一段时间。按 protocol/baton.md 停机条件自查：当前是否处于合法停机（已交棒送达 / gate 门铃已发出）？若是，回一行确认即可；若不是，继续推进手头批次。'

list_agents() { # $1=session → 行: pane_id agent status
  local s="$1" env=()
  [ "$s" != "default" ] && env=(env "HERDR_SESSION=$s")
  ${env[@]+"${env[@]}"} herdr agent list 2>/dev/null | python3 -c '
import json,sys
try: d=json.load(sys.stdin)
except: sys.exit(0)
for a in d.get("result",{}).get("agents",[]):
    print(a["pane_id"], a["agent"], a["agent_status"])'
}

send_ping() { # $1=session $2=pane
  local s="$1" p="$2" env=()
  [ "$s" != "default" ] && env=(env "HERDR_SESSION=$s")
  ${env[@]+"${env[@]}"} herdr pane send-text "$p" "$PING" && sleep 1 && \
    ${env[@]+"${env[@]}"} herdr pane send-keys "$p" enter
}

echo "backstop 启动：sessions=${SESSIONS[*]} 阈值=${IDLE_THRESHOLD}s"
while true; do
  now=$(date +%s)
  for s in "${SESSIONS[@]}"; do
    while read -r pane agent status; do
      [ -z "${pane:-}" ] && continue
      key="$STATE_DIR/${s}-${pane//:/_}"
      if [ "$status" = "idle" ]; then
        if [ ! -f "$key.idle_since" ]; then echo "$now" > "$key.idle_since"; fi
        idle_since=$(cat "$key.idle_since")
        if [ $((now - idle_since)) -ge $IDLE_THRESHOLD ] && [ ! -f "$key.pinged" ]; then
          send_ping "$s" "$pane" && touch "$key.pinged" \
            && echo "$(date +%T) ping → $s/$pane ($agent)"
        fi
      else
        rm -f "$key.idle_since" "$key.pinged"   # 干活了/blocked：重置周期
      fi
    done < <(list_agents "$s")
  done
  sleep $INTERVAL
done
