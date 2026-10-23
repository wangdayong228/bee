# P0/P1 CI 窗口发现测试确定性修补报告

## 结论与范围

已完成并提交 `87b28a29aa84c2543b6b80b7e31204646e4fa76a`（`test(desktop): make primary window discovery clock deterministic`）。提交仅包含 `desktop/src-tauri/vendor/tauri-plugin-single-instance/src/platform_impl/windows_registration.rs`。未修改生产调用点、依赖、权限、平台目标、CI、UI、产品超时预算；未 push、未执行全套 Rust/E2E 或原生打包。

原 CI 失败证据按 brief：MacIntel run39931368193/source2681 成功夹具的 100ms 真实预算观测到 185ms；这是墙钟成功夹具受调度影响，不是已证明的原生 HWND 故障，也不能定位哪一次 sleep 被调度。

## 实现与边界

公开 `forward_to_primary` 签名保留，薄 wrapper 传入 `Instant::now`、`std::thread::sleep`；私有 `forward_to_primary_with_clock` 接收两个闭包。沿用 Instant/Duration，无新依赖、trait 或全局状态。

循环仍先 find，再按同一 deadline 计算 remaining；remaining 为零优先失败，即使 find 刚返回 Some 也不发送。sleep 为 `min(remaining, 20ms)`。send 成功或失败均立即返回，不重复发送；原 1460 错误保留。超时消息保留失败检查、limit、elapsed 证据，elapsed 使用本轮 deadline 检查的同一时间样本。

测试覆盖：第三次 probe 返回 42、仅发送一次、100ms 经两次 20ms 后精确剩余 60ms；无窗口的 10ms 预算被一次受限 sleep 消耗后报超时、不发送；发送错误仅一次且保留 1460；find 恰好推进到 100ms 或越过至 101ms 时不发送。另用零预算覆盖公开真实时钟 wrapper，不执行真实 sleep。原 NULL handle/native error 测试保留。

## 实际 RED/GREEN

证据目录：`.cache/qa/p1-ci-discovery-clock/`，stdout/stderr 合并保存 `.log`，退出码保存对应 `.exit`。

1. RED：先仅把原成功测试的剩余预算断言改为精确 60ms，生产代码未改。

```sh
RUSTUP_TOOLCHAIN=1.94 rustc --test desktop/src-tauri/vendor/tauri-plugin-single-instance/src/platform_impl/windows_registration.rs -o .cache/qa/p1-ci-discovery-clock/windows-registration-red
.cache/qa/p1-ci-discovery-clock/windows-registration-red
```

编译退出 0；运行退出 101，3 passed / 1 failed。失败为 `left: 54.325167ms, right: 60ms`。证明旧测试通路无法给出逻辑预算的确定性结果；新 deadline 边界断言是既有正确 fail-closed 行为的回归覆盖，不声称其在旧生产实现上失败。证据：`red-compile.log/.exit`、`red-test.log/.exit`。

2. GREEN（最终源码）：

```sh
RUSTUP_TOOLCHAIN=1.94 rustc --test desktop/src-tauri/vendor/tauri-plugin-single-instance/src/platform_impl/windows_registration.rs -o .cache/qa/p1-ci-discovery-clock/windows-registration-green
.cache/qa/p1-ci-discovery-clock/windows-registration-green
RUSTUP_TOOLCHAIN=1.94 CARGO_HOME="$PWD/.cache/cargo-home" cargo test --offline --locked --manifest-path desktop/src-tauri/Cargo.toml windows_registration
```

最终 rustc 编译退出 0，单文件运行退出 0，5 passed / 0 failed，0.00s。Cargo 退出 0，lib 5 passed / 0 failed / 37 filtered out，main 0 tests；最终输出无 warning。证据：`green-compile.log/.exit`、`green-test.log/.exit`、`cargo-test.log/.exit`。这些结果只证明该覆盖范围，不代表新 source 的全套通过。

工具备注：第一次未显式指定工具链的 rustc 触发 rustup 尝试获取 `1.94.0`；发现后停止该进程，后续全部显式使用已安装的 `1.94`（Rust 1.94），未更改仓库工具链配置。首次 Cargo 曾因 wrapper 在 Mac 测试中未引用产生 dead_code warning，补充零预算 wrapper 断言后重新运行上述最终 GREEN 命令，无 warning。

## 自审与限制

`git diff --check` 退出 0，证据 `diff-check.log/.exit`。逐项检查：单文件范围、公开生产 wrapper、deadline 顺序、受限 sleep、精确预算、迟到拒绝、发送至多一次及错误保留均符合 brief。提交前 staged stat 为 1 file，70 insertions / 10 deletions；提交后工作区 tracked 状态干净。

无已知阻塞顾虑。未在 Windows 原生环境运行，不把这些闭包测试宣称为 Windows HWND 集成验证；远端 CI 与其他原生证据由 root 另行处理。
