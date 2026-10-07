#!/usr/bin/env bash

# 用途：执行一个正式 Web Flow。参数：<flow.yaml> [env-file]。
# 输出：JUnit 与 pytest 日志；失败非 0。限制：需要虚拟环境依赖、浏览器和可用 Web。

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
exec bash "$ROOT_DIR/scripts/lib/run-single-pytest-flow.sh" web "${1:-}" "${2:-$ROOT_DIR/env/web.env.example}"
