#!/usr/bin/env bash

# 用途：使用临时 Maestro 替身验证执行脚本的参数、环境加载和失败状态传播。
# TODO: [待完善] 增加真实 data 脚本加载顺序、output 层级引用和敏感变量不泄露的契约断言。
# TODO: [待完善] 在具备 Android/iOS 设备的 CI 任务中补充真实 Maestro Smoke 验证。

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
TEST_DIR="$(mktemp -d)"
trap 'rm -rf "$TEST_DIR"' EXIT

FAKE_BIN="$TEST_DIR/maestro"
FAKE_LOG="$TEST_DIR/maestro-args.log"
FAKE_CALLS="$TEST_DIR/maestro-calls.log"
TEST_ENV="$TEST_DIR/android.env"
TEST_IOS_ENV="$TEST_DIR/ios.env"

printf '%s\n' \
  '#!/usr/bin/env bash' \
  'printf "%s\n" "$@" > "$FAKE_MAESTRO_LOG"' \
  'printf "CALL" >> "$FAKE_MAESTRO_CALLS"' \
  'printf "\t%s" "$@" >> "$FAKE_MAESTRO_CALLS"' \
  'printf "\n" >> "$FAKE_MAESTRO_CALLS"' \
  'for arg in "$@"; do' \
  '  if [ "$arg" = "--device=${FAKE_MAESTRO_FAIL_DEVICE:-__none__}" ]; then exit "${FAKE_MAESTRO_FAIL_STATUS:-9}"; fi' \
  'done' \
  'for arg in "$@"; do' \
  '  if [ "$arg" = "test" ]; then exit "${FAKE_MAESTRO_EXIT:-0}"; fi' \
  'done' \
  'exit 0' > "$FAKE_BIN"
chmod +x "$FAKE_BIN"

printf '%s\n' \
  'APP_ID=com.example.android' \
  'MAESTRO_DEVICE=emulator-5554' \
  'TEST_ADMIN_PASSWORD=test-password' \
  'TEST_MEMBER_PASSWORD=wrong-password' \
  'TEST_DISABLED_PASSWORD=disabled-password' > "$TEST_ENV"

printf '%s\n' \
  'APP_ID=com.example.ios' \
  'MAESTRO_DEVICE=ios-simulator-udid' \
  'TEST_ADMIN_PASSWORD=test-password' \
  'TEST_MEMBER_PASSWORD=wrong-password' \
  'TEST_DISABLED_PASSWORD=disabled-password' > "$TEST_IOS_ENV"

export MAESTRO_BIN="$FAKE_BIN"
export FAKE_MAESTRO_LOG="$FAKE_LOG"
export FAKE_MAESTRO_CALLS="$FAKE_CALLS"
export MAESTRO_ARTIFACT_ROOT="$TEST_DIR/artifacts"
# 契约测试使用假 Maestro，不连真机、不跑 adb 预启动。
export MAESTRO_SKIP_PRELAUNCH=1
if command -v cygpath >/dev/null 2>&1; then
  export MAESTRO_BIN_WRAPPER="$(cygpath -w "$(command -v bash)")"
fi

fail_test() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_log_contains() {
  grep -Fqx -- "$1" "$FAKE_LOG" || fail_test "missing Maestro argument: $1"
}

if "$ROOT_DIR/scripts/maestro/run-flow.sh" unsupported "$ROOT_DIR/flows/mobile/demo/TC-MOBILE-DEMO-001.yaml" "$TEST_ENV" >/dev/null 2>&1; then
  fail_test 'unsupported platform should fail'
fi

if "$ROOT_DIR/scripts/maestro/run-flow.sh" android "$ROOT_DIR/flows/mobile/demo/TC-MOBILE-DEMO-001.yaml" "$TEST_DIR/missing.env" >/dev/null 2>&1; then
  fail_test 'missing environment file should fail'
fi

"$ROOT_DIR/scripts/maestro/run-flow.sh" android "$ROOT_DIR/flows/mobile/demo/TC-MOBILE-DEMO-001.yaml" "$TEST_ENV" JUNIT
assert_log_contains '--device=emulator-5554'
assert_log_contains 'test'
assert_log_contains '--format=JUNIT'
assert_log_contains '-e'
assert_log_contains 'APP_ID=com.example.android'
grep -Fq 'TC-MOBILE-DEMO-001.yaml' "$FAKE_LOG" || fail_test 'missing flow file in Maestro args'
grep -Fq -- '--config=' "$FAKE_LOG" || fail_test 'missing --config'

"$ROOT_DIR/scripts/maestro/run-suite.sh" android smoke "$TEST_ENV" HTML
assert_log_contains '--format=HTML'
grep -Fq -- '--device=emulator-5554' "$FAKE_LOG" || fail_test 'suite should pass Android device'

"$ROOT_DIR/scripts/maestro/run-suite.sh" ios smoke "$TEST_IOS_ENV" JUNIT
assert_log_contains '--device=ios-simulator-udid'
assert_log_contains 'APP_ID=com.example.ios'

unset TEST_RUNNER
MAESTRO_PLATFORM=android MAESTRO_ENV_FILE="$TEST_ENV" "$ROOT_DIR/scripts/run-smoke-mobile.sh"
assert_log_contains '--device=emulator-5554'
MAESTRO_PLATFORM=android MAESTRO_ENV_FILE="$TEST_ENV" "$ROOT_DIR/scripts/run-regression.sh"
assert_log_contains '--device=emulator-5554'
MAESTRO_PLATFORM=android MAESTRO_ENV_FILE="$TEST_ENV" "$ROOT_DIR/scripts/run-all.sh"
grep -Ei 'flows[/\\]|journeys[/\\]' "$FAKE_LOG" >/dev/null || fail_test 'all suite should run a Flow or Journey'

unset MAESTRO_RUN_ID
: > "$FAKE_CALLS"
"$ROOT_DIR/scripts/maestro/build-and-test.sh" android "$TEST_ENV"
run_id_count="$(tr '\\' '/' < "$FAKE_CALLS" | tr '\t' '\n' | grep '^--output=' | sed -E 's#.*artifacts/android/([^/]+)/.*#\1#' | sort -u | wc -l | tr -d ' ')"
[ "$run_id_count" -eq 1 ] || fail_test "expected one build run id, got $run_id_count"

unset MAESTRO_RUN_ID
: > "$FAKE_CALLS"
"$ROOT_DIR/scripts/maestro/build-all-platforms.sh" "$TEST_ENV" "$TEST_IOS_ENV"
grep -Fq -- '--device=emulator-5554' "$FAKE_CALLS" || fail_test 'dual-platform build did not run Android'
grep -Fq -- '--device=ios-simulator-udid' "$FAKE_CALLS" || fail_test 'dual-platform build did not run iOS'

export FAKE_MAESTRO_FAIL_DEVICE=emulator-5554
: > "$FAKE_CALLS"
if "$ROOT_DIR/scripts/maestro/build-all-platforms.sh" "$TEST_ENV" "$TEST_IOS_ENV" >/dev/null 2>&1; then
  fail_test 'dual-platform build should fail when Android fails'
fi
grep -Fq -- '--device=ios-simulator-udid' "$FAKE_CALLS" || fail_test 'iOS should still run after Android failure'
unset FAKE_MAESTRO_FAIL_DEVICE

export FAKE_MAESTRO_EXIT=7
if "$ROOT_DIR/scripts/maestro/run-suite.sh" android regression "$TEST_ENV" JUNIT >/dev/null 2>&1; then
  fail_test 'Maestro failure should propagate'
else
  status=$?
  [ "$status" -eq 7 ] || fail_test "expected status 7, got $status"
fi

printf 'Maestro script contract tests passed.\n'
