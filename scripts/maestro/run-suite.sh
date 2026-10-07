#!/usr/bin/env bash

# 用途：按 Tag 执行 Flow/Journey。Shell 负责环境与产物目录，Python 负责逐条执行、预启动与汇总报告。
# 用法：run-suite.sh <android|ios> <smoke|regression|e2e|special|all> [env-file] [JUNIT|HTML]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

platform="${1:-}"
scope="${2:-}"
maestro_validate_platform "$platform"
case "$scope" in
  smoke|regression|e2e|special|all) ;;
  *) maestro_die 'suite must be smoke, regression, e2e, special or all' ;;
esac

env_file="${3:-$(maestro_default_env_file "$platform")}"
format="${4:-JUNIT}"
maestro_validate_format "$format"
maestro_load_environment "$platform" "$env_file"
maestro_resolve_binary
maestro_prepare_artifacts "$platform" "$scope" "$format"

printf 'Run Maestro suite via python_runner: %s (%s)\n' "$scope" "$platform"
if [ "$scope" = all ]; then
  maestro_invoke_python "$platform" "$env_file" "$format"
else
  maestro_invoke_python "$platform" "$env_file" "$format" --tags "$scope"
fi
printf 'Report: %s\n' "$MAESTRO_RUN_DIR/summary.json"
printf 'Maestro report: %s\n' "$MAESTRO_REPORT_FILE"
