#!/usr/bin/env bash
# Prepare one pane and start/resume one long-lived agent seat.
# Usage: herdr-agent-start.sh <name> <kind> <pane> [runtime args...]
set -euo pipefail

SESSION_NAME="${HERDR_SESSION:-default}"
HERDR_BIN="${HERDR_BIN:-$(command -v herdr)}"
PS_BIN="${PS_BIN:-$(command -v ps)}"

AGENT_NAME="${1:?agent name}"
AGENT_KIND="${2:?agent kind}"
PANE_ID="${3:?pane id}"
shift 3
RUNTIME_ARGS=("$@")

hcmd() {
  "$HERDR_BIN" --session "$SESSION_NAME" "$@"
}

if [ "$AGENT_KIND" = "codex" ]; then
  pane_json="$(hcmd pane get "$PANE_ID")"
  pane_cwd="$(printf '%s' "$pane_json" | python3 -c '
import json, sys
pane = json.load(sys.stdin)["result"]["pane"]
print(pane.get("cwd") or pane.get("foreground_cwd") or "")
')"
  if [ -z "$pane_cwd" ] || [ ! -d "$pane_cwd" ]; then
    echo "agent start failed invalid pane cwd: $AGENT_NAME@$PANE_ID · $pane_cwd" >&2
    exit 4
  fi

  has_explicit_cwd=false
  for ((i = 0; i < ${#RUNTIME_ARGS[@]}; i++)); do
    case "${RUNTIME_ARGS[$i]}" in
      -C|--cd)
        has_explicit_cwd=true
        explicit_cwd="${RUNTIME_ARGS[$((i + 1))]:-}"
        if [ "$explicit_cwd" != "$pane_cwd" ]; then
          echo "agent start failed cwd mismatch: pane=$pane_cwd runtime=$explicit_cwd" >&2
          exit 4
        fi
        ;;
      --cd=*)
        has_explicit_cwd=true
        explicit_cwd="${RUNTIME_ARGS[$i]#--cd=}"
        if [ "$explicit_cwd" != "$pane_cwd" ]; then
          echo "agent start failed cwd mismatch: pane=$pane_cwd runtime=$explicit_cwd" >&2
          exit 4
        fi
        ;;
    esac
  done
  if [ "$has_explicit_cwd" = false ]; then
    RUNTIME_ARGS+=(--cd "$pane_cwd")
  fi
fi

marker="__DUET_ENV_READY__"
hcmd pane run "$PANE_ID" \
  "unset NO_COLOR CODEX_CI CODEX_INTERNAL_ORIGINATOR_OVERRIDE CODEX_PERMISSION_PROFILE CODEX_THREAD_ID; export TERM=xterm-256color COLORTERM=truecolor; printf '__DUET_ENV_READY__\\n'"
hcmd pane wait-output "$PANE_ID" --match "$marker" --source recent --timeout 5000 >/dev/null

if [ "${#RUNTIME_ARGS[@]}" -gt 0 ]; then
  hcmd agent start "$AGENT_NAME" --kind "$AGENT_KIND" --pane "$PANE_ID" --timeout 120000 -- "${RUNTIME_ARGS[@]}"
else
  hcmd agent start "$AGENT_NAME" --kind "$AGENT_KIND" --pane "$PANE_ID" --timeout 120000
fi

# These host variables silently disable Codex's terminal palette. Assert the
# live process environment, not merely the pane setup command.
if [ "$AGENT_KIND" = "codex" ]; then
  process_json="$(hcmd pane process-info --pane "$PANE_ID")"
  agent_pid="$(printf '%s' "$process_json" | python3 -c '
import json, sys
processes = json.load(sys.stdin)["result"]["process_info"]["foreground_processes"]
print(next(item["pid"] for item in processes if item.get("name") == "codex"))
')"
  process_env="$($PS_BIN eww -p "$agent_pid" -o command= | tr ' ' '\n')"
  if printf '%s\n' "$process_env" | grep -Eq '^(NO_COLOR|CODEX_CI)=' \
    || ! printf '%s\n' "$process_env" | grep -Fxq 'TERM=xterm-256color' \
    || ! printf '%s\n' "$process_env" | grep -Fxq 'COLORTERM=truecolor'; then
    echo "agent start failed color preflight: $AGENT_NAME@$PANE_ID" >&2
    exit 4
  fi
  echo "agent ready: $AGENT_NAME@$PANE_ID · color=ok"
fi
