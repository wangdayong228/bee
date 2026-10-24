# Linux 860×600 客户端窗口补证

工具绑定 `9ca837d902fbf026be9931f796a3d1289e33dad3`；目标分别为原始 `2681edca2c56bca9d2ce30db4198fb5784d98b65` 和 `87b28a29aa84c2543b6b80b7e31204646e4fa76a` 的 Ubuntu24 ARM AppImage。两包均完成提取模式下同一 owned 窗口 1000×700→860×600、完整十秒观察及最终尺寸核对；只证明客户端几何、进程存活和末图，不代表整个 P0/P1 或真实桌面验收通过。

## 来源与环境

各目标有独立真实 Git checkout，仅覆盖已经独立审查 Approved 的新 smoke 工具；`combination.json` 和 `tool-overlay.diff` 记录双来源。原 CLI 的 checkout/source revision、固定 TEE、Go 目标、包内 Bee 与 SHA 校验均保留。不是9源码产品包，不改写87原CI自身1000×700的观测。

QA镜像 `bee-linux-minimum-window-qa:20261023`，image SHA `ef455d7cb089d177ce7b17aebf3b3cc9639aec8bd7b4e88221d0dd060a18a5a4`；实际 Ubuntu24.04.5 arm64 / LinuxKit6.10.11。nonroot1001、network=none、只读输入、独立 D-Bus/Xvfb 与 Docker init；无WM、无FUSE设备，未关闭sandbox或扩大权限。Node24.22.1 linux-arm64官方归档SHA `dbabf7a1cbf947e6059ffad2c27b80041db97dea1e553b62afdee7f13fca336e` 已对照SHASUMS。镜像构建与预检exit0，原始文件位于 `environment/`。

## 实际结果

| 目标包 | 包SHA256（均139078152bytes） | resize后观察 | 末图 |
| --- | --- | --- | --- |
| 2681 | `b6fcd0c14889fe200d48d9d01bc38d4bc2cf3b005be1b5d7c708a174f8500eae` | 10190ms，exit0 | [860×600](target-2681edc/extract-utf8/startup/window.png) |
| 87 | `db710f967c04eb938affcb0db9fb3cfeac4460bc11c8b135082ba69e31fbe20a` | 10212ms，exit0 | [860×600](target-87b28a2/extract-runnable-utf8/startup/window.png) |

两次均同owned窗口ID2097155，resize后及最终采图前后读回860×600；cleanup记录parentClosed=true、liveRemaining=[]、zombies=[]。末图已实际查看，均为非空英文P1 Overview，显示Demo data；初始灰色1000×700图保留，不以初图推断ready。独立PNG尺寸清单见 `image-dimensions.json`。

2681包内Bee SHA `b3a5c7687767a53292b57e07a1bf04a7343d5d12a902aa8a823d274f19e3b309`；87包内Bee SHA `3e940d479ccf9e0358dafd7491cbfaf3b0a48d281810c360ec7f898e71c8eae7`，87 source.json原始SHA `f0c21ee7a01fe11f70759a69a093468a26a7883ccde0a95435708301ff481363`。两份原始source.json及dirty版本后缀保留，未伪装发行版本。固定TEE为 `a687f86d781e825c04c1d84d75b41bba5d862254`。

## 保留的失败与修正

2681前两轮20秒找窗失败。第二轮独立X11树已有1000×700窗口，并明确记录UTF8_STRING转换到ANSI_X3.4-1968失败；仅将第三轮QA进程LANG/LC_ALL设为C.UTF-8，保持产品、查找和观察预算及安全参数不变后通过。两轮RED与成功分别保存在 `target-2681edc/extract/`、`extract-diagnostic/`、`extract-utf8/`。stderr的DRI3/appsink/accessibility警告原样保留，不自行认定为找窗根因。

87从保留ZIP提取的原始包mode0644，首次CLI提取前EACCES退出1。原下载未改；专用runnable-payload副本只恢复0755，包/source字节SHA不变，第二轮通过。失败在 `target-87b28a2/extract-utf8/`，成功在 `extract-runnable-utf8/`；不是产品启动失败，也没有绕过来源门禁。

## 工具验证与范围

`review-and-tests/` 保留末次geometry读取期间退出/改属的真实RED2例、GREEN2例、完整34/34（0fail/skip/cancelled）日志及独立Spec✅/Approved复核。最终工具在最后一次geometry读取后再次确认owned窗口与进程存活，随后才能成功。

本次没有业务交互、native manager ready、真实WM/标题栏无遮挡、托盘、菜单退出、干净用户安装或原生125%/150%显示证据，也没有FUSE运行。Docker init下当次zombies=[]不外推为远端CI无zombie。专用QA容器均已退出；未操作用户数据库容器。

`manifest.json` 精确列出本目录除自身外的全部文件及原始来源、字节数和SHA256。精选归档不含安装包、ZIP、工具链、Git数据库；完整缓存仍按目标独立保留。9源码Linux远端CI另行收证，不与此双来源补证合并。
