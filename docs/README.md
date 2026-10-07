# Docs：规范与协作指南

`docs/` 保存测试资产的长期规范，而不是运行产物或某次执行记录。

## 当前结构

```text
docs/
├── README.md
├── FORK-CHECKLIST.md          从模板创建产品仓
├── test-asset-guide.md
├── design-standard.md
├── case-standard.md
├── flow-standard.md
├── module-standard.md
├── journey-standard.md
├── data-env-standard.md
├── maestro-guide.md           Mobile 执行实践
└── ai-agent-guide.md
```

仓库级 Agent 强制规则见 [`../AGENTS.md`](../AGENTS.md)；测试设计、Case、Flow、执行、审查和分析 Skill 见 [`../skills/README.md`](../skills/README.md)。

## 使用方式

首次使用按“根 README → `test-asset-guide.md` → 当前任务的专项规范”阅读。Agent 还须先遵循根目录 `AGENTS.md`，再阅读 `ai-agent-guide.md`。架构设计和计划是历史决策记录，不是运行时配置或当前操作手册。

## 推荐阅读路径

| 角色或任务 | 必读文档 |
| --- | --- |
| 新成员了解工程 | `test-asset-guide.md`、根目录 `README.md` |
| 从 OpenAPI 启动 API 测试 | [`skills/test-openapi-import/`](../skills/test-openapi-import/) 的导入规范和示例、根 README 快速开始 |
| 编写测试设计 | [`skills/test-design/`](../skills/test-design/)（`SKILL.md` 与 `references/`、`examples/` 样例）、`data-env-standard.md`、`../designs/` |
| 编写测试用例 | [`skills/test-case/`](../skills/test-case/)（`SKILL.md` 与 `references/`、`examples/` 样例）、`../cases/` |
| 从 Case 实现 Flow | `test:flow`（[`skills/test-flow/`](../skills/test-flow/)）、`module-standard.md` |
| 接入或运行 Maestro | `maestro-guide.md`、`flow-standard.md` |
| 设计端到端链路 | `journey-standard.md`、`module-standard.md` |
| AI Agent 修改资产 | 根目录 `AGENTS.md`、`ai-agent-guide.md` 及对应资产规范 |
| 评审变更 | `test-asset-guide.md` 的质量门禁与各规范评审清单 |

## 使用规范

- 每份规范只负责一个主题；跨目录总览放 `test-asset-guide.md`，具体资产规则放对应标准文件。
- 文档中的路径、字段和命令必须与仓库当前实现一致，示例不得包含真实凭据。
- 规则变化时同时更新受影响的 README、校验脚本和示例资产，避免文档与实现分叉。
- `superpowers/specs/` 记录已经确认的设计决策，`superpowers/plans/` 记录实施步骤；不要在其中维护日常操作说明。
- 若历史方案与当前实现不同，以根 README、`AGENTS.md` 和正式规范为准。

## 文档更新流程

1. 确认变更影响的是总览、Case、Flow 还是 Agent 协作规则。
2. 更新最具体的规范文件，再同步相关目录 README。
3. 对照实际文件树、变量名和脚本参数复核示例。
4. 运行 `./scripts/validate-cases.sh`、相关脚本测试和 `git diff --check`。

## 提交前检查

- 链接目标、文件路径、字段和命令真实存在；
- 同一术语在所有文档中含义一致；
- 没有把执行工具名称写入资产模型；
- data、env、Skill 与脚本的边界没有混用；
- 新成员仅阅读 README 和对应规范即可完成一次规范变更。
