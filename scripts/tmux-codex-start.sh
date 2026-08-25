#!/usr/bin/env bash
# Start or resume Codex in an existing tmux solo seat.
# Usage: tmux-codex-start.sh <session> <window> <cwd> [codex args...]
set -euo pipefail

SESSION_NAME="${1:?usage: tmux-codex-start.sh <session> <window> <cwd> [codex args...]}"
WINDOW_NAME="${2:?window name}"
EXPECTED_CWD="${3:?cwd}"
shift 3
CODEX_ARGS=("$@")
TARGET="$SESSION_NAME:$WINDOW_NAME.0"

command -v tmux >/dev/null || {
  echo "tmux not found" >&2
  exit 4
}

tmux has-session -t "=$SESSION_NAME" 2>/dev/null || {
  echo "tmux session not found: $SESSION_NAME" >&2
  exit 4
}

pane_cwd="$(tmux display-message -p -t "$TARGET" '#{pane_current_path}')"
pane_cwd="$(cd "$pane_cwd" && pwd -P)"
expected_real="$(cd "$EXPECTED_CWD" && pwd -P)"
if [ "$pane_cwd" != "$expected_real" ]; then
  echo "tmux pane cwd mismatch: $TARGET · expected=$expected_real actual=$pane_cwd" >&2
  exit 4
fi

pane_command="$(tmux display-message -p -t "$TARGET" '#{pane_current_command}')"
case "$pane_command" in
  zsh|bash|fish|sh) ;;
  *)
    echo "tmux pane is not at a shell prompt: $TARGET · command=$pane_command" >&2
    exit 4
    ;;
esac

CODEX_EXECUTABLE="${CODEX_BIN:-$(command -v codex || true)}"
if [ -z "$CODEX_EXECUTABLE" ] || [ ! -x "$CODEX_EXECUTABLE" ]; then
  echo "codex executable not found: ${CODEX_EXECUTABLE:-<empty>}" >&2
  exit 4
fi
command -v python3 >/dev/null || {
  echo "python3 not found for codex binary preflight" >&2
  exit 4
}
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

has_explicit_cwd=false
for ((i = 0; i < ${#CODEX_ARGS[@]}; i++)); do
  case "${CODEX_ARGS[$i]}" in
    -C|--cd)
      has_explicit_cwd=true
      explicit_cwd="${CODEX_ARGS[$((i + 1))]:-}"
      if [ "$explicit_cwd" != "$expected_real" ]; then
        echo "codex cwd mismatch: pane=$expected_real runtime=$explicit_cwd" >&2
        exit 4
      fi
      ;;
    --cd=*)
      has_explicit_cwd=true
      explicit_cwd="${CODEX_ARGS[$i]#--cd=}"
      if [ "$explicit_cwd" != "$expected_real" ]; then
        echo "codex cwd mismatch: pane=$expected_real runtime=$explicit_cwd" >&2
        exit 4
      fi
      ;;
  esac
done
if [ "$has_explicit_cwd" = false ]; then
  CODEX_ARGS+=(--cd "$expected_real")
fi

command_parts=(env -u NO_COLOR -u CODEX_CI -u CODEX_INTERNAL_ORIGINATOR_OVERRIDE
  -u CODEX_PERMISSION_PROFILE -u CODEX_THREAD_ID COLORTERM=truecolor
  "$CODEX_EXECUTABLE" "${CODEX_ARGS[@]}")
printf -v command_text '%q ' "${command_parts[@]}"
command_text="exec ${command_text% }"

tmux send-keys -t "$TARGET" C-u
tmux send-keys -l -t "$TARGET" "$command_text"
tmux send-keys -t "$TARGET" Enter

for _ in {1..60}; do
  pane_command="$(tmux display-message -p -t "$TARGET" '#{pane_current_command}')"
  if [ "$pane_command" = codex ]; then
    printf 'codex process ready: %s · cwd=%s · bin=%s\n' "$TARGET" "$expected_real" "$CODEX_EXECUTABLE"
    exit 0
  fi
  sleep 0.25
done

echo "codex process did not become visible in tmux: $TARGET · command=$pane_command" >&2
exit 4
