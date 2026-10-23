# P1 三浏览器页面验收证据

本目录保存可提交的日志、48 张代表截图、5 张人工比对截图、失败 trace 及完整截图清单。完整 558 张截图保存在本次实施检出的 `.cache/qa/p1-browser-c4a5540/screenshots/`；它是持久本地证据，不随 Git 分发。每浏览器 186 张，原始清单的 SHA256 已逐项核对。`matrix-manifest.json` 为全部截图补充尺寸、语言、主题及内容缩放；`selected-screenshots.json` 列出本目录实际提供的 48 张。

## 绑定源码及实际结果

| 范围 | 实际结果 | 原始日志 |
| --- | --- | --- |
| Task6 页面最终完整三浏览器回归 | 414 passed，4.5m；每浏览器138项 | `browser-e2e-final.log` |
| 完整回归之前的 Firefox 动态翻译问题 | 410 passed / 1 failed，保留失败与 trace；之后修复 | `browser-e2e-before-translation-fix.log`、`firefox-missing-transfer-translation-red-*` |
| 完整回归之后仅补错误实际 count 诊断的定点覆盖 | 三浏览器3 passed | `client-after-error-evidence-copy.log` |
| Important I1：完成后旧生命周期请求破坏新状态 | 未修源码6 failed / 3 passed；修补后三浏览器96 passed，53.6s | `i1-red.log`、`i1-green.log` |
| I1 同一源码类型及两种前端构建 | typecheck、build、build:demo退出0 | `i1-typecheck.log`、`i1-build.log`、`i1-build-demo.log` |
| Node系统桥回归 | 10 passed | `bridge.log` |

页面与截图归入 `4a521448..c4a5540b` 实施范围。414项和截图来自错误诊断文案最后调整之前的页面实现；该文案调整以随后3项专项覆盖，没有宣称又跑过414全套。I1 修补基线 `6488ca35`，提交 `79193cab67190b9bc8ec4dd8c90672de3890f0e9`；仅修改演示客户端和生命周期回归，独立复核确认 I1 关闭。96项是最新生命周期专项，不等于最新完整页面套件。

## 覆盖与复核

三浏览器为锁定 Chromium、Firefox、WebKit。覆盖1280×860、1024×768、860×600中英文，以及最低尺寸深色、125%/150%内容缩放；五页、引导、账号抽屉、报价/划转/提现、退出/更新与未知状态均有截图。自动断言整窗无横向裁切、金额不拆位、账号按钮不越行容器，弹层键盘焦点与金融操作可达。

`screenshot-manifest.json` 原样保留绝对 `/tmp` 路径和截图 SHA。`matrix-manifest.json` 根据当时测试标题及已锁定 Playwright 的相同路径转换函数重建54个实际目录，并逐项检查存在性。`manifest.json` 记录本目录分发文件的相对路径、大小和 SHA；完整本地证据另有 `archive-manifest.json`。本目录不包含所有558张原图，不能把完整清单误认为全部原图已提交。

这些结果只证明演示网页层。CSS内容缩放不代表原生显示缩放；Playwright WebKit不代表Linux WebKitGTK或macOS WKWebView。原生App/DMG/NSIS/AppImage、托盘、干净用户安装和最低系统的实际运行另行记录，不能从本目录推断通过。
