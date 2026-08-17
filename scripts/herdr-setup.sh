#!/usr/bin/env bash
# 兼容入口：旧 Claude Code(spec_owner) + Codex(delivery_owner) 组合。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_REPO="${1:?用法: herdr-setup.sh <work-repo> [codex-dir] [label]}"
CODEX_DIR="${2:-$WORK_REPO}"
LABEL="${3:-duet-$(basename "$WORK_REPO")}"

exec "$SCRIPT_DIR/pair-setup.sh" "$WORK_REPO" "$CODEX_DIR" "$LABEL" claude codex
