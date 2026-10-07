# Module 编写规范

## 1. 定义

Module 是可被多个 Flow 或 Journey 复用的执行操作，例如启动应用、登录、退出、导航或创建业务对象。Module 负责“完成一个操作”，不负责判断完整业务测试是否通过。

## 2. 位置与命名

```text
modules/{domain}/{action}.yaml
```

领域和动作使用小写短横线命名，如 `modules/auth/login.yaml`。通用操作可放入 `modules/common/`，但应避免把领域明确的操作都堆入 common。

## 3. Maestro 推荐结构

```yaml
appId: ${APP_ID}
name: 提交登录
---
- tapOn:
    id: "${output.selectors.login.usernameId}"
- inputText: "${USERNAME}"
- tapOn:
    id: "${output.selectors.login.passwordId}"
- inputText: "${PASSWORD}"
- tapOn:
    id: "${output.selectors.login.submitId}"
```

Module 是可由 `runFlow` 调用的 Maestro 子 Flow。入口 Flow 先加载业务 data 和平台 selector data，再通过 `runFlow.env` 传入 Module 专属参数；选择器直接使用已加载的 `${output.selectors...}`。`runFlow.env` 不等同于 `env/*.env` 文件。

## 4. 抽取条件

满足任一条件时应考虑 Module：

- 相同操作被两个及以上 Flow/Journey 使用；
- 操作步骤复杂，需要集中维护；
- 操作具有稳定业务含义和明确输入输出。

只出现一次且简单的场景步骤可保留在 Flow。不要为每一个点击或字段创建过细 Module。

## 5. 输入与状态

- Module 专属输入使用大写蛇形命名，由调用方通过 `runFlow.env` 传入；全局应用、设备和敏感值才由 CLI `-e` 注入。
- Module 不读取未声明变量，不保存真实凭据或环境专属值。
- 需要特定起始页面或业务状态时，在名称、注释或执行器适配层显式说明。
- Module 完成后应进入可预期状态，供调用方继续执行或判断。

## 6. 边界

Module 可以包含确保自身动作完成的局部等待或技术检查，但不应包含场景的业务结论。例如登录 Module 可以等待提交动作完成，不能固定断言“登录一定成功”，因为错误密码 Flow 也会复用登录动作。

## 7. 平台差异

- 共用动作优先保留在同一 Module；入口 Flow 按平台加载不同 selector JS，Module 统一引用相同的 `output.selectors` 层级。
- 权限、系统页面或导航行为不同，使用 `runFlow.when.platform` 调用平台子 Flow。
- 平台子 Flow 只处理真实差异，不复制完整业务动作。
- `optional: true` 只用于可能不存在的系统提示，不用于关键业务操作或断言。

## 8. 变更兼容性

修改 Module 前运行：

```bash
rg 'modules/{domain}/{action}.yaml' flows journeys
```

输入重命名、动作后置状态变化和错误处理变化都可能影响全部引用者。破坏性变化应一次更新所有调用方，并执行相关回归。

## 9. 评审清单

- 是否只有一个明确职责，并达到合理复用价值？
- 输入是否完整、命名清楚且无隐式依赖？
- 是否没有场景专属断言、真实数据和环境硬编码？
- 调用完成后的状态是否可预期？
- 所有引用者是否已检查和回归？
- 调用方是否在调用 Module 前完成所需 data/selector 加载？
