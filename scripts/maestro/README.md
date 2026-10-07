# Maestro 执行脚本

本目录只负责启动 Maestro；测试数据由 Flow 按需执行 `data/**/*.js` 加载。脚本不会解析业务数据，也不会把业务数据转换成扁平环境变量。

## 命令与参数

| 命令 | 用途 | 参数 |
| --- | --- | --- |
| `preflight.sh` | 资产、环境、CLI 和设备预检 | `<android|ios> [env-file]` |
| `run-flow.sh` | 执行一个 Flow | `<android|ios> <flow-file> [env-file] [JUNIT|HTML]` |
| `run-suite.sh` | 按 Tag 执行套件 | `<android|ios> <smoke|regression|e2e|special|all> [env-file] [JUNIT|HTML]` |
| `build-and-test.sh` | 单平台预检→Smoke→Regression→E2E | `<android|ios> [env-file]` |
| `build-all-platforms.sh` | 依次执行 Android 和 iOS | `[android-env] [ios-env]` |

示例：

```bash
./scripts/maestro/run-flow.sh android flows/auth/login/TC-AUTH-LOGIN-001.yaml env/android.env JUNIT
./scripts/maestro/run-suite.sh ios smoke env/ios.env HTML
./scripts/maestro/build-and-test.sh android env/android.env
./scripts/maestro/build-all-platforms.sh env/android.env env/ios.env
```

## 完整调用链

```text
run-flow.sh / run-suite.sh / run-smoke.sh
  → common.sh 读取 env、准备 artifacts 目录
  → python_runner/main.py run（按 Flow 或 Tag 筛选）
  → Android 可选 adb 预启动
  → maestro CLI test --device ... --config ... <Flow>
  → Flow 执行 runScript，加载 data/**/*.js
  → Python 校验退出码/日志，写入 summary.json、report.html、junit.xml
```

`build-and-test.sh` 的调用链为：

```text
preflight.sh → run-suite.sh smoke → run-suite.sh regression → run-suite.sh e2e
```

`special`（故障注入类 Flow）不在上述门禁中。需要时单独执行 `run-suite.sh <platform> special` 或 `run-flow.sh`。不要用 `all` 作为默认门禁。

## 环境文件参数

环境文件只提供运行环境和敏感参数：

```dotenv
APP_ID=com.example.android
MAESTRO_DEVICE=emulator-5554
TEST_ADMIN_PASSWORD=通过 CI Secret 注入
TEST_MEMBER_PASSWORD=通过 CI Secret 注入
TEST_DISABLED_PASSWORD=通过 CI Secret 注入
```

`APP_ID` 用于 Flow 的 `appId`，`MAESTRO_DEVICE` 传给 CLI 的 `--device`；`TEST_*_PASSWORD` 由 data 脚本读取。应用 URL、Token、数据库密码等同样只能从 env/CI Secret 提供。脚本禁止打印这些值。

## Flow 如何控制数据范围

Flow 需要什么数据，就显式加载什么文件；没有被 `runScript` 调用的数据不会进入本次执行：

```yaml
---
- runScript: ../../../data/auth/users.js
- runScript: ../../../data/contracts/selectors/android.js
- inputText: ${output.auth.users.normal.username}
- tapOn:
    id: ${output.selectors.login.usernameId}
```

批量场景可以只加载：

```yaml
- runScript: ../../data/operations/users-batch.js
- evalScript: ${output.runtime.records = output.data.users.insertUsers.records}
```

数据文件路径相对于当前 Flow 文件；`runScript` 的先后顺序就是加载顺序。重复执行同一领域的脚本前，必须确认其采用增量写入，不覆盖已有 `output` 数据。

## 数据变量规则

数据脚本定义的 Object 层级就是引用层级：

```javascript
output.data.users.insertUsers.expectedCount
```

Flow 中写作：

```yaml
- assertTrue: ${output.data.users.insertUsers.expectedCount == 2}
```

批量数组可以传入子 Flow：

```yaml
- runFlow:
    file: ../../modules/users/import.yaml
    env:
      records: ${output.data.users.insertUsers.records}
```

子 Flow 通过 `${records}` 使用调用方传入的参数；跨步骤产生的数据统一写入 `output.runtime`。

## 平台选择器

共享 Flow 通过平台条件加载选择器：

```yaml
- runFlow:
    when:
      platform: Android
    commands:
      - runScript: ../../../data/contracts/selectors/android.js
- runFlow:
    when:
      platform: iOS
    commands:
      - runScript: ../../../data/contracts/selectors/ios.js
```

后续统一使用 `${output.selectors.login.usernameId}`，不在 env 中重复定义选择器。

## 验证与返回码

```bash
bash scripts/tests/test-maestro-scripts.sh
bash -n scripts/*.sh scripts/maestro/*.sh scripts/tests/*.sh
```

返回 `0` 表示成功；非 `0` 表示参数错误、环境缺失、CLI/设备不可用或测试失败。报告位于 `artifacts/maestro/<platform>/<run-id>/`。
