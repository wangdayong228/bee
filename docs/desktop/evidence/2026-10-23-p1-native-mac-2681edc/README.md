# 2681 Mac arm64 原生修补与导出验收证据

绑定源码 `2681edca2c56bca9d2ce30db4198fb5784d98b65`；macOS15.7.7/24G720 arm64、SDK14.4。仅 P1 演示开发包/ad-hoc签名；未开始真实贡献、资金或账号授权。

## 已实际验证

- preflight、固定TEE sidecar及App/DMG构建退出0；codesign deep/strict通过，App与包内Bee实际minos均13.0。signed专项2/2通过；不代表Mac13实机或全套Rust复跑。
- DMG 22,892,859 bytes，SHA256 `5ad9e81dd61e4e4262b88a12e75d7a12df3d4dd9aa27071f02a3d243a0b34b75`。包原件留本机cache，不提交二进制。`packages.json`保存App、Bee、来源和系统实值。
- 最小860×600真实WebView中英文设置完整回执与Off placeholder可读，`native-settings-en-860-bottom.jpg`与`native-settings-en-860-proxy.jpg`两张860×600原图已独立视觉复核Approved、C/I/M均0，见 `native-settings-copy-review.md`。另存的`native-settings-en-final-*`是1000×700位置截图，不把它们标成最小窗口复核图，不覆盖历史。
- 实际Info.plist合入NSDownloadsFolderUsageDescription，与源配置一致。点击演示报告导出最终交付两份377字节JSON；精确内容、mtime和SHA核验见 `native-export-file-verification.json`。SHA均为 `716ff7d89cc80a5fa275e1263fc59a431cbf4a7c14deb0de5c7590c65354eabd`。
- 导出首次工具14.168s返回noWindowsAvailable后，系统17:32:29明确记录Downloads授权Allowed，主线程恢复正常事件循环。第二次导出工具约0.8757s返回、界面继续可操作。代理未点击系统授权，也未修改TCC；未拍到提示或证明允许动作来源，不能宣称首次授权全自动完成。只归档本事件精简TCC片段和主线程片段，完整系统日志留本机。
- 终端直接读取Downloads中生成报告曾PermissionError；经CUA Finder只选择这两份报告、普通复制到专用cache后完成字节/白名单校验。未扫描或归档其它Downloads内容，没有授予终端全盘访问。
- 真实Bee Dev菜单退出后测试parent6842/owned6847均消失。原用户Bee70292在导出前仍存在、退出后核对已不存在，**来源未建立，保留断言未通过**；代理没有对它发signal或自动重启。不得沿用旧b94“原Bee保留”结论解释本轮，见 `native-menu-exit-result.json` 与 `process-exit-summary.json`。
- DMG verify后只读挂载，ditto复制App到带空格QA路径，Info与两个可执行文件字节匹配、签名通过、已卸载卷；CUA精确副本路径启动显示native manager ready，真实供给未启动。真实菜单退出parent36844/owned36961均回收。此项是QA目录复制启动，**不是Finder拖入Applications或干净用户安装**，见 `dmg-copy-verification.json`。
- 演示语言/主题恢复跟随系统，全部测试App已退出。未改系统代理、开机启动或账号。

## 未验证与历史边界

旧b94导出挂起RED保持独立归档；新版本Allowed及实际文件交付不能改写旧结果。Downloads拒绝/取消、干净用户首次授权、原生下载完成/失败反馈尚缺；当前UI“已发起下载”不等于原生Finished反馈已接入。

关窗隐藏→托盘找回、完整原生缩放矩阵、Mac13双架构、Win10/11官方来源/GUI、干净安装仍缺。源码87b28a2的确定性测试修补不属于此2681包。

归档文件按原字节复制；`manifest.json`含除自身外的SHA256与大小；`complete-local-cache-manifest.json`记录本机原始顶层cache，包含未归档的原始日志元数据。截图格式/尺寸由magick实际识别，见 `screenshot-dimensions.json`。所有持久证据都只覆盖所列源码与运行范围。
