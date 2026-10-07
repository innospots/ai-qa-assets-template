# SKILL.md 写作规范

## 原则

**SKILL.md 是入口契约，不是知识库。**

Agent 读取顺序：

```text
解决什么问题 → 何时调用 → 需要什么输入 → 执行步骤 → 规则 → 输出什么 → 细节查 references
```

## 各节写作要点

| 节 | 内容 | 避免 |
| --- | --- | --- |
| Purpose | 一句话能力 + 产出目录 | 业务背景长文 |
| Scope | 支持/不支持 bullet | 与 Purpose 重复 |
| When to Use | 触发词、前置条件 | 完整 workflow |
| Inputs | 表格：输入类型与说明 | 粘贴 PRD |
| Outputs | 路径模式 + 交付物清单 | 模板全文 |
| Workflow | 编号步骤 + 链到 references/workflow | 逐步操作细节 |
| Rules | 必须/禁止，可引用 spec 章节 | 整章规范复制 |
| Quality Criteria | 清单或脚本命令 | 审查细则全文 |
| References | 表格链到 references/*.md | 内嵌大段 markdown |
| Templates | 表格链到 templates/ | 模板正文 |
| Scripts | 命令与路径 | 脚本源码 |
| Examples | 表格链到 examples/ | 完整样例 |

## Front Matter

```yaml
---
name: test-design
description: 一行说明，含触发场景（供 Skill 发现）
metadata:
  namespaced-name: "test:design"
---
```

`description` 应包含：做什么、主要产出、用户说什么时用。

## references 拆分

- 单文件超过 ~300 行或含多主题 → 拆文件  
- 方法论（边界值、等价类）独立成文  
- 审查清单统一 `{topic}-checklist.md` 或 `review-checklist.md`  
- workflow / guided-intake 独立，SKILL 只链入口  

## 链接约定

- Skill 内：`references/foo.md`、`examples/bar.md`（相对 SKILL.md）  
- 跨 Skill：`../test-design/references/tds-spec.md`  
- 仓库 docs：`../../docs/case-standard.md`  
- 禁止链接已删除的旧扁平路径（`reference.md`、`sample-*` 在 Skill 根目录）

## 示例 Skill

- `skills/test-design/` — TDS，references + templates + examples  
- `skills/test-case/` — Case + data 引用  
- `skills/skill-authoring/` — 本规范自身  
