---
name: test-review
description: 只读审查 TDS、Case、Flow、Module、data 覆盖与一致性。用户说审查资产、review、检查覆盖 时使用。
metadata:
  namespaced-name: "test:review"
---

# test:review

## 1. Purpose

对 Design、Case、Flow、Module、data 做**质量与追溯审查**，输出分级问题清单与覆盖报告。

## 2. Scope

**支持：** 只读审查；覆盖度计算；规范一致性检查。

**不支持：** 默认不修改文件（除非用户明确要求修复）。

## 3. When to Use

- 提交前或 Skill 生成后的质量门禁
- 跨平台/追溯/敏感信息专项检查
- 评估 Flow 实现进度

## 4. Inputs

| 输入 | 说明 |
| --- | --- |
| 审查范围 | domain、路径或全仓 |
| 相关 docs/ 与 Skill references | 判定标准 |

## 5. Outputs

- 问题清单：严重程度、证据、影响、建议
- 覆盖：`Flow 数 / Case 测试 ID 数`、缺失与孤立资产

## 6. Workflow

1. 读 [review-checklist.md](references/review-checklist.md) 及链到的规范
2. 按 Design → Case → Flow → Module/data 顺序检查
3. 计算覆盖；区分必须修复 / 建议 / 需业务确认

## 7. Rules

- 默认只读；修复需明确授权
- 以 Case 为意图源，不根据 Flow 偶然行为反改 Case
- 引用最新 Skill references 路径，不用已废弃扁平文件

## 8. Quality Criteria

- [review-checklist.md](references/review-checklist.md) 项均有结论或 N/A 说明
- 每条问题有文件证据
- 覆盖数字可复算

## 9. References

| 文档 | 用途 |
| --- | --- |
| [review-checklist.md](references/review-checklist.md) | 审查清单 |
| [../test-design/references/tds-spec.md](../test-design/references/tds-spec.md) | TDS |
| [../test-case/references/test-case-spec.md](../test-case/references/test-case-spec.md) | Case |
| [../../docs/flow-standard.md](../../docs/flow-standard.md) | Flow |

## 10. Templates

无。

## 11. Scripts

| 脚本 | 用途 |
| --- | --- |
| [`../../scripts/validate-cases.sh`](../../scripts/validate-cases.sh) | Case 结构辅助 |

## 12. Examples

[API 资产审查示例](examples/api-review.md) 展示 DS→TC→Flow→执行节点的证据与问题记录。
