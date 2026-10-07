# Skill 审查清单

## 目录结构

- [ ] 存在 `SKILL.md`
- [ ] `SKILL.md` 含完整 12 节（无节可写「无」并说明原因）
- [ ] 长规范在 `references/`，不在 SKILL 正文
- [ ] 有产出物时提供 `templates/` 或说明为何不需要
- [ ] 有完整样例时放在 `examples/`
- [ ] 确定性工具在 `scripts/` 或明确使用仓库 `scripts/`

## SKILL.md 质量

- [ ] Purpose / Scope 不矛盾
- [ ] When to Use 含用户触发词
- [ ] Workflow 可独立执行（或链到 references/workflow）
- [ ] Rules 含禁止项（不写什么、不改什么）
- [ ] Quality Criteria 可验证（清单或命令）
- [ ] References 表格链接有效
- [ ] description front matter 适合 Skill 发现

## 内容与边界

- [ ] 不复制 `docs/` 全文；跳转或摘要 + 链接
- [ ] 脚本不含提示词编排或模型决策
- [ ] 示例无真实密码、Token、生产地址
- [ ] 能力命名非工具名

## 仓库同步

- [ ] `skills/README.md` 已更新
- [ ] 相关 `docs/*-standard.md` 跳转指向新路径
- [ ] `AGENTS.md` Skill 表与目录一致（若适用）
- [ ] `rg 'reference\.md|sample-customer'` 无 stale 链接

## 新 Skill 额外项

- [ ] metadata `namespaced-name` 唯一
- [ ] 与上下游 Skill 的 Inputs/Outputs 对齐
- [ ] 至少一个 example 或说明暂无原因
