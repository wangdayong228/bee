# 87b28a2 原生远程 CI 证据报告

精确源码 `87b28a29aa84c2543b6b80b7e31204646e4fa76a`，仓库 `wangdayong228/bee`，分支 `feat/bee-desktop-p0`；push事件2026-10-23T10:03:42Z。只读监控与下载，不更改源码/index/HEAD，不触发、重跑或取消CI，不执行本机产品构建/测试/GUI。

## 最终结论

| 平台 | 精确run | 当前结果与已核证据 |
| --- | --- | --- |
| Mac15 Intel | [39936378073](https://github.com/wangdayong228/bee/actions/runs/39936378073) | failure；WebKit4例30s测试超时，485通过/4失败；后续产品原生步骤全部skipped |
| Windows Server2022 x64 | [39936377992](https://github.com/wangdayong228/bee/actions/runs/39936377992) | success；NSIS/source/packages.json下载字节已独立核对 |
| Linux四行 | [39936378139](https://github.com/wangdayong228/bee/actions/runs/39936378139) | run cancelled；22x64/22ARM/24ARM success且包/source/provenance/smoke已核；24x64超90分钟job上限，原生步骤skipped |

证据目录 `.cache/qa/p1-native-remote-87b28a2/`。Windows验证摘要、三条Linux逐行验证摘要、Mac环境与失败分析均已落盘；全部完整raw job logs、最终run/jobs快照、未过期artifact metadata均已取得并核对精确run/source/branch。全部本轮实际artifacts已下载，Linux24x64仅有checks，无test包；本地全量字节清单与选定归档另见目录中的manifest。

独立Bee checks39936377907在相同source success，不替代三端原生workflow。2681/b94/e1与后续9ca837d保留各自目录；不继承不同source的通过结果、包或哈希。root另做的harness9/target87本机Docker补证不属于本轮原始CI证据。

## Windows 独立包字节核对

run39936377992 success。实际Server2022 Datacenter10.0.20348/ProductType3、CPU9/x64，image win22/**20261012.333.1**。Rust **31 passed / 0 failed / 0 ignored**；实际构建日志含 `vite build --mode demo`。workflow未在Windows运行Go全量或浏览器。

NSIS **16,280,031 bytes / SHA256 `5e7e5504ac75ddea1c0461a7eca1aa19f312d53877985ea968059abc3773e594`**，与两个packages.json一致。实际source.json原始SHA=`c7e790c4861c2f78d255fab7fb248dc34005b5ef160c3a16c9f87e402b5f4f42`，内容与manifest全等，完整87/固定TEE/Windows x64 target/Go1.27.3 windows-amd64匹配。runner观测原Bee SHA=`2cfd3dd0ff3724e06de1da2d8e9cbbcb3313f671a5fae3bf1d51e8a6ce1553b1`。

原Bee未独立上传；本机未提取NSIS payload、安装或执行EXE，不证明Windows10/11、GUI、托盘、菜单退出或干净用户安装。核对见 `windows/verification-summary.json`。

## Linux 三条完成行的独立核对

三条实际raw job log和下载browser/cargo日志均相互匹配：**489 browser passed、Rust36 passed/0failed/0ignored**；Go七个包均ok；实际执行 `vite build --mode demo`。

| 行 | 实际AppImage bytes | 本地包SHA256 | 本地source.json原始SHA256 |
| --- | ---: | --- | --- |
| ubuntu-22.04 x64 | 148675064 | `949c2f962051646c18d9cddaf5673e2bc77a9fccaed66aa4258da337fe2eaff0` | `90b6523f0a323e6198d211d98777ae9185a89bd545ebf964fef1988f2126c7a7` |
| ubuntu-22.04 ARM | 138983944 | `7bfc141be13704c273ad0c43e822cdda7a1017754ec1bfd292c139d3165378ec` | `26716ea8c9c1b9f22a1eefb2a8338accbca8cc83d3c5f0e95fbb294e134443ee` |
| ubuntu-24.04 ARM | 139078152 | `db710f967c04eb938affcb0db9fb3cfeac4460bc11c8b135082ba69e31fbe20a` | `f0c21ee7a01fe11f70759a69a093468a26a7883ccde0a95435708301ff481363` |

逐行只读Python断言exit0：native完整source/run/target/host/arch和全部checks正确；本地AppImage bytes/SHA与extract、FUSE两份报告相等；本地source.json原始SHA与smoke.sourceSha256相等，内容与provenance.source全等；完整87/TEE/target/GOOS/GOARCH正确；source.binarySha256、packagedBee.sha256、provenance.binarySha256相等。不能用远端ZIP digest替代包SHA。

| 行 | extract observedMs / zombies | 真实FUSE observedMs / zombies |
| --- | --- | --- |
| 22x64 | 10204 / 1条PID1 WebKitWebProces(pid49519, Zl) | 10161 / [] |
| 22ARM | 10266 / [] | 10169 / [] |
| 24ARM | 10288 / 1条PID1 WebKitWebProces(pid50059, Zl) | 10265 / [] |

六模式均observation.ok=true、parentClosed=true、liveRemaining=[]，SIGTERM结束。两条zombie原样保留，不等同“进程完全无残留”。六张最终window.png已逐张目视可见1000×700 Bee demo Overview非空内容（Demo data可见）；本轮未做最小窗resize。观测范围仅原生窗口启动≥10s；无交互/业务ready、托盘、菜单退出或干净用户安装验收。workflow没有对最终ELF执行RUNPATH实际测量，构建参数不替代测量。

### Linux24x64超时取消

job120356826767 completed cancelled。annotation原文为 **`The job has exceeded the maximum execution time of 1h30m0s`**，没有代理取消。step5依赖安装10:04:00–10:57:43（53m43s）；native环境checks和随后Go七包、前端/tooling成功。step10自10:59:24至11:34:04 cancelled，raw log显示仍在 `playwright install --with-deps chromium firefox webkit`；Chromium和Headless刚下载完成，Firefox155下载刚开始即取消，浏览器测试未实际执行。step11–15原生Bee/Rust、AppImage、extract/FUSE、test包均skipped。仅checks ZIP46050bytes，已核metadata SHA/size/CRC；无本轮AppImage或smoke结论。详见 `linux-ubuntu-24.04-failure-analysis.json`、原始job log与annotations。

## Mac 失败证据与边界

run39936378073/job120356825943 completed failure。实际macOS **15.7.9** Intel，image **20260824.0482.1**，Xcode16.4/16F6、SDK15.5、Node24.22.1 darwin/x64、Go1.27.3 darwin/amd64、Rust1.94.0 x86_64-apple-darwin；native环境JSON完整source/run和全部checks正确。Go七包ok，前端普通/demo构建、tooling/bridge步骤成功。

浏览器step10从10:11:01至10:47:11 failure，原始日志 `macos-job.log:731–867` 与下载browser-e2e.log一致：**485 passed / 4 failed (34.3m)**，均WebKit账号测试，`Test timeout of 30000ms exceeded`、`locator.click`：

| 测试声明行 / 实际失败点击 | 原始实际action阶段 |
| --- | --- |
| accounts.spec.ts:8 / helper:6 AI账号导航 | locator resolved，等待visible/enabled/stable |
| accounts.spec.ts:24 / helper:6 AI账号导航 | waiting locator |
| accounts.spec.ts:43 / :46确认换号 | 已visible/enabled/stable、scroll完成 |
| accounts.spec.ts:58 / :61移除账号 | 已visible/enabled/stable、scroll完成、performing click |

四份trace内嵌accounts.spec.ts均逐字节等于 `git show 87b28a29aa84c2543b6b80b7e31204646e4fa76a:desktop/tests/accounts.spec.ts`；原始SHA=`5de4fd365c6eee0be98782dbf9b7d4f4b7a91ad9f68ea3f04bfd2ed01d2c4d6f`。精确Playwright配置retries=0；其webServer timeout与test timeout分开。详细原始单调时钟时间线、library动作日志、runner错误Call log见 `macos-failure-analysis.json`。

以下秒数统一以runner `Before Hooks`开始为0，**不是精确charged timeout clock**：

| 测试声明行 | runner goto区间 | 前一导航点击区间 | 失败点击开始 / timeout后After Hooks开始 |
| --- | --- | --- | --- |
| 8 | 28.673–47.229 | — | 47.240 / 47.826 |
| 24 | 28.556–49.782 | — | 49.800 / 47.707 |
| 43 | 1.127–5.867 | 5.870–27.615 | 27.624 / 30.043 |
| 58 | 1.033–12.978 | 13.002–27.457 | 27.486 / 30.032 |

前两例含worker browser fixture17.783s/17.649s，不能把整个墙钟时长直接当30s预算。仅作算术诊断，扣去这段fixture后，第一失败click开始29.457s，第一/第二After Hooks开始30.042s/30.058s。第二例在goto尚未返回时先记录test-timeout error，随后click仅168.947ms即返回错误。第三、第四失败点击前，先前goto/点击已消耗大部分时间。timeout error事件本身无timestamp，After Hooks仅为其后的记录边界；不能据此还原精确charged deadline或单项click独立30s超时。library trace有尾事件未落盘，runner错误Call log另保留其更晚实际阶段。

**根因未知**。时间线只证明这些记录中的耗时和共用test deadline，不归因CPU、产品或浏览器实现。不改timeout/retry，不以旧b94单例多场景预算或2681 Rust helper失败作为本轮原因。

step11–15全部skipped：原生Bee/普通Rust、App/DMG、signed bundled Bee测试、Mach-O/package hash、test artifact。因此本轮Mac没有Rust通过计数、DMG、签名或Mach-O产品结论，不能用环境checks替代。也不证明Mac13最低基线、GUI、生产签名、托盘/菜单退出或干净用户安装。

## 固定TEE与本机下载中断

本轮实际构建依赖TEE revision=`a687f86d781e825c04c1d84d75b41bba5d862254`，archiveSHA256=`4bc9caad3ad2ce5de01b9983a750cee6380098fc308333c30c098fbf8e7bad38`；各实际TEE日志已核对。tooling测试临时fixture的其他TEE revision不作为产品构建来源。

22x64 test、22ARM checks/test、24ARM test的首次gh下载均 `unexpected EOF`；22x64第二次gh下载为read operation timed out。五次失败均保留精确artifact/source/error JSON，不等于CI失败。后续保留ZIP的三个ARM下载分别连续约6–10分钟无写入，记录大小/时长后只终止对应本地curl，确认其wrapper结束再从原部分ZIP续传；未取消CI或触及native产品进程，没有同一artifact并行重复下载。

恢复后的Mac checks、22x64 test、22ARM checks/test、24ARM test五个ZIP均已独立核对remote artifact metadata size/SHA256及ZIP CRC；再单独核对解包文件。两份首次正常完成的Linux checks和Windows artifacts也按其内部数据/本地包字节核对；不声称未保留ZIP的远端digest曾被本机重算。所有成功和失败记录保留，下载问题根因未知。

## 验证与一致性清单

全部87监控及下载进程已结束。通过实际下载字节与原始JSON/log断言后生成 `local-byte-manifest.json`，逐文件复核SHA/size；`p1-native-remote-87b28a2-archive-stage`仅原字节复制选定记录与最终截图，清单记录来源、大小和SHA。归档排除AppImage/EXE/DMG/ZIP和浏览器截图集合，完整下载仍留独立cache。

Consistency Checklist:
- ✅ 对话约束：完整source隔离，只读远端，无CI/源码/index/HEAD/native产品干预；本地下载恢复如实记录。
- ✅ 纵向：最终表、平台章节与失败/跳过范围一致；不再保留进行中结论。
- ✅ 横向：包字节、source、provenance、smoke、raw logs和平台摘要逐项相符；Mac四内嵌源码对比一致。
- ✅ 配置：未改配置；test timeout与webServer timeout、artifact ZIP与产品包SHA明确区分。
- ✅ 文档：Mac未知根因、Linux90min取消、实际zombie、GUI/安装/最小窗/RUNPATH证据缺口保留。

Verdict：已知验收缺口均已记载，最终远端证据收集完成；不宣称三端全部通过。
