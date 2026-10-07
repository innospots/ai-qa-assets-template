#!/usr/bin/env bash

# 用途：运行移动端 Maestro Smoke；需 MAESTRO_PLATFORM 与 MAESTRO_ENV_FILE。

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

platform="${MAESTRO_PLATFORM:-}"
[ -n "$platform" ] || { printf 'MAESTRO_PLATFORM is not configured.\n' >&2; exit 1; }

if [ -n "${MAESTRO_ENV_FILE:-}" ]; then
  "$ROOT_DIR/scripts/maestro/run-suite.sh" "$platform" smoke "$MAESTRO_ENV_FILE"
else
  "$ROOT_DIR/scripts/maestro/run-suite.sh" "$platform" smoke
fi
