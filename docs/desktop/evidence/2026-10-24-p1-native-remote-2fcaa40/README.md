# 2fc 三端原生构建补验

日期：2026-10-24。绑定产品源码 `2fcaa409df4cd2d6de66e1391bedce872e770024`，固定 TEE `a687f86d781e825c04c1d84d75b41bba5d862254`。原生下载回执修补后的新源码已在本机 Mac arm64 实测，本目录补齐新源码的托管构建；P0/整体 P1 仍未全部验收。

## 工作流与实际结果

| 环境 | 工作流 | 已核对结果 |
| --- | --- | --- |
| macOS15.7.9 Intel | [40079654076](https://github.com/wangdayong228/bee/actions/runs/40079654076) | success；Go7包、三浏览器504/504（15.2m）、普通Rust40通过/2忽略；App打包后signed专项另2/2，开发App/DMG成功 |
| Windows Server2022 x64 | [40079654094](https://github.com/wangdayong228/bee/actions/runs/40079654094) | success；原生Rust31/31，真实原生Bee握手/ping/stop、开发NSIS构建通过 |
| Ubuntu22 x64 | [40079654195](https://github.com/wangdayong228/bee/actions/runs/40079654195) | success；Go7包、三浏览器504/504（11.0m）、Rust36/36、AppImage及extract/FUSE启动通过 |
| Ubuntu24 x64 | 同上 | success；Go7包、三浏览器504/504（10.0m）、Rust36/36、AppImage及extract/FUSE启动通过 |
| Ubuntu22 ARM64 | 同上 | success；Go7包、三浏览器504/504（8.9m）、Rust36/36、AppImage及extract/FUSE启动通过 |
| Ubuntu24 ARM64 | 同上 | success；Go7包、三浏览器504/504（8.8m）、Rust36/36、AppImage及extract/FUSE启动通过 |

[最终状态快照](snapshot-latest.json)与[运行绑定](runs.json)保留全部run/job ID；`metadata/` 是五条工作流的最终run/jobs/artifacts API字节。常规 [Bee checks 40079654116](https://github.com/wangdayong228/bee/actions/runs/40079654116) 和 [Windows固定TEE 40079654112](https://github.com/wangdayong228/bee/actions/runs/40079654112) 也成功，原始完整日志在 `actions/`。Mac/Linux各自typecheck、普通构建、tooling37/37、bridge10/10通过。Windows本入口没有浏览器E2E，不把其它runner的504算给Windows。

可直接复核：[Mac browser](macos-intel/ci/browser-e2e.log)、[普通Rust](macos-intel/ci/cargo-test.log)、[包后signed](macos-intel/ci/signed-app.log)、[Windows Rust](windows-server2022/ci/cargo-test.log)、[Linux22 x64 browser](linux/ubuntu-22.04/ci/browser-e2e.log)、[Linux24 x64 browser](linux/ubuntu-24.04/ci/browser-e2e.log)、[Linux22 ARM browser](linux/ubuntu-22.04-arm/ci/browser-e2e.log)、[Linux24 ARM browser](linux/ubuntu-24.04-arm/ci/browser-e2e.log)。Rust40与signed2是两条实际命令，不能合称一次42全绿。

## 下载包与来源

六个安装包均按实际下载字节核对大小/SHA256，再与同run的packages或smoke报告、sidecar来源JSON关联。[汇总核验](artifact-validation-latest.json)保留原始测试计数、包hash、source与八次smoke记录；[Windows专项核验](windows-verification.json)额外核对两个artifact中的packages JSON一致及source JSON字节hash。

| 包 | 字节数 | SHA256 | 归档核验记录 |
| --- | ---: | --- | --- |
| Windows Server2022 x64 | 16,283,129 | `7e438882726cd8c731f61eee97e38521811634cd3862e84aff64303ddb56ee61` | [ZIP核验](artifacts/12554593556-verification.json) |
| Ubuntu22 ARM64 | 139,008,520 | `bcc44a17cb577f5155a49b6a7ac26a10bac9fb93a36c1687d5e0418774cd2515` | [ZIP核验](artifacts/12554669640-verification.json) |
| Ubuntu24 x64 | 148,937,208 | `2575c8600863bc55ac49292f20ba019ef5c086933050ed2f5dc6ca2e1b8d6436` | [ZIP核验](artifacts/12554698128-verification.json) |
| Ubuntu24 ARM64 | 139,131,400 | `49eede2f660a8ee980a87e3cd81e330e71eed37b040b557cca8fbf78471f1be7` | [ZIP核验](artifacts/12554749531-verification.json) |
| Ubuntu22 x64 | 148,699,640 | `f95a03e00a7efe05e7965ef334cd0e70fe9eb9ac325b7b0645f6bb8777301fec` | [ZIP核验](artifacts/12555291607-verification.json) |
| macOS15 Intel | 24,182,525 | `f7e2eda347c3f476a7907831e724672998dd79a8752e971a31e399b580a0fbad` | [ZIP核验](artifacts/12555641370-verification.json) |

Mac/Windows包的来源在各自 `source/` 与 `test-packages.json`；Linux四行来源在 `linux/<runner>/source/`。均绑定完整2fc、原固定TEE及原生目标。部分Bee版本字符串带 `-dirty`，按实际值保留；未采样CI全工作树状态，不由revision/hash记录推出“整个CI检出始终无修改”。未改变源码/测试预算/工作流，不把文档提交SHA冒充打包源码。

## Linux启动观测与清理限制

八次extract/FUSE观测均为860×600，resize后的观察时间分别为10,188–10,313ms，末次geometry与owned存活复核通过。主控逐张查看了八张末次原图，均为清晰的英文演示概览，保留“贡献未开始/真实供给未启动”。初图仍按原始字节保留，不用初图代替末图。

| runner | extract末图 | FUSE末图 | 清理记录 |
| --- | --- | --- | --- |
| Ubuntu22 x64 | [原图](linux/ubuntu-22.04/ci/smoke-extract/startup/window.png) | [原图](linux/ubuntu-22.04/ci/smoke-fuse/startup/window.png) | 两次liveRemaining空、无zombie |
| Ubuntu24 x64 | [原图](linux/ubuntu-24.04/ci/smoke-extract/startup/window.png) | [原图](linux/ubuntu-24.04/ci/smoke-fuse/startup/window.png) | 两次liveRemaining空、无zombie |
| Ubuntu22 ARM64 | [原图](linux/ubuntu-22.04-arm/ci/smoke-extract/startup/window.png) | [原图](linux/ubuntu-22.04-arm/ci/smoke-fuse/startup/window.png) | extract无zombie；FUSE留1条PID1的WebKitWebProces zombie（PID51909） |
| Ubuntu24 ARM64 | [原图](linux/ubuntu-24.04-arm/ci/smoke-extract/startup/window.png) | [原图](linux/ubuntu-24.04-arm/ci/smoke-fuse/startup/window.png) | 两次liveRemaining空、无zombie |

每模式 `smoke.json` / `startup/observation.json` 保留时间、进程、截图、来源与信号清理；八次parentClosed均true，不能因此声称“无任何后代残留”。这些是Xvfb客户端启动/尺寸观测，SIGTERM清理不等于原生菜单退出；不证明WM标题栏、托盘点击、业务ready或干净用户安装。旧87/9的失败与zombie记录保留，不用本次结果反推旧问题已修复。

## Intel镜像只读复核

[本机只读核验](intel-dmg-verification.json)共9条命令检查通过：DMG checksum、禁止自动浏览的只读挂载、App deep/strict seal、两二进制x86_64及minos13.0、签名后Bee字节/SHA与runner报告一致、卸载及卸载后的新鲜inventory。bundleID、Downloads用途说明和最低系统配置也核对。库存只保存本次镜像是否仍挂载的过滤结果，不归档其它镜像信息。

主控未执行Intel代码、未操作Intel GUI。App为ad-hoc签名，DMG本身未签名，未公证或生产签名；minos13.0不代表Mac13实机通过。

## 证据与剩余验收

[manifest](manifest.json)记录276份选定原文件的相对来源、字节数和SHA256。12个ZIP均匹配GitHub digest/size，CRC通过，解包3030份文件各有SHA256记录；这些全量列表在 `artifacts/`。App/DMG/AppImage/NSIS、ZIP与完整浏览器report留在忽略的QA目录，Git中保存选定CI目录和核验记录，原始字节不改写。

下载辅助脚本首次采用180秒整包下载，后保留partial并改为官方artifact续传；一次局部变量遮蔽令核验记录写入失败，修补后重新核验完整ZIP，未重下已完成字节。[准备说明](download-preparation-correction.json)保留，最终收证命令exit0；这些不是产品或CI失败。`verification/`保留本轮QA脚本的原始字节；复现脚本需使用manifest所指的原QA目录布局与忽略的完整产物。[下载脚本](verification/collect-artifacts.py)的凭证与临时签名URL仅在进程内存/stdin使用，不归档其值。

[本机原生报告成功/写拒绝失败反馈](../2026-10-24-p1-native-download-feedback/README.md)独立保留。真实TCC用户拒绝/取消、其它OS的原生下载交互、Mac13双架构、Win10/11官方来源/GUI、Ubuntu真实桌面托盘/WM、干净用户安装、Applications拖拽、原生缩放与生产签名/公证仍未验收。87 Intel旧四例WebKit超时根因仍未知，本次2fc通过不充当旧问题的修复证明。所有P0/P1剩余checkbox保持未勾，不进入整计划finishing。
