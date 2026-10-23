# 提交29240a0对应Mac原生包复验

2026-10-23，macOS15.7.7 arm64。使用真实固定TEE在HEAD29240a0重新build-bee，然后以ad-hoc签名/locked/offline构建App，build成功。构建时Windows测试改动尚未提交，版本如实为dev+29240a0-dirty；这是该构建的P0验证页，不冒充后续P1页面或新HEAD。

- Rust41/41、0失败、0忽略，包含2项签名包测试（完整日志rust-test.log）。
- CUA打开真实tauri://localhost，显示内置Bee真实版本及darwin/arm64，hello后ready，点击ping显示管理进程响应正常；ping.ax.txt与ping.jpg为实际结果。
- 从App菜单明确退出，App31058与ownedBee31070均确认消失，见processes.json和exit.json。codesign deep/strict通过，主程序及Bee的SHA见sources.json。
- CtrlF8尝试未定位托盘表面，仍未验收托盘；不据此修改产品行为。该包未重新做最低OS或干净用户安装。
