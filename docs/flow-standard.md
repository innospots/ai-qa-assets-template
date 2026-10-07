# Flow 编写规范

Flow 是一个正式 Case ID 的执行实现。文件位于 `flows/{domain}/{scene}/{case-id}.yaml`；文件名、`name` 开头的 ID 与 Case 标题完全一致。一条 TC 只对应一个正式 Flow，Flow 必须可独立执行、判断结果并留下失败证据。

| 平台 | Flow 格式 | 执行实现 | 示例 |
| --- | --- | --- | --- |
| API | `executor`、`name`、`tags`、`test` YAML 清单 | `executors/api/tests/` pytest + httpx | `flows/api/health/TC-API-HEALTH-001.yaml` |
| Web | 同上 | `executors/web/tests/` pytest-playwright | `flows/web/home/TC-WEB-HOME-001.yaml` |
| Mobile | Maestro Header、`---`、命令与断言 | 业务域下的 `flows/`、`modules/` | `flows/mobile/demo/TC-MOBILE-DEMO-001.yaml` |

`api`、`web`、`mobile` 是当前示范业务域名称。产品工程可按真实业务域组织目录；API/Web 按 `executor` 筛选，Mobile 按 Maestro Flow 格式发现。

API/Web 的请求、页面动作、断言与清理写在 executor 测试节点，Flow 只负责 Case ID、Tag 与节点映射。Mobile 的每项关键 Case 预期应落实为等价断言。Case 和 TDS 不写任何执行器 DSL。

数据、环境与共享资产遵循：结构化业务数据和选择器置于 `data/`；应用、环境地址和敏感值置于 env/CI；Mobile Flow 用 `runScript` 显式加载 data。修改共享 Module 或 data 前先查全部引用者，之后运行直接受影响范围。

OpenAPI 导入产物位于 `generated/openapi-drafts/`，属于待审查草稿；不得仅凭接口契约将其作为正式业务用例。详见 [`test:openapi-import`](../skills/test-openapi-import/SKILL.md)。

## 校验

```bash
./scripts/validate-cases.sh
python3 skills/test-flow/scripts/validate-flow.py flows/api/health/TC-API-HEALTH-001.yaml
```

结构校验不能证明端到端通过。执行命令见 [`test:execution`](../skills/test-execution/references/execution-guide.md)。详细平台规则见 [`test:flow`](../skills/test-flow/SKILL.md) 与 [`repo-conventions.md`](../skills/test-flow/references/repo-conventions.md)；Maestro 专项语法见 [`references/README.md`](../skills/test-flow/references/README.md)。
