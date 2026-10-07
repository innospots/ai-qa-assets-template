# Mobile Flow：示范首页

正式资产链路：`designs/mobile/demo.design.md` → `cases/mobile/demo.case.md` 的 `TC-MOBILE-DEMO-001` → `flows/mobile/demo/TC-MOBILE-DEMO-001.yaml`。

Mobile Flow 使用 Maestro YAML；从当前 Flow 读取配置区、命令和断言，检查是否逐项对应 Case 预期。单 Flow 执行：

```bash
./scripts/maestro/preflight.sh android env/android.env
./scripts/maestro/run-flow.sh android flows/mobile/demo/TC-MOBILE-DEMO-001.yaml env/android.env
```

需要 Maestro CLI、可用设备和真实测试应用配置；结构校验不能代替端到端执行。
