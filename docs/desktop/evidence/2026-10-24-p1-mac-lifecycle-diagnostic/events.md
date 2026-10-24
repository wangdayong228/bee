# 操作记录

1. 归档 eb3 源码至 ignored QA 目录，记录原包/sidecar source 三文件 SHA；原正式源码未改。
2. sidecar 首次缺 rustc PATH；第二次走系统 Go 自动查找，精确取消自有 `go version` PID31636/PPID31619；第三次固定 Go 路径少一层 `go/`；第四次继承 GOROOT=/usr/local/go，导致 std uuid 解析失败。最终修正本次进程 PATH并 unset GOROOT，固定本地 Go1.27.3，attempt5成功。全部失败/取消日志原样保留。
3. 临时原生 `--no-bundle` 构建成功。用原包副本换入已构建主程序/sidecar，重新 ad-hoc 签名并 strict/deep 验证；原 .app 未覆盖。
4. 绑定原包5669/5787，打开菜单。先保存完整菜单树导致索引从退出4变为3；旧索引4被工具拒绝，未执行退出。核对保存树后点击3，清单及精确 ps 均确认原父子消失。
5. 启动临时 App，父35734/owned子35749。记录关闭前截图/AX；依次执行 AX1、延后 AX2、截图三组。逐组保存 getter 前后的日志；第二组先独立 ps，再读取 AX，日志先后见 README。
6. 单独截图后重新获取完整树，打开连接详情，保存真实 ready。打开原生菜单并点击退出，清单及精确 ps 确认诊断父子都消失；无 App signal。
7. 重新启动原87包，经原生菜单打开，连接详情真实ready；Escape恢复概览和触发器焦点。当前父37620/owned子37628。再次 strict/deep 验签、原三文件SHA一致。
8. 临时未打包 native executable 移入 QA；诊断 App/源码/缓存留在 ignored QA，未加入产品或默认构建。
