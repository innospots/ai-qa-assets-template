---
name: test-design
description: 从 PRD/PDD 编写或对齐分层 TDS（designs/）；using-superpowers 拆任务、逐份生成与审查。不写 Case/Flow。用户说测试设计、TDS、写 design、调整设计文档 时使用。
metadata:
  namespaced-name: "test:design"
---

# test:design

## 1. Purpose

将需求转化为**测试设计说明书（TDS）**：模块 Index + 场景文档，回答测什么、覆盖与风险；产出写入 `designs/`。

## 2. Scope

**支持：** 新建/扩展/对齐 TDS；PRD/PDD 或 AskQuestion 引导；存量 `designs/` 规范迁移（保留 `DS-`）。

**不支持：** 编写 Case、Flow、Maestro；逐步操作与下游资产模板。

## 3. When to Use

- 新业务/变更需测试设计或调整 `designs/`
- 存量 TDS 结构不符合规范
- 无 PRD 时需引导式梳理范围（见 References → guided-intake）

## 4. Inputs

| 输入 | 说明 |
| --- | --- |
| PRD / 产品功能文档 | 范围与验收 |
| `designs/` 存量 | 变更/对齐 |
| 用户任务 | 平台、优先级、是否仅对齐 |

## 5. Outputs

- `designs/{domain}/index.md`
- `designs/{domain}/{scene}.design.md`
- 交付：sources 映射、任务清单、审查结果、`DS-` 清单与暂缓项

## 6. Workflow

1. 读 **References**（按需，不要一次加载全部）
2. **`using-superpowers`** 拆任务 → T0 盘点 → T1 Index → T2… 各场景 → 逐份 **review-checklist** 审查
3. 禁止一次性生成整个模块全部 TDS

详见 [workflow.md](references/workflow.md)。

## 7. Rules

- TDS 不写逐步操作、Case/Flow、`TC-` 映射
- 公共规则只在 Index；场景继承不重复粘贴
- 已发布 `DS-` 不重编号、不扩未确认范围
- 规范变更写 `references/`，同步 `docs/design-standard.md` 跳转

## 8. Quality Criteria

- [review-checklist.md](references/review-checklist.md) 全部通过
- Index 与场景文件一一对应；`DS-` 与 §9 清单一致
- 无禁止内容（Case 生成指引、Maestro 等）

## 9. References

| 文档 | 用途 |
| --- | --- |
| [tds-spec.md](references/tds-spec.md) | TDS 完整规范 |
| [workflow.md](references/workflow.md) | 分步生成 |
| [guided-intake.md](references/guided-intake.md) | AskQuestion 引导 |
| [review-checklist.md](references/review-checklist.md) | 生成后审查 |

## 10. Templates

| 模板 | 用途 |
| --- | --- |
| [module-index.md](templates/module-index.md) | 模块 Index 骨架 |
| [scenario-tds.md](templates/scenario-tds.md) | 场景 TDS 骨架 |

## 11. Scripts

本 Skill 无专用脚本。结构校验见仓库 `./scripts/validate-cases.sh`（Case 阶段）及 `test:review`。

## 12. Examples

| 示例 | 说明 |
| --- | --- |
| [customer-index.md](examples/customer-index.md) | 模块 Index |
| [customer-create-customer-tds.md](examples/customer-create-customer-tds.md) | 场景 TDS |
