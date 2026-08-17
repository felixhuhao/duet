#!/usr/bin/env bash
# 建一个职责与 runtime 解耦的 herdr pair。
# 用法: pair-setup.sh <spec-dir> [delivery-dir] [label] [spec-kind] [delivery-kind]
# 默认: <session>-spec=codex/spec_owner, <session>-delivery=opencode/delivery_owner。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

SPEC_DIR="${1:?用法: pair-setup.sh <spec-dir> [delivery-dir] [label] [spec-kind] [delivery-kind]}"
DELIVERY_DIR="${2:-$SPEC_DIR}"
LABEL="${3:-pair-$(basename "$SPEC_DIR")}"
SPEC_KIND="${4:-codex}"
DELIVERY_KIND="${5:-opencode}"
SESSION_NAME="${HERDR_SESSION:-default}"
PAIR_KEY="${DUET_PAIR_KEY:-$SESSION_NAME}"
SPEC_NAME="${DUET_SPEC_NAME:-${PAIR_KEY}-spec}"
DELIVERY_NAME="${DUET_DELIVERY_NAME:-${PAIR_KEY}-delivery}"
HERDR_BIN="$(command -v herdr)"

hcmd() {
  "$HERDR_BIN" --session "$SESSION_NAME" "$@"
}

SPEC_DIR="$(cd "$SPEC_DIR" && pwd)"
DELIVERY_DIR="$(cd "$DELIVERY_DIR" && pwd)"

SERVER_STATUS="$(hcmd status server 2>/dev/null || true)"
if ! printf '%s\n' "$SERVER_STATUS" | grep -q "status: running"; then
  nohup env -i HOME="$HOME" PATH="$PATH" SHELL="${SHELL:-/bin/zsh}" \
    USER="$USER" LOGNAME="$USER" TMPDIR="${TMPDIR:-/tmp}" \
    LANG="${LANG:-en_US.UTF-8}" TERM=xterm-256color \
    "$HERDR_BIN" --session "$SESSION_NAME" server >/dev/null 2>&1 &
  sleep 2
fi

GLOBAL_AGENTS="$(python3 "$SCRIPT_DIR/herdr-federation.py" peers --json)"
for candidate in "$SPEC_NAME" "$DELIVERY_NAME"; do
  if printf '%s\n' "$GLOBAL_AGENTS" | python3 -c '
import json,sys
name=sys.argv[1]
sys.exit(0 if any(item["name"] == name for item in json.load(sys.stdin)) else 1)' "$candidate"; then
    echo "全局 agent 名称已存在: ${candidate}；请用 <pair>-<role> 唯一命名" >&2
    exit 1
  fi
done

if hcmd workspace list 2>/dev/null | python3 -c '
import json,sys
label=sys.argv[1]; ws=json.load(sys.stdin)["result"]["workspaces"]
sys.exit(0 if any(w.get("label")==label for w in ws) else 1)' "$LABEL" 2>/dev/null; then
  echo "workspace '$LABEL' 已存在；拒绝重建" >&2
  exit 1
fi

INTEGRATION_STATUS="$(hcmd integration status 2>/dev/null || true)"
for kind in "$SPEC_KIND" "$DELIVERY_KIND"; do
  if ! command -v "$kind" >/dev/null 2>&1; then
    echo "runtime 不在 PATH: $kind" >&2
    exit 1
  fi
  if ! printf '%s\n' "$INTEGRATION_STATUS" | grep -Eq "^${kind}: current"; then
    echo "警告: $kind 的 herdr integration 不是 current；qualification 前先安装/更新" >&2
  fi
done

if [ "$SPEC_KIND" = "codex" ] || [ "$DELIVERY_KIND" = "codex" ]; then
  if ! codex sandbox -P workspace-full -C "$SPEC_DIR" "$HERDR_BIN" \
    --session "$SESSION_NAME" agent list 2>/dev/null | python3 -c '
import json,sys
r=json.load(sys.stdin)
sys.exit(0 if "result" in r and "error" not in r else 1)'; then
    echo "Codex workspace-full 尚未 allow 本 session 的 herdr.sock；先补精确 socket 权限" >&2
    exit 1
  fi
fi

if [ "$SPEC_KIND" = "opencode" ]; then
  CREATE_JSON="$(hcmd workspace create --cwd "$SPEC_DIR" --label "$LABEL" \
    --env OPENCODE_DISABLE_CLAUDE_CODE=1 --no-focus)"
else
  CREATE_JSON="$(hcmd workspace create --cwd "$SPEC_DIR" --label "$LABEL" --no-focus)"
fi
P1="$(printf '%s\n' "$CREATE_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')"
if [ "$DELIVERY_KIND" = "opencode" ]; then
  SPLIT_JSON="$(hcmd pane split "$P1" --direction right --cwd "$DELIVERY_DIR" \
    --env OPENCODE_DISABLE_CLAUDE_CODE=1 --no-focus)"
else
  SPLIT_JSON="$(hcmd pane split "$P1" --direction right --cwd "$DELIVERY_DIR" --no-focus)"
fi
P2="$(printf '%s\n' "$SPLIT_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')"

hcmd agent start "$SPEC_NAME" --kind "$SPEC_KIND" --pane "$P1" --timeout 120000
hcmd agent start "$DELIVERY_NAME" --kind "$DELIVERY_KIND" --pane "$P2" --timeout 120000

SPEC_ROUTE="$(python3 "$SCRIPT_DIR/herdr-federation.py" resolve "$SESSION_NAME/$SPEC_NAME")"
DELIVERY_ROUTE="$(python3 "$SCRIPT_DIR/herdr-federation.py" resolve "$SESSION_NAME/$DELIVERY_NAME")"
SPEC_INSTANCE="$(printf '%s\n' "$SPEC_ROUTE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["instance_id"])')"
DELIVERY_INSTANCE="$(printf '%s\n' "$DELIVERY_ROUTE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["instance_id"])')"

cat <<DONE
workspace: $LABEL
spec_owner:     $SPEC_NAME · $SESSION_NAME · $SPEC_KIND · $SPEC_INSTANCE · $P1 · $SPEC_DIR
delivery_owner: $DELIVERY_NAME · $SESSION_NAME · $DELIVERY_KIND · $DELIVERY_INSTANCE · $P2 · $DELIVERY_DIR
下一步: 分别发送只读冷启动 prompt，并让其回报 instance/棒位；qualification 通过前不得进入产品 batch。
DONE
