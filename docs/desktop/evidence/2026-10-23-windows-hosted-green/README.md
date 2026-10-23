# Windows Server 2022 真实构建与 Rust 验证

2026-10-23，[run39904695326](https://github.com/wangdayong228/bee/actions/runs/39904695326) 全部步骤成功；绑定源码 `30487662d0eab4c42a392648818e1378e2b79ffa`。首轮失败因 Git Bash 将 `/usr/bin/link` 放在 MSVC 前；Cargo/Tauri 改用原生 PowerShell 并在实际消费工具前核验 linker 后复验。原始失败记录仍保留于执行账本，不将其当作产品 Rust 测试失败。

- 原生 Server2022 Datacenter build20348、x64，Node24.22.1、Go1.27.3、Rust1.94.0；WebView2 Runtime131.0.2903.86。
- Cargo **30/30、0失败、0忽略**（12.31s），包含真实 Bee 管理二进制握手/ping/stop；其它OS cfg不在本轮计数。
- NSIS开发包成功生成，16,257,683字节，SHA256 `fb86428fbac7a44756e8c15fd7f493937a2140009964c437947a226afd11c13b`。主代理下载实际安装包后独立核对其字节数与SHA，均与 packages.json 一致。包未提交仓库，测试artifact保留14天。
- source记录实际版本 `dev+30487662d0ea-dirty`，如实保留dirty标识；固定TEE revision未变。本轮不声称clean构建。

只证明该Server环境中的开发构建和集成测试；未安装或启动该NSIS，Win10/11、含空格安装路径、GUI/托盘、官方登录来源、生产签名及更新仍未验证。

`run.json`保存服务端步骤状态；其余原始日志和版本/包清单保留原CRLF字节。`manifest.json`记录这些归档文件的精确SHA。
