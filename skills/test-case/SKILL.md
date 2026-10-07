---
name: test-case
description: 从 TDS 生成或更新 cases/**/*.case.md；维护 DS→TC 映射与业务数据集，不写执行器 DSL。
metadata:
  namespaced-name: "test:case"
---

# test:case

## 1. Purpose

将 TDS 的 `DS-` 落实为可执行、可判定的 **Case**（`TC-` 步骤与预期），写入 `cases/`。

## 2. Scope

**支持：** 从 TDS 新建/增补 Case；`data/{domain}/*.js` 数据集引用；数组 `records[]` 批量驱动单条 TC。

**不支持：** 编写 Flow/Maestro；修改 TDS 业务意图（除非用户另要求）。

## 3. When to Use

- TDS 已就绪（或用户授权按 draft 落盘）
- 需新增/对齐 `cases/{domain}/{scene}.case.md`
- 需补充 `data/` 数据集

## 4. Inputs

| 输入 | 说明 |
| --- | --- |
| 场景 TDS | `designs/{domain}/{scene}.design.md` |
| 模块 Index | 公共规则 |
| 已有 Case / data | 保留已发布 `TC-` |

## 5. Outputs

- `cases/{domain}/{scene}.case.md`
- `data/{domain}/*.js`（及按需 `fixtures/`）
- 交付：DS→TC 对照、校验结果、缺 Flow 清单

## 6. Workflow

1. T0：DS→TC 映射（见 [workflow.md](references/workflow.md)）
2. T1：编写/增补 data 脚本
3. T2：编写 Case
4. T_review：[review-checklist.md](references/review-checklist.md) + `./scripts/validate-cases.sh`

## 7. Rules

- 一场景一 Case 文件；每条 TC 可追溯 `DS-`
- Case 只引用**数据集名称**，具体值在 `data/`（见 [test-case-spec.md](references/test-case-spec.md) §9）
- 必填 `## 正向测试`、`## 反向测试`
- 专项异常标 `execution: deferred`；不进 smoke/regression
- 不修改 `flows/`（交 `test:flow`）

## 8. Quality Criteria

- [review-checklist.md](references/review-checklist.md) 通过
- `./scripts/validate-cases.sh` 通过；改 data 时 `node --check`

## 9. References

| 文档 | 用途 |
| --- | --- |
| [test-case-spec.md](references/test-case-spec.md) | Case 完整规范 |
| [workflow.md](references/workflow.md) | 从 TDS 落 Case |
| [review-checklist.md](references/review-checklist.md) | 审查清单 |
| [examples/sample-customer-customers.js](examples/sample-customer-customers.js) | data 格式标准参照 |
| [../../docs/data-env-standard.md](../../docs/data-env-standard.md) | data 与 env 边界 |

## 10. Templates

| 模板 | 用途 |
| --- | --- |
| [case.md](templates/case.md) | Case 文件骨架 |

## 11. Scripts

| 脚本 | 用途 |
| --- | --- |
| [`../../scripts/validate-cases.sh`](../../scripts/validate-cases.sh) | Case 结构与 ID 校验 |
| `node --check data/**/*.js` | data 语法检查 |

## 12. Examples

| 示例 | 说明 |
| --- | --- |
| [customer-create-customer.case.md](examples/customer-create-customer.case.md) | 完整 Case（18 TC） |
| [batch-one-case.md](examples/batch-one-case.md) | 数组 `records[]` 单 TC |
| [sample-customer-*.js](examples/) | data 脚本样例 |
