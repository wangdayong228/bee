# Mac关窗找回补验：工具未取得窗口

2026-10-24，目标为原87b28a2开发App；本轮没有构建新包。启动前没有匹配的App/管理进程，包文件SHA与既有87 packages.json相符，codesign深度严格校验exit0。

CUA按精确App路径启动后，App父66092及其owned管理子66099存活；两次getApp均返回`Computer Use server error -10005: cgWindowNotFound`，listApps仅确认isRunning=true，没有窗口记录。独立Finder目标同样cgWindowNotFound，Dock目标timeoutReached。工具没有提供Mac显式launch_app能力，未使用其它桌面控制机制绕过。

因此关窗、隐藏与找回动作未执行，也没有新的截图或native ready结论。不能把进程存活当成窗口可见，不能据此判断产品回归、系统锁屏、权限或沙箱根因。此前87真实窗口和菜单退出证据仍只适用于原验证时点。

清理时重新核对本轮唯一父进程精确可执行路径与子进程PPID/命令，只对父66092发SIGTERM；父和owned子66099随后均不存在。没有按名称终止其它Bee，不将清理当作菜单退出验收。本轮关窗找回保持未通过。

原始进程/包字节记录见before-processes.json，CUA错误逐项记录见attempt.json，定点清理见cleanup.json。manifest保存原字节大小/SHA及来源。
