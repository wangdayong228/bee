# 原生诊断报告下载反馈

日期：2026-10-24。本机 macOS 15 arm64，源码 `2fcaa409df4cd2d6de66e1391bedce872e770024`。这是 P1 诊断导出反馈的增量验收，P0/P1 整体仍未完成。

## 问题与修补

旧 `87b28a2` 包在正常情况下能交付报告；相同字节副本在每进程 Downloads 写拒绝下，WebKit 明确报 `NSURLErrorDomain error -999`，页面仍仅提示“已发起报告文件下载”。[旧包负向观察](raw/21-negative-observation.json)、[原生 stderr](raw/14-sandbox-app.stderr)、[旧页面截图](raw/19-negative-bottom.jpg)保留真实问题。

`2fcaa40` 使用 Tauri `DownloadEvent::Finished.success` 回传结果，页面先订阅，再按本次 Blob URL 等待回执；完成、失败与 30 秒无回执分别反馈。普通浏览器只报告“发起”。未新增依赖、文件写入命令、权限或目的地规则。macOS 的 `path=None` 不用于判断失败。

[独立审查](review.md)首次发现监听注册失败会遗留 JS callback；连续三次失败的真实红灯后，修补持有 callback ID 并清理，保留原 cause。窄复核 Approved，I1 关闭，无新增问题。

## 新包原生正负对照

| 场景 | 直接证据与结果 |
| --- | --- |
| 正常导出 | [完整 AX](raw/52-fixed-positive-full-ax.txt)、[截图](raw/52-fixed-positive.jpg)显示“脱敏报告已下载。”；Finder 精确选中文件后只复制该报告，[文件核验](raw/54-fixed-positive-verification.json)为 377 字节、白名单内容完全一致 |
| 写入被拒绝 | [临时 profile](raw/download-write-deny.sb)仅对这个进程拒绝 Downloads 写入；[副本字节/签名](raw/48-fixed-qa-copy.json)与正常包一致；[原生 stderr](raw/56-fixed-restricted.stderr)两次均报 `-999` |
| 失败反馈与重试 | 首次及真实重试后均明确失败，按钮仍可用；[完整 AX](raw/62-fixed-negative-full-ax.txt)、[截图](raw/62-fixed-negative.jpg)、[结果摘要](raw/64-fixed-negative-summary.json)保留；[Finder 报告名集合](raw/63-fixed-negative-reports.json)仍只有原四份，没有新报告 |
| 测试后恢复 | 正常正向实例与受限副本都通过真实菜单退出；[受限父898/子916回收](raw/65-fixed-restricted-exited.json)；重新启动正常包，[原生 ready](raw/67-restored-native-ready.txt)及[概览](raw/66-restored-overview.txt)可见，[新父3919/子3931](raw/68-restored-processes.json)保留供使用 |

两份本轮实际交付报告均为 377 字节，SHA256 `716ff7d89cc80a5fa275e1263fc59a431cbf4a7c14deb0de5c7590c65354eabd`：[旧包报告](<positive-report/bee-demo-diagnostics (2).json>)、[新包报告](<fixed-positive-report/bee-demo-diagnostics (3).json>)。内容只有 product/mode/checks/logs 白名单。终端直接读取 Downloads 被 TCC 拒绝，[实际错误](raw/08-downloads-explicit-before.json)保留；文件存在与交付依据 Finder 和精确复制后的文件核验，不依据空 glob。

此负向对照是临时进程写拒绝，**不能代替真实用户 TCC 拒绝或保存对话框取消**。未修改全局 TCC、系统权限或原型基线。托盘、非侵入式关窗画面、其它 OS 的原生下载反馈仍未验收。

## 测试、构建与失败记录

| 检查 | 实际范围 |
| --- | --- |
| 行为红灯 | [首组](raw/24-native-download-red.log)、[五组](raw/25-native-download-all-red.log)；[首轮绿色尝试](raw/26-download-green.log)为 120 通过/3 失败，暴露英文选择器与两句漏译，保留失败 |
| 页面回归 | [123/123](raw/29-download-final-green.log)，覆盖三浏览器的下载和诊断/设置相关回归；发生在 callback 清理修补前，不冒充最终全套 |
| 审查修补 | [callback 泄漏红灯](raw/33-callback-leak-red.log)后，[最终下载专项15/15](raw/34-download-cleanup-green.log)，Chromium/Firefox/WebKit 每端5组 |
| 最终静态与桥 | [typecheck](raw/35-typecheck.log)、[桥10/10](raw/41-bridge-final.log)；[普通构建](raw/27-build.log)与[demo构建](raw/31-build-demo.log)为清理修补前；最终打包内部也重新执行当前源码 demo 构建 |
| Rust | [普通40通过/2忽略](raw/32-rust-tests.log)；Rust 产品代码与最终提交相同。最终签名包另跑 [signed2/2](raw/46-signed-tests-green.log)，含真实包内 Bee 握手/ping/回收及篡改拒绝；不能将两条命令合称一次42全绿 |
| 最终开发包 | [签名 App 与 DMG 构建](raw/44-signed-app-dmg-build.log)、[签名/minos/来源及哈希](raw/45-packages.json)、[DMG完整性 VALID](raw/47-dmg-verify.log) |

准备失误也保留：首次 sidecar 测试未指定 `RUSTUP_TOOLCHAIN`，仅停止自有卡住的 rustc proxy，随后固定工具链重跑，[说明](raw/28-preparation-correction.json)、[失败](raw/28-sidecar-test-build.log)、[成功](raw/30-sidecar-test-build.log)。首次打包遗漏既有 `APPLE_SIGNING_IDENTITY=-`，[seal 拒绝](raw/43-unsigned-package-rejection.json)和[40通过/2失败](raw/42-rust-with-signed-package.log)保留；该未签名包没有启动，重新正确签名后才做上述原生正负对照。没有放宽来源或签名门禁。

最终本机工具环境沿用锁定 Node24.22.1、Go1.27.3、Rust1.94，`CARGO_HOME=$PWD/.cache/cargo-home`，`MACOSX_DEPLOYMENT_TARGET=13.0`，`APPLE_SIGNING_IDENTITY=-`，取消外部 `GOROOT`。打包命令：

```sh
npm --prefix desktop run tauri -- build --debug --ci \
  --config src-tauri/tauri.demo.conf.json --bundles app,dmg -- --locked --offline
```

App 主二进制 27,663,216 字节，SHA256 `94751aa598e2a3c4c40316dd80252fcc70767a5ee26b4dc42ae0ab21481bb192`；签名后 Bee 为 30,630,144 字节，SHA256 `f1c0f1dd20a2bdea2dcda67800a710254e48ab9994a8576ba4c8c99eb2b1656e`。DMG 为 22,900,410 字节，SHA256 `03eb0ec6136798e289a29e66996de376d7849d3c992e07e9524b552ba6cf7ec1`。[sidecar 来源](bee-aarch64-apple-darwin.source.json)绑定完整 `2fcaa40` 和既有固定 TEE。两个 Mach-O 的 minos 都为13.0，仅证明产物标记；App 使用 ad-hoc 签名，DMG 本身未签名；不代表生产签名、公证或 macOS13 实机通过。

## 三端补验状态与归档边界

`2fcaa40` 已推个人 fork，触发 [Mac Intel](https://github.com/wangdayong228/bee/actions/runs/40079654076)、[Linux 四环境](https://github.com/wangdayong228/bee/actions/runs/40079654195)、[Server2022](https://github.com/wangdayong228/bee/actions/runs/40079654094)。归档时运行中；不使用旧87/9通过替代新源码结果，最终结果另行补证。

[manifest](manifest.json)记录81份原文件的相对来源、字节数和 SHA256，复制不修改原始字节。只保存本轮报告元数据，不保存 Downloads 其它用户文件名。App/DMG留在忽略的 QA/构建目录，不作为文档提交。全部验收结论限定于各日志绑定的源码、运行阶段与工具，计划未完成格不变。
