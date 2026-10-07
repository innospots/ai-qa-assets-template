# Skill 目录结构规范

本仓库每个 Skill 采用统一布局，便于 Agent 按需加载与人类维护。

## 标准目录

```text
skills/{skill-name}/
├── SKILL.md              # 必须：入口、工作流、规则（精简）
├── references/           # 推荐：详细规范、术语、清单
├── templates/            # 推荐：输出骨架
├── examples/             # 推荐：完整样例
├── scripts/              # 可选：校验、生成、转换
└── assets/               # 可选：Schema、静态配置
```

根目录 [`skills/README.md`](../../README.md) 为全集合索引。

## 文件职责

| 路径 | 用途 | 必需 |
| --- | --- | ---: |
| `SKILL.md` | 能力定义、When to Use、Workflow、Rules、Outputs | 是 |
| `references/` | 长规范、方法论、审查清单 | 推荐 |
| `templates/` | Case、TDS 等输出模板 | 推荐 |
| `examples/` | 可对照的完整示例 | 推荐 |
| `scripts/` | 确定性程序（无 LLM 编排） | 按需 |
| `assets/` | JSON Schema、默认 YAML | 按需 |

## SKILL.md 十二节契约

1. Purpose  
2. Scope  
3. When to Use  
4. Inputs  
5. Outputs  
6. Workflow  
7. Rules  
8. Quality Criteria  
9. References  
10. Templates  
11. Scripts  
12. Examples  

各节应简短；超过一屏的细节放入 `references/`。

## 命名

- 目录名：`kebab-case`，按**能力**命名（`test-design`、`test-case`）
- metadata：`namespaced-name: "test:design"` 等形式
- 不以执行工具命名 Skill（Maestro、Playwright 等属于实现层）

## 与仓库资产的关系

```text
skills/     Agent 如何工作（规范 + 流程）
designs/    TDS 产出
cases/      Case 产出
flows/      Flow 产出
data/       业务数据
scripts/    确定性执行与校验
docs/       仓库级标准（Skill references 可跳转，避免双份维护）
```

## 测试 Skill 链路

```text
test:design → test:case → test:flow → test:review
                              ↓
                       test:execution → test:analysis
```

## 变更同步

修改 Skill 规范时：

1. 更新 `references/` 源文件  
2. 确认 `SKILL.md` 链接仍有效  
3. 同步 `docs/*-standard.md` 中的跳转（指向 references，不复制全文）  
4. 运行 `git diff --check` 与相关校验脚本  
