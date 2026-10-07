---
name: skill-authoring
description: 编写与审查本仓库 skills/ 下的 Agent Skill；统一目录结构、SKILL.md 契约与 references 拆分原则。用户说新建 Skill、优化技能目录、Skill 规范 时使用。
metadata:
  namespaced-name: "skill:authoring"
---

# skill:authoring

## 1. Purpose

定义本仓库 **Skill = 能力 + 执行规范 + 参考资料 + 模板/示例 + 可选脚本** 的统一结构，便于 Agent 按需加载、人类维护一致。

## 2. Scope

**支持：** 新建/重构 Skill 目录；审查 SKILL.md 是否过胖；规范 references/templates/examples 职责。

**不支持：** 替代各业务 Skill 的领域规范（TDS、Case 等仍在其 Skill 的 references 中）。

## 3. When to Use

- 新增 Java/测试/产品类 Skill
- 重构现有 Skill 目录或拆分 reference 大文件
- 审查 Skill 是否符合仓库约定

## 4. Inputs

- 能力名称与产出物类型
- 现有 `docs/` 规范（跳转而非复制）
- 是否需要 scripts/assets

## 5. Outputs

```text
skills/{skill-name}/
├── SKILL.md          # 必须：12 节入口契约
├── references/       # 推荐：详细规范
├── templates/        # 推荐：输出骨架
├── examples/         # 推荐：完整样例
├── scripts/          # 可选：确定性工具
└── assets/           # 可选：Schema、静态配置
```

根目录 [`skills/README.md`](../README.md) 索引更新。

## 6. Workflow

1. 读 [skill-structure-spec.md](references/skill-structure-spec.md)
2. 用 [SKILL.template.md](templates/SKILL.template.md) 创建入口
3. 大规范拆入 `references/`；样例进 `examples/`
4. [skill-review-checklist.md](references/skill-review-checklist.md) 审查
5. 更新 `skills/README.md` 与相关 `docs/` 跳转

## 7. Rules

- **SKILL.md 保持精简**：只写 Purpose→Workflow→Rules→Outputs；细节链到 references
- **按能力命名**，不以工具命名（如 `test-execution` 而非 `maestro`）
- references 与 SKILL 分离，Agent **按需读取**
- 脚本只做确定性校验/转换，不含提示词编排
- 不提交 secrets；示例用占位符

## 8. Quality Criteria

- [skill-review-checklist.md](references/skill-review-checklist.md) 通过
- 目录内链接有效；外部 `docs/` 跳转已同步
- SKILL.md 含完整 12 节且每节有实质内容或明确「无」

## 9. References

| 文档 | 用途 |
| --- | --- |
| [skill-structure-spec.md](references/skill-structure-spec.md) | 目录与文件职责 |
| [skill-writing-spec.md](references/skill-writing-spec.md) | SKILL.md 写作要点 |
| [skill-review-checklist.md](references/skill-review-checklist.md) | 审查清单 |

## 10. Templates

| 模板 | 用途 |
| --- | --- |
| [SKILL.template.md](templates/SKILL.template.md) | 新 Skill 入口骨架 |

## 11. Scripts

本 Skill 无专用脚本。资产校验使用仓库 `scripts/` 中与产出类型对应的脚本。

## 12. Examples

[技能目录示例](examples/skill-layout.md)；各业务 Skill 的 `examples/` 展示对应资产。
