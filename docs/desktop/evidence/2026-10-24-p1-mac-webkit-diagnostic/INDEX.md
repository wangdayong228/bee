# Mac WebKit 调查证据导航

本目录保留原报告的字节及其当时的缓存路径。归档后的直接入口如下：

- [无 Sleep 单轮5/5复测报告](README.md)：同5例/5workers、30秒、retries0，3.7秒通过；只代表本机arm64该样本，Intel根因仍未知。
- [两轮长停顿与系统睡眠的核对](sleep-and-workers-assessment.md)：原5worker与单worker失败、trace时间线及追加电源证据。
- [本轮Playwright JSON](awake-5workers/playwright-report.json)与[完整测试日志](awake-5workers/test.log)：每例duration、worker、timeout和结果。
- [系统相关电源日志](workers-assessment/pmset-window-lines.log)与[绝对时间窗](workers-assessment/sleep-wake-windows.json)：直接重叠记录；不是Intel系统日志。

`baseline-5workers/`、`workers-assessment/workers-1/` 保留原失败的日志、error-context与trace成员；`awake-5workers/` 保存唯一无Sleep记录的复测及断言快照。原报告中提到的 `p1-macos-webkit-parallelism-assessment-report.md` 在本归档对应 `sleep-and-workers-assessment.md`。文件来源、字节数和SHA256见 `manifest.json`；原报告副本没有为补导航而重写。
