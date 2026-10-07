#!/usr/bin/env bash

# 用途：加载 API 环境并执行带指定 Tag 的 pytest 节点（从所有业务域的 API Flow 清单发现）。
# 用法：run-suite.sh <smoke|regression|e2e|special|all> [env-file]
# 输出：artifacts/api/ 下的 JUnit 与日志；发现失败或测试失败返回非 0。
# 限制：按 Flow 的 executor: api 跨业务域发现；需要已安装 pytest/httpx/PyYAML 与可用目标环境。

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SCOPE="${1:-}"
ENV_FILE="${2:-$ROOT_DIR/env/api.env.example}"

case "$SCOPE" in
  smoke|regression|e2e|special|all) ;;
  *) printf 'suite must be smoke, regression, e2e, special or all\n' >&2; exit 1 ;;
esac

if [ ! -f "$ENV_FILE" ]; then
  printf 'env file not found: %s\n' "$ENV_FILE" >&2
  exit 1
fi
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

RUN_ID="$(date '+%Y%m%d-%H%M%S')-$$"
ARTIFACT_DIR="$ROOT_DIR/artifacts/api/$RUN_ID/$SCOPE"
mkdir -p "$ARTIFACT_DIR"

TEST_NODES=()
DISCOVERED="$(python3 "$ROOT_DIR/scripts/lib/discover_flow_tests.py" api "$SCOPE" --root "$ROOT_DIR")"
while IFS= read -r node; do
  TEST_NODES+=("$node")
done <<< "$DISCOVERED"

cd "$ROOT_DIR"
python3 -m pytest "${TEST_NODES[@]}" \
  --junitxml="$ARTIFACT_DIR/junit.xml" \
  | tee "$ARTIFACT_DIR/pytest.log"

printf 'Report: %s/junit.xml\n' "$ARTIFACT_DIR"
