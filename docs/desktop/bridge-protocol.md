# Bee 桌面私有管理协议（P0）

`bee desktop` 是桌面壳与本次创建的 Bee 子进程之间的机器入口，不能附加参数。它不读取账号或设备配置、不连接 Hive、不启动贡献、不开放监听端口。其他 CLI 命令仍走原入口。此协议可用不代表 Bee 已具备接单条件。

## 帧与关联

- stdin 接收请求，stdout 只输出响应；诊断写入 stderr，父进程须持续消费两个输出管道。
- 每个输入和输出帧是一个 UTF-8 JSON 对象，以 `\n` 结束；换行前最多 1,048,576 字节。分段读取和多个帧合并写入均支持。编码后的输出同样检查上限，防止 JSON 字符串转义扩大响应。
- 请求字段必须恰好为 `protocol`（整数 1）、`id`（非空字符串）、`method`（字符串）和 `params`（空对象）。未知字段、重复 JSON 字段、非空 params、缺失字段和不合法的 JSON 类型均拒绝。
- 每次 `Run` 创建新的随机 128 位 `instance`；一次会话内保持一致。父进程用 `id` 关联请求，用 `instance` 区分重新启动的管理实例。
- 相同 ID 的前一响应尚未完整写入时，返回 `DUPLICATE_ID`，不执行重复操作。父进程应为每次请求生成新 ID。
- ID 及版本号属于公开元数据，不能放入凭证。协议错误不回显完整请求、未知字段名、未知方法值或 JSON 解析器引用的载荷字节；JSON 语法错误报告字节位置和帧长度。
- 输入超过上限或在 EOF 时缺少终止换行，会尽力发送错误帧后结束本次会话。完整但不合法的请求返回错误后可继续接收下一帧。空输入直接正常结束。

## 握手与允许的操作

先发送：

```json
{"protocol":1,"id":"hello-1","method":"hello","params":{}}
```

响应示例（版本和实例以实际运行值为准）：

```json
{"protocol":1,"id":"hello-1","instance":"0d957c72d63b4c06ae544c10f4c549799","result":{"bee_version":"dev+revision-dirty","os":"darwin","arch":"arm64","capabilities":["ping","shutdown"]}}
```

版本不匹配返回 `VERSION_MISMATCH`，不进入 ready；未成功握手的 `ping` 和 `shutdown` 返回 `NOT_READY`。握手成功后再发 `hello` 返回 `ALREADY_READY`，不会替换实例。只有以下两个后续方法：

| 请求 method | result | 含义 |
| --- | --- | --- |
| `ping` | `{"alive":true}` | 管理进程仍响应，不表示已连接 Hive 或开始贡献 |
| `shutdown` | `{"stopped":true}` | 停止接受后续输入，写完已接收的响应后退出；父进程仍须等待并回收本次子进程 |

不存在 `start`、授权、资金或任意 Shell 操作。成功响应含 `result`，失败响应以 `error` 取代 `result`：

```json
{"protocol":1,"id":"ping-1","instance":"0d957c72d63b4c06ae544c10f4c549799","error":{"code":"NOT_READY","message":"hello handshake has not succeeded; required=hello before other methods"}}
```

请求含有唯一有效 ID 时，未知字段或重复非 ID 字段的错误仍关联原 ID。无法可靠解码请求信封、重复 ID 字段有歧义，或编码后的响应超过上限时，错误响应的 `id` 为空字符串。输出超长只发送小型 `FRAME_TOO_LARGE` 错误帧并终止会话；父进程应将这种响应作为协议错误处理，不能据此完成某个正常请求。

## 取消与资源所有权

`desktopbridge.Run(ctx, in, out, diagnostics, version)` 不关闭外部传入的流；返回前会等待自己创建的响应写入 goroutine 结束。输入 EOF 正常结束，context 取消保留 `context.Canceled` / `context.DeadlineExceeded`，底层读写错误保留错误链。响应队列有界，只允许一个输出写入者，避免响应交错和无界积压。

通用 `io.Reader` / `io.Writer` 没有中断方法。**调用方必须在取消时解除正在阻塞的 Read / Write**；单独取消 context 不能保证唤醒任意外部流。这里不通过遗留读取 goroutine 假装已经退出。

命令入口拥有其标准管道：Unix 将继承的管道复制为 close-on-exec、非阻塞描述符，并注册 Go runtime poller；取消时关闭自有输入和输出，唤醒空闲读取和堵塞写入。普通文件不修改描述符标志。Windows 保留 Go 标准管道关闭行为，仍缺少原生测试证据。输出失败也会触发命令入口取消并回收本次资源。

关闭、EOF、信号和错误路径均不枚举系统进程，不查杀外部 Bee。此处仅管理 P0 的空闲协议进程；真实贡献运行及任务收尾属于后续阶段。

## 验证

从 Bee 实施检出运行：

```sh
go test ./desktopbridge ./cmd/bee -count=1
go test -race ./desktopbridge ./cmd/bee -count=1
go run ./cmd/bee version
go run ./cmd/bee help
```

协议测试覆盖分段/合并帧、帧长度边界、错误输入、重复未完成 ID、实例关联、版本不匹配、流所有权、取消和底层 I/O 错误。命令测试创建真实测试子进程，验证握手、拒绝贡献操作、shutdown、父输入 EOF、空闲输入/堵塞输出时的中断、CLI 帮助与版本一致，以及工作目录配置样本未改变。

当前证据仅来自 macOS arm64；独立协议包的交叉编译不替代 Windows/Linux 的行为测试。已打包的旧开发 App 尚未集成此协议，不能用本文件宣称 Rust 桥、托盘或三端产品已通过。
