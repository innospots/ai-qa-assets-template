# 脚本契约测试

## 当前文件

- `test-maestro-scripts.sh`：创建临时伪 Maestro CLI，验证平台参数、环境加载、报告格式、Tag、构建运行编号和失败传播。
- `test-executor-scripts.sh`：验证 API/Web Flow 清单发现与入口脚本。
- `test_openapi_import.py`：验证接口选择、草稿包生成和不覆盖既有草稿。
- `test_asset_validation.py`：验证缺失 Flow 漏检修复和三平台 Flow 结构。

## 使用方式

```bash
source .venv/bin/activate
bash scripts/tests/test-maestro-scripts.sh
bash scripts/tests/test-executor-scripts.sh
python3 -m pytest -q scripts/tests/test_openapi_import.py scripts/tests/test_asset_validation.py
```

测试不需要真实 Maestro、模拟器或设备，不会输出真实凭据。它只能验证脚本契约；发布前仍需在 Android 和 iOS 真实执行环境运行 Smoke。
