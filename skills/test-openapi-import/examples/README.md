# Catalog API 导入示例

在仓库根目录执行：

```bash
python3 scripts/openapi/import.py --spec skills/test-openapi-import/examples/catalog.openapi.yaml --list
python3 scripts/openapi/import.py --spec skills/test-openapi-import/examples/catalog.openapi.yaml --domain catalog --operation 'GET /items/{itemId}'
```

第一条列出 `GET /items/{itemId}`；第二条在 `generated/openapi-drafts/catalog/` 创建独立草稿包。打开包内 `README.md` 和 `resources/operation.json`，再根据产品需求确认：商品 ID 的测试值、200 响应的业务字段、404 的业务含义、鉴权和清理要求。草稿中的 pytest 骨架会跳过，直到上述预期被确认并落实到正式资产。
