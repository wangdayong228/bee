# Mac 已显示窗口后的生命周期补验

日期：2026-10-24。实际环境macOS15.7.7 arm64。源码包绑定`87b28a29aa84c2543b6b80b7e31204646e4fa76a`，仓库记录时HEAD为`5ada0898eda96e212895e559c93b52e57f60e2e7`。本轮只增加验收证据，不修改产品或放宽通过标准。

用户打开窗口后，CUA已能取得真实窗口并执行原生菜单。**native ready、真实菜单退出回收原父子、Finder重启后再次ready已取得证据；关窗隐藏的可见转换与托盘仍未通过。** 不能把早前取不到窗口继续写成当前状态，也不能把进程存活或菜单打开当作隐藏/托盘验收通过。

| 检查 | 实际证据与结论 |
| --- | --- |
| 来源 | [22绑定与最终进程](22-binding-final-processes.json)严格核对现App和bundled Bee字节/哈希，与[既有87包清单](../2026-10-23-p1-native-mac-87b28a2/packages.json)一致；[21签名检查](21-signature.json)exit0。开发ad-hoc包，非生产签名/公证。 |
| 真实状态 | [03连接详情](03-native-ready-ax.txt)为native ready，明确未启动真实贡献；[03原图](03-native-ready.jpg)。 |
| 关闭尝试 | 04/05/06及18/19执行关闭后仍返回窗口内容；[06进程](06-after-close-processes.json)证明同父96946/owned子96975存活，未证明窗口已隐藏。[18原图](18-focused-close.jpg)仍有详情内容。不能据此确定工具或产品根因。 |
| 菜单打开 | [07原生菜单](07-native-menu-ax.txt)与[08概览](08-menu-open-ax.txt)、[同PID](08-menu-open-processes.json)；只证明菜单可操作，不算托盘或完整隐藏找回。 |
| 真实退出 | [09菜单](09-before-quit-menu-ax.txt)点击退出后，[10精确ps](10-after-quit-processes.json)为exit1/空输出，原96946/96975均不存在；[11最终清单](11-after-quit-final-inventory.json)为未运行。紧接退出的[10清单](10-after-quit-inventory.json)仍running的早期快照原样保留，不当最终状态。无signal或按名字终止。 |
| Finder重启 | [12精确App URL](12-finder-app-path-ax.txt)选中文件Cmd+O；[13新进程](13-relaunch-processes.json)5669/owned5787。14/15/16点击详情没有展开，文件名含ready不代表结果通过；原生菜单打开后[17详情](17-focused-relaunch-ready-ax.txt)与[原图](17-focused-relaunch-ready.jpg)才确实为ready。 |
| 结束状态 | [20概览](20-final-overview-ax.txt)及[原图](20-final-overview.jpg)，22再次核对5669/5787存在。保留此演示实例供查看，不声称全部测试进程均已清空。 |
| 托盘 | CUA选择Dock返回`-10005: timeoutReached`，未取得托盘项；[操作记录](events.md)保留具体返回。未验收无托盘场景。 |

完整动作、无效点击、截图限制和最初source路径探测失败见[操作记录](events.md)。原始AX/JPEG/JSON逐字节复制自本轮`.cache/qa/2026-10-24-mac-visible-lifecycle`；[manifest](manifest.json)记录每份原始文件的大小、SHA256及本机来源。README和manifest本身不计入条目。

本轮未执行外部Bee保留夹具，不重复声称已有87记录中的该项为新证据；未测Mac13/其它架构、干净用户/Applications安装、原生缩放、Downloads拒绝/取消或正式更新。P0/P1整体及任务6剩余checkbox保持未完成。
