# Mac15 Intel 同源码第二次运行证据

2026-10-24，对原失败 run39936378073 执行 `gh run rerun --failed --debug`。本目录只对应 **attempt2 / job120769897286**，源码仍为 `87b28a29aa84c2543b6b80b7e31204646e4fa76a`；没有修改产品、workflow、超时、重试或断言。

## 实际结果

[第二次运行](https://github.com/wangdayong228/bee/actions/runs/39936378073/attempts/2)最终 **success**。[run](run-final.json)、[jobs](jobs-final.json)及[环境原始记录](ci/native.json)绑定同一源码：macOS15.7.9 Intel、image20260824.0482.1、Xcode16.4/16F6、SDK15.5、Node24.22.1、Go1.27.3、Rust1.94.0，原生x64且无Rosetta。

| 检查 | 本轮证据 |
| --- | --- |
| Go | vet成功，完整7包测试ok，见[原始日志](ci/go-test.log) |
| 前端 | typecheck、普通/demo构建、tooling及bridge步骤成功，原始记录在`ci/` |
| 三浏览器 | [489 passed，13.9m](ci/browser-e2e.log)；[带时间戳日志](actions/browser-step.log)确认489项、2workers、无重试放宽 |
| Rust普通测试 | [40 passed / 0 failed / 2 ignored](ci/cargo-test.log)；这2项需要先构建签名App |
| 打包后签名测试 | [2 passed / 0 failed / 0 ignored](ci/signed-app.log)，包含真实包内Bee握手/ping/回收和篡改拒绝；上行2项在此执行，不当作仍被跳过 |
| App/DMG | demo开发包构建、Mach-O/source记录、产物上传全部成功；[包清单](ci/packages.json) |

[检查核对](checks-verification.json)13项断言通过。首次本地检查尝试读取未上传的`.last-run.json`而停止；ZIP确实不含该文件，记录于[检查准备说明](verification-preparation-note.json)。这不是产品测试失败，最终计数来自完整原始测试日志及对应成功步骤。

## 下载与独立包核验

同一run现在含两份同名checks；按artifact ID和创建时间区分，不能只按名称下载。[产物元数据](artifacts-final.json)保留旧artifact12496660787，未覆盖首次失败证据。

| attempt2产物 | ZIP字节 / SHA256 |
| --- | --- |
| test12547925393，创建04:12:19Z | 23,990,953 / `9ca5fb312213491cfd59c9ec3d940be8e8e0503e76487041c0e144c175c8a0b5` |
| checks12547234173，创建04:12:27Z | 108,318,068 / `5f71494c2e2265fe117040d2cd1b6a6c0a5ce6f24e1cce4e72dd9c405e057b0d` |

两个ZIP的大小、远端digest及全部CRC均独立核对通过，见[test核对](artifacts/12547925393-verification.json)、[checks核对](artifacts/12547234173-verification.json)。解包后的586份本地文件另有[字节清单](local-byte-manifest.json)，未把ZIP digest当作DMG哈希。

DMG为 **24,174,868 bytes / SHA256 `1a734744561a6d02b13bee2e02859461280a191c818a7aee4134ad6efadaf5f7`**。本机arm64主控仅做只读镜像检查，18项[包核对](package-verification.json)通过：

- DMG与远端packages.json大小/SHA相等，`hdiutil verify`成功。
- 只读、nobrowse/noautoopen挂载后，`codesign --verify --deep --strict`成功；App两主程序均为x86_64、minos13.0，Info.plist最低系统13.0。
- 包内签名Bee为32,695,168bytes、SHA256 `35276b2faabb4645aa4b5e6383f0a85accd5ce84cdf908c1d1fb10516ffea73d`，与runner记录相等；外置source JSON370bytes、SHA256 `4b5e8f22e0b9ea6850e2b4aa2d0b18df7858b8246258e2d410e61cfde07f538c`，完整source/TEE/target/Go字段均匹配。
- 镜像已成功卸载，见[卸载输出](local-package/dmg-detach.stdout)。没有在arm64主控执行Intel程序、安装App或操作桌面。

签名前Bee哈希与签后不同，分别保留在包清单中；没有拿签名前哈希校验签后文件。固定TEE revision和archive SHA仍为原批准值，见[TEE来源](ci/tee-source.log)。这是ad-hoc开发签名，不是生产签名或公证。

## 首次失败仍保留

[attempt1报告](../2026-10-23-p1-native-remote-87b28a2/README.md)的485/489、4例WebKit账号30s超时及原生步骤跳过不变。attempt2相同源码、相同2workers全套通过，只能说明本次未复现，**不证明旧超时已修复，根因仍未知**。[输入比对](input-comparison.json)核对了workflow、Playwright配置及accounts.spec.ts；当前检出HEAD不是此次运行源码，不外推为整个当前HEAD已完成Intel验收。

完整debug ZIP已下载并校验CRC，解出的Runner/Worker日志留在ignored QA缓存。[诊断检索记录](diagnostic-search-summary.json)保留两日志大小/SHA；均无CPU、Memory关键字或`Runner environment resources`采样。因此不能据此归因资源、睡眠、WebKit或产品，也不把本机休眠调查当作Intel原因。

仍未覆盖Mac13、GUI/托盘/关窗找回、干净用户安装、原生125%/150%显示、Downloads拒绝/取消或生产更新。P0/P1及任务6未完成的checkbox保持不变。

## 归档范围

[manifest](manifest.json)记录60份选定原始文件的来源、大小和SHA256；README/manifest不在这60份内。完整包、ZIP、586份解包文件及runner诊断日志留在`.cache/qa/p1-macos-intel-87-attempt-2-debug/`，不把二进制或重复视觉截图提交Git。正式产品、配置、原Mac arm64 App及既有改动均未修改。

3份Actions日志的空输出行带时间戳后空格，4份ci日志末尾有空行，均保留原始字节；不清理原始证据使其通过空白检查。排除这7份已逐字节核对的raw日志后，暂存差异空白检查通过；未改Git配置或跳过hooks。
