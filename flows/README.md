# Flow

每个 Case ID 对应**一个** Flow 文件：`flows/{domain}/{feature}/TC-....yaml`。

## 三类 Flow

| 类型 | 文件内容 | 执行 |
| --- | --- | --- |
| API | 清单：`executor: api`、`tags`、`test` | `scripts/api/run-flow.sh` 或 `run-suite.sh` |
| Web | 清单：`executor: web`、`tags`、`test` | `scripts/web/run-flow.sh` 或 `run-suite.sh` |
| Mobile | Maestro DSL | `scripts/maestro/` |

目录按业务域命名；当前 `api`、`web`、`mobile` 是示范域。API/Web 套件跨业务域扫描，依据清单中的 `executor` 选择执行器。

规范：[`docs/flow-standard.md`](../docs/flow-standard.md)
