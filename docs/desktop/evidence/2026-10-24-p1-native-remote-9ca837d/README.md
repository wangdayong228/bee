# 9ca837d Linux 原生 CI 最终证据报告

本报告仅归属源码 `9ca837d902fbf026be9931f796a3d1289e33dad3`。Linux run [39941148651](https://github.com/wangdayong228/bee/actions/runs/39941148651) 已结束，结论 `success`；四个矩阵 job 全部成功。它证明本次 Linux 开发包的构建、既有测试与两种启动方式的客户端尺寸/启动 smoke，不代表跨平台产品全部验收通过。

## 来源与复核边界

- 分支：`feat/bee-desktop-p0`；实际源码、打包 Bee 来源 JSON、两个 smoke provenance 及下载 artifact 元数据均绑定上述完整 revision 和本 run。
- 固定 TEE：`a687f86d781e825c04c1d84d75b41bba5d862254`；归档 SHA-256：`4bc9caad3ad2ce5de01b9983a750cee6380098fc308333c30c098fbf8e7bad38`。
- 本次仅只读监控、下载及离线复核；未触发/重跑/取消 CI，未执行本地产品构建、测试、原生程序、GUI 或 Docker，未改源码/index/HEAD。文中的主动取消由主代理先前明确执行，单独列示。
- `87b28a29aa84c2543b6b80b7e31204646e4fa76a` 的 macOS/Windows/Linux 证据及主代理的本地 Docker/macOS 调查各自独立；不计入本 revision 的通过数。

## 四行 Linux 最终结果

四行独立下载日志均有 Go 7 个 `ok` 包、浏览器 `489 passed`、Rust `36 passed; 0 failed; 0 ignored`。原始 job 日志也独立核对浏览器/Rust 数量与实际 `vite build --mode demo`，均为 demo development AppImage。

| Runner | Target | Job | 结论 | AppImage 字节数 |
|---|---|---:|---|---:|
| ubuntu-22.04 | `x86_64-unknown-linux-gnu` | 120391948718 | success | 148675064 |
| ubuntu-22.04-arm | `aarch64-unknown-linux-gnu` | 120391948499 | success | 138983944 |
| ubuntu-24.04 | `x86_64-unknown-linux-gnu` | 120391948358 | success | 148912632 |
| ubuntu-24.04-arm | `aarch64-unknown-linux-gnu` | 120391948517 | success | 139078152 |

## 本地文件校验值

下表 SHA-256 直接针对解压后的本地 AppImage 和原始 `.source.json` 字节计算。它们分别匹配 smoke 的 package/source 哈希；来源内容、target、GOOS/GOARCH、固定 TEE 与打包 Bee binary SHA 亦已交叉验证。**这些值不是 artifact 下载 ZIP 的 digest。**

| Runner | AppImage SHA-256 | 原始 source JSON SHA-256 |
|---|---|---|
| ubuntu-22.04 | `4d3cb97ece12c946395691e2156256a1f177daaa4285a928dda202f748b77235` | `aa93def8ed1d879c7cb13b866152d90d6360a76c735528e7242041a2e130d8fb` |
| ubuntu-22.04-arm | `6e8fb8faaabcf649ed3f0c8a6e593ca21c6a130d5d697e69e8fb6909bb188e77` | `81df25c67125db368828a8d093aac1699ded97dab7644bab44945ce6682f4407` |
| ubuntu-24.04 | `07355ee68591a14d1d9fec0d06a141cc4117d38db042296513caf80cce71ede4` | `853f8737117c1d632b3bfa369d03e82e191852277321227b8acada0221c2914c` |
| ubuntu-24.04-arm | `e56cb6596caa97dc0048c22e8961a0146f9162993fe70995243549e740324499` | `a7ee237f504dbcf8b63408390861880c71b248d77d5174c75c0e6687cce59a90` |

八个 artifact ZIP 均已逐一通过 API 元数据 size/digest 与 ZIP CRC 核验后解压；原始 ZIP 校验值见 `segmented-download-result.json`、`artifact-zips/*-verification.json` 与 `linux-artifacts-final.json`。完整下载文件和大型包留在本地 cache，选定归档不重复放入二进制/ZIP。

## 两种启动方式与最小客户端尺寸

全部八次由初始 1000×700 调整到请求的 860×600。原始 resize geometry、最终 geometry、相同 window ID、owner PID、最后 owned-window probe 与存活非 zombie 父进程记录已交叉核验；最终 PNG 的 IHDR 均为 860×600，八张图已逐张目视查看，显示非空白英文 Bee demo Overview。

| Runner | 方式 | 观测毫秒 | 最终客户端 | parentClosed / liveRemaining | zombies |
|---|---|---:|---|---|---|
| ubuntu-22.04 | extract | 10333 | 860×600 | true / [] | 无 |
| ubuntu-22.04 | fuse | 10317 | 860×600 | true / [] | 无 |
| ubuntu-22.04-arm | extract | 10235 | 860×600 | true / [] | 无 |
| ubuntu-22.04-arm | fuse | 10245 | 860×600 | true / [] | PID 49208, PPID 1, PGID 49133, Zl, `WebKitWebProces <defunct>` |
| ubuntu-24.04 | extract | 10242 | 860×600 | true / [] | 无 |
| ubuntu-24.04 | fuse | 10325 | 860×600 | true / [] | 无 |
| ubuntu-24.04-arm | extract | 10218 | 860×600 | true / [] | PID 50202, PPID 1, PGID 50129, Zl, WebKitWebProces |
| ubuntu-24.04-arm | fuse | 10275 | 860×600 | true / [] | PID 50763, PPID 1, PGID 50674, Zl, WebKitWebProces |

八次 smoke 均 `ok=true`、观测至少 10 秒，并以 SIGTERM 结束；父进程关闭，未留下存活后代。22 ARM FUSE、24 ARM extract/FUSE 各有一个由 PID 1 接管的 WebKit zombie，原始记录保留；其余五次 zombies 为空。因此不能写成“所有清理均无残留”。

smoke 自身声明范围：`native client window size and startup only; no readiness, content visibility or desktop decoration assertion`。截图目视观察不升级为业务 ready、内容可见性的自动断言或完整 UI 验收；未证明桌面装饰/标题栏、托盘与菜单退出、干净用户安装、生产签名、实测 ELF RUNPATH。此次 860×600 属于客户端窗口尺寸，不是含桌面装饰的外框尺寸。

## 下载失败与恢复记录

首轮八个本地 artifact 下载均失败：长传输 timeout 后，curl 自动重试出现 HTTP 403，并丢弃了原先的部分文件。原始 `*-download.log` 与 `download-failure-analysis.json` 保留。HTTP 403 的原因未被独立证明，不将“签名 URL 过期”写为定论，也不据此归因产品或 CI。

恢复采用四个下载 worker、每 4 MiB Range 请求重新获取只读 API redirect、带 cache-busting 查询、禁用 curl 自动 retry、限制超时，并先核对 Content-Range 再保留分段。同一 artifact 没有并行重复下载；最终八个 ZIP 均通过完整 size/SHA-256/CRC 后才解压。分段记录 `*-segments.jsonl` 与最终结果同时保留；这些传输失败没有改变远端四行成功结论。

## 主代理主动取消的冗余平台 run

主代理先前明确取消以下三个同 revision 的冗余平台 run，既有 `redundant-runs-cancel-request.json` 记录 cancelExit=0。本次只读获取其最终元数据，三者均为 `completed/cancelled`。取消理由是相对基准源码的变化集中于文档与 Linux smoke/test，并保留 87 的平台证据；这不等于 9 的 macOS/Windows 通过。

| 平台 | Run | 取消前 | 实际终态 | 已知中断点 |
|---|---:|---|---|---|
| macOS Intel supplemental | 39941148799 | pending | completed / cancelled | 最终 jobs 为空，未取得本 run 原生构建结果 |
| Windows Server 2022 build | 39941148571 | in_progress | completed / cancelled | Rust 测试步骤 cancelled，NSIS 与包哈希/上传 skipped |
| Windows protected files | 39941148637 | in_progress | completed / cancelled | protected-file 行为、Go vet、全量 Go regression 步骤成功；实际 Windows Bee 构建步骤 cancelled |

上述是主代理主动取消，与 87 的 Ubuntu 24.04 x64 job 超过 1h30m 限制后取消的事实分开。后者不归入本 revision 的 Linux 失败或主动取消数。

## 自检、一致性与证据位置

离线核验记录为 `all-row-verification.log`、四行 `verification-summary.json`、`final-evidence-verification.json`；两份绑定源码位于 `pinned-source/desktop/`。原始 job 日志、最终 run/取消元数据、来源 JSON、smoke JSON、最终窗口 PNG、ZIP 下载校验和实际失败日志随选定归档保存。

- [x] 会话/范围：仅完成授权的远端取证；源码 revision、run 与分支分隔，没有将 87 或主代理本地结果移植为 9 通过。
- [x] 内部一致性：四行成功、Go7/浏览器489/Rust36、八次启动时长/860×600 与三处 zombie 逐项核对。
- [x] 跨材料一致性：原始日志、下载 package/source 字节、smoke provenance、固定 TEE、PNG 与终态元数据相互匹配；ZIP digest 与本地 AppImage SHA 明确区分。
- [x] 配置：本子任务未改源码、工作流、依赖或运行配置；仅写 ignored QA/report 文件。
- [x] 文档/边界：保留首轮下载失败、实际 zombie、主代理主动取消及 skipped 步骤；没有宣称全平台/业务 ready/安装/签名验收完成。

选定归档的 `README.md` 与本报告原字节一致；`manifest.json` 对每个原字节副本记录来源、字节数与 SHA-256。大型二进制、ZIP 和浏览器截图集合不纳入选定归档。全量本地 cache 清单另存 `local-byte-manifest.json`；归档完成后独立核验来源/目标字节、SHA 和 ignored 状态。
