# Case 编写规范

Case 编写规范已归属 **`test:case` Skill** 管理，本文件不再维护正文。

| 内容 | 路径 |
| --- | --- |
| Skill 入口 | [`../skills/test-case/SKILL.md`](../skills/test-case/SKILL.md) |
| 规范正文 | [`../skills/test-case/references/test-case-spec.md`](../skills/test-case/references/test-case-spec.md) |
| 分步工作流 | [`../skills/test-case/references/workflow.md`](../skills/test-case/references/workflow.md) |
| 生成后审查清单 | [`../skills/test-case/references/review-checklist.md`](../skills/test-case/references/review-checklist.md) |
| 完整 Case 样例 | [`../skills/test-case/examples/customer-create-customer.case.md`](../skills/test-case/examples/customer-create-customer.case.md) |
| data 脚本样例（对齐 `data/web/`） | [`../skills/test-case/examples/sample-customer-customers.js`](../skills/test-case/examples/sample-customer-customers.js)、[`sample-customer-batch-records.js`](../skills/test-case/examples/sample-customer-batch-records.js) |
| 数组批量 Case 片段 | [`../skills/test-case/examples/batch-one-case.md`](../skills/test-case/examples/batch-one-case.md) |
| 仓库 data 标准参照 | [`../data/web/`](../data/web/) |

Case **产出**仍写入 `cases/{domain}/`，见 [`../docs/test-asset-guide.md`](../docs/test-asset-guide.md)。

**校验脚本**仍检查 Front Matter、`## 正向测试` / `## 反向测试` 与 TC ID 格式；语义与 DS 覆盖见 Skill 内 [`review-checklist.md`](../skills/test-case/references/review-checklist.md)。
