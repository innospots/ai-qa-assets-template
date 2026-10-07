# Modules：公共测试操作

`modules/` 封装 Mobile Maestro Flow 可复用的步骤。API/Web 复用逻辑放在 `executors/` 的 pytest 模块中。

## 使用方式

1. 多个 Mobile Flow 重复相同操作时，抽取为 `modules/{domain}/{action}.yaml`。
2. 父 Flow 通过 `runFlow` 引用，并用 `env` 传参。
3. 修改 Module 前用 `rg 'modules/' flows journeys` 查找引用者。

规范：[`docs/module-standard.md`](../docs/module-standard.md)
