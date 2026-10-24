# P1 Linux 最小客户端窗口窄修复报告

## 结果与范围

已按 `p1-linux-minimum-window-fix-brief.md` 实施，基线 `57a6fd13a714467e018797a8454a219a982ac506`。source 只改 `desktop/scripts/smoke-linux-appimage.mjs`、`desktop/tests/linux-appimage.test.mjs`。本报告及测试日志位于忽略的 `.superpowers/sdd/`，不纳入 source commit。

保留 initial 默认窗口采样及 `window.initial.png`；采图后重新核对同一窗口 ID 仍属于本次活进程组，才用现有 command 包装执行 `xdotool windowsize --sync <owned-id> 860 600`，单命令硬 timeout 为 5000ms，无重试/轮询预算叠加。只增加 resizeWindow 注入点，复用 inspectWindow 立即读取真实 geometry。

解析独立 WIDTH/HEIGHT 整数行，拒绝缺失、非法、重复/冲突及不安全整数，实际尺寸必须恰为 860×600。resize 完成、读回达标并复核归属后才开始原观察周期（生产默认 10000ms）。final 采图前和末图/归属复核后分别再读回并校验尺寸；末图路径仍是 `window.png`、`root.png`，samples 仍只有 initial/final 两个阶段。

observation 记录 resize 请求值、窗口、原始 geometry、实际尺寸、开始/检查/完成时点及 observationStartedAt；最终复核原文与尺寸保存在 finalGeometry。scope 明确只有客户端尺寸和 startup，不验证 readiness、无遮挡或桌面装饰。错误包含本轮原因、实际值、要求值；resize 包装保留原错误消息和堆栈。所有新增失败仍由原 finally 记录并清理专用进程组。

精确包/source/sidecar SHA 门禁、extract/FUSE 分支、20秒找窗含义、原有早退、进程组清理逻辑均未修改。

## TDD 与实际命令

所有命令工作目录为 `/Users/dayong/myspace/mywork/tokenhive/.worktrees/bee-desktop-p0`；Node 使用本机已有缓存 `/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node`，实际 `--version` 为 `v24.18.1`。未安装工具或依赖。

RED（先改测试、未改生产脚本）：

```sh
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --test desktop/tests/linux-appimage.test.mjs > .superpowers/sdd/p1-linux-minimum-window-red.log 2>&1
```

退出 1，30 tests、15 pass、15 fail。失败包括旧采样最终仍为1000×700（要求860×600）、resize 请求为空，以及尺寸不变、坏 geometry、回弹、resize 错误、归属变化的 `Missing expected rejection`。原因是基线根本未 resize 或断言实际几何，符合预期 RED。

首次实现完整运行的日志为 `p1-linux-minimum-window-green-iteration.log`：30 tests、29 pass、1 fail，退出1。剩余用例同时模拟“resize期间归属丢失”和“resize后仍返回1000×700”，先被正确的尺寸不符拦截，未抵达归属检查；已将该 fixture 隔离为实际尺寸达标、仅丢失归属，未为迁就断言削弱生产校验。

随后增加默认命令实际调用边界覆盖：临时可执行 xdotool fixture 真实退出19或阻塞，并由原 spawnSync 的5000ms timeout实际触发 ETIMEDOUT；不依赖 X11。定点命令：

```sh
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --test --test-name-pattern='ownership loss during resize|default resize command' desktop/tests/linux-appimage.test.mjs > .superpowers/sdd/p1-linux-minimum-window-focused.log 2>&1
```

退出0，3 tests、3 pass、0 fail；日志显示硬timeout用例约5247ms，这只是观测耗时，测试没有依赖精确墙钟调度断言。

完整 GREEN 命令：

```sh
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --test desktop/tests/linux-appimage.test.mjs > .superpowers/sdd/p1-linux-minimum-window-green.log 2>&1
```

退出0，32 tests、32 pass、0 fail、0 skipped/cancelled，约13503ms。自审将 helper 中子进程早退与归属失效分开报告，以保留早退 stderr 后，对最终版本再次执行：

```sh
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --test desktop/tests/linux-appimage.test.mjs > .superpowers/sdd/p1-linux-minimum-window-green-final.log 2>&1
```

最终退出0，32 tests、32 pass、0 fail、0 skipped/cancelled，13614.386208ms；无测试警告。

静态检查在最终版本执行，均退出0、无输出：

```sh
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --check desktop/scripts/smoke-linux-appimage.mjs
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --check desktop/tests/linux-appimage.test.mjs
git diff --check
```

## 覆盖与自审

- 成功流真实 Node child：initial1000×700→final860×600；只请求本次owned窗口，旁边无关窗口不参与；最终 PNG 路径、原始geometry、实际尺寸、时点及scope均被检查。
- resize fixture 延迟180ms，observeMs150ms；断言末图距离resize完成至少observeMs，未用精确调度等值断言。生产默认10秒未缩短。
- resize退出成功但实际不变拒绝；末图前回弹、末图后回弹均拒绝；缺失、inline、非法、负值、重复、冲突字段均拒绝并保留原始geometry。
- 注入失败/超时，以及默认 command 的真实非零退出/硬timeout均进入finally；报告保留原因、要求及cleanup为空。
- resize之前/期间丢归属均失败，之前失效时不会发送resize请求；原有末图期间丢归属失败及cleanup回归保留。
- 原有SHA、revision、包外symlink拒绝，子环境隔离、真实子孙进程和无关进程存活、无窗/早退/采图失败等用例全部保留。

已逐项核对brief和两文件diff，未发现未解决的本次实现缺口。未新增产品设计、泛化viewport平台、持久状态、WM、权限、依赖或workflow变化。root仍需执行独立fresh task review。

## 原生边界与顾虑

本机运行只证明控制流程、真实进程组清理、PNG fixture与默认命令的失败/超时包装；geometry和图片是fixture，临时xdotool也不是Linux原生命令。因此不能声称真实AppImage已接受860×600，不能声称Linux原生矩阵通过，更不能关闭完整P1任务6。真实标题栏、桌面装饰、无遮挡、readiness、三端及缩放等仍待后续独立原生/人工证据。

本轮未push、未构建或运行native、未安装、未启动1420、未触发/取消/重跑CI。未操作现87远端运行或混用其证据。没有已知实现正确性顾虑；上述原生未知边界保留。

## 提交

`a4611f3` — `test(desktop): verify Linux minimum client window geometry`，仅以上两个源文件。提交前 staged diff check 退出0；未push。

## I1 末次 geometry 后活性与归属复核修补（2026-10-23）

按 `p1-linux-final-geometry-liveness-fix-brief.md`，从干净基线 `a4611f3` 开始。根因是末次 `requireOwnedWindow('after final capture')` 后仍有一次 await inspectWindow；该外部读取可跨过 child 退出或同 ID 窗口改属，而合法尺寸后直接进入 ok。现仅在 finalGeometry 尺寸校验后增加 `await requireOwnedWindow('after final geometry')`，复用原 helper 的事件 drain、活 child、进程组和同 ID 窗口归属检查；未修改生产错误文本。

新增两条真实 spawned child 回归：末次 inspect 写入退出请求，child 自行写 stderr E47 并 exit(7)，探针等待真实 PID 消失后仍返回合法860×600；另一条在末次 inspect 中把同 ID 42 改属测试父进程。两条均要求 reject、observation.ok=false、finalGeometry.actual仍为860×600、没有observedMs、末图存在、cleanup.liveRemaining为空且parentClosed=true；退出分支另核对exit code与stderr诊断。退出等待有3000ms上限，未使用精确墙钟等值断言；fixture超时失败包含实际PID/状态、时间与要求截止时间。

沿用本机已有 Node `/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node`，实际版本 `v24.18.1`。以下命令均在本worktree运行，日志完整保存在忽略的 `.superpowers/sdd/`：

```sh
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --test --test-name-pattern='final geometry.*cannot pass' desktop/tests/linux-appimage.test.mjs > .superpowers/sdd/p1-linux-final-geometry-red.log 2>&1
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --test --test-name-pattern='final geometry.*cannot pass' desktop/tests/linux-appimage.test.mjs > .superpowers/sdd/p1-linux-final-geometry-green.log 2>&1
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --test desktop/tests/linux-appimage.test.mjs > .superpowers/sdd/p1-linux-final-geometry-full.log 2>&1
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --test desktop/tests/linux-appimage.test.mjs > .superpowers/sdd/p1-linux-final-geometry-full-final.log 2>&1
```

RED在只写新测试、未改生产脚本时执行，exit 1，2 tests / 0 pass / 2 fail；两条均为 `Missing expected rejection`，证明旧实现错误成功。增加一行复核后定点GREEN exit 0，2 tests / 2 pass / 0 fail；完整文件首次exit 0，34 tests / 34 pass / 0 fail，14861.886542ms。之后仅完善fixture等待失败诊断，最终完整文件结果见下方验证记录。

范围自审：source只改允许的两个文件；生产只新增一行调用；原SHA/source/sidecar门禁、20秒找窗、10秒观察、5000ms resize timeout、finally cleanup均未变。采用systematic-debugging、test-driven-development、verification-before-completion与git-commit流程；fixture失败文案按fail-fast-with-evidence补足诊断。未引入依赖、WM、平台配置或放宽验证。未push、未启动native/1420/GUI、未操作CI。原生/标题栏/无遮挡/readiness/完整P1任务6边界仍保持，未以fixture代替原生证据。

最终验证：`p1-linux-final-geometry-full-final.log` exit 0，34 tests / 34 pass / 0 fail / 0 skipped / 0 cancelled，14434.161625ms。以下三条在最终源文件状态分别执行，各自 exit 0、无输出：

```sh
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --check desktop/scripts/smoke-linux-appimage.mjs
/Users/dayong/.npm/_npx/387698761821791d/node_modules/node/bin/node --check desktop/tests/linux-appimage.test.mjs
git diff --check
```

未发现本次范围内未解决正确性问题；原生环境仍未执行。

I1修补提交：`9ca837d` — `fix(desktop): recheck Linux window ownership after final geometry`。仅精确stage并提交两个源文件；staged diff check exit 0。提交后git status --short无输出，未push。
