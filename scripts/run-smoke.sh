#!/usr/bin/env bash

# 用途：运行默认 Smoke（API + Web）；不依赖 Maestro。移动端见 run-smoke-mobile.sh。
# 设置 TEST_RUNNER 可覆盖为单一自定义命令。

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ -n "${TEST_RUNNER:-}" ]; then
  sh -c "$TEST_RUNNER --include-tags smoke"
  exit 0
fi

API_ENV="${API_ENV_FILE:-env/api.env.example}"
WEB_ENV="${WEB_ENV_FILE:-env/web.env.example}"

"$ROOT_DIR/scripts/api/run-suite.sh" smoke "$API_ENV"
"$ROOT_DIR/scripts/web/run-suite.sh" smoke "$WEB_ENV"
printf 'Smoke (api + web) passed.\n'
