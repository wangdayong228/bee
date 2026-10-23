# 2681edc 原生远程 CI 证据报告

精确源码 `2681edca2c56bca9d2ce30db4198fb5784d98b65`，仓库 `wangdayong228/bee`，分支 `feat/bee-desktop-p0`；push事件时间2026-10-23T09:22:17Z。只读查询与下载，报告/cache为忽略文件；不更改源码/index/HEAD，不占用主控1420/build，不触发、重跑或取消CI。

## 精确运行

| 平台 | run | 当前状态 |
| --- | --- | --- |
| Mac15 Intel | [39931368193](https://github.com/wangdayong228/bee/actions/runs/39931368193) | completed failure；浏览器489通过、Rust模拟窗口发现测试超时，App/DMG跳过 |
| Windows Server2022 x64 | [39931368298](https://github.com/wangdayong228/bee/actions/runs/39931368298) | completed success；下载包/source字节已核对 |
| Linux四行 | [39931368185](https://github.com/wangdayong228/bee/actions/runs/39931368185) | completed failure；三行success，24x64 Firefox通道关闭 |

完整discovery与三平台初始source/jobs/steps快照在 `.cache/qa/p1-native-remote-2681edc/`。每次监控校验完整source后才写入本目录。b94/e1证据分别留在原目录，不继承其通过结果、包或哈希。

## 本轮结论与边界

本轮已完成Windows与Linux三行实际包/source/smoke的下载及字节核对；Mac的失败日志/checks，以及Linux24x64的失败日志/checks/trace均已收齐。两条失败导致相关原生包验证缺失，不能写成全平台原生通过。Mac13、Windows10/11、GUI业务ready、托盘/菜单退出与干净用户安装不由这些hosted构建自动证明。

## Windows 已完成并核对下载文件

run39931368298 success。两个精确artifact metadata的run、完整source、branch、expired=false匹配；raw log、metadata、完整checks/test已下载。Python只读哈希/JSON核对exit0，结果在 `windows/verification-summary.json`。

实际Server2022 Datacenter10.0.20348/ProductType3、CPU9/x64，image win22/**20261021.343.1**（本轮独立核实，不能照抄b94）。Rust30 passed/0 failed/0 ignored；构建日志实际含 `vite build --mode demo`。此Windows workflow未跑Go全量或浏览器，不借其他平台补齐。

NSIS **16,283,838 bytes / SHA256 `1c3cc2ccd1234120b1e461b5e9e3c6ed2094ff111fdc7f4c0a520dcd1d2319d7`**，与两个artifact的packages.json一致。实际source.json原始SHA为 `8708a840875d2ed3b191da1db3291225dff4ca3063acb5cba80e05235aa6fcf6`，与manifest匹配、内容全等；完整2681edc/固定TEE/Windows x64 target/Go1.27.3 windows-amd64均匹配。Runner观测原Bee SHA=`d6c1f02a7a6a2d3dfc4cfc4d519b9a9fd8c3eb24bfd30416edbc1953394dcfbb`，TEE archive=`4bc9caad3ad2ce5de01b9983a750cee6380098fc308333c30c098fbf8e7bad38`。

未独立上传原Bee，没有在本机提取NSIS payload、安装或执行EXE；不能写成Win10/11、GUI、托盘、安装或干净用户验收通过。

## Mac Intel 首个真实失败（原生Rust测试阶段）

精确run39931368193/job120340177201。Go步骤、tooling37/bridge10、三浏览器**489 passed（11.8m）**均通过；实际Bee构建后，Rust **38 passed / 1 failed / 2 ignored**，exit101。唯一失败为 `singleton_tests::windows_registration::tests::existing_instance_waits_for_its_window_and_forwards_exactly_once`。raw `macos-job.log:1345–1356`：windows_registration.rs:87 unwrap TimedOut，`single-instance primary window discovery exceeded 100ms; elapsed=185ms; required=valid HWND before forwarding`。

绑定完整2681源码：helper使用真实Instant/deadline、每轮最多sleep20ms，find后先检查deadline再send；该test给100ms，Cell模拟find在第三次probe返回Some(42)，期望只发送一次。singleton_tests.rs:49–50无平台cfg include该helper，所以这是Mac上运行的注入闭包测试，未调用真实Windows HWND。证据确定实际185ms超过100ms；无probe次数/调度原因日志，不能推断具体某次sleep、实际窗口竞态或产品来源。源码副本与 `macos-failure-analysis.json` 已保存。

App+DMG、签名App验证、Mach-O/package metadata及DMG上传全部skipped。本轮无Mac原生包，不能借主控本机arm64成功结果写成Intel通过。唯一always checks已完整下载；不改测试/预算、不重跑。

Mac下载checks独立核对：native.json完整2681/run/Intel target/全部检查匹配，Go7包、browser489与Rust38/1/2计数一致；真实Bee管理握手/ping/stop测试也明确ok。环境与失败证据以本轮原始文件为准，未生成或核对DMG。

## Linux24x64 首个真实失败（Firefox通道关闭）

精确run39931368185/job120344049923。浏览器结果 **488 passed / 1 failed（10.1m）**，exit1；失败为Firefox `tests/accounts.spec.ts:8`“双入口、检测登录和详情分别表达能力、市场与额度时效”，在line21点击“概览”时 `locator.click: Target page, context or browser has been closed`。raw `linux-ubuntu-24.04-job.log:2787–2837`记录按钮已解析、可见/可用/稳定、滚动完成，performing click时通道关闭；Firefox err为 `Exiting due to channel error.`。

同时有Sandbox user-namespace EPERM、Firefox RemoteSettings cache/JSON.parse信息，但不能据此确定它们导致通道关闭，也没有证据将其归因为产品断言失败。实际Bee/Rust、AppImage、extract/FUSE全部skipped。原始job日志通过只读jobs/logs REST取得（gh run日志入口在整run结束前拒绝），失败artifact与trace已完整下载。源码副本及 `linux-ubuntu-24.04-failure-analysis.json` 已保存。

Linux24x64 trace补充：trace内嵌accounts.spec.ts与精确2681源码逐字节相同；正确点击行是line21（line20为Escape）。点击在test累计4397.110ms开始，2920.235ms后因关闭报错，总累计7317.345ms，远未到默认30秒。这不是预算超时；trace只含test.trace，没有browser library trace/进程退出码或信号，不能进一步证明关闭原因。

## Linux 三行实际产物最终核对

run39931368185最终failure：22x64/22arm/24arm三个job success，24x64为上述Firefox失败。7个精确artifact metadata的run、完整source、branch、expired=false均匹配；完整run日志、逐行日志、checks/test全部下载。每行只读Python核对exit0，见 `linux/<runner>/verification-summary.json`。

三条成功行各Go7包、tooling37/AppImage tooling16/bridge10、三浏览器489 passed、Rust35 passed/0 failed/0 ignored，实际 `vite build --mode demo`。下载checks与raw log计数独立一致。

| runner | 实际AppImage bytes | 实际SHA256 | extract/FUSE observedMs |
| --- | ---: | --- | --- |
| ubuntu-22.04 | 148,675,064 | `ec8cacdc9a53db46a093362db2cad6809547e9f0e30fc98e6db0e9cb61ca5f98` | 10281/10297 |
| ubuntu-22.04-arm | 138,983,944 | `d54ea3726e0150cfd92d9a51a988f884671bb2f7bdd2a62a46f6b9eeba333044` | 10239/10236 |
| ubuntu-24.04-arm | 139,078,152 | `b6fcd0c14889fe200d48d9d01bc38d4bc2cf3b005be1b5d7c708a174f8500eae` | 10247/10199 |

每行实际下载包bytes/SHA、source JSON原始SHA、完整source内容与smoke内嵌source、原Bee/包内Bee/provenance SHA全部一致；native host/target、完整2681/run及固定TEE均匹配。extract与真实FUSE均ok，parentClosed=true/liveRemaining=[]、均SIGTERM清理。**22arm与24arm的extract各记录一个PID1 WebKitWebProces zombie**；这两条FUSE及22x64两模式zombies=[]。不能把无活跃残留写成无任何残留。

启动观测仅证明对应原生runner窗口至少10秒，不是业务ready、GUI操作、托盘/菜单退出或干净用户安装；无新增最终ELF RUNPATH测量。Windows未安装/执行，Mac Intel无本轮App/DMG；主控本机arm64结果不能填充Intel缺口。后续87b28a2按新source独立取证，不沿用2681包或通过结论。

## 收证一致性清单

- ✅ 会话约束：只读远端及ignored cache/report写入，未触碰source/index/HEAD/native/1420，未触发/重跑/取消。
- ✅ 文内一致：表格、平台段落与结论统一；失败、skipped与真实运行阶段明确区分。
- ✅ 跨证据一致：精确source/run/target、artifact metadata、下载包/source/hash、smoke/trace与日志计数匹配；ZIP digest与包SHA分别标记。
- ✅ 配置一致：Linux失败trace7317.345ms早于默认30秒，Mac模拟helper100ms与185ms错误一致；未修改实现、接口或配置，传播项不适用。
- ✅ 文档与实际一致：三行Linux和Windows包核对完成；两个原生验证缺口与ARM extract zombie完整记录，不宣称全平台原生验收通过。

结论：本轮收证已完成且记录一致；已知缺口如上，后续源码独立验证。
