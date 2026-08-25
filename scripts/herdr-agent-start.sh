#!/usr/bin/env bash
# Prepare one pane and start/resume one long-lived agent seat.
# Usage: herdr-agent-start.sh <name> <kind> <pane> [runtime args...]
set -euo pipefail

SESSION_NAME="${HERDR_SESSION:-default}"
HERDR_BIN="${HERDR_BIN:-$(command -v herdr)}"
PS_BIN="${PS_BIN:-$(command -v ps)}"
CODEX_EXECUTABLE=""

AGENT_NAME="${1:?agent name}"
AGENT_KIND="${2:?agent kind}"
PANE_ID="${3:?pane id}"
shift 3
RUNTIME_ARGS=("$@")

hcmd() {
  "$HERDR_BIN" --session "$SESSION_NAME" "$@"
}

if [ "$AGENT_KIND" = "codex" ]; then
  CODEX_EXECUTABLE="${CODEX_BIN:-$(command -v codex || true)}"
  if [ -z "$CODEX_EXECUTABLE" ] || [ ! -x "$CODEX_EXECUTABLE" ]; then
    echo "agent start failed codex executable not found: ${CODEX_EXECUTABLE:-<empty>}" >&2
    exit 4
  fi
  python3 - "$CODEX_EXECUTABLE" <<'PY'
import subprocess
import sys

try:
    probe = subprocess.run(
        [sys.argv[1], "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=5,
        check=False,
    )
except subprocess.TimeoutExpired:
    print(f"codex binary preflight timed out: {sys.argv[1]}", file=sys.stderr)
    raise SystemExit(4)
if probe.returncode != 0:
    print(f"codex binary preflight failed: {sys.argv[1]} · exit={probe.returncode}", file=sys.stderr)
    print(probe.stdout, file=sys.stderr, end="")
    raise SystemExit(4)
PY

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
path_setup=""
if [ "$AGENT_KIND" = "codex" ]; then
  codex_dir="$(cd "$(dirname "$CODEX_EXECUTABLE")" && pwd -P)"
  printf -v codex_dir_q '%q' "$codex_dir"
  path_setup="export PATH=$codex_dir_q:\$PATH; "
fi
hcmd pane run "$PANE_ID" \
  "${path_setup}unset NO_COLOR CODEX_CI CODEX_INTERNAL_ORIGINATOR_OVERRIDE CODEX_PERMISSION_PROFILE CODEX_THREAD_ID; export TERM=xterm-256color COLORTERM=truecolor; printf '__DUET_ENV_READY__\\n'"
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
