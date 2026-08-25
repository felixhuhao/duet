#!/usr/bin/env bash
# Open one canonical window plus owner-prepared worktree windows in a tmux session.
# Usage: tmux-solo-setup.sh <session> <canonical-path> [seat=/absolute/worktree ...]
set -euo pipefail

SESSION_NAME="${1:?usage: tmux-solo-setup.sh <session> <canonical-path> [seat=worktree ...]}"
CANONICAL_PATH="${2:?canonical path}"
shift 2

command -v tmux >/dev/null || {
  echo "tmux not found" >&2
  exit 4
}

canonical_real="$(cd "$CANONICAL_PATH" && pwd -P)"
git -C "$canonical_real" rev-parse --show-toplevel >/dev/null
canonical_common_raw="$(git -C "$canonical_real" rev-parse --git-common-dir)"
canonical_common="$(cd "$canonical_real" && cd "$canonical_common_raw" && pwd -P)"

window_path() {
  tmux display-message -p -t "$1" '#{pane_current_path}'
}

assert_window_path() {
  local target="$1"
  local expected="$2"
  local actual
  actual="$(window_path "$target")"
  actual="$(cd "$actual" && pwd -P)"
  if [ "$actual" != "$expected" ]; then
    echo "tmux window cwd mismatch: $target · expected=$expected actual=$actual" >&2
    exit 4
  fi
}

if ! tmux has-session -t "=$SESSION_NAME" 2>/dev/null; then
  tmux new-session -d -s "$SESSION_NAME" -n main -c "$canonical_real"
fi

if tmux list-windows -t "=$SESSION_NAME" -F '#{window_name}' | grep -Fxq main; then
  assert_window_path "$SESSION_NAME:main.0" "$canonical_real"
else
  tmux new-window -d -t "=$SESSION_NAME" -n main -c "$canonical_real"
fi

for seat_spec in "$@"; do
  case "$seat_spec" in
    *=*) ;;
    *)
      echo "invalid seat spec: $seat_spec (expected name=/absolute/path)" >&2
      exit 4
      ;;
  esac
  seat_name="${seat_spec%%=*}"
  seat_path="${seat_spec#*=}"
  case "$seat_name" in
    ''|*[!a-zA-Z0-9_-]*)
      echo "invalid tmux window name: $seat_name" >&2
      exit 4
      ;;
  esac
  seat_real="$(cd "$seat_path" && pwd -P)"
  seat_root="$(git -C "$seat_real" rev-parse --show-toplevel)"
  if [ "$seat_root" != "$seat_real" ]; then
    echo "seat path is not a worktree root: $seat_real" >&2
    exit 4
  fi
  seat_common_raw="$(git -C "$seat_real" rev-parse --git-common-dir)"
  seat_common="$(cd "$seat_real" && cd "$seat_common_raw" && pwd -P)"
  if [ "$seat_common" != "$canonical_common" ]; then
    echo "seat does not belong to canonical repository: $seat_real" >&2
    exit 4
  fi

  if tmux list-windows -t "=$SESSION_NAME" -F '#{window_name}' | grep -Fxq "$seat_name"; then
    assert_window_path "$SESSION_NAME:$seat_name.0" "$seat_real"
  else
    tmux new-window -d -t "=$SESSION_NAME" -n "$seat_name" -c "$seat_real"
  fi
done

tmux list-windows -t "=$SESSION_NAME" -F '#{window_name} · #{pane_current_command} · #{pane_current_path}'
echo "attach: tmux attach -t $SESSION_NAME"
