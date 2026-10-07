# Flow 实现要点（仓库入口）

Case → Flow 的完整规范在本 Skill 的 `references/` 目录。

## 快速入口

| 文档 | 用途 |
| --- | --- |
| [workflow.md](workflow.md) | 分步工作流 T0–T4 |
| [repo-conventions.md](repo-conventions.md) | 本仓库 paths、modules、data |
| [flow-structure.md](flow-structure.md) | YAML 结构与 Assertion 映射 |
| [review-checklist.md](review-checklist.md) | 生成后审查 |
| [source-index.md](source-index.md) | Maestro 官方原文链接 |

## 核心约束（摘要）

- Case 是唯一测试意图来源；一 Case 测试 ID → 一 Main Flow
- 预期 → 执行层断言；API/Web 在 pytest，Mobile 在 Maestro
- 业务数据 → `data/*.js`；Mobile 使用 `runScript` 与 `${output...}`
- Mobile 复用 → `modules/`；禁止用 Condition 掩盖失败
- 详见 [SKILL.md](../SKILL.md) §7

## 仓库 docs

- [`../../../docs/flow-standard.md`](../../../docs/flow-standard.md)
- [`../../../docs/module-standard.md`](../../../docs/module-standard.md)
- [`../../../docs/data-env-standard.md`](../../../docs/data-env-standard.md)
