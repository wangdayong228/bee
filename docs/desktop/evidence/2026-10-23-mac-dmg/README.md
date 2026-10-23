# Mac 实际第二实例与 DMG 安装验收

2026-10-23，在当前 macOS arm64 开发用户环境自动执行。文件 SHA256 见 [manifest.json](manifest.json)。原始截图为 JPEG。

- [第二实例进程收据](duplicate-processes.json)：对原签名 App 的确切可执行文件启动第二个真实原生进程，PID 64857 退出 0；主进程 34970 与其 Bee 35004 保持不变，15 次进程采样均只有一个管理子进程。随后原窗口仍显示就绪并可真实 ping，见 [窗口截图](duplicate-window.jpg)和 [AX 收据](duplicate-window.ax.txt)。这次使用实际 GUI App，不是 MockRuntime；关窗后的 AX 读取可能激活窗口，因此不据此断言隐藏可见性。
- Tauri 生成开发 DMG，22,837,507 字节，SHA256 `c4c663e253c22a62d55d1f8aa16073dc9ce8e1e23aa1c1293a1f5f508c59e6a9`。`hdiutil verify` 通过，只读挂载后用 `ditto` 复制到用户 Applications 下含空格的独立测试目录；未覆盖已有安装。见 [包与来源收据](package.json)、[DMG 校验](dmg-verify.log)和[安装副本签名校验](codesign-installed.log)。这验证复制安装，不冒充 Finder 拖动操作。
- 旧 App 及 owned Bee 退出后，CUA 启动安装副本；原生 WebView 显示真实握手，点击“检查存活”显示“管理进程响应正常”。见 [安装副本截图](installed-ping.jpg)和 [完整 AX 收据](installed-ping.ax.txt)。程序从复制后的 App 同目录启动 Bee，进程路径见 [退出前进程](processes-before-exit.json)。
- 通过 App 自身菜单退出，安装副本 87342 与 owned Bee 87427 均消失，见 [退出收据](exit-result.json)。测试目录保留供复查；未运行用户数据库、修改系统设置或发布软件。

两次验收对应不同构建：第二实例使用此前 App 主程序 SHA256 `b6b4fb0866f99e37745295487e85cc6b4e8e7284eac2368482f694ee940adda1`；本轮 DMG 中主程序为 `ffcb462486e553b4558e94dffd7a3c0dec8abcd857276f656cf6077e01694eb4`，包内 Bee 仍为 `f34969cfe6cf849a75cbf8a73a78f73ce1851e271ff9ea9071ac228b4a617738`。Tauri DMG 构建会清理临时 `.app`；已从同一 DMG 安装副本恢复构建目录的签名包，供签名包测试使用。

本轮未证明干净用户无开发工具环境、macOS 13 实机、Intel、Windows、Ubuntu 桌面或托盘。Control Center 可访问性读取超时，托盘继续标为未验证，不能将 App 菜单冒充托盘。开发包仅 ad-hoc 签名，未公证。
