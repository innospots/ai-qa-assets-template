# OpenAPI 导入契约

## 输入与选择

只接受本地、UTF-8、最多 10 MiB 的 OpenAPI 3.0/3.1 YAML 或 JSON。用 `--list` 取得 `METHOD /path` 选择键。默认不选择任何接口；可指定单个 `--operation` 或显式 `--all`。业务域用小写短横线 slug，不能从 `info.title` 自动推断。

## 输出

每个接口单独生成草稿包，位置为 `generated/openapi-drafts/{domain}/{method-path-hash}/`。同一选择键生成稳定目录；如目标已存在，命令失败且不覆盖。包内包含：

业务域可含短横线；data Object 命名空间将短横线转换为下划线（例如 `customer-service` → `output.customer_service`），生成包内 README 会写明映射。

| 路径 | 用途 |
| --- | --- |
| `designs/{domain}/index.md`、`*.design.md` | 待确认的范围与 DS 意图 |
| `cases/{domain}/*.case.md` | 待确认的 TC、步骤与业务预期 |
| `flows/{domain}/{scene}/TC-*.yaml` | 指向 pytest 骨架的 API 执行清单 |
| `data/{domain}/*.js` | 方法、路径、必填参数的结构化快照 |
| `env/api.env.example` | 环境地址占位符 |
| `executors/api/tests/*.py` | 默认跳过的实现骨架 |
| `resources/operation.json` | 所选接口、路径参数及 components 快照 |

脚本不执行网络请求、不解析远程 `$ref`，不会推导有效请求值、业务成功条件、权限、清理策略或完整反向场景。`responses` 中的状态码只作为契约线索。

## 入正式资产的审核门槛

1. 对照需求确认场景范围、DS 意图与 Case 业务预期。
2. 确认请求数据、鉴权、前置条件、数据清理和响应断言。
3. 如复用现有领域，核对 DS/TC 稳定 ID；草稿 ID 不自动占用正式编号。
4. 按 TDS → Case → Flow/data/executor 顺序落正式资产；删除 pytest 的跳过标记并完成断言。
5. 运行结构校验、单 Flow、相关套件。未经此审核，草稿不能作为可执行测试的成功依据。
