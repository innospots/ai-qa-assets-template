# Data

JavaScript Object 业务数据与选择器。Mobile Flow 通过 `runScript` 加载；API/Web pytest 在执行器中读取经确认的业务数据，环境地址和敏感值从 env/CI 获取。OpenAPI 导入会在草稿包中创建接口 data 快照。

## 示范

| 路径 | 用途 |
| --- | --- |
| [`web/pages.js`](web/pages.js) | Web 路径与标题期望 |
| [`mobile/selectors.js`](mobile/selectors.js) | Mobile 占位选择器 |

规范：[`docs/data-env-standard.md`](../docs/data-env-standard.md)
