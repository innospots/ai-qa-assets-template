# Test Flow References

> 适用于 `test-flow` Skill 的参考规范集。  
> 整理日期：2026-09-10  
> 平台总入口见 [`../SKILL.md`](../SKILL.md)；本目录除 `repo-conventions.md`、`flow-structure.md`、`workflow.md`、`review-checklist.md` 外的命令/选择器资料主要用于 Mobile Maestro。

## 1. 使用目的

本目录不是 Maestro 官方文档的镜像，而是面向 AI Agent / Coding Agent 的 **Flow 生成规范层**。

它解决以下问题：

- 如何把标准 Test Case 转换为可执行 Flow；
- 如何选择稳定的 Selector；
- 如何把 Expected Result 转换为 Assertion；
- 如何管理参数、测试数据与运行态数据；
- 如何拆分和复用 Subflow；
- 如何使用 Condition、Loop、Wait、Retry；
- 什么情况下可以使用 JavaScript；
- 如何保证 Flow 可独立运行、可追踪、可维护；
- 如何在 Flow、Test Case 和测试报告之间建立稳定映射；
- 何时用 Maestro MCP 探索 Selector 与试跑草稿。

## 2. Reference 文档

| 文档 | 用途 |
|---|---|
| [flow-structure.md](flow-structure.md) | Flow YAML 基本结构、Header、Commands、元数据规范 |
| [command-guide.md](command-guide.md) | Command 分类、选用规则和受控使用原则 |
| [selector-guide.md](selector-guide.md) | UI 元素定位优先级、组合规则和反模式 |
| [data-binding-guide.md](data-binding-guide.md) | 参数、常量、测试数据、`output` 数据传递规范 |
| [subflow-guide.md](subflow-guide.md) | Subflow 拆分、参数传递、复用和目录规范 |
| [control-flow-guide.md](control-flow-guide.md) | Condition、Loop、Wait、Retry、Optional 规范 |
| [javascript-guide.md](javascript-guide.md) | JavaScript 使用边界、`evalScript`、`runScript`、HTTP、Faker |
| [environment-platform-guide.md](environment-platform-guide.md) | App 状态、权限、平台差异、Locale、设备运行环境 |
| [naming-conventions.md](naming-conventions.md) | Flow、Subflow、Tag、变量、Script 命名规范 |
| [workspace-guide.md](workspace-guide.md) | Workspace、`config.yaml`、目录发现和 Tag 管理 |
| [traceability-reporting.md](traceability-reporting.md) | Case → Flow → Report 追踪和报告元数据 |
| [best-practices.md](best-practices.md) | 综合最佳实践、反模式和生成后审查清单 |
| [repo-conventions.md](repo-conventions.md) | **本仓库** paths、modules、data/*.js、Tag |
| [workflow.md](workflow.md) | Case → Flow 分步工作流 |
| [review-checklist.md](review-checklist.md) | 生成后审查清单 |
| [mcp-guide.md](mcp-guide.md) | Maestro MCP 探索、试跑与 Cursor 配置 |
| [source-index.md](source-index.md) | 本规范引用的官方原文链接索引 |

## 3. 规范优先级

生成 Flow 时按以下优先级处理冲突：

1. 当前 Test Case 的测试意图和 Expected Result；
2. 本 `references/` 目录中的工程规范；
3. Maestro 官方当前版本文档；
4. 示例文件；
5. Agent 自身推断。

如果 Test Case 与可执行能力存在冲突，不得通过删除断言、增加 `optional: true`、增加无边界 `retry` 或修改测试意图来“让脚本跑通”。

## 4. 核心原则

```text
Test Case
   │
   ├── Steps ───────────────► Commands
   │
   ├── Expected Results ────► Assertions
   │
   ├── Test Data ───────────► Variables
   │
   └── Preconditions ───────► Setup / Subflow / API
                                │
                                ▼
                           Executable Flow
```

必须保证：

- 一个 Main Flow 对应一个 Test Case；
- 关键 Expected Result 必须有可执行 Assertion；
- 业务测试数据与 Flow 逻辑分离；
- 共享行为优先提取为原子化 Subflow；
- Main Flow 应尽量可在重置设备/环境后独立运行；
- 不使用容错机制隐藏产品缺陷；
- Case ID 必须进入 Flow 元数据并传递至测试报告。

## 5. 官方入口

- Maestro Flows: https://docs.maestro.dev/maestro-flows
- Complete documentation index: https://docs.maestro.dev/llms.txt
- Commands: https://docs.maestro.dev/reference/commands-available
- Selectors: https://docs.maestro.dev/reference/selectors
- Workspace configuration: https://docs.maestro.dev/reference/workspace-configuration
