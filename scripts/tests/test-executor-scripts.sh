#!/usr/bin/env bash

# 用途：离线检查 API/Web Flow 发现脚本与 Smoke 入口的命令结构。
# 参数：无。输出：通过信息；任一发现或语法检查失败时返回非 0。
# 限制：不连接真实 API/Web，也不验证业务断言。

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

python3 "$ROOT_DIR/scripts/lib/discover_flow_tests.py" api smoke --root "$ROOT_DIR" | grep -q 'test_tc_api_health_001'
python3 "$ROOT_DIR/scripts/lib/discover_flow_tests.py" web smoke --root "$ROOT_DIR" | grep -q 'test_tc_web_home_001'

bash -n "$ROOT_DIR/scripts/api/run-suite.sh"
bash -n "$ROOT_DIR/scripts/web/run-suite.sh"
bash -n "$ROOT_DIR/scripts/run-smoke.sh"
bash -n "$ROOT_DIR/scripts/run-smoke-mobile.sh"

printf 'Executor script checks passed.\n'
