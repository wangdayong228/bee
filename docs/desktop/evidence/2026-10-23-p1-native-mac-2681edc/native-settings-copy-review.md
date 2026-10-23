# P1 英文设置文案原生窄复验

日期：2026-10-23。来源提交：`2681edca2c56bca9d2ce30db4198fb5784d98b65`（由主控指定的最终 source）。本次只检查原 M1 英文设置回执和代理输入占位文案，不重审已 Approved 的两项英文映射与六项专项，不重新验收其他页面。

## 结论

**本次范围 Approved：原 M1 的英文回执连写/残句已闭合，代理 placeholder 已闭合。新增 C/I/M 均为 0。** 结论来自两张原生原图的实际目视检查，并由同名 AX 文本交叉确认，不是仅根据源码或专项测试推断。

| 检查项 | 原生目视证据 | AX 交叉证据 | 结果 |
| --- | --- | --- | --- |
| 英文设置回执 | `native-settings-en-860-bottom.jpg` 底部金色提示完整显示 `Demo only: Settings saved. Switching Hive requires a new login and device binding. System proxy, startup and system notification permissions were not changed.`，两行正常换行，无 `binding.System` 连写、句尾裁切或原残句。 | 同名 AX 节点 45 文本一致；滚动值 1 与截图实际底部相符。 | 原 M1 闭合。 |
| 代理占位文案 | `native-settings-en-860-proxy.jpg` 的 Proxy address 输入框完整显示 `Off (leave blank)`；字符、空格和括号可读，Save proxy 操作也完整可见。 | 同名 AX 节点 34 明确记录 `Placeholder: Off (leave blank)`；滚动值约 0.329 对应代理区域。 | 占位文案闭合。 |

## 证据与边界

两张 JPG 均位于 `.cache/qa/p1-native-local-2681edc/`，本次逐张使用 `view_image(detail="original")` 实际查看，并读取同名 `.ax.txt`。原生逻辑窗口为 **860×600**，Retina 截图为 **1720×1200**；没有将截图像素尺寸当成逻辑窗口尺寸。

此次为英文、深色、两个已采样滚动位置的原生复验，不声称覆盖全部语言、主题、系统缩放或其他页面，也不推断真实资金、退出、更新和导出行为。未启动 GUI，未运行测试或 build，未修改 src、Git index 或 HEAD；只新增本报告。历史 b94 报告保留原发现与当时证据，不回写为历史通过。
