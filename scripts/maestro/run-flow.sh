#!/usr/bin/env bash

# 用途：在指定 Android/iOS 设备上执行一个 Flow。Shell 负责环境与产物目录，Python 负责执行与汇总报告。
# 用法：run-flow.sh <android|ios> <flow-file> [env-file] [JUNIT|HTML]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

platform="${1:-}"
flow_file="${2:-}"
maestro_validate_platform "$platform"
[ -n "$flow_file" ] || maestro_die 'flow file is required'

if [[ "$flow_file" != /* ]]; then
  flow_file="$MAESTRO_ROOT/$flow_file"
fi
[ -f "$flow_file" ] || maestro_die "Flow not found: $flow_file"

env_file="${3:-$(maestro_default_env_file "$platform")}"
format="${4:-JUNIT}"
maestro_validate_format "$format"
maestro_load_environment "$platform" "$env_file"
maestro_resolve_binary
maestro_prepare_artifacts "$platform" "$(basename "$flow_file" .yaml)" "$format"

printf 'Run Maestro flow via python_runner: %s (%s)\n' "$flow_file" "$platform"
maestro_invoke_python "$platform" "$env_file" "$format" --flow "$flow_file"
printf 'Report: %s\n' "$MAESTRO_RUN_DIR/summary.json"
printf 'Maestro report: %s\n' "$MAESTRO_REPORT_FILE"
