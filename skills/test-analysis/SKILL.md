---
name: test-analysis
description: 分析失败 artifact、日志与资产关系，分类根因并给出最小复验建议。用户说分析失败、看报告、定位问题 时使用。
metadata:
  namespaced-name: "test:analysis"
---

# test:analysis

## 1. Purpose

基于失败 **Artifact** 与 Case/Flow/Module/data，区分产品缺陷与测试资产/环境问题，输出证据与下一步。

## 2. Scope

**支持：** 读报告/日志/截图；根因分类；最小复验命令建议。

**不支持：** 无证据改资产；用户仅要分析时自动实施修复。

## 3. When to Use

- 自动化失败需归因
- CI 红构建需摘要
-  flaky 或环境疑似问题

## 4. Inputs

| 输入 | 说明 |
| --- | --- |
| Artifact | 报告、日志、截图路径 |
| 关联 Flow/Case | ID 与平台 |
| 执行命令与环境摘要 | 复现上下文 |

## 5. Outputs

- 事实 vs 推断分离的分析报告
- 主因分类与置信度
- 建议负责人与最小验证命令

## 6. Workflow

1. 读 [analysis-guide.md](references/analysis-guide.md)
2. 锁定 Case ID、平台、失败步骤与时间
3. 对照 Case 预期、Flow 断言、data/Module
4. 分类根因；证据不足标 `Unknown`

## 7. Rules

- 不凭单截图断言产品根因
- 不为通过而降预期或改 Case
- 日志脱敏（密码、Token、PII）
- 修复交对应 Skill 或显式授权

## 8. Quality Criteria

- 含实际/预期、证据路径、置信度
- 首因与连锁失败已区分
- 建议可执行（具体命令或文件）

## 9. References

| 文档 | 用途 |
| --- | --- |
| [analysis-guide.md](references/analysis-guide.md) | 步骤与限制 |

## 10. Templates

无。

## 11. Scripts

无专用脚本；复验时使用 `test:execution` 命令。

## 12. Examples

[API 失败分析示例](examples/api-failure.md) 区分观察事实与推断。
