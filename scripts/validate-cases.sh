#!/usr/bin/env bash

# 用途：校验 cases/ 中的 Case 是否符合基础规范，并检查 Case ID 与 Flow 文件的对应关系。
# 默认校验仓库内的 cases/ 和 flows/；测试或 CI 可通过 CASE_DIR、FLOW_DIR 覆盖目录。
# 校验失败时会列出全部已发现的问题，最终以非 0 状态退出。
# 限制：仅做结构与 TC↔Flow 映射校验；DS 意图、断言等价性需由 test:review 审查。

set -euo pipefail

# 统一从脚本位置计算仓库根目录，确保在任意工作目录调用都有效。
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CASE_DIR="${CASE_DIR:-$ROOT_DIR/cases}"
FLOW_DIR="${FLOW_DIR:-$ROOT_DIR/flows}"
FAILED=0
ID_PATTERN='TC-[A-Z0-9]+-[A-Z0-9-]+-[0-9]{3}'

# 记录错误但不中断当前文件检查，以便一次返回尽可能完整的问题清单。
fail() {
  printf 'ERROR: %s\n' "$1"
  FAILED=1
}

while IFS= read -r file; do
  printf 'Checking: %s\n' "$file"
  # Front Matter 必须位于文件头部，并包含两个 --- 分隔符。
  front_matter="$(sed -n '1,/^---$/p' "$file")"

  if [ "$(printf '%s\n' "$front_matter" | grep -c '^---$')" -lt 2 ]; then
    fail "missing YAML front matter: $file"
  fi
  for key in id name module priority tags platform; do
    if ! printf '%s\n' "$front_matter" | grep -q "^${key}:"; then
      fail "missing ${key}: $file"
    fi
  done
  for section in '## 正向测试' '## 反向测试'; do
    if ! grep -Fq "$section" "$file"; then
      fail "missing section ${section}: $file"
    fi
  done

  # 根据 Case 的相对路径推导约定的 Flow 目录：flows/{domain}/{feature}/。
  relative="${file#"$CASE_DIR"/}"
  domain="${relative%%/*}"
  feature="$(basename "$file" .case.md)"
  while IFS= read -r id; do
    if ! [ -f "$FLOW_DIR/$domain/$feature/$id.yaml" ]; then
      fail "missing Flow for ${id}: $file"
    fi
  done < <(grep -E '^### '"$ID_PATTERN" "$file" | grep -Eo "$ID_PATTERN" | sort -u)
done < <(find "$CASE_DIR" -type f -name '*.case.md' | sort)

# 正式 Flow 也必须能回溯到同路径下的 Case 标题，避免孤立执行实现。
if [ -d "$FLOW_DIR" ]; then
  while IFS= read -r flow; do
    relative="${flow#"$FLOW_DIR"/}"
    domain="${relative%%/*}"
    remainder="${relative#*/}"
    feature="${remainder%%/*}"
    id="$(basename "$flow" .yaml)"
    case_file="$CASE_DIR/$domain/$feature.case.md"
    if ! [ -f "$case_file" ] || ! grep -Eq "^### ${id}([[:space:]]|$)" "$case_file"; then
      fail "orphan Flow without matching Case: $flow"
    fi
  done < <(find "$FLOW_DIR" -type f -name 'TC-*.yaml' | sort)
fi

# 跨全部 Case 检查重复 ID（仅统计 ### 标题中的 TC，忽略清单表等引用）
duplicate_ids="$(grep -Erh '^### '"$ID_PATTERN" "$CASE_DIR" --include='*.case.md' | grep -Eo "$ID_PATTERN" | sort | uniq -d || true)"
if [ -n "$duplicate_ids" ]; then
  while IFS= read -r id; do
    fail "duplicate Case ID: $id"
  done <<< "$duplicate_ids"
fi

# 捕获 ### 标题中以 TC- 开头但不符合编号规范的字符串
invalid_ids="$(grep -Erh '^### TC-[^[:space:]]+' "$CASE_DIR" --include='*.case.md' | grep -Eo 'TC-[^[:space:]]+' | grep -Ev "^${ID_PATTERN}$" || true)"
if [ -n "$invalid_ids" ]; then
  while IFS= read -r id; do
    fail "invalid Case ID: $id"
  done <<< "$invalid_ids"
fi

if [ "$FAILED" -ne 0 ]; then
  printf 'Case validation failed.\n'
  exit 1
fi

printf 'Case validation passed.\n'
