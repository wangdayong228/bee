# 本轮操作记录（由工具返回整理）

- 用户明确表示“窗口已显示”后，CUA按精确App路径成功取得窗口；01为设置页，02为概览，03连接详情实际显示native ready/未启动真实贡献。
- 第一组关闭尝试：Escape后最新diff中的系统关闭按钮19；截图坐标[28,28]；再完整读取当前树并点击系统关闭按钮72。04/05/06均返回同一窗口树，04截图仍有内容。06进程检查在最后一次close之后、下一次Bee getter之前执行，原父96946/owned子96975仍在，路径/PPID/启动时间未变。仅此不能证明隐藏。
- CUA选择Finder成功；选择com.apple.dock返回“Computer Use server error -10005: timeoutReached”。没有使用未提供的launch_app、AppleScript、osascript、CGEvent或命令行open代替UI操作。
- 07原生App菜单提供“打开 Bee/退出”；菜单截图工具返回“Screenshot unavailable for .../Bee Dev.app.”，未生成07 PNG。08点击“打开 Bee”后返回概览和截图，进程仍为96946/96975。由于此前隐藏未证，08不算完整隐藏→找回通过，也不算托盘。
- 09/10点击原生菜单“退出”。紧接着的inventory仍报告running（10），后续ps精确PID查询退出1、stdout/stderr均空；11最终inventory为not running。未再调用旧Bee getter、未发signal。旧父和owned子退出已证。
- Finder“前往文件夹”输入已核App所在macos目录；12列出Bee Dev.app精确URL。选中该文件后Cmd+O启动，13新父5669/owned子5787，旧PID不复用。此后才绑定新App。
- 14/15点击连接详情仍只得到概览，不是ready证据；16按截图像素坐标[1830,1055]按下120ms，同样没有展开。Raise动作后也没有AX变化。此处未建立产品/工具/焦点的唯一根因。
- 新实例原生菜单“打开 Bee”后出现HTML focused；随后按最新树点击连接详情，17实际显示native ready。只记录此可复现顺序，不宣称已修复输入根因。
- 18在上述聚焦/详情状态点击系统关闭按钮19，AX仍返回详情、随后截图仍有内容。读取截图时一次跨realm instanceof判断为false；再用byteLength成功保存原始Uint8Array，18截图已保存。19尝试Retina截图两倍比例对应逻辑坐标[14,14]，仍返回详情树；比例只是本次输入假设，未证明其为根因。
- 末次经原生菜单“打开 Bee”后Escape关闭连接详情；20保留概览。22精确路径/PPID再次确认5669/5787仍在，供用户继续查看。未点击开始贡献、恢复平台、导出、真实资金或系统权限。

00初次baseline尝试了Contents/Resources/bee-source.json，该路径不存在，原记录保留。后续source.json来自实际desktop/src-tauri/binaries/bee-aarch64-apple-darwin.source.json，22与既有87 packages源信息及两份App二进制SHA/字节严格匹配；这不是在App资源中发现source文件。

归档自检发现CUA截图返回实际为JPEG，初次保存使用了.png文件名。归档将10张图改为.jpg扩展名，未重编码、未修改原始图片字节；manifest.source保留.cache初次文件名以便逐字节核对。
