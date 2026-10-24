# P1 任务6：Linux 最小客户端窗口窄审查

## Spec Compliance

- ❌ Issues found：最终 geometry 读取期间失去活进程或窗口归属仍可进入 `ok=true`，不满足 brief 的“丢窗/归属失效不能 ok”；见下方 Important I1。其余本 diff 可见要求符合。
- ✅ 默认 resize 对原窗口 ID 请求 `860×600`，使用既有 command 包装且硬 timeout 为 `5000ms`，未加入重试预算（`desktop/scripts/smoke-linux-appimage.mjs:86`、`:164`、`:165`、`:166`）。
- ✅ geometry 按独立 WIDTH/HEIGHT 行检查缺失、重复、非法与安全整数，并严格比较 `860/600`；记录原文、实际值与检查时点（`desktop/scripts/smoke-linux-appimage.mjs:117`、`:120`、`:127`、`:131`、`:133`）。
- ✅ 保留 initial/final 采样与既有图片路径，resize 成功、尺寸与归属读回通过之后才开始观察；final 采图前和采图后均校验尺寸（`desktop/scripts/smoke-linux-appimage.mjs:143`、`:148`、`:149`、`:163`、`:170`、`:174`、`:185`、`:186`）。
- ✅ scope 明确仅客户端尺寸和 startup，排除 readiness、内容可见与桌面装饰断言（`desktop/scripts/smoke-linux-appimage.mjs:97`）。
- ⚠️ 窄 scope 无法证明：真实 Linux AppImage 接受 `860×600`、标题栏、无遮挡、readiness、三端与缩放。本次 fixture 与 diff 不能代替原生/人工证据，也不能关闭完整 P1 任务6。
- ⚠️ 窄 scope 无法证明：未出现在 diff 中的 bundle/source/sidecar SHA 门禁、提取/FUSE、20秒找窗及完整 finally 清理实现本身是否正确；本 diff 未改动这些实现。需要继续沿用已有独立证据，而非由本审查重新背书。

## Strengths

- 尺寸失败信息包含本轮原始 geometry、实际尺寸、字段/原因与要求；resize 包装保留原错误 stack 和 cause，符合 fail-fast-with-evidence（`desktop/scripts/smoke-linux-appimage.mjs:127`、`:133`、`:168`）。
- 测试检查实际 observation 报告、图片是否生成和真实 child 的 cleanup，涵盖成功但尺寸不变、坏字段、前后回弹、resize 错误/超时及归属变化，而非仅断言 mock 调用（`desktop/tests/linux-appimage.test.mjs:156`、`:165`、`:178`、`:190`、`:203`、`:212`）。
- 默认命令测试通过临时可执行 xdotool 验证真实非零退出和 spawnSync 硬 timeout，同时检查具体参数及原始错误证据；延迟 resize 用下界断言验证不抵扣观察时间，未要求精确调度等值（`desktop/tests/linux-appimage.test.mjs:144`、`:226`、`:236`、`:237`）。

## Issues

### Critical（Must Fix）

- 无（0）。

### Important（Should Fix）

- **I1 — 末次 geometry 调用后的活进程/归属状态没有复核。** `desktop/scripts/smoke-linux-appimage.mjs:184` 先执行最后一次 `requireOwnedWindow`，随后 `:185` 再 await `inspectWindow`，`:186` 只验证尺寸，`:188` 直接置 `ok=true`。默认 inspect 包含两个各最多5000ms的外部调用（`:88`、`:89`）；若此期间 child 退出，或同一窗口 ID 改属无关进程而探针仍返回 `860×600`，没有任何后续 drain/活进程/归属检查阻止成功。该风险正是新增 `requireOwnedWindow` 在 `:108` 注释说明的阻塞调用风险。现有归属用例在 resize 或截图阶段触发失效（`desktop/tests/linux-appimage.test.mjs:212`、`:247`），没有覆盖最后一次 inspect。修复应在末次 geometry 读取与尺寸校验之后再执行活进程/同 ID 归属复核，并补一项在最后一次 inspect 中改变归属或使 child 退出、返回合法尺寸仍必须失败并 cleanup 的针对性用例；保留原早退 stderr 证据。

### Minor（Nice to Have）

- 无（0）。

## Assessment

- **Task quality: Needs fixes。** C/I/M = **0/1/0**。实现主体范围克制、诊断证据充分，但最后一段外部探针重新打开了错误成功窗口，需要关闭后再通过本任务门禁。
- 审查输入：按序读取 brief、实现报告与 `review-57a6fd1..a4611f3.diff` 一次；base `57a6fd1`、head `a4611f3`，仅两个源文件。没有重新打开已改源码，没有定点扩读调用接口；I1 所需控制流及默认接口已完整包含于 diff。
- 验证边界：实现报告记录最终 Node 测试 **32/32**、syntax 与 diff 检查通过；本审查未复跑测试、未另读日志，未执行 native/GUI/1420、git/分支写操作、push 或 CI 操作。I1 来自 diff 的静态时序路径，不是已有通过日志已排除的场景。

## I1 修补复核（2026-10-23，head 9ca837d）

- **Spec Compliance：✅ Spec compliant。Task quality：Approved。当前未解决 C/I/M = 0/0/0。** 本节替代前文对旧 head `a4611f3` 的阻断结论；前文作为发现历史保留。
- **I1 已关闭。** `desktop/scripts/smoke-linux-appimage.mjs:185` 的末次 geometry 读取与 `:186` 的尺寸校验之后，`:187` 新增 `await requireOwnedWindow('after final geometry')`，再于 `:189` 置 `ok=true`。复用 helper 的事件 drain、child exit 检查与同 ID 活进程组归属检查（`:107`、`:109`、`:110`、`:111`、`:113`），修补了原 I1 指出的读取期间退出/改属仍成功路径；未修改生产错误文本或弱化原校验。
- **针对性覆盖充分。** 新增两条分支从末图后的 inspect 触发失效，仍返回合法 `860×600`（`desktop/tests/linux-appimage.test.mjs:258`、`:263`、`:264`、`:277`）。退出分支让真实 spawned child 收到文件请求后写 E47 并 exit(7)，等待真实 PID 消失；归属分支把同 ID 42 改属测试父进程（`:267`、`:269`、`:275`、`:280`、`:282`）。两条均经既有 helper 要求 reject、`ok=false` 与 cleanup 成功（`:156`、`:285`），并确认末次尺寸合法但没有成功 observation 时长、末图已存在（`:288`、`:289`、`:290`）；退出 code/stderr 和改属实际窗口分别有断言（`:292`、`:293`、`:294`）。
- **新增 fixture 失败文案符合 fail-fast-with-evidence。** 有界3000ms等待在超限时给出本轮仍存在的实际 PID、当前时间及要求截止时间（`desktop/tests/linux-appimage.test.mjs:268`、`:272`），没有用精确墙钟等值断言。
- **原任务要求未被修补破坏。** 完整 range 中生产修补仅增加上述一次归属复核；默认5000ms resize（`desktop/scripts/smoke-linux-appimage.mjs:86`）、严格尺寸解析（`:117`）、initial/final 图路径（`:149`、`:150`）、resize 完成后起算观察（`:170`、`:174`、`:175`）、采图前后尺寸核对（`:148`、`:186`）及 scope（`:97`）均保留。新增测试未替换原成功、回弹、坏 geometry、resize 失败/超时、归属失败回归（`desktop/tests/linux-appimage.test.mjs:126`、`:165`、`:178`、`:190`、`:203`、`:212`、`:226`、`:247`）。
- **验证沿用已有证据。** root 已核 RED 两条均为 `Missing expected rejection`、最新完整 **34/34** 日志与 clean status；实现报告记录最终 syntax/diff 检查均通过。本复核未重跑测试或另行 git 操作，不把报告当作新增运行结果。
- **⚠️ 窄 scope 仍无法证明：** 真实 Linux AppImage、标题栏、无遮挡、readiness、三端与缩放；也未扩大审查未变的 SHA/提取/FUSE/cleanup 实现。本结论仅关闭最小客户端窗口自动证据子任务的代码审查与 I1，不代表完整 P1 任务6完成。
- **复核读取边界：** 按序重读原 brief、修补 brief 与实现报告新增 I1 段，并完整读取 `review-57a6fd1..9ca837d.diff` 一次。仅两个源文件、两提交；未重新打开源文件或扩读接口，未执行 native/GUI/1420、push 或 CI 操作。
