---
name: test-flow
description: 从已确认 Case 创建或修改 API、Web、Mobile Flow；一条 TC 对应一个 Flow，执行实现不改变业务预期。
metadata:
  namespaced-name: "test:flow"
---

# test:flow

## 1. Purpose

把已确认 Case 中的步骤与预期落实为可独立执行的 Flow，并保持 DS → TC → Flow 追溯。

## 2. Scope

API/Web：创建指向 pytest 节点的 Flow 清单及相应 `executors/` 实现。Mobile：创建 Maestro YAML，按需复用 Module 与 selector data。不负责新增业务测试意图。

## 3. When to Use

已有 Case 需要自动化、接口或页面实现变化需要调整执行层、Mobile 选择器变化时使用。OpenAPI 草稿须先经 TDS/Case 审核。

## 4. Inputs

已确认 Case ID、对应 TDS、现有 Flow/Module/data、目标平台和可用测试环境。

## 5. Outputs

`flows/{domain}/{scene}/{case-id}.yaml`；按需更新 `executors/api/`、`executors/web/`、`modules/` 与 `data/`；交付追溯和验证结果。

## 6. Workflow

1. 读 [仓库 Flow 约定](references/repo-conventions.md) 与 [工作流](references/workflow.md)。
2. 逐条映射 Case 步骤和关键预期；先查现有共享资产及全部引用者。
3. 按平台实现：[API](examples/api-flow.md)、[Web](examples/web-flow.md)、[Mobile](examples/mobile-flow.md)。
4. 执行结构校验、单 Flow 和受影响范围；不能运行时记录准确原因。

## 7. Rules

- 一 TC 一正式 Flow，文件名等于 Case ID；不改变 Case 业务预期。
- API/Web 清单必须有 `executor`、`name`、`tags`、`test`；断言写在 pytest 节点。
- Mobile YAML 由 Maestro 执行；关键预期必须有等价断言。
- 业务数据在 `data/`，环境地址和敏感值在 env/CI；不写真实凭据。
- 修改共享 Module/data 前搜索全部引用者。

## 8. Quality Criteria

Case 与 Flow 一一对应，节点或 Maestro 断言可判断结果；[审查清单](references/review-checklist.md) 通过；结构与相关执行验证有记录。

## 9. References

[仓库约定](references/repo-conventions.md)、[Flow 结构](references/flow-structure.md)、[Maestro 专项索引](references/README.md)、[仓库标准](../../docs/flow-standard.md)。

## 10. Templates

[Mobile Case Flow](templates/case-flow.yaml)、[Mobile Module](templates/module.yaml)、[Mobile Setup](templates/setup-flow.yaml)；API/Web 参照正式清单及对应执行器测试。

## 11. Scripts

`./scripts/validate-cases.sh` 检查 Case↔Flow；`python3 skills/test-flow/scripts/validate-flow.py <flow>` 按平台检查；`check-references.py` 用于 Mobile 相对引用。

## 12. Examples

[API](examples/api-flow.md)、[Web](examples/web-flow.md)、[Mobile](examples/mobile-flow.md) 使用仓库现有正式资产，路径可直接核对。
