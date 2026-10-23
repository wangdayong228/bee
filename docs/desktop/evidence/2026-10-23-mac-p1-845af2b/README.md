# P1 Task1 Mac 原生五页壳验收

2026-10-23，macOS15.7.7 arm64，源码845af2b，demo模式，ad-hoc签名、未公证。实际Tauri App由固定TEE和独立Go Bee构建；sources.json记录本次主程序与Bee哈希。

- CUA在真实tauri://localhost逐页检查概览、AI账号、收益、诊断、设置，五页均有常驻“演示数据”标识；每页JPEG和AX保存于本目录。
- 连接抽屉区分业务演示连接、原生管理进程ready、真实贡献未启动；Escape关闭后AX显示焦点回到“查看连接详情”。
- 菜单退出后App52858与owned Bee52878均消失，exit.json为独立进程核查。
- 本次系统深色外观，真实原生标题栏；未据此宣称托盘、最低macOS、干净安装、Windows或Linux WebView验收通过。
- 后续35873d5仅修补金额显示，其RED/GREEN页面20/20及build已另行验证；本目录属于845af2b原生包，不能冒充最终修补包验收。
