---
name: test-openapi-import
description: 从本地 OpenAPI 3.0/3.1 YAML 或 JSON 导入指定 API 接口，创建待审查的 TDS、Case、Flow、data、契约快照和 pytest 骨架。
metadata:
  namespaced-name: "test:openapi-import"
---

# test:openapi-import

## 1. Purpose

把接口契约转为**待审查草稿包**，帮助产品工程启动 API 测试资产链路。

## 2. Scope

支持本地 OpenAPI 3.0/3.1 YAML/JSON、按 `METHOD /path` 选择接口或显式 `--all`。不推断业务规则、不解析远程 `$ref`、不直接写正式资产。

## 3. When to Use

用户提供 OpenAPI/Swagger 规范，希望创建 API 测试用例、流程与相关资源时使用。

## 4. Inputs

本地规范文件、业务域 slug、接口选择键、可选草稿输出目录；业务需求或验收标准用于后续审核。

## 5. Outputs

每接口一份 `generated/openapi-drafts/{domain}/{operation-slug}/`，含 TDS Index/场景、Case、API Flow 清单、data、env 模板、pytest 骨架与契约快照。

## 6. Workflow

1. 读 [导入规范](references/import-contract.md)，先 `--list` 确认接口。
2. 用 `--operation 'GET /path'` 导入；批量导入须显式 `--all`。
3. 对照需求审查草稿，完成 TDS、Case 和执行断言。
4. 按 `test:design` → `test:case` → `test:flow` 写入正式目录，执行 `test:review` 与结构校验。

## 7. Rules

- `operationId` 只作辅助信息；`METHOD /path` 是选择键。
- 草稿中的待确认结果不得视为业务预期；pytest 骨架保持跳过状态。
- 已有草稿不覆盖。不得把真实 Token、生产数据写入 data 或 env 模板。
- `$ref` 与 security scheme 仅随契约快照保留，使用前人工确认。

## 8. Quality Criteria

- 来源、接口选择键、待确认项明确；草稿资产间的 DS/TC/Flow 名称可追溯。
- 审核进入正式目录后运行 `./scripts/validate-cases.sh`、单 Flow 与受影响套件。

## 9. References

[导入规范与边界](references/import-contract.md)；[仓库资产模型](../../docs/test-asset-guide.md)。

## 10. Templates

草稿骨架由确定性脚本输出，无独立模板文件。

## 11. Scripts

`python3 scripts/openapi/import.py --spec <file> --list`；创建时加入 `--domain <slug> --operation 'METHOD /path'`。

## 12. Examples

[Catalog API 示例](examples/README.md) 含本地规范、命令与审核清单。
