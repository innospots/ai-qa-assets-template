# 数据资产与环境配置规范

## 1. 职责划分

`data/` 定义可执行的业务测试数据、数据集名称和平台选择器契约；环境配置只提供应用、设备、环境地址及不可提交的密钥。两者都不承载测试步骤和预期结果。

```text
Data：有哪些用户、批量记录和查询条件
Environment：当前应用、设备、环境地址和敏感值
Flow：按 Object 层级引用 `${output.auth.users.normal.username}`、`${output.data.users.insertUsers.records}` 并执行步骤
```

## 2. data 位置与命名

```text
data/{domain}/{business-object}.js
```

文件按业务对象命名，使用 `output.<domain>` 和业务含义数据集名：

```javascript
output.auth = output.auth || {};
output.auth.users = {
  normal: {
    tenantCode: 'demo-east',
    username: 'qa.admin@demo-east.example',
    password: TEST_ADMIN_PASSWORD
  }
};
```

禁止使用 `data1`、`test2` 等无法表达场景的数据集名称。

## 3. 可提交与禁止内容

可以提交：

- 数据字段结构、枚举、格式说明；
- 明确非敏感的边界值和占位值；
- 测试环境专用、可回收的脱敏账号和固定边界值；

禁止提交：

- 生产账号、个人账号、Token、API Key、Cookie；
- 生产地址、生产数据、个人身份信息；
- 可由多项非敏感数据组合还原出的敏感信息。

## 4. 环境模板

Git 只跟踪 `env/*.env.example`。模板中的变量名使用大写蛇形命名，真实敏感值保持为空：

```dotenv
APP_ID=
MAESTRO_DEVICE=
TEST_ADMIN_PASSWORD=
```

实际 `env/*.env` 已被 `.gitignore` 排除。不同环境需要相同能力时保持变量名一致，只改变实际值。

## 5. 本地使用

```bash
cp env/android.env.example env/android.env
MAESTRO_PLATFORM=android MAESTRO_ENV_FILE=env/android.env ./scripts/run-smoke-mobile.sh
```

执行脚本会自行读取 `MAESTRO_ENV_FILE`，无需在终端提前 `source`。环境文件中若确有密钥，应通过安全渠道获得。业务测试数据不应复制到环境文件。

## 6. CI 使用

- 在 CI 的密钥管理功能中配置敏感值，不提交环境文件。
- 限制密钥只在需要的环境、分支和任务中可用。
- 日志输出前脱敏，禁止打印完整环境变量。
- 为测试账号授予完成测试所需的最小权限，并定期轮换。

## 7. 变更规则

新增运行环境变量时：

1. 在适用的 `*.env.example` 中声明空值；
2. 更新实际消费者（data 脚本、Flow 或 Module）的引用；
3. 更新 CI 密钥配置；
4. 更新相关 README；
5. 验证未配置时能得到明确失败，而不是静默使用错误默认值。

删除或重命名变量前，使用 `rg 'VARIABLE_NAME' .` 查找全部引用者。

## 8. 安全事件处理

如果敏感值进入 Git、日志或报告：

1. 立即停用或轮换凭据；
2. 限制相关 Artifact 的访问并按安全流程清理；
3. 评估历史提交和远端副本影响；
4. 修复输出脱敏和忽略规则；
5. 不要认为仅删除当前文件即可消除泄露。

## 9. 评审清单

- 数据集名称和字段是否表达业务含义？
- 固定值是否确定不敏感、与环境无关？
- 环境变量是否只保存环境差异，业务数据是否全部位于 data/？
- 是否存在未使用、重复或命名不一致的变量？
- Git 变更、日志和报告中是否没有真实敏感信息？

## 10. Maestro 双平台变量

Maestro 当前使用以下分层：

- `data/auth/users.js`：跨平台共用登录数据集；
- `data/operations/users-batch.js`：批量创建、列表查询数据集；
- `data/contracts/selectors/android.js`：Android resource-id/accessibility id 契约；
- `data/contracts/selectors/ios.js`：iOS accessibility identifier 契约；
- `env/android.env.example`、`env/ios.env.example`：可执行变量模板；
- `env/android.env`、`env/ios.env`：未提交的实际值。

入口 Flow 通过 `runScript` 按需加载数据脚本，数据写入 `output.auth`、`output.data`、`output.selectors`。共享 Flow 使用相同层级变量，例如 `${output.selectors.login.usernameId}`；两个平台只加载不同 selector JS。新增页面元素时必须同步更新两个 selector 文件和调用它的 Flow/Module。

执行脚本只把 env 文件中的运行参数通过 Maestro `-e KEY=VALUE` 注入；data 文件路径由每个 Flow 的 `runScript` 决定，不需要另传“数据文件列表”参数。JUnit/HTML/debug 输出写入 `artifacts/maestro/`。详见 [`maestro-guide.md`](maestro-guide.md)。

## 11. 数据加载范围与参数传递

数据采用“入口 Flow 负责加载、子 Module 只接收所需参数”的规则：

```yaml
- runScript: ../../../data/operations/users-batch.js
- runFlow:
    file: ../../../modules/users/import.yaml
    env:
      RECORDS: ${output.data.users.insertUsers.records}
      EXPECTED_COUNT: ${output.data.users.insertUsers.expectedCount}
```

- `runScript` 路径相对于当前 Flow 文件；加载顺序就是命令顺序。
- `${output...}` 是加载后的结构化数据引用，层级必须与 JS Object 一致。
- `runFlow.env` 是父 Flow 向子 Flow/Module 的参数映射，不代表数据来自操作系统 env。
- Module 中使用 `${RECORDS}`、`${EXPECTED_COUNT}`，不应再次猜测或重新加载调用方数据。
- 未加载的数据文件不在本次作用域内；需要不同数据集时修改 Flow 的 `runScript` 和引用，而不是切换全局 env。
- 本次运行生成的动态值写入 `output.runtime`，仅在当前执行链路中传递。
