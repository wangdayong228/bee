# P1 Task6 本机 WebKit 防 Idle Sleep 单轮复测

结果：本机 macOS 15.7.7 arm64 的这一轮 **5例/5workers 全部通过**，exit0，Playwright 总耗时3.7秒；同次短时电源日志未发现 Sleep/DarkWake/Wake 事件。仅证明本机该样本通过，远端 Intel 根因仍为 unknown。

## 绑定与执行

HEAD `9ca837d902fbf026be9931f796a3d1289e33dad3`。测试 SHA256 `5de4fd365c6eee0be98782dbf9b7d4f4b7a91ad9f68ea3f04bfd2ed01d2c4d6f`，配置 SHA256 `4df9a9c50b9bf16c0afc38da3e0fae3e6195130e3a06097ac51dceb03a0d20b7`，与先前调查相同。使用既有 Node24.22.1、npm11.19.1、Playwright1.63.0，移除 FORCE_COLOR/NO_COLOR；没有修改源码、配置、断言、scene、pmset/TCC/系统偏好，没有CI或native/CUA操作。

开始前1420无监听。PATH前置工作树已有Node24工具目录；`PLAYWRIGHT_JSON_OUTPUT_FILE` 指向本轮独立目录。唯一测试命令：

```sh
/usr/bin/caffeinate -i npm --prefix desktop run test:e2e -- tests/accounts.spec.ts --project=webkit --grep '双入口|官方授权未接通|换号明确|removal-pending' --reporter=line,json --output /Users/dayong/myspace/mywork/tokenhive/.worktrees/bee-desktop-p0/.cache/qa/p1-mac-webkit-awake-diagnostic/results --workers=5
```

JSON报告核实 workers=5、timeout=30000ms、retries=0；五例 retry 均为0。grep仍包含远端四个失败场景及额外“移除收尾守门 removal-pending”，不将五例说成远端四例。

进程时间 UTC 2026-10-24 02:23:16.753–02:23:20.794（上海10:23:16.753–10:23:20.794），墙钟4.041秒。JSON测试起点02:23:17.116Z，duration3664.918ms，expected5/unexpected0/skipped0/flaky0。

| 用例 | workerIndex | 结果 | duration ms |
| --- | --- | --- | --- |
| 双入口、检测登录和详情 | 0 | passed | 2388 |
| 官方授权未接通 | 1 | passed | 2230 |
| 换号明确 | 2 | passed | 2267 |
| removal-pending 卡片 | 3 | passed | 2298 |
| 移除收尾守门 removal-pending | 4 | passed | 2570 |

## 电源证据与限制

`caffeinate -i` 只包裹该测试进程，未请求修改持久系统设置；它阻止 Idle Sleep，但不能保证阻止合盖睡眠。本次测试前/中/后均保存 `pmset -g assertions`：已有 powerd/coreaudiod 的 PreventUserIdleSystemSleep，且 powerd有lidopen记录。中途快照在启动Popen后立即采集，没有捕获caffeinate自有assertion；相关分钟的pmset日志也未检索到caffeinate断言事件，因此不能把此快照当作caffeinate已建立断言的直接证据。实际命令被执行并exit0是包装进程证据。

`pmset -g log` 按进程start/end前后各60秒筛选Sleep/DarkWake/Wake/SleepService事件，`power-window.log` 无相关事件；因此此次运行期间无记录的睡眠事件。它与前两轮已证实睡眠直接重叠的失败样本不同，支持“之前本机结果受睡眠混杂”的判定；不能据单次通过证明caffeinate为唯一原因、产品绝对稳定或Intel CI已修复。

没有失败trace（配置retain-on-failure，全部通过）。本轮后停止，未追加其他worker/timeout/retry试跑。结束后1420无监听，自己启动的Vite已随测试回收；未重启既有App。

原始证据目录：`.cache/qa/p1-mac-webkit-awake-diagnostic/`，包括 command.json、result.json、test.log、playwright-report.json、assertions-before/during/after.log、power-window.log、caffeinate-assertion-events.log。前两轮睡眠重叠证据见 `p1-macos-webkit-parallelism-assessment-report.md`。
