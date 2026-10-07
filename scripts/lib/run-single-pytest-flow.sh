#!/usr/bin/env bash

# 用途：加载环境并执行一个已登记的 API/Web Flow 所指向的 pytest 节点。
# 参数：<api|web> <flow.yaml> [env-file]；路径相对仓库根目录。
# 输出：artifacts/<executor>/ 下的 JUnit 与日志；解析或测试失败返回非 0。
# 限制：只执行正式 flows/ 资产，依赖 PyYAML、pytest 与目标环境。

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
EXECUTOR="${1:-}"
FLOW="${2:-}"
ENV_FILE="${3:-$ROOT_DIR/env/$EXECUTOR.env.example}"

case "$EXECUTOR" in
  api|web) ;;
  *) printf 'executor must be api or web\n' >&2; exit 1 ;;
esac
if [ -z "$FLOW" ]; then
  printf 'usage: run-single-pytest-flow.sh <api|web> <flow.yaml> [env-file]\n' >&2
  exit 1
fi
if [ ! -f "$ENV_FILE" ]; then
  printf 'env file not found: %s\n' "$ENV_FILE" >&2
  exit 1
fi
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

TEST_NODE="$(python3 "$ROOT_DIR/scripts/lib/resolve_flow_test.py" "$EXECUTOR" "$FLOW" --root "$ROOT_DIR")"
CASE_ID="$(basename "$FLOW" .yaml)"
RUN_ID="$(date '+%Y%m%d-%H%M%S')-$$"
ARTIFACT_DIR="$ROOT_DIR/artifacts/$EXECUTOR/$RUN_ID/$CASE_ID"
mkdir -p "$ARTIFACT_DIR"
cd "$ROOT_DIR"
if [ "$EXECUTOR" = web ]; then
  python3 -m pytest "$TEST_NODE" --browser chromium --junitxml="$ARTIFACT_DIR/junit.xml" | tee "$ARTIFACT_DIR/pytest.log"
else
  python3 -m pytest "$TEST_NODE" --junitxml="$ARTIFACT_DIR/junit.xml" | tee "$ARTIFACT_DIR/pytest.log"
fi
printf 'Report: %s/junit.xml\n' "$ARTIFACT_DIR"
