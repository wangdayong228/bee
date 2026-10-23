# Ubuntu 原生 AppImage 修补验证证据

2026-10-23，[run39905806798](https://github.com/wangdayong228/bee/actions/runs/39905806798) 绑定 source `22c5f912659bad7af4a602cf2e3a8b019cd5ce94`，包含 RUNPATH 修补 `1e1019d`。本目录归档已完成的 Ubuntu22.04 x64、22.04 arm64、24.04 arm64 三行原始检查产物；24.04 x64 尚在准备依赖，本快照不能证明四行全部通过。

三行 Go vet/全量7包、前端类型和构建、tooling37/37、AppImage tooling16/16、bridge10/10、Chromium53/53、Rust35/35 均通过，AppImage构建及提取/FUSE两种独立启动完成。包内 Bee SHA 与构建source清单一致，未放宽来源门禁。

`ubuntu-*/` 保留完整原始检查产物、初/末窗口及桌面图、采样时间/几何、进程和 stderr。初图在启动后约309–532ms为黑，10.5–10.8s末图已显示五页和准确的“真实业务未接入”状态；不冒充 bridge ready、真实业务或托盘验收。正常末图存在时仍有部分WebKit/GStreamer警告；清理liveRemaining为空不代表所有zombie已回收。详细证据与边界见 [assessment.md](assessment.md)。

两份 `*-elf.log` 记录从实际22.04 x64及24.04 arm64 AppImage定向提取的Bee：均含动态libc、对应解释器及 DT_RUNPATH `[$ORIGIN/../lib]`，SHA精确匹配source清单。CI未直接采bundle前readelf，结论通过字节等同性连接；22.04 arm64未额外提取ELF。实际AppImage未提交仓库，远端测试artifact保留14天。

本次是原生构建及无输入窗口观察；没有干净用户安装、托盘/无托盘行为、菜单退出、官方登录来源、生产签名或更新验收。`run-snapshot.json`为当时状态；manifest记录归档原始文件字节和SHA。

原始日志保留工具输出的CRLF、空行及ELF表尾空格，未为格式检查改写证据；Markdown/JSON另行执行差异格式检查。
