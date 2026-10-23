# Task 6 hosted Linux 第二轮实证报告

## 运行绑定与当前结论

run [39905806798](https://github.com/wangdayong228/bee/actions/runs/39905806798) 绑定 source `22c5f912659bad7af4a602cf2e3a8b019cd5ce94`，包含 RUNPATH/截图修补提交 `1e1019d87a69f66fca817790459e45c874e13d48`。2026-10-23 05:26:59Z 开始。当前三行已 success；Ubuntu 24.04 x64 尚未完成，**不能宣称四行全绿**。

在 05:44:07Z 查询时，24.04 x64 的 `Prepare native Rust and Ubuntu desktop dependencies` 自 05:27:16Z 持续 1012 秒（16 分 52 秒）。in-progress 尚无完整 job 日志或 checks 可读，无法区分 rustup/apt 或具体网络/依赖原因，保持未知。没有取消、重跑或触发额外 workflow。

## 已完成三行与实际回归

| Runner | Job | 原构建 source.json 与包内 Bee 相同的 SHA256 | extract / FUSE 观察毫秒 |
| --- | --- | --- | --- |
| ubuntu-22.04 | success | `3821afa055bc15b2b86c5545d7a13962940e427be52b9e6ade08a9d2536684e8` | 10232 / 10255 |
| ubuntu-22.04-arm | success | `38d5b74ac2adafa0598667df73ebbc20c5ef12957ca0f0ede403ed1ec35c1f30` | 10203 / 10248 |
| ubuntu-24.04-arm | success | `14616e4797057a0874b06a4575d328d785b572e4fcf7223e5933d13ae531340d` | 10248 / 10243 |

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

本地：`.cache/qa/linux-hosted-39905806798-run.json`、`…-artifacts.json`、`…-checks/`、`…-image-statistics.json`、两份 ELF 日志与两个定向下载测试产物。没有下载其他整包，没有修改源码/index/HEAD，没有 commit、push、触发或取消 workflow；P1 Task 4 的源码写窗口始终由主代理/其执行者持有。本报告在忽略目录 `.superpowers/sdd/`，随第四行结果继续补记。
