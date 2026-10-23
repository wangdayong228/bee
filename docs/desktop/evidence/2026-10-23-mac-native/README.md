# 当前 Mac 自动验收证据

日期：2026-10-23。环境：macOS 15.7.7 arm64，当前开发包 `Bee Dev.app`，Tauri 原生 WebView。使用用户授权的电脑控制工具真实点击和输入；图片只包含 Bee 窗口，未使用浏览器替身制作原生截图。

- `minimum-ready.jpg`：拖动到批准的逻辑 860×600，Retina 截图 1720×1200；真实握手 ready、版本和按钮完整可见。
- `background-return.jpg` / 对应 AX：App 已运行时，Safari 经系统协议投递普通测试参数；页面显示“已收到登录返回”，仍是“尚未开始贡献”。App/owned Bee 仍为原 PID 25143/25179。
- `cold-return.jpg` / 对应 AX：通过 App 菜单退出并确认两个进程消失，再由 Safari 经系统协议启动 App；读取窗口前已用只读进程检查确认 App/owned Bee 新 PID 34970/35004，避免观察工具自身启动 App 而冒充冷回跳。
- `minimum-ping.jpg` / 对应 AX：冷回跳后再缩到 860×600，实际点击“检查存活”，页面显示“管理进程响应正常”；完整内容可见并有原生滚动入口。
- `browser-native-unavailable.txt`：Ego 普通浏览器打开本地 Vite 并点击“重新检查”；明确返回 NATIVE_UNAVAILABLE，未模拟原生成功。任务空间已关闭，临时 Vite 已退出。

当前签名 App 主程序 SHA256：`b6b4fb0866f99e37745295487e85cc6b4e8e7284eac2368482f694ee940adda1`；包内 Bee SHA256：`f34969cfe6cf849a75cbf8a73a78f73ce1851e271ff9ea9071ac228b4a617738`。截图均为工具返回的原始 JPEG，哈希见 manifest；AX 文件只保存 Bee 可见文本。

以上不是完整三端、托盘、重复 GUI 实例、最低 OS 或干净用户安装验收。后台回跳和冷回跳的完整 URL/code/state 未进入 Bee 截图或前端 AX；它们只验证 P0 boolean 收据，不代表真实登录。
