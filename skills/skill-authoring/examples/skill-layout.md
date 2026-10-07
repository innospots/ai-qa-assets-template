# 技能目录示例：接口契约导入

`test-openapi-import/` 是本仓库的完整非对话型示例：

```text
test-openapi-import/
├── SKILL.md                    十二节入口契约
├── references/import-contract.md 详细边界与审核门槛
└── examples/
    ├── README.md               可复制命令和审核步骤
    └── catalog.openapi.yaml    无敏感值的本地输入
```

脚本位于仓库 `scripts/openapi/import.py`，因为它是产品工程的正式确定性入口；Skill 只负责指导何时运行与如何审核。新增 Skill 时先确定产出物和边界，再按 [`../references/skill-review-checklist.md`](../references/skill-review-checklist.md) 检查链接、示例与脚本职责。
