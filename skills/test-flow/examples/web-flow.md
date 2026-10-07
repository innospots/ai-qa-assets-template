# Web Flow：首页

正式资产链路：`designs/web/home.design.md` → `cases/web/home.case.md` 的 `TC-WEB-HOME-001` → `flows/web/home/TC-WEB-HOME-001.yaml` → `executors/web/tests/test_home.py::test_tc_web_home_001`。

Flow 清单只做映射，页面操作与断言在 pytest-playwright 节点。单 Flow 执行：

```bash
source .venv/bin/activate
./scripts/web/run-flow.sh flows/web/home/TC-WEB-HOME-001.yaml env/web.env
```

需先安装 Chromium，并配置 `WEB_BASE_URL`。
