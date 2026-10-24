# Mac 关窗观察副作用调查（2026-10-24）

本机 macOS 15.7.7 arm64 的隔离诊断版，三次关闭均实际执行隐藏（Tauri `is_visible=Ok(false)`）；随后两次读取 AX、一次单独截图，各引发 macOS `Reopen`，窗口变回 `Ok(true)`。此前“关闭后仍读到窗口”不能据此判定 Bee 隐藏失败。本轮没有修改正式产品代码。

## 来源与限制

- 原开发包绑定 `87b28a29aa84c2543b6b80b7e31204646e4fa76a`；[baseline.json](baseline.json) 记录两份包内二进制及外置 source JSON 的大小和 SHA256。
- 临时源码来自 `eb3bf109b0e941628fdec01629ed2d3f963ae16e` 的 Git archive；`desktop/src`、`desktop/src-tauri/src` 与 87 的 Git diff 为空。仅在忽略的 QA 副本中添加 [diagnostic.patch](diagnostic.patch)，记录事件、意图及 Tauri 自身窗口状态；完整两文件见 [lib](diagnostic-lib.rs)、[lifecycle](diagnostic-lifecycle.rs)。未增加 UI 动作、未改 Hide/Show 决策。
- sidecar 按 eb3 实际 HEAD 重新构建，[元数据](diagnostic-sidecar.source.json) 经过原有来源/target/TEE/工具链/SHA 门禁；[原生构建日志](build-native.log) 为 `--no-bundle` 构建，退出 0。临时 App 复制原包后换入新主程序/sidecar并 ad-hoc 签名，[签名日志](codesign.log) 与 [临时包清单](diagnostic-app-manifest.json) 分别留证。不得把该临时 App 冒充原 87 包验收。
- [早期构建尝试](events.md) 保留工具 PATH/GOROOT 错误及自有 `go version` 取消，不代表产品失败。最终 [sidecar构建](build-sidecar-attempt-5.log) 成功，固定 TEE 未修改。

## 对照结果

| 试验 | 读窗口前 | 读取后的原生事件/状态 |
| --- | --- | --- |
| AX 1 | [关闭后的原生日志](07-runtime-after-close-before-getter.log)：CloseRequested 后 `visible=false` | [AX后的日志](07-runtime-after-getter.log)：Reopen 前 false、后 true；[AX仍有窗口](07-after-close-ax.txt) |
| AX 2，延后读取 | [立即日志](08-runtime-immediate.log) 与 [延后日志](08-runtime-before-observation-delayed.log) 字节一致；6.567s 后精确 [ps](08-control-processes.json) 仍有父/owned子，无 Reopen | [getter开始时间](09-getter-start.json) 后出现 Reopen，[日志](09-runtime-after-getter.log) 的关闭→Reopen 间隔为 13.894s，状态 false→true |
| 截图，不先读 AX | [截图前日志](10-runtime-before-screenshot.log)：隐藏成功 | [截图后日志](10-runtime-after-screenshot.log)：Reopen 前 false、后 true；[所得图片](10-after-close-screenshot.jpg) 是重新打开后的窗口 |

三个“读前日志”均在对应 CUA click 返回后、任何 Bee 窗口观察前保存。测试中所有桌面控制均经 CUA；日志读取及 ps 不操作 UI。该对照证实了本轮工具调用与 Reopen 的可重复关联，无法仅靠这些记录判断工具内部具体调用；不外推到所有工具版本或旧的 cgWindowNotFound/timeout 原因。诊断日志不是无人干预期间持续采样，6.567s 时只证明未新增已记录事件及进程仍在。

## 清理与恢复

诊断版真实 [native ready](11-diagnostic-ready-ax.txt)，托盘创建返回成功（runtime seq0），但未执行托盘点击。原生菜单退出后，父35734/owned子35749的精确 [ps](13-diagnostic-quit-processes.json) 均不存在，无 App signal。原包恢复为父37620/owned子37628，真实 [ready](14-original-restored-ready-ax.txt) 后关闭详情，保留 [概览](15-original-restored-final-ax.txt)。[最终绑定](16-final-binding.json) 确认来源、原包签名及三个原文件 SHA 未变。临时未打包主程序已移入 QA 目录，避免占据普通 build 输出。

[验证结果](verification.json)：隐藏3/3、读取触发 Reopen 3/3；原包/元数据原字节保留，诊断进程回收。全部原始材料的大小、SHA256与来源见 [manifest](manifest.json)，图像实际为 JPEG。

仍未通过：原 87 包的非侵入式隐藏画面、真实托盘点击、Mac13/Win10/11/Ubuntu桌面矩阵、干净安装、原生显示缩放与 Downloads 拒绝/取消。临时诊断结果不能填这些格子；P0/P1整体保持未完成。
