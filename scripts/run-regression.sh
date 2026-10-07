#!/usr/bin/env bash

# 用途：运行带 regression Tag 的回归测试；默认调用仓库内 Maestro 执行层。
# 设置 TEST_RUNNER 可覆盖默认执行器；Maestro 模式使用 MAESTRO_PLATFORM 和 MAESTRO_ENV_FILE。

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT_DIR"
if [ -n "${TEST_RUNNER:-}" ]; then
  # 自定义命令属于受信任的本地或 CI 配置。
  sh -c "$TEST_RUNNER --include-tags regression"
else
  platform="${MAESTRO_PLATFORM:-}"
  [ -n "$platform" ] || { printf 'MAESTRO_PLATFORM is not configured.\n' >&2; exit 1; }
  if [ -n "${MAESTRO_ENV_FILE:-}" ]; then
    "$ROOT_DIR/scripts/maestro/run-suite.sh" "$platform" regression "$MAESTRO_ENV_FILE"
  else
    "$ROOT_DIR/scripts/maestro/run-suite.sh" "$platform" regression
  fi
fi
