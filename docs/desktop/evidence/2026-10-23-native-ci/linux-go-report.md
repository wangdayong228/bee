# Linux arm64 容器 Go 验证报告

日期：2026-10-23（Asia/Shanghai）。工作目录：`/Users/dayong/myspace/mywork/tokenhive/.worktrees/bee-desktop-p0`。

最新状态：下文追加的官方 Go 归档方案已完成 Linux arm64 容器 Go 验证，最终稳定基线的聚焦测试、vet、全量测试和 CLI 构建均返回 0。以下首轮记录作为历史证据保留。

## 首轮官方 Go 镜像下载尝试

本轮状态为**下载前置条件阻塞，Go 验证未执行**。官方 `golang:1.27.3` 镜像拉取在本次约五分钟调查期限内未完成，因此没有实际运行 Linux 容器、没有取得容器中的 Go 版本，也没有测试通过或测试失败的结论。

Docker CLI 显示镜像已解析到七个文件系统分层，日志没有提供字节进度。在 05:09 时结束本任务的拉取客户端，是本次调查期限到达；不能由此推断下载完全没有传输字节、官方镜像不存在或 Linux arm64 不受支持。最终 `docker image inspect golang:1.27.3` 返回 `No such image`。

## 实际执行与证据

1. 已加载 `global-conventions` 和 `verification-before-completion`。
2. `docker info --format '{{.OSType}}/{{.Architecture}}'` 返回 `linux/aarch64`，确认现有引擎的 OS/架构。未改变 Docker 引擎、配置或已有容器。
3. 项目 `go.mod` 声明 `go 1.27.3`，原有替换为 `github.com/reclaimprotocol/reclaim-tee => ./.cache/reclaim-tee`。本轮未改变依赖、版本、替换或校验信息。
4. 既有 TEE 目录存在、模式为 `drwxr-xr-x`，包含真实项目源码及 `go.mod`、`go.sum`。未将其替换为 stub。本轮未验证其上游提交身份；目录没有被作为独立 Git 仓库认定。
5. 宿主 `go env GOMODCACHE` 为 `/Users/dayong/go/pkg/mod`；其 `cache/download` 为 `drwxr-xr-x dayong staff`。仅准备将官方模块下载缓存作为只读 `file://` 代理来源，不挂载用户 HOME、凭证、SSH 或 Docker socket；由于容器未启动，实际没有挂载。
6. 运行 `docker pull golang:1.27.3`，从 `2026-10-23 02:51:51 UTC` 左右持续至 `02:57:00 UTC`。05:09 时仅向本任务拉取客户端 PID 39366 发送 SIGINT；CLI 随后输出 `context canceled`，退出码为 1。没有收到独立的注册表网络错误文本。仅保留此精确事实，不把人工结束的退出码作为镜像错误。
7. 最终镜像检查退出码 1，内容为 `Error response from daemon: No such image: golang:1.27.3`。实际镜像 ID、RepoDigest、镜像 OS 发行版及容器 `go version` 均未取得，不能填入期望值冒充观测值。
8. 没有创建任何验证容器；预留名称为 `bee-p0-qa-linux-arm64-20261023-linuxgo-a91c07`，最终对应 `docker ps -a` 过滤结果为空。PID 39366 已不存在。没有删除共享镜像层。

## Go 检查状态

| 检查 | 实际状态 | 说明 |
| --- | --- | --- |
| `go test -v ./agent -run 'Test.*(PrivateFile\|StateLock\|Codex\|ClaudeStore)' -count=1` | 未执行 | 无可用的官方同版本容器镜像 |
| `go vet ./...` | 未执行 | 同上 |
| `go test ./... -count=1` | 未执行 | 同上 |

已准备但未运行的容器脚本在 `.cache/qa/linux-go/run-verification.sh`。它要求实际执行身份为 UID 1000，实际 `GOOS/GOARCH` 为 `linux/arm64`，实际 `go version` 必须精确为 `go version go1.27.3 linux/arm64`。未通过这些前置断言便不运行测试。

预备设置为：源码只读挂载到 `/src`，官方宿主模块下载缓存只读挂载到 `/official-go-download-cache`；`GOCACHE` 与 `GOMODCACHE` 使用容器 `/tmp/bee-p0-linux-go.*`；`GOPROXY=file:///official-go-download-cache,https://proxy.golang.org`；保留默认校验和机制；`GOTOOLCHAIN=local`；`GOFLAGS='-buildvcs=false -mod=readonly'`。不重设 `HOME`，不以 root 绕过 Unix 权限检查。每项命令分别有 480/240/240 秒上限。以上均为待执行配置，不能作为已运行的证据。

`-buildvcs=false` 的原因是只读工作树在容器中不能访问宿主 Git 管理目录；它仅关闭 Go 构建的 VCS 元数据注入，不伪造构建元数据。未来使用这一设置得到的检查结果也应保留该边界。

## 输入稳定性

本轮前后计算的 SHA-256 一致，且 `git diff -- go.mod go.sum` 为空：

| 文件 | SHA-256 |
| --- | --- |
| `go.mod` | `bcacb6c6318c9ee4b35f73809bce2630aae1239b0ee145bf6f325dbbf9b449a3` |
| `go.sum` | `733427441b64e4cb1e8f2e90d76e2d045f7c26ab8ca9f4a13633534b529b6fc3` |
| `.cache/reclaim-tee/go.mod` | `83ab0dc8b75c4e2cfbd4e25502fe5de631dea85bb805ec3ecc0ef26b33ca44d9` |
| `.cache/reclaim-tee/go.sum` | `f5148e43977ea9767af4710372bc7534e86e80d0db80e25cd42fdbae85cf6443` |

宿主工作树基线提交为 `f4374af17a6c380f4ff779fe43f30f9dcc1b334a`，当时已有未提交的 P0 修改；本轮没有暂存、提交、推送或修改生产实现。

## 原始材料与范围

- `.cache/qa/linux-go/host-preflight.log`：引擎、宿主模块缓存路径/权限、工作树基线及依赖校验信息。
- `.cache/qa/linux-go/docker-pull.log`：官方镜像拉取的原始输出。
- `.cache/qa/linux-go/pull-deadline.log`：调查期限、唯一客户端 PID 和定向 SIGINT 记录。
- `.cache/qa/linux-go/final-evidence.log`：镜像不可用、具名容器为空、客户端结束与输入校验信息。
- `.cache/qa/linux-go/run-verification.sh`：尚未执行的容器内检查脚本。

本轮没有运行 Cargo、浏览器或 Bee App，没有创建 Windows 或 GUI 环境。Linux 容器 Go 验证本身也不等于 Ubuntu 桌面 GUI、安装流程、托盘或整个 P0 验收通过；本轮连该 Go 验证也尚未执行。

## 追加：官方 Go 归档与现有 Linux arm64 镜像验证

补充验证日期：2026-10-23（Asia/Shanghai）。最终稳定基线的容器执行区间为 `2026-10-23 03:39:53–03:41:41 UTC`。本节更新首轮的当前状态，不删除此前下载受阻的事实。

### 工具链与实际环境

本次从官方 `https://go.dev/dl/go1.27.3.linux-arm64.tar.gz` 下载工具链。接管原下载时保留了 24,260,608 字节，后续使用官方 URL 的 Range 续传；第一轮续传 300 秒到期时保留 48,997,797 字节，再从该偏移完成下载。没有丢弃已保留的下载进度。

独立获取 `https://go.dev/dl/?mode=json&include=all`，筛选到唯一对应的 `go1.27.3.linux-arm64.tar.gz` 条目。归档实际尺寸和 SHA-256 均与官方发布信息一致，**在校验通过后才解压、运行**：

| 项目 | 实际值 |
| --- | --- |
| 归档尺寸 | `67,076,044` 字节 |
| 官方/实测 SHA-256 | `a06e99309dbcbdca1a8ccd2282c3ee146e55930886e26b4f1193269587165f49` |
| 实际 Go 版本 | `go version go1.27.3 linux/arm64` |
| 现有官方镜像 | `mysql:latest`，仅覆盖 entrypoint 运行 `/bin/sh`，未启动数据库 |
| 镜像 ID | `sha256:58a1158ce681432027078e6fc3667c83421acacf8a5fee527a66db3e9eaff7b1` |
| 镜像 RepoDigest | `mysql@sha256:2be51594eba5983f47e67ff5cb87d666a223e309c6c64450f30b5c59a788ea40` |
| 镜像/内核架构 | `linux/arm64`；实际 `uname` 为 `aarch64` |
| 内核 | `6.10.11-linuxkit` |
| 容器发行版/运行库 | Oracle Linux Server 9.4 / glibc 2.34 |
| 执行身份 | `uid=1000 gid=1000 groups=1000` |
| 镜像原有 HOME | `/`；本任务未重设 |
| 默认 CGO 设置 | `CGO_ENABLED=0`；`gcc` 和 `cc` 不在 PATH |

最终容器名称为 `bee-p0-qa-linux-arm64-20261023-tar-go-d46b05`。命令使用 `--rm --network none --user 1000:1000 --entrypoint /bin/sh`，以实际镜像 ID 固定输入，未设置跨目标 GOOS/GOARCH。源码、校验后解压的工具链、宿主官方模块下载缓存和本任务补充模块缓存均只读挂载；仅容器内专用 `/tmp` 目录作为 `GOCACHE`、`GOMODCACHE` 和 CLI 输出位置。完整命令参数保存于 `.cache/qa/linux-go/native-tar-container-command.json`。

`GOTOOLCHAIN=local` 禁止切换工具链。`GOFLAGS='-buildvcs=false -mod=readonly'` 保留首轮说明的 VCS 元数据边界，并固定依赖文件。仍使用默认 `sum.golang.org` 校验机制，没有关闭校验、挂载凭证或访问 Docker socket。容器禁网期间的 `go: downloading` 文本也会出现在读取本地 `file://` 模块代理时，不表示容器获得了外网访问。

### 依赖补齐与中间结果

开始时宿主缓存缺少三个 Linux 构建路径实际使用的锁定模块归档：

- `github.com/aws/aws-sdk-go-v2/service/cloudwatchlogs@v1.82.2`
- `github.com/google/go-configfs-tsm@v0.3.3`
- `github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream@v1.7.18`

在宿主机从官方 `https://proxy.golang.org` 下载到本任务独立 `.cache/qa/linux-go/additional-modules`，未修改宿主共享模块缓存。逐项验证下载结果的 `Sum` 和 `GoModSum` 与项目现有 `go.sum` 一致，然后将补充下载缓存只读挂载供容器使用。未修改任何依赖版本、替换或 `go.sum` 条目。

前两次归档方案容器运行因缺少上述模块、禁网下无法回退代理而退出 1，属于依赖准备失败；原始证据分别保留在 `native-tar-go-attempt1.log` 和 `native-tar-go-attempt2.log`，不能作为测试断言失败。

第三次运行恰逢主线程的 Task 2 代理拆分 `doctor_test.go` 的平台锁 helper：聚焦命令在文件写入期间运行，产生 `doctor_test.go:145:12: undefined: lockDoctorTestFile`。两份相关文件的落盘时间均为 `11:38:10 +0800`；主线程随后确认该修改已完成并暂停源码写入。因此将该结果保留为写入重叠期间的中间结果，不视为稳定基线代码缺陷。本次中间运行的 vet、全量 7 包测试和 CLI 构建已返回 0，但不将其作为最终稳定基线的整体结果。完整日志保留为 `native-tar-go-attempt3.log`。

### 最终稳定基线结果

在主线程确认停止源码写入后，对项目与 TEE 替换目录的 535 个 Go 源文件及 `go.mod`、`go.sum` 生成 SHA-256 清单，重新创建容器执行整套检查。执行后重新扫描、计算清单，文件集合和全部哈希完全一致，记录于 `source-manifest-before.json`、`source-manifest-after.json`、`source-stability.json`。

| 命令 | 退出码 | 实际结果 |
| --- | --- | --- |
| `go list -deps -f '{{if .CgoFiles}}{{.ImportPath}} {{.CgoFiles}}{{end}}' ./...` | `0` | 当前默认构建路径未选择任何 CgoFiles |
| `go test -v ./agent -run 'Test.*(PrivateFile\|StateLock\|Codex\|ClaudeStore)' -count=1` | `0` | 23 个顶层测试通过、1 个跳过、0 个失败；包耗时 `32.328s` |
| `go vet ./...` | `0` | 无诊断输出 |
| `go test ./... -count=1` | `0` | 全部 7 个包通过，见下表 |
| `go build -o <容器专用临时目录>/bee ./cmd/bee` | `0` | CLI 构建成功，输出随容器回收 |
| 整个 Docker 检查进程 | `0` | 所有阶段成功结束 |

聚焦检查中的跳过项仅为 `TestCodexCredentialInspectionThroughMacOSKeychain`，原因是它要求 Darwin 和显式 `TEST_CODEX_KEYCHAIN=1`。`TestCodexLinuxKeyringDoesNotSilentlySelectFile` 在本次 Linux 上实际执行并通过；私有文件权限、符号链接拒绝、FIFO 锁拒绝、跨进程排他、持有进程退出后锁释放、旧 unlock 回调和 Claude Store 平台选择等测试也实际通过。该 Keyring 测试验证既有兼容性拒绝行为，未验证真实桌面 Secret Service。

| 全量测试包 | 结果/耗时 |
| --- | --- |
| `github.com/tokhive/bee/agent` | `ok 50.921s` |
| `github.com/tokhive/bee/beewire` | `ok 0.004s` |
| `github.com/tokhive/bee/cmd/bee` | `ok 0.039s` |
| `github.com/tokhive/bee/desktopbridge` | `ok 0.012s` |
| `github.com/tokhive/bee/logx` | `ok 0.002s` |
| `github.com/tokhive/bee/relay` | `ok 1.042s` |
| `github.com/tokhive/bee/telemetry` | `ok 0.006s` |

### 覆盖边界与清理

这是实际 Linux 内核、实际 Linux arm64 Go 工具链的补充证据；使用 Oracle Linux 容器，不能冒充 Ubuntu 桌面、原生 WebView、安装、托盘、Windows 或整个 P0 通过。未运行 Cargo、浏览器或 Bee App，未启动数据库，未停止用户服务。

该环境没有 gcc，Go 默认禁用 CGO。本次证明默认纯 Go 路径可以测试、vet 和构建 CLI，不证明启用 CGO 或 `go test -race` 的路径，也未验证 Ubuntu 的系统依赖。使用了既有真实 TEE 源目录替换，`go list -m -json` 确认目录为 `/src/.cache/reclaim-tee`；这不构成硬件 TEE、生产凭证或真实外部服务的端到端验收。

最终 `docker ps -a --filter name=bee-p0-qa-linux-arm64-20261023` 为空，本任务各具名 `--rm` 容器均已回收。未删除共享镜像层，未修改 Docker 设置，未暂存、提交或推送。校验过的下载归档、工具链、独立模块缓存及证据保留在项目 `.cache`，便于复查和后续复用；生产实现、依赖和计划均未由本验证代理修改。

### 追加证据索引

以下路径均相对 `.cache/qa/linux-go/`：

- `official-go-downloads.json`、`official-linux-arm64-release.json`、`tar-checksum-verification.json`：官方清单与完整归档校验。
- `download-handoff.log`、`tar-download-resume.log`：原下载接管和 Range 续传的字节证据。
- `tar-container-preflight.log`：最小环境命令结果。
- `additional-module-download.log`、`additional-eventstream-download.log`：三个锁定模块的下载来源及校验和。
- `native-tar-go-attempt1.log`、`native-tar-go-attempt2.log`、`native-tar-go-attempt3.log`：依赖准备与写入重叠期间的中间结果。
- `native-tar-go.log`：最终稳定基线完整输出，是本节通过结论的原始依据。
- `native-tar-container-command.json`、`native-tar-container-exit.json`、`native-go-summary.json`：实际容器参数、退出码与结果提取。
- `source-manifest-before.json`、`source-manifest-after.json`、`source-stability.json`：535 个文件前后稳定性证据。
- `native-container-final.log`：实际镜像身份、容器回收、依赖文件未改变的最终检查。
