# 原生报告下载反馈增量审查

日期：2026-10-24。基线：`5a81eae`。范围：本次 6 个 tracked 文件与 `desktop/tests/native-download.spec.ts`，依据 `p1-native-download-feedback-brief.md`；未审查整体 P0/P1 验收矩阵。

结论：**Needs fixes**。C：0，I：1，M：0。

## I1：注册失败后遗留 Tauri JS 回调，重复尝试持续累积

- 位置：`desktop/src/system/bridge.ts:30`；漏检位置：`desktop/tests/native-download.spec.ts:14`、`:98`。
- 触发：`plugin:event|listen` 注册被拒绝。已安装的 `@tauri-apps/api` 2.12.4 在 `event.js:139` 调用 `transformCallback(handler)`，随后才等待原生注册；该 Promise 拒绝时不会注销这个 callback。当前 `onDownload()` 直接传播拒绝，因此拿不到 `unlisten`，也没有清理已分配 callback 的路径。
- 影响：每次失败重试都会在当前 webview 生命周期内留下新的 JS callback 及其闭包。这里的闭包还引用本次下载的结果 listener。报告的 `finally` 会撤销 Blob URL，但无法释放这个 callback，违反方案“监听失败均释放监听与 URL”的要求。现有失败测试的 `listeners()` 仅返回 `subscriptions.size`，所以无法发现注册前创建的 callback 残留。
- 可复现证据：用 Node 直接导入当前 `createSystemBridge` 与已安装的真实 Tauri API，仅替换原生 transport（不启动 GUI、服务或构建）；连续三次令 `plugin:event|listen` 抛出 `listen-denied`。每次均正确向调用方保留拒绝错误，但 callback Map 大小依次为 **1、2、3**，没有安装任何原生订阅。这是 JS 资源清理证据，不是原生下载行为证据。
- 最小修补建议：在现有 SystemBridge 内将下载监听的 callback 生命周期纳入控制，使注册拒绝时也能按其 ID 注销，并保留原始注册错误；无需新增权限或依赖。补充注册失败后 callback 数回到基线、连续重试不增长的断言。成功注销也应保留现有的 active 标记，继续隔离迟到事件。

## 其余核对

- 原生使用 `Finished.success`，未依赖 macOS 恒为 `None` 的 path；回执经现有 SystemBridge 传递。
- JS 先订阅后点击；按本次 Blob URL 匹配；桥接层拒绝非布尔 success 和非字符串 URL；Promise 首次结算与 active 标记隔离重复和迟到回执。
- 30 秒无回执返回未确认；普通浏览器返回 initiated；原生 success=false 的错误保留实际值，页面不把它当完成。
- 本次新增展示文案及失败组合文案已有英文映射；未引入文件写入命令、依赖或权限。
- 尚未提供新包的原生正负测试结果，本审查不据网页 transport fixture 声称原生成功或失败已验证。该验证由主控执行。

本审查只读取源码、配置和测试，执行一次无 GUI 的 Node 清理复现；未运行 1420、产品构建或 CI，未改源码、index 或 HEAD。

## 附录：I1 修补窄复核

日期：2026-10-24。本节保留上方首次 **Needs fixes** 的历史结论，仅复核 I1 修补。

复核结论：**Approved（I1 已闭合）**。本次窄复核无新增 C/I/M 问题。

- `desktop/src/system/bridge.ts:33` 起显式持有 `transformCallback` 返回的 handler ID；原生注册拒绝时先令 `active=false`，再通过锁定运行时的 `unregisterCallback(handler)` 回收 callback，并重新抛出原 cause。成功路径的 target、event 参数和注销顺序与锁定 `@tauri-apps/api` 2.12.4 的 `listen` / `_unlisten` 一致；同版本 `core.Channel.cleanupCallback()` 使用相同 callback 注销入口。未新增依赖或权限。
- `desktop/tests/native-download.spec.ts:103` 起连续三次触发注册拒绝，每次断言 callback 数回到 0；成功用例亦增加 callback 清理断言，覆盖了首次审查中只统计原生订阅的缺口。
- 独立重跑无 GUI Node 复现，直接导入当前 SystemBridge 和已安装 Tauri API。连续三次注册拒绝后，callback 数和原生订阅数均为 **0、0、0**；每次向调用者抛出的错误与注入的原 cause 为同一对象。
- 同一复现额外令成功注册的 event ID 与 callback ID 不同，验证按 event ID 注销后两张表均清空；重复注销无额外动作；错误 success 类型被忽略，注销前已捕获的迟到 callback 也被 active 标记隔离。

以上为 I1 的 JS callback 生命周期验证；不代替新包的原生下载正负测试。本次仅追加本报告，未修改产品文件，未启动 GUI、1420、构建或 CI。
