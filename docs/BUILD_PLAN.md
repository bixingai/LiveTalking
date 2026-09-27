# LiveTalking 构建计划

适配层 `presenter-gateway` 已经按本仓库现有接口完成翻译。本仓库不实现网关协议，也不加入培训、客服或带货业务。

还缺三件引擎能力。没有它们，适配层只能绕开，不能真正释放显卡或判断一句话是否已经开始。

## 不做什么

- 不增加 `/sessions`、`/speech`、举手、知识库或调用凭证。
- 不把「同时只允许一路说话」放进本仓库。名额仍由适配层保持。
- 不改现有 `/is_speaking` 的布尔含义。旧调用方继续只看 `data` 里的 true 或 false。

## L1 按会话号关闭引擎会话

现在只有浏览器断开 WebRTC 时，`session_manager.remove_session` 才会运行。适配层的 DELETE 只能释放自己的名额，显卡上的会话还在。

增加一个只接受 `sessionid` 的关闭接口。它关闭对应的 PeerConnection，停止该会话的推理和录音，然后调用 `remove_session`。会话不存在时返回明确的未找到，不返回堆栈。

完成标准：打开一路 `/offer` 后调用关闭，该 `sessionid` 从会话表消失，随后可以再打开一路。关闭不接受讲稿、举手或业务字段。

## L2 区分「已收下文字」和「正在出声」

`is_speaking` 只在渲染循环拿到非静音帧时变成 true。文字已经交给 `/human` 之后、第一帧出来之前，它仍是 false。适配层因此无法知道这句话是还没开始，还是已经说完。

在现有响应里增加一个状态，取值只有 `idle`、`queued`、`speaking`。`/human` 接受文字后直到第一帧之前是 `queued`。正在渲染非静音帧时是 `speaking`。队列空并且不再渲染时回到 `idle`。原有的布尔值保持不变：只有 `speaking` 时为 true。

完成标准：发送一句文字后，状态先变为 `queued`，出声后变为 `speaking`，说完变为 `idle`。打断后不再停留在 `queued`。

## L3 录制文件可被取走

`POST /record` 的 `end_record` 返回成功时，`data/record/{sessionid}.mp4` 可能还没写完。`GET /record/{sessionid}` 这时是 404。

`end_record` 的响应增加 `ready`。文件可以下载时为 true。未完成时为 false，并且不把服务器路径放进响应。现有下载地址保持不变。

完成标准：停止录制后，`ready` 为 false 时下载接口仍是 404。`ready` 变为 true 后，下载接口返回该 mp4。

## 顺序

L1 先做。它直接补上适配层无法完成的资源释放。L2 其次，让适配层可以去掉现在的超时猜测。L3 最后。每一项用引擎自己的 HTTP 接口验证，不通过 Teachora 页面。
