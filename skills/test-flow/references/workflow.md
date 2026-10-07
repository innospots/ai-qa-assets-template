# Case → Flow 工作流

## T0 盘点

读取场景 TDS、正式 Case、已有 Flow、执行器、Module 和 data。列出每条 TC 的步骤、关键预期、目标平台与现有覆盖。OpenAPI 导入草稿须先完成 TDS/Case 审核。

## T1 映射

一 TC 对应一 Flow。API/Web 将 TC 映射到唯一 pytest 节点；Mobile 将步骤映射到 Maestro 命令、预期映射到断言。Case 预期无法自动判定时报告缺口，不自行降低预期。重复公共操作先搜索引用者，再决定复用或提取 Module。

## T2 实现

| 平台 | 实现内容 | 示例 |
| --- | --- | --- |
| API | `executor: api` 清单 + `executors/api/tests/` 中的 httpx 断言 | [API](../examples/api-flow.md) |
| Web | `executor: web` 清单 + `executors/web/tests/` 中的 Playwright 断言 | [Web](../examples/web-flow.md) |
| Mobile | Maestro Header、命令、data/selector 加载和断言 | [Mobile](../examples/mobile-flow.md) |

Mobile 的高级控制流、selector、MCP 探索分别见 [control-flow-guide.md](control-flow-guide.md)、[selector-guide.md](selector-guide.md)、[mcp-guide.md](mcp-guide.md)。

## T3 校验与执行

先用 [review-checklist.md](review-checklist.md) 对照 Case；运行 `python3 skills/test-flow/scripts/validate-flow.py <flow>` 与 `./scripts/validate-cases.sh`。Mobile 还运行 `check-references.py`。然后单 Flow 执行，再验证直接受影响的套件或共享资产引用者。

## T4 交付

报告 TC↔Flow↔执行节点、共享资产影响、结构校验与实际执行结果、未执行原因。`generate-flows.sh` 等历史兼容入口不负责 AI 生成。
