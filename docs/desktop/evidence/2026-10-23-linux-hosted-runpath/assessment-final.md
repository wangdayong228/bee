# Task 6 hosted Linux 第二轮实证报告

## 运行绑定与当前结论

run [39905806798](https://github.com/wangdayong228/bee/actions/runs/39905806798) 绑定 source `22c5f912659bad7af4a602cf2e3a8b019cd5ce94`，包含 RUNPATH/截图修补提交 `1e1019d87a69f66fca817790459e45c874e13d48`。2026-10-23 05:26:59Z 开始、06:03:04Z 最后一行结束，最终 run conclusion 为 **failure：三行 success、一行 failure，不能宣称四行全绿**。24.04 x64 在 AppImage 工具测试 15/16 处失败，产品构建与原生烟测尚未运行；详见第四行最终结果。

在 05:44:07Z 查询时，24.04 x64 的 `Prepare native Rust and Ubuntu desktop dependencies` 自 05:27:16Z 持续 1012 秒（16 分 52 秒）。当时 in-progress 无完整 job 日志或 checks 可读，无法区分 rustup/apt 或具体网络/依赖原因，保持未知。结束后日志已将耗时定位到 apt 归档下载，见末节。没有取消、重跑或触发额外 workflow。

## 三行成功与实际回归

| Runner | Job | 原构建 source.json 与包内 Bee 相同的 SHA256 | extract / FUSE 观察毫秒 |
| --- | --- | --- | --- |
| ubuntu-22.04 | success | `3821afa055bc15b2b86c5545d7a13962940e427be52b9e6ade08a9d2536684e8` | 10232 / 10255 |
| ubuntu-22.04-arm | success | `38d5b74ac2adafa0598667df73ebbc20c5ef12957ca0f0ede403ed1ec35c1f30` | 10203 / 10248 |
| ubuntu-24.04-arm | success | `14616e4797057a0874b06a4575d328d785b572e4fcf7223e5933d13ae531340d` | 10248 / 10243 |
| ubuntu-24.04 x64 | failure：AppImage 工具测试 15/16 | 未构建 Bee/AppImage，没有本轮包内 SHA | 未运行 / 未运行 |

三行实际 tools/native 证据均为普通 runner uid=1001，Node 24.22.1、npm 11.19.1、Go 1.27.3、Rust/Cargo 1.94.0；Node/Go/Rust host 与 x64/arm64 的原生 runner 架构匹配，native.json 各检查均通过，Ubuntu baseline 精确匹配。

三行 `go vet ./...` 与 `go test ./... -count=1` 均通过，后者为 7 包；锁文件 npm ci、typecheck、前端 build 均通过；tooling 37/37、AppImage tooling 16/16、bridge 10/10、Chromium E2E 53/53、Rust 35/35 均通过（Rust main/doc 额外 0 项通过）。本轮 E2E 已包含 source 提交中的 P1 UI 测试，与首轮 32 项不同，不能沿用首轮计数。三行实际 Bee 构建、AppImage bundle、extract 与独立 FUSE 均完成。

各 smoke 的 provenance 同时核对 source revision、TEE `a687f86d781e825c04c1d84d75b41bba5d862254`、target、linux/goarch、Go 精确版本与 binarySha256；提取模式和 FUSE 模式不是互相代替。两模式 AppImage SHA 在观察前后保持一致。

## RUNPATH 的实际产物证据与来源边界

checks 的 sidecar.log 只记录构建成功、revision 与 target，tauri-build.log 记录下载 linuxdeploy-07333c6；**CI 没有采集原 Bee 或包内 Bee 的 readelf 动态表**，不能把参数或工具退出码冒充实际 RUNPATH 值。

为闭环两架构修补，仅下载成功的 22.04 x64 与 24.04 arm64 两个具体测试产物，分别定位有效 SquashFS v4 superblock，只提取 `usr/bin/bee`，没有启动产品程序。在现有隔离诊断容器 `bee-linux-task6-diagnostic`（image `bb63634f0bdb…`、`--network none`、仅挂载 `.cache/qa`）执行 `readelf -l -d -S` 与 SHA256：

| 实际提取产物 | AppImage SHA256 | 包内 Bee 动态表 |
| --- | --- | --- |
| 22.04 x64 | `b9c55e621816fbd6bf3d9f461eb4631e6edb1500c312b4f1c6c0490c56b10b3c` | DT_RUNPATH `[$ORIGIN/../lib]`、NEEDED `libc.so.6`、解释器 `/lib64/ld-linux-x86-64.so.2` |
| 24.04 arm64 | `1c70cf49bf0d9e032c24a5497c2c6a286f22d4b03d09e8ff6f74656cb55af9f5` | DT_RUNPATH `[$ORIGIN/../lib]`、NEEDED `libc.so.6`、解释器 `/lib/ld-linux-aarch64.so.1` |

提取 Bee 的 SHA 再次精确等于上表 source.json/两烟测 SHA。由字节等同性，可将观察到的 DT_RUNPATH 连接到原构建清单绑定的 Bee 字节；这不是声称 runner 在 bundle 前直接运行了 readelf。绑定 source 的 Linux 构建参数为 Go `-ldflags=-r=$ORIGIN/../lib`，构建完成才计算来源 SHA；两份真实产物表明目标 RUNPATH 已存在且打包未改字节。arm64 本次来源通过不能再归因为首轮 patchelf 失败后字节未变：实际 arm64 成品已含所需 DT_RUNPATH。22.04 arm64 未额外提取 ELF，只有精确 SHA 与原生烟测证据，不能把其动态表字段冒充直接实测。

日志 `.cache/qa/linux-hosted-39905806798-{x64,arm64}-elf.log`。arm64 附加的非必要 `file` 命令因诊断镜像未安装该工具返回 127；所需 readelf 与 sha256sum 均 exit 0，不影响上述动态表/SHA 结论，没有为此扩大环境。

## 初末画面、时间与 stderr

三行共六份 `window.initial.png` 全为 1000×700、单色、mean=0。initial 采样在 spawn 后约 309–532ms；final 在约 10.5–10.8 秒采样，`window.png` 为 1000×700、1083–1108 色，`root.png` 为 1280×1024、1084–1109 色。root 中窗口位于 (0,0)，同一窗口几何为 1000×700，剩余黑区为 Xvfb 桌面背景，不能误认整个应用黑屏。每个 sample 均保存窗口树、几何、进程、窗口及两次捕获起止时间。

已目视 22.04 x64、24.04 arm64 的 extract 末窗口以及 22.04 arm64 FUSE root，主代理亦亲自查看 22.04 x64 与 24.04 arm64 的 FUSE 末窗口：五页侧栏、“概览”、提示“业务服务未接通：当前构建尚未配置真实 Bee/Hive 业务适配器”清晰可读。这是普通真实业务未接入构建，不是 demo 数据，不是 ready 握手成功证据。

初图黑而同次末图出现页面内容，支持过早取样是黑图因素；第二轮 source 同时含有 P1 UI 改动，不能反事实证明首轮 source 只延后截图就一定呈现同一画面，也不能给出实际首次渲染完成时间。当前不能据首轮单张黑图判定持续渲染失败。24.04 arm64 extract/FUSE stderr 仍包含 DRI3 device/accelerated rendering 与 GStreamer appsink 警告，而末图已有内容，所以这些警告本身不足以证明渲染失败。22.04 两架构 stderr 为 AT-SPI accessibility bus 缺失警告，extract 另有 fonts mtime 警告；本轮未更改沙箱/WebKit 环境，也未做 UI 输入。

六次末采样的进程组均含 bee-desktop、WebKitNetworkPr、WebKitWebProces、bee，说明该时点存在 Bee 进程，**不能据此断言 bridge ready、业务后端连接、托盘行为或生产服务正确**。清理均为 SIGTERM、parentClosed=true、liveRemaining=[]；22.04 arm64 FUSE、24.04 arm64 两模式保留 WebKit zombie 记录，不宣称所有后代均被 reap。没有干净用户安装、托盘/无托盘、UI ready、菜单退出或签名发行验收。

## 持久证据建议（尚未修改源码或 workflow）

1. CI 在 Go 构建后、生成 source SHA 时保存原 Bee 的 `readelf -l -d` 与完整 SHA；bundle 提取后保存包内动态表与 SHA，明确检查 DT_RUNPATH 类型和值，并与 source 绑定，避免今后只能用字节相等推导原始元数据。
2. 保留当前初图、实际观察末窗口/root、每轮时间/几何/窗口树和 stderr；若今后增加画面异常检查，应独立命名为截图诊断，不能替代真实 UI ready 握手或交互验收。
3. 原始 job 元数据、artifact 清单、工具版本、TEE/source revision 与检查日志继续按 source SHA 留存；当前 artifact retention 为 14 天，若用于长期验收应在到期前按项目证据存储规则归档，不把本机忽略目录当永久归档。

## 留存与只读边界

本地：`.cache/qa/linux-hosted-39905806798-run.json`、`…-artifacts.json`、`…-checks/`、`…-image-statistics.json`、两份 ELF 日志与两个定向下载测试产物。没有下载其他整包，没有修改源码/index/HEAD，没有 commit、push、触发或取消 workflow；P1 Task 4 的源码写窗口始终由主代理/其执行者持有。本报告在忽略目录 `.superpowers/sdd/`；第四行结束后已补齐所有现有证据。三行成功证据另由主代理归档到 `docs/desktop/evidence/2026-10-23-linux-hosted-runpath/` 并提交 `8c506f4`，本代理没有重复归档或修改该目录。

## 第四行最终结果与失败定位

24.04 x64 job `120257386609` 于 06:03:04Z completed/failure。依赖步骤 05:27:16Z→06:01:00Z success（2024 秒，33 分 44 秒）；native/tools 与 TEE success；Go vet/full native regression 06:01:04Z→06:02:51Z success，7 包通过。npm ci（0 vulnerabilities）、typecheck、前端 build、tooling 37/37 均通过。随后 `node --test desktop/tests/linux-appimage.test.mjs` 为 15 passed、1 failed、0 skipped（1934.431287ms），使该复合步骤在 06:03:00Z failure。bridge、Chromium、实际 Bee/Rust、bundle、extract/FUSE 均未运行，不能从其他三行补算本行通过。

唯一失败：`desktop/tests/linux-appimage.test.mjs:162–164` 的 `exit zero before completing the visible observation still fails`，fixture 子进程执行 `setTimeout(() => process.exit(0), 200)`，要求观察 450ms。测试只接受 `/early exit.*code=0/`；实际在 254.720978ms 被 `smoke-linux-appimage.mjs:136` 拒绝，错误是：

```text
observed window disappeared: actual=[{"id":"42","pid":18131,"title":"fixture window"}]; required window={"id":"42","pid":18131,"title":"fixture window"}
```

绑定 source 的观察循环先检查 Node child.exitCode/signalCode，再同步执行 `ps` 取 PGID 进程，调用 findWindows 后按同 PID 且非 zombie 的进程筛选 owned；若此前已选定的 window 没有 owned 匹配，就报该错误。实际错误中的候选 window id/PID 与 required 相同，因此拒绝来自“该轮没有符合条件的 live owned process”，不是候选窗口列表单纯变空。测试 fixture 始终返回同 id/PID，且将子进程退出设置在观察完成前；静态路径与实际错误显示两种拒绝路径的错误分类断言对退出事件/同步 ps 采样时序敏感。

这是工具测试失败，观察器没有把提前结束误判为成功；仍是 CI 阻塞，不能降格为产品验收通过。该次 fixture teardown 删除了临时 observation，checks 未保存失败时点 ps 断面或 report.exit，故不能把“具体为 zombie 还是已经离组”或确切 Node 退出事件送达顺序冒充直接观测。未在源码上修补，也没有通过重跑掩盖失败。若主代理安排修补，应先固定该竞争路径的可复现证据，同时验证提前结束必须拒绝、实际退出码与清理报告，而非仅扩大正则隐藏其他失败。

## 第四行依赖耗时的原始证据

完整 job 日志和 checks 已可读：Rust 在 05:27:17.455Z 同步并在 05:27:26.856Z 安装完成；apt-update 明确 `Fetched 12.5 MB in 1s (9980 kB/s)`。apt-install 明确 `Fetched 125 MB in 33min 17s (62.6 kB/s)`，随后正常 unpack/setup/restart 并结束为 success。原始时间行中，fonts-noto-cjk 61.2MB 下载自 05:28:20.712Z 的 Get:13 到 05:42:34.099Z 的下一 Get:14；其他包也持续慢速下载。可将长耗时主要定位到 apt 归档传输；没有日志证据证明特定公网路由故障或镜像服务端根因，不猜测这些更深原因。它与后续工具测试断言失败是两件独立事实。

证据定位：第四行 `desktop-ci-evidence/apt-install.log:313`，完整 job `.cache/qa/linux-hosted-39905806798-ubuntu2404-x64.log:596`；Rust 完成行约 259，apt-update 完成约 282；工具测试失败完整 job 约 1768 起，checks 的 appimage-tooling.log 保留完整堆栈。第四行 checks 共 18 文件，没有烟测图、包内 SHA 或测试包 artifact。四行 checks 与最终 run/artifact 元数据均已取得，未下载不存在的第四行整包。


## 失败测试的最小修补建议（仅建议，尚未实施）

本次直接可证的是 `observeOwnedProcess` reject；具体 `report.exit.code`、`report.ok`、`cleanup.liveRemaining` 在 CI artifact 中缺失，不能凭 fixture 的预定 `process.exit(0)` 或源码预期补写为实际值。观察器 catch 确会将 report.ok=false，finally 也确会 await cleanupGroup/close 并保存 observation.json，但测试 teardown 紧接着删除根目录，本次没有逐字段输出。这一证据缺口必须在修补后的实际验证中补齐。

最小建议仅调整该测试的验收层次，不调整产品/观察器的 fail-closed 行为：保留 `assert.rejects` 并将可接受错误限定为“native app early exit: code=0”或“observed window disappeared”两条已确认失败路径；随后读取本次 observation.json，强制断言 `report.exit.code === 0`、`report.exit.signal === null`、`report.ok === false`、`report.cleanup.parentClosed === true`、`report.cleanup.liveRemaining` 深等于 `[]`，必要时确认未达到 observeMs/没有成功末次观察。这样真正的 SIGTERM 清理抢先、非零退出、清理失败或错误成功仍会失败，不能仅放宽正则或删除退出语义断言。原有非零退出保存 stderr、真实丢窗和最终归属丢失用例继续保留。

正则现在过度约束的是“Node child 退出事件必须先于 ps 进程归属失效被处理”的错误优先级；安全不变量应为“450ms 观察完成前退出的进程不能通过，实际退出码为0且清理完成”。只读调查没有把源码中的事件顺序解释为已抓取的运行时序；修补后应保留该次报告字段证据，并对定向用例重复运行和完整16项工具套件执行独立窄复核，再由主代理决定原生CI后续运行。按主代理指令本轮没有写代码、跑新测试或重跑CI。
