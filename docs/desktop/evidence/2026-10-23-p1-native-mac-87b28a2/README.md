# 87b28a2 Mac arm64 原生回归证据

精确源码 `87b28a29aa84c2543b6b80b7e31204646e4fa76a`；Mac15.7.7/arm64、SDK14.4。此提交仅将窗口发现逻辑测试改用可控时钟，公开生产wrapper仍使用真实Instant/sleep，生产预算与发送至多一次保持。修补报告及独立Approved审查见同目录clock文件，跨任务约束不能由此窄diff新增证明。

- preflight、固定TEE原生Bee构建、P1演示App/DMG构建实际退出0，命令/时间见 `commands.json`。codesign deep/strict及App与Bee minos=13.0均核验；只证明产物标记，不是Mac13运行证据。Info.plist Downloads用途与源一致。
- 完整Rust含signed测试：42 passed、0 failed、0 ignored，4.21s；包含真实包内Bee握手/ping/回收、签名seal篡改拒绝与新deadline边界测试。完整日志与退出码均保留。
- DMG 22,892,856 bytes，SHA256 `1c47faa7ee05393ca03aac95ce62eff4e70fa9b71997191540869a053331677b`；hdiutil verify通过。App/DMG为开发ad-hoc包，未公证、未生产签名，二进制只留本机cache。
- CUA精确App路径真实启动、缩到860×600（Retina1720×1200），`tauri://localhost`连接详情显示native manager ready、真实供给未由演示启动；Escape关闭后焦点回到连接详情触发器。截图/AX保留，不重复旧版本五页/资金/导出矩阵。
- 真实系统菜单退出后parent53551/owned53566均消失。独立空闲Bee desktop夹具56027仍响应alive=true、实例一致，随后由夹具正常shutdown、退出0；全部三个QA进程已清理。该夹具不读取账号/配置、不连Hive或供给；不解释2681中旧用户Bee70292缺失原因。
- 关窗按钮及Cmd+W后清单显示App仍运行，但随后的工具观察仍返回窗口；SystemUIServer工具timeoutReached。因此不宣称隐藏可见状态或托盘找回通过，不据此猜测产品隐藏失败或关闭权限保护。

2681导出与英文设置的实际验收保留原版本证据；87没有重跑它们。Mac13双架构、Win10/11官方来源/GUI、干净用户安装、原生缩放与托盘等完整矩阵仍未覆盖。87远端CI另行按新source收证。

本目录保存精选原始字节及manifest大小/SHA256；截图由magick实际识别，未将物理像素当逻辑窗口。历史失败日志仍保留于各自版本目录，不用新结果覆盖旧RED。
