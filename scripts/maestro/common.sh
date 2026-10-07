#!/usr/bin/env bash

# 用途：为 Maestro 执行脚本提供路径、平台、环境变量、报告目录和命令参数的公共函数。
# 本文件由其他脚本 source，不直接执行；不得在日志中输出环境变量值。

set -euo pipefail

MAESTRO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MAESTRO_CONFIG="$MAESTRO_ROOT/.maestro/config.yaml"

maestro_die() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

maestro_validate_platform() {
  case "${1:-}" in
    android|ios) ;;
    *) maestro_die 'platform must be android or ios' ;;
  esac
}

maestro_validate_format() {
  case "${1:-}" in
    JUNIT|HTML) ;;
    *) maestro_die 'report format must be JUNIT or HTML' ;;
  esac
}

maestro_default_env_file() {
  printf '%s/env/%s.env\n' "$MAESTRO_ROOT" "$1"
}

maestro_load_environment() {
  local platform="$1"
  local env_file="$2"

  [ -f "$env_file" ] || maestro_die "environment file not found: $env_file"

  # 环境文件属于受信任的本地/CI 配置；加载时自动导出变量供 Maestro 使用。
  set -a
  # shellcheck disable=SC1090
  source "$env_file"
  set +a

  local required=(APP_ID MAESTRO_DEVICE TEST_ADMIN_PASSWORD TEST_MEMBER_PASSWORD TEST_DISABLED_PASSWORD)
  local key
  for key in "${required[@]}"; do [ -n "${!key:-}" ] || maestro_die "required variable is empty: $key"; done
}

maestro_resolve_binary() {
  MAESTRO_BIN="${MAESTRO_BIN:-maestro}"
  command -v "$MAESTRO_BIN" >/dev/null 2>&1 || maestro_die "Maestro CLI not found: $MAESTRO_BIN"
}

maestro_prepare_artifacts() {
  local platform="$1"
  local scope="$2"
  local format="$3"
  local extension

  MAESTRO_RUN_ID="${MAESTRO_RUN_ID:-$(date '+%Y%m%d-%H%M%S')-$$}"
  MAESTRO_ARTIFACT_ROOT="${MAESTRO_ARTIFACT_ROOT:-$MAESTRO_ROOT/artifacts/maestro}"
  MAESTRO_RUN_DIR="$MAESTRO_ARTIFACT_ROOT/$platform/$MAESTRO_RUN_ID/$scope"
  MAESTRO_DEBUG_DIR="$MAESTRO_RUN_DIR/debug"
  MAESTRO_TEST_OUTPUT_DIR="$MAESTRO_RUN_DIR/tests"
  extension=xml
  [ "$format" = HTML ] && extension=html
  MAESTRO_REPORT_FILE="$MAESTRO_RUN_DIR/report.$extension"
  mkdir -p "$MAESTRO_DEBUG_DIR" "$MAESTRO_TEST_OUTPUT_DIR"
}

maestro_build_env_args() {
  local keys=(
    APP_ID TEST_ADMIN_PASSWORD TEST_MEMBER_PASSWORD TEST_DISABLED_PASSWORD
  )
  local key

  MAESTRO_ENV_ARGS=()
  for key in "${keys[@]}"; do
    if [ -n "${!key:-}" ]; then
      MAESTRO_ENV_ARGS+=("-e" "${key}=${!key}")
    fi
  done
}

maestro_resolve_python() {
  if [ -n "${PYTHON_BIN:-}" ]; then
    command -v "$PYTHON_BIN" >/dev/null 2>&1 || maestro_die "Python not found: $PYTHON_BIN"
    return
  fi
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN=python
  else
    maestro_die "Python not found (python3 or python). Set PYTHON_BIN."
  fi
}

maestro_native_path() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$1"
  else
    printf '%s' "$1"
  fi
}

# 用途：由 Shell 入口调用 python_runner，执行 Flow 并写入 artifacts 汇总报告。
# 位置参数：<android|ios> <env-file> <JUNIT|HTML> [传给 python 的筛选参数...]
maestro_invoke_python() {
  local platform="$1"
  local env_file="$2"
  local format="$3"
  shift 3

  maestro_resolve_python
  local py_args=(
    "$MAESTRO_ROOT/python_runner/main.py"
    run
    --workspace "$(maestro_native_path "$MAESTRO_ROOT")"
    --platform "$platform"
    --env-file "$(maestro_native_path "$env_file")"
    --device "$MAESTRO_DEVICE"
    --maestro-bin "$(maestro_native_path "$MAESTRO_BIN")"
    --maestro-config "$(maestro_native_path "$MAESTRO_CONFIG")"
    --format "$format"
    --output "$(maestro_native_path "$MAESTRO_REPORT_FILE")"
    --debug-output "$(maestro_native_path "$MAESTRO_DEBUG_DIR")"
    --test-output-dir "$(maestro_native_path "$MAESTRO_TEST_OUTPUT_DIR")"
    --reports-dir "$(maestro_native_path "$MAESTRO_RUN_DIR")"
    --flat-reports
  )
  if [ "${MAESTRO_SKIP_PRELAUNCH:-}" = 1 ]; then
    py_args+=(--skip-prelaunch)
  fi

  local converted=()
  local prev=""
  local arg
  for arg in "$@"; do
    if [ "$prev" = "--flow" ]; then
      converted+=("$(maestro_native_path "$arg")")
    else
      converted+=("$arg")
    fi
    prev="$arg"
  done
  if [ "${#converted[@]}" -eq 0 ]; then
    "$PYTHON_BIN" "${py_args[@]}"
  else
    "$PYTHON_BIN" "${py_args[@]}" "${converted[@]}"
  fi
}
