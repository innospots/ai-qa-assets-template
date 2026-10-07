#!/usr/bin/env bash

# 用途：按预检、Smoke、Regression、Journey 顺序完成一个平台的 Maestro 构建验证。
# 用法：build-and-test.sh <android|ios> [env-file]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
platform="${1:-}"
env_file="${2:-}"

# 同一构建中的各套件共用运行编号，报告按 smoke/regression/e2e 子目录汇总。
MAESTRO_RUN_ID="${MAESTRO_RUN_ID:-$(date '+%Y%m%d-%H%M%S')-$$}"
export MAESTRO_RUN_ID

if [ -n "$env_file" ]; then
  "$SCRIPT_DIR/preflight.sh" "$platform" "$env_file"
  "$SCRIPT_DIR/run-suite.sh" "$platform" smoke "$env_file" JUNIT
  "$SCRIPT_DIR/run-suite.sh" "$platform" regression "$env_file" JUNIT
  "$SCRIPT_DIR/run-suite.sh" "$platform" e2e "$env_file" JUNIT
else
  "$SCRIPT_DIR/preflight.sh" "$platform"
  "$SCRIPT_DIR/run-suite.sh" "$platform" smoke
  "$SCRIPT_DIR/run-suite.sh" "$platform" regression
  "$SCRIPT_DIR/run-suite.sh" "$platform" e2e
fi

printf 'Maestro build and test passed for %s.\n' "$platform"
