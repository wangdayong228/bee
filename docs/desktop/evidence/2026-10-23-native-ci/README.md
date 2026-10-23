# 2026-10-23 原生构建与测试证据

这些结果只覆盖下述组件，不代表完整 P0、Windows 10/11 或 Ubuntu 桌面验收。

- 源码提交：`e4b0df8b72c223e4754a3e552baaa6e27490cfd7`（Windows 两项）。
- Windows TEE：[成功 run 39896456139](https://github.com/wangdayong228/bee/actions/runs/39896456139)。Windows Server 2022 10.0.20348 x64、Node 24.22.1、Git 2.56.0.windows.2。tooling 32 项：29 通过、0 失败、3 项 POSIX 专属跳过；真实固定 TEE 3 项全部通过。首次导出、完整缓存重验、物化位置与原目标分别篡改后拒绝并保留原缓存通过。
- 固定 TEE revision `a687f86d781e825c04c1d84d75b41bba5d862254`，原归档 SHA256 `4bc9caad3ad2ce5de01b9983a750cee6380098fc308333c30c098fbf8e7bad38`；服务文件 SHA256 `2ed07bb2f6b4f5bc1d18fa41c142fda772a0c754c11b52cf0380b2502c17a594`。Windows 采用同归档普通文件内容副本，不依赖 symlink 权限。
- Windows 安全操作：[行为 RED run 39896456172](https://github.com/wangdayong228/bee/actions/runs/39896456172)。实际 Go 1.27.3 windows/amd64 已编译并执行聚焦测试，16 个顶层测试失败，包含私有文件写入、ACL、no-reparse 与锁操作的明确 not-implemented 错误。它证明安全操作尚未实现，不能写作通过；原生日志用于驱动后续实现。完整 vet/test/build 步骤因前置失败未执行。
- Linux：实际 Oracle Linux 9.4 aarch64 容器、glibc 2.34、Go 1.27.3、非 root UID 1000、CGO=0、network none。聚焦 23 项通过、1 项 macOS 专属跳过；vet、全量 7 包测试、CLI 构建退出 0。535 个源码及模块文件前后 hash 一致。源码快照与容器命令见 linux-go-report.md；这不是 Ubuntu GUI/WebKitGTK 或安装验收。

两个 Windows 摘录由 GitHub 原始日志保留操作结果，不复制 checkout 凭证字段。完整日志在本地 `.cache/qa/windows-tee/run-39896456139.log` 与 `.cache/qa/windows-security-run-39896456172.log`；下列 manifest 同时记录原始日志 SHA256，便于复核。
