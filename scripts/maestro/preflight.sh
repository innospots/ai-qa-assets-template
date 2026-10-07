#!/usr/bin/env bash

# 用途：在连接设备前检查 Case、Shell、平台环境、Maestro CLI 和 Mobile Flow 文件。
# 用法：preflight.sh <android|ios> [env-file]
# 输出：预检通过信息；缺环境、设备工具或 Mobile Flow 时返回非 0。
# 限制：只检查可执行准备条件，不代表真实设备端到端测试通过。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

platform="${1:-}"
maestro_validate_platform "$platform"
env_file="${2:-$(maestro_default_env_file "$platform")}"

"$MAESTRO_ROOT/scripts/validate-cases.sh"
bash -n "$MAESTRO_ROOT"/scripts/*.sh "$MAESTRO_ROOT"/scripts/maestro/*.sh
maestro_load_environment "$platform" "$env_file"
maestro_resolve_binary

[ -f "$MAESTRO_CONFIG" ] || maestro_die "Maestro config not found: $MAESTRO_CONFIG"

mobile_count=0
while IFS= read -r flow; do
  if grep -q '^appId:' "$flow"; then
    grep -q '^---$' "$flow" || maestro_die "invalid Maestro Flow separator: $flow"
    mobile_count=$((mobile_count + 1))
  fi
done < <(find "$MAESTRO_ROOT/flows" -type f -name 'TC-*.yaml' | sort)
[ "$mobile_count" -gt 0 ] || maestro_die "no Mobile Maestro flows under flows/"

"$MAESTRO_BIN" --version >/dev/null
printf 'Maestro preflight passed for %s.\n' "$platform"
