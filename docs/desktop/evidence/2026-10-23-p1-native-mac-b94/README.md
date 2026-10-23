# b94 Mac arm64 原生 P1 演示验收证据

绑定源码 `b94bc6b56eae1f5045ec57e7bcd731bb07ee93bc`；实机 macOS 15.7.7（24G720）/arm64，SDK14.4。Node24.22.1、Go1.27.3、Rust1.94.0；固定TEE a687f86d781e825c04c1d84d75b41bba5d862254，archive SHA256 4bc9caad3ad2ce5de01b9983a750cee6380098fc308333c30c098fbf8e7bad38。仅开发包、ad-hoc签名；无生产签名、公证或真实业务操作。

## 已实际通过

- 原生sidecar与演示 `tauri build --debug --ci --config src-tauri/tauri.demo.conf.json --bundles app,dmg -- --locked --offline` 成功，保留App与DMG两个bundle。签名deep/strict验证成功，App与包内Bee实际LC_BUILD_VERSION minos均13.0；这不是Mac13运行证据。
- 完整Rust `--include-ignored --nocapture`：41 passed、0 failed、0 ignored（24.53s），包含签名包真实握手/ping/回收及seal篡改拒绝。
- CUA连接精确最终App路径成功，真实WebView URL为tauri://localhost。窗口从1000×700缩至860×600逻辑尺寸；本批19张JPEG均1720×1200物理像素（Retina2x）。最早两张误标.png已仅改扩展名为.jpg，字节保留；没有把JPEG按PNG头解析所得垃圾尺寸用于证据。
- 中文深色五页；英文浅色五页，英文深色设置；详情抽屉到底可滚动，Tab停留于唯一关闭按钮，Escape关闭后焦点回到触发按钮。报价保存/放弃在页底可达，资金确认框在最小窗内可见。
- 纯演示划转1.234567891 USD：128.56→127.325432109，24.6→25.834567891，回执DEMO-TR-1。提现提交返回“暂不支持提现”；未显示成功或扣款。重启演示数据重置，未触发真实资金。
- 连接详情显示真实Native manager ready，演示业务连接独立，真实贡献未启动。零任务Exit demo/Update demo仅完成演示流程，真实App仍运行；未安装软件。
- 真实Bee Dev菜单“退出”：parent35455与ownedBee35471均消失；用户原Bee70292（10月20日启动）仍在。此项不同于演示退出。测试前后进程原文与JSON在同目录。
- 验收期间更改的演示语言/主题均恢复为跟随系统，未改系统主题、代理、开机启动、通知权限或官方账号。

## 仍有RED或未证明的项目

报告导出：真实点击后CUA noWindowsAvailable/timeout；pid19199与owned19206仍在。两次sample分别为16:15:43.878与16:16:43.577，主线程停在WebKit download_policy→SandboxExtension→_sandbox_extension_issue→__mac_syscall。有限TCC日志显示Downloads授权Unknown→Prompting，并缺NSDownloadsFolderUsageDescription；不能说Downloads被拒绝，也不代表App启用了App Sandbox。尚未证明系统提示可见性/决定/返回或实际文件交付。

恢复仅SIGTERM精确测试parent19199；parent与owned19206随后均消失，原Bee70292保留。完整采样和有限TCC日志留本机cache，原始SHA列在complete-cache-manifest.json。后续用途说明配置修补必须在新source单列，不能改写此b94 RED。

真实关窗：点击close和系统快捷键后的工具观察仍返回窗口，无法在本轮证明隐藏→找回的可见状态转换；不据此声称托盘/关窗验收通过。截图或AX可能触发重新激活，原因本轮未证明。App菜单本身已看见“打开 Bee”和“退出”，不等于托盘已验。

英文设置回执存在binding.System连写及后半句语法不完整，原图和AX保留。该Minor后续修补应单列来源，勿覆盖旧图。英文Hive address的演示字符串是输入值而非普通文案，本批截图未滚到该字段，不外推为可见图形缺陷。

本批不覆盖Mac13双架构、Win10/11官方来源/GUI、Linux页面操作、干净用户安装、全部托盘/无托盘和原生125%/150%显示缩放。网页CSS zoom和旧包不能代替。

## 包与复现

b94 DMG：22,892,515 bytes，SHA256 `74b11b7888be43806d5ce54ae56f28dcc21ee2745a00ca5bcaa96a39d83afc20`。原件在本机 `.cache/qa/p1-native-local-final/packages-b94bc6b/`，不提交二进制。完整App/sidecar/DMG哈希与实际最低版本见packages.json。

同时保留旧DMG-only构建exit0却删除.app的日志，以及完整Rust39pass/2missing-App RED；修补为app,dmg后41/41 GREEN。远程旧Mac run在打包前取消，不能说远端复现同一RED。

归档文件按原字节复制；manifest.json包含本目录除manifest自身外的SHA256和bytes。complete-cache-manifest.json是本机完整原始cache文件清单，含未持久复制的额外截图与采样。截图格式/尺寸由magick实际识别，见screenshot-dimensions.json。AX文本中的窗口开发标题保持原生壳既有中文，不把它外推成所有系统语言本地化通过。
