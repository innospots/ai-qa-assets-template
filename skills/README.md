# Test Skills

本目录保存测试相关的 AI Agent **能力规范**。Skill 定义如何设计、生成、执行、审查和分析测试；不存放 Case、Flow、业务数据或运行结果。

## 目录结构（统一约定）

每个 Skill 遵循相同布局（详见 [`skill-authoring/`](skill-authoring/)）：

```text
skills/{skill}/
├── SKILL.md          # 入口：12 节契约（Purpose → Examples）
├── references/       # 详细规范、workflow、清单
├── templates/        # 输出骨架
├── examples/         # 完整样例
├── scripts/          # 可选：确定性工具
└── assets/           # 可选：Schema 等
```

命名：目录 `test-design`；metadata `test:design`。Skill 按**能力**命名，不按 Maestro/Playwright 等工具命名。

## 技能列表

| Skill | 目录 | 主要 references | 主要产出 |
| --- | --- | --- | --- |
| `test:design` | [`test-design/`](test-design/) | `references/tds-spec.md`、`workflow.md`、`guided-intake.md`、`review-checklist.md` | `designs/{domain}/index.md`、`designs/**/*.design.md` |
| `test:openapi-import` | [`test-openapi-import/`](test-openapi-import/) | `references/import-contract.md` | `generated/openapi-drafts/` 待审查 API 资产包 |
| `test:case` | [`test-case/`](test-case/) | `references/test-case-spec.md`、`workflow.md`、`review-checklist.md` | `cases/**/*.case.md`、`data/` |
| `test:flow` | [`test-flow/`](test-flow/) | `references/repo-conventions.md`、`examples/{api,web,mobile}-flow.md`、`templates/`、`scripts/` | `flows/`、`executors/`、`modules/` |
| `test:execution` | [`test-execution/`](test-execution/) | `references/execution-guide.md` | `artifacts/`、执行摘要 |
| `test:review` | [`test-review/`](test-review/) | `references/review-checklist.md` | 问题与覆盖报告 |
| `test:analysis` | [`test-analysis/`](test-analysis/) | `references/analysis-guide.md` | 根因分类与建议 |
| `skill:authoring` | [`skill-authoring/`](skill-authoring/) | `references/skill-structure-spec.md` | 新 Skill 目录与 SKILL.md |

## 推荐调用顺序

```text
需求 / PRD 或 OpenAPI 契约（先由 test:openapi-import 生成草稿并审核）
    ↓
test:design  →  designs/
    ↓
test:case    →  cases/ + data/
    ↓
test:flow    →  flows/
    ↓
test:review  （提交前或生成后）
    ↓
test:execution  →  artifacts/
    ↓
test:analysis   （失败时）
```

## 与工程资产的边界

```text
skills/       Agent 如何工作（规范 + 流程 + 样例）
designs/      TDS 测试设计（产出）
cases/        测什么（唯一意图源）
flows/        如何执行一个测试
modules/      可复用操作
data/         JavaScript Object 业务数据
scripts/      确定性校验与执行
artifacts/    运行结果
docs/         仓库级标准（Skill references 跳转，避免双份维护）
```

Skill 使用模型做理解、生成与分析；Shell 脚本不做提示词编排或模型决策。

## 新建 Skill

使用 [`skill-authoring/SKILL.md`](skill-authoring/SKILL.md) 与 [`skill-authoring/templates/SKILL.template.md`](skill-authoring/templates/SKILL.template.md)。
