# Env：环境变量模板

`env/` 保存不同环境所需变量的模板。模板可以提交；从模板复制出的实际环境文件包含凭据，必须被 Git 忽略。

## 当前结构

```text
env/
├── README.md
├── android.env.example        Maestro Android 模板
├── ios.env.example            Maestro iOS 模板
├── local.env.example          本地环境模板
├── test.env.example           测试环境模板
└── staging.env.example        预发布环境模板
```

## 当前文件

`android.env.example`、`ios.env.example` 声明应用 ID、设备 ID 和敏感密码变量。业务数据、页面文本、选择器和权限文案都在 `data/` 中维护，由 Flow 的 `runScript` 加载。

## 使用方式

1. 复制所需模板，例如 `cp test.env.example test.env`。
2. 只在本地或安全的 CI 密钥管理中填写值。
3. 将环境文件路径传给执行脚本；Maestro 脚本会自行加载。
4. 变量新增后同步更新所有适用的 `*.env.example`，但不提交实际 `*.env` 文件。

Maestro 执行时复制平台模板为 `android.env` 或 `ios.env`，替换应用 ID、设备 ID，并填写敏感值；再通过 `scripts/maestro/*.sh` 显式加载。双平台通过不同的 selector data 脚本保持差异。

## 使用规范

- 变量名使用大写蛇形命名，并表达用途，例如 `TEST_ADMIN_PASSWORD`。
- 所有模板只声明键，不提供真实密码、Token、API Key 或生产地址。
- 多环境需要相同能力时保持变量名一致，仅实际值不同。
- 新增变量时同步更新 data 脚本、Flow、Module 和 CI 密钥配置中的引用。
- `*.env` 已由 `.gitignore` 排除；提交前仍应运行 `git status --short` 再确认。

## 本地加载示例

```bash
cp env/android.env.example env/android.env
MAESTRO_PLATFORM=android MAESTRO_ENV_FILE=env/android.env ./scripts/run-smoke.sh
```

环境文件只应从可信来源获取。若凭据疑似进入 Git，应立即停用并轮换该凭据，而不是只删除文件。

## 提交前检查

- 仅有 `*.env.example` 被跟踪，模板值为空或明确为非敏感默认值；
- 每个变量有实际消费者，废弃变量已从全部模板和引用处删除；
- 本地 `*.env`、CI 密钥值和运行日志均未进入变更。
