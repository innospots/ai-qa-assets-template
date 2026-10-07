# Executors

与 Flow 清单配套的自动化实现。

| 目录 | 技术 | 映射方式 |
| --- | --- | --- |
| [`api/`](api/) | pytest + httpx | Flow 中 `test:` 指向 pytest 节点 |
| [`web/`](web/) | pytest-playwright | 同上 |

Mobile 不经过本目录，实现位于对应业务域的 `flows/` 与可选 `modules/`。
