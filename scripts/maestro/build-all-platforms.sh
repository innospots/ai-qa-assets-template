#!/usr/bin/env bash

# 用途：依次执行 Android 和 iOS 的完整 Maestro 构建验证，并保留两个平台的独立结果。
# 用法：build-all-platforms.sh [android-env-file] [ios-env-file]
# 任一平台失败时仍继续执行另一平台，最终返回第一个失败状态。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
android_env="${1:-}"
ios_env="${2:-}"
overall_status=0

# 两个平台共用构建编号，但报告按 platform/scope 分目录，不会相互覆盖。
MAESTRO_RUN_ID="${MAESTRO_RUN_ID:-$(date '+%Y%m%d-%H%M%S')-$$}"
export MAESTRO_RUN_ID

if [ -n "$android_env" ]; then
  if ! "$SCRIPT_DIR/build-and-test.sh" android "$android_env"; then
    overall_status=1
  fi
elif ! "$SCRIPT_DIR/build-and-test.sh" android; then
  overall_status=1
fi

if [ -n "$ios_env" ]; then
  if ! "$SCRIPT_DIR/build-and-test.sh" ios "$ios_env"; then
    [ "$overall_status" -ne 0 ] || overall_status=1
  fi
elif ! "$SCRIPT_DIR/build-and-test.sh" ios; then
  [ "$overall_status" -ne 0 ] || overall_status=1
fi

if [ "$overall_status" -ne 0 ]; then
  printf 'Maestro build failed for one or more platforms.\n' >&2
  exit "$overall_status"
fi

printf 'Maestro build and test passed for Android and iOS.\n'
