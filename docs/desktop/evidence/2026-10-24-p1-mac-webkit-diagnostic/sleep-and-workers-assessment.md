# P1 Task6 Mac WebKit workers 定点调查

结论（原 workers 对照，追加电源证据见文末）：远端 Intel 根因仍为 unknown；本机两轮已证实与系统 Sleep/DarkWake 窗口直接重叠，不能作为有效的纯 workers 因果对照。降低到单 worker 没有消除异常长停顿；不能认定是并行资源竞争，也不能把本机结果当作远端 Intel 修复证据。本次没有修改产品、测试、配置、索引、HEAD、分支，没有 push、CI、native App 或用户浏览器操作。

## 范围与绑定

本机 macOS 15.7.7 arm64；HEAD `9ca837d902fbf026be9931f796a3d1289e33dad3`。使用已有 Node v24.22.1、npm 11.19.1、Playwright 1.63.0。accounts.spec.ts SHA256 `5de4fd365c6eee0be98782dbf9b7d4f4b7a91ad9f68ea3f04bfd2ed01d2c4d6f`，Playwright 配置 SHA256 `4df9a9c50b9bf16c0afc38da3e0fae3e6195130e3a06097ac51dceb03a0d20b7`，两者均逐字节等于 87b28a2（证据 `source-binding.json`）。测试仍为默认 30000ms，retries=0，断言、scene 未变，清除 FORCE_COLOR 和 NO_COLOR。

## 既有证据与可验证假设

远端 87 Mac15 Intel 为 485pass/4fail，四个 WebKit accounts 场景在不同 click 阶段耗尽共享测试预算，native 后续 skipped；其原因原报告明确 unknown。

本机既有相同 grep 实际匹配 **5例/5workers**，并非远端四例：多了 accounts.spec.ts:149 的“移除收尾守门 removal-pending”。结果 1pass/4fail，2.8m。本次对照保持这五例，不能把本地失败集合等同远端。

读取四份本机 trace 的 test.trace 与 error-context 后，发现不同动作在同一段运行时序出现很长跨度；以下时间为各 trace 单调时间戳，不能当作精确 timeout 计费起点：

| 本机原失败例 | 长步骤 | start→end（ms） | 跨度（ms） |
| --- | --- | --- | --- |
| 双入口 | 详情“更新时间”断言 | 16948.527→166833.995 | 149885.468 |
| 换号 | 点击“确认换号” | 16851.543→166879.922 | 150028.379 |
| removal-pending 卡片 | After Hooks | 16931.504→166839.344 | 149907.840 |
| 移除收尾守门 | Evaluate | 16269.183→166838.740 | 150569.557 |

其中 teardown 失败并非产品断言失败；换号 error-context 显示演示确认处理中。双入口最终报错是“概览”click，但该动作在 timeout error 和 After Hooks 开始后才记录；不能把最终堆栈行直接等同最初停顿点。trace 允许事件在超时后继续到达，不能据此自行推断 Playwright/操作系统具体机制。完整抽取见 `baseline-timing.json`。

可检验假设：若这段长停顿依赖五个并行 worker，则保持入口和预算不变而降为一个 worker 应消除长停顿。测试只检验本机这一预测，不预设原因。

## 实际单变量对照

从工作树根执行；PATH 前置 `$PWD/.cache/toolchains/node-v24.22.1-darwin-arm64/bin`，移除 FORCE_COLOR/NO_COLOR，CI 未设置。命令：

```sh
npm --prefix desktop run test:e2e -- tests/accounts.spec.ts --project=webkit --grep '双入口|官方授权未接通|换号明确|removal-pending' --reporter=line --output /Users/dayong/myspace/mywork/tokenhive/.worktrees/bee-desktop-p0/.cache/qa/p1-mac-webkit-workers-diagnostic/workers-1/results --workers=1
```

启动日志明确 `Running 5 tests using 1 worker`。exit=1，**4 passed / 1 failed (15.6m)**；进程记录墙钟跨度 934.281449 秒。仅执行此一轮，没有加 timeout、retry、sleep 或全量测试。

| 用例 | 实际结果 | 每例耗时证据 |
| --- | --- | --- |
| 双入口 | pass | line reporter 未输出，通过 trace 被 retain-on-failure 删除；精确耗时未保留 |
| 官方授权未接通 | fail | Before Hooks 215.071ms；Navigate 227.876ms；导航 click 926223.884ms；After Hooks 221.422ms |
| 换号明确 | pass | 精确耗时未保留，同上 |
| removal-pending 卡片 | pass | 精确耗时未保留，同上 |
| 移除收尾守门 removal-pending | pass | 精确耗时未保留，同上 |

官方授权失败 trace：Before Hooks 3091.550→3306.621ms，Navigate 3307.199→3535.075ms，导航 click 3536.550→929760.434ms，After Hooks 929547.136→929768.558ms。最终报 `Test timeout of 30000ms exceeded`，locator 已解析但停在 visible/enabled/stable 等待日志。926秒是记录到的步骤跨度，不代表批准/配置了926秒 timeout，也不能据此重建精确 charged budget。

原定命令的 line reporter 与 retain-on-failure 无法事后提供四个通过例的精确持续时间，这是本轮取证缺口；没有为补齐数字重复测试或虚构耗时。实际命令、版本、平台、exit、start/end 在 `workers-1/command.json`、`workers-1/result.json`，完整输出在 `workers-1/test.log`，失败 trace 原始事件另存 `workers-1/trace-events.json`。

## 判定与限制

单 worker 仍有长停顿，故“五 worker 并行是出现此异常的必要条件”这一预测未成立。两轮失败集合也不同：原本通过的官方授权在单 worker 下失败；原四个失败在单 worker 下通过。通过数量改善不能单独证明因果或稳定性。

尚未证明长跨度来自 CPU、内存、WebKit、Playwright、系统调度、机器休眠或产品事件循环；本轮没有对应系统监测证据，不选择其中任何一个作为结论。无法证明本机 arm64 与 Intel hosted 同根因。

未追加 workers=2：单 worker 已不能排除长停顿，一次本机两 worker 成败都不能实质判定 Intel CI 两 worker 风险；继续测试会增加一次不可外推的样本。本次不实施任何配置方案。若后续单独批准最小验证选择，应在目标 Intel runner 上保留既有 timeout/retries/测试断言，明确 workers 数并在同次运行增加能够保留每例持续时间的结果采集；该选择仍只覆盖测试执行稳定性，不替代 native/package 验证。

结束后 `lsof -nP -iTCP:1420 -sTCP:LISTEN` 无输出，1420 已回收；没有重启任何既有 App。


## 追加：两轮长跨度与本机 Sleep/DarkWake 的绝对时间核对

按 root 追加授权，仅作只读 `pmset -g log` 调查；未再启动浏览器/测试，未改电源或系统设置。以每份 `test.trace` 首个 context-options 的 `wallTime`、`monotonicTime` 为基准，计算 `UTC epoch ms = wallTime + event monotonic ms − context monotonicTime`。保存 `sleep-wake-windows.json`，包含基准换算后的UTC、Asia/Shanghai与epoch边界。这里只在两个异常时间窗前后各60秒内筛选 Sleep/Wake/SleepService 相关短行，未保存完整系统日志或读取账户配置；`pmset` exit=0，保留原始相关行于 `pmset-window-lines.log`。

| 轮次/步骤 | UTC窗口 | Asia/Shanghai窗口 |
| --- | --- | --- |
| 5worker 守门 Evaluate | 2026-10-23 10:57:43.602–11:00:14.171 | 2026-10-23 18:57:43.602–19:00:14.171 |
| 5worker 换号 click | 2026-10-23 10:57:44.184–11:00:14.212 | 2026-10-23 18:57:44.184–19:00:14.212 |
| 5worker removal After Hooks | 2026-10-23 10:57:44.264–11:00:14.172 | 2026-10-23 18:57:44.264–19:00:14.172 |
| 5worker 双入口断言 | 2026-10-23 10:57:44.281–11:00:14.167 | 2026-10-23 18:57:44.281–19:00:14.167 |
| 1worker 官方授权 click | 2026-10-24 01:27:09.274–01:42:35.498 | 2026-10-24 09:27:09.274–09:42:35.498 |

直接重叠的原始行（日志时间精度为秒，+0800）：

```text
2026-10-23 18:57:42 +0800 Sleep               	Entering Sleep state due to 'Idle Sleep':TCPKeepAlive=active Using Batt (Charge:100%) 151 secs
2026-10-23 19:00:13 +0800 DarkWake            	DarkWake from Deep Idle [CDNP] : due to smc.70070000 wifibt SMC.OutboxNotEmpty/ Using BATT (Charge:100%) 9 secs
2026-10-24 09:27:06 +0800 Sleep               	Entering Sleep state due to 'Clamshell Sleep':TCPKeepAlive=active Using Batt (Charge:100%) 929 secs
2026-10-24 09:42:35 +0800 DarkWake            	DarkWake from Deep Idle [CDNP] : due to smc.70070000 wifibt SMC.OutboxNotEmpty/ Using BATT (Charge:100%) 14 secs
```

原5worker四个长步骤均在18:57:42进入睡眠后约1.6–2.3秒开始记录，在19:00:13 DarkWake后约1.2秒结束；系统记录睡眠151秒，与约150秒长跨度直接重叠。单worker click在09:27:06进入Clamshell Sleep后约3.274秒开始记录，在09:42:35 DarkWake同秒结束；系统记录睡眠929秒，与926.224秒步骤跨度直接重叠。

因此，证据**支持本机睡眠/唤醒与两轮异常长跨度直接关联**，提供了此前缺失的系统层证据。本机 workers 对照受电源状态混杂，不能据4pass/1fail认定并行改善或认定单worker本身不稳定。换算与秒级日志不能证明每个毫秒的执行状态，也没有证明具体Playwright timeout取消机制或全部产品行为因果；远端Intel是否有同样电源事件仍未知，不能套用本机结论。此前“尚未证明机器休眠”的表述仅代表追加调查前状态，由本节证据更新。
