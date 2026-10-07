---
name: test-execution
description: 按 Case ID 或 Tag 执行 API、Web、Mobile 测试，记录环境、命令、退出码与 artifact；不修改测试预期。
metadata:
  namespaced-name: "test:execution"
---

# test:execution

## 1. Purpose

通过仓库正式脚本执行确认过的测试，并留下可复核的结果摘要。

## 2. Scope

支持 API/Web pytest 清单与 Mobile Maestro Flow 的单条或套件执行；不把 OpenAPI 草稿作为可运行正式测试。

## 3. When to Use

用户要求单 Case、Smoke、Regression 或移动端设备验证时使用。

## 4. Inputs

平台、Case ID/范围、环境文件、可用的网络或设备，以及是否具备运行条件。

## 5. Outputs

`artifacts/` 中的日志/报告，以及命令、退出码、通过/失败/跳过数、未执行项说明。

## 6. Workflow

1. 读 [执行指南](references/execution-guide.md)，定位 Flow 与对应脚本。
2. 检查所需 env、依赖、设备和范围，不打印敏感值。
3. 先运行单条受影响 Flow，再运行受影响套件。
4. 记录实际结果；失败交 `test:analysis`。

## 7. Rules

- API/Web 用 `scripts/api/`、`scripts/web/`；Mobile 用 `scripts/maestro/`。
- 默认 Smoke 入口 `./scripts/run-smoke.sh`；Mobile 使用专门入口。
- 不为通过而改 Case/TDS，结构校验不代表端到端通过。

## 8. Quality Criteria

执行范围、环境、退出码和 Artifact 路径明确；无法执行的项目及原因可复现。

## 9. References

[执行指南](references/execution-guide.md)、[脚本索引](../../scripts/README.md)。

## 10. Templates

无；执行摘要由命令结果和 Artifact 组成。

## 11. Scripts

`scripts/api/run-flow.sh`、`scripts/api/run-suite.sh`、`scripts/web/run-flow.sh`、`scripts/web/run-suite.sh`、`scripts/maestro/run-flow.sh`、`scripts/maestro/run-suite.sh`、`scripts/run-smoke.sh`。

## 12. Examples

[API/Web/Mobile 执行示例](examples/execution-readout.md)。
