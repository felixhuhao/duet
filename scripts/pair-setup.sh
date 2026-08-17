#!/usr/bin/env bash
# 建一个职责与 runtime 解耦的 herdr pair。
# 用法: pair-setup.sh <spec-dir> [delivery-dir] [label] [spec-kind] [delivery-kind]
# 默认: role1=codex/spec_owner, role2=opencode/delivery_owner。
set -euo pipefail

SPEC_DIR="${1:?用法: pair-setup.sh <spec-dir> [delivery-dir] [label] [spec-kind] [delivery-kind]}"
DELIVERY_DIR="${2:-$SPEC_DIR}"
LABEL="${3:-pair-$(basename "$SPEC_DIR")}"
SPEC_KIND="${4:-codex}"
DELIVERY_KIND="${5:-opencode}"
SPEC_NAME="${DUET_SPEC_NAME:-role1}"
DELIVERY_NAME="${DUET_DELIVERY_NAME:-role2}"

SPEC_DIR="$(cd "$SPEC_DIR" && pwd)"
DELIVERY_DIR="$(cd "$DELIVERY_DIR" && pwd)"

SERVER_STATUS="$(herdr status server 2>/dev/null || true)"
if ! printf '%s\n' "$SERVER_STATUS" | grep -q "status: running"; then
  nohup env -i HOME="$HOME" PATH="$PATH" SHELL="${SHELL:-/bin/zsh}" \
    USER="$USER" LOGNAME="$USER" TMPDIR="${TMPDIR:-/tmp}" \
    LANG="${LANG:-en_US.UTF-8}" TERM=xterm-256color \
    herdr server >/dev/null 2>&1 &
  sleep 2
fi

if herdr workspace list 2>/dev/null | python3 -c '
import json,sys
label=sys.argv[1]; ws=json.load(sys.stdin)["result"]["workspaces"]
sys.exit(0 if any(w.get("label")==label for w in ws) else 1)' "$LABEL" 2>/dev/null; then
  echo "workspace '$LABEL' 已存在；拒绝重建" >&2
  exit 1
fi

INTEGRATION_STATUS="$(herdr integration status 2>/dev/null || true)"
for kind in "$SPEC_KIND" "$DELIVERY_KIND"; do
  if ! command -v "$kind" >/dev/null 2>&1; then
    echo "runtime 不在 PATH: $kind" >&2
    exit 1
  fi
  if ! printf '%s\n' "$INTEGRATION_STATUS" | grep -Eq "^${kind}: current"; then
    echo "警告: $kind 的 herdr integration 不是 current；qualification 前先安装/更新" >&2
  fi
done

if [ "$SPEC_KIND" = "opencode" ]; then
  CREATE_JSON="$(herdr workspace create --cwd "$SPEC_DIR" --label "$LABEL" \
    --env OPENCODE_DISABLE_CLAUDE_CODE=1 --no-focus)"
else
  CREATE_JSON="$(herdr workspace create --cwd "$SPEC_DIR" --label "$LABEL" --no-focus)"
fi
P1="$(printf '%s\n' "$CREATE_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')"
if [ "$DELIVERY_KIND" = "opencode" ]; then
  SPLIT_JSON="$(herdr pane split "$P1" --direction right --cwd "$DELIVERY_DIR" \
    --env OPENCODE_DISABLE_CLAUDE_CODE=1 --no-focus)"
else
  SPLIT_JSON="$(herdr pane split "$P1" --direction right --cwd "$DELIVERY_DIR" --no-focus)"
fi
P2="$(printf '%s\n' "$SPLIT_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')"

herdr agent start "$SPEC_NAME" --kind "$SPEC_KIND" --pane "$P1" --timeout 120000
herdr agent start "$DELIVERY_NAME" --kind "$DELIVERY_KIND" --pane "$P2" --timeout 120000

cat <<DONE
workspace: $LABEL
spec_owner:     $SPEC_NAME · $SPEC_KIND · $P1 · $SPEC_DIR
delivery_owner: $DELIVERY_NAME · $DELIVERY_KIND · $P2 · $DELIVERY_DIR
下一步: 分别发送只读冷启动 prompt；qualification 通过前不得进入产品 batch。
DONE
