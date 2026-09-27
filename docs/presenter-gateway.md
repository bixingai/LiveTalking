# presenter-gateway

`C:\Coding\BixingAI\presenter-gateway` 是 Teachora、Helpora、Shopora 共用的内部适配层。它没有产品界面。协议已经由适配层实现。本仓库仍只做引擎，缺的三项引擎能力写在 [BUILD_PLAN.md](BUILD_PLAN.md)。本仓库自己的记忆在 [MEMORY.md](../MEMORY.md)，不要写进全局记忆。

本仓库只做数字人引擎：口型、语音、推流和录制。产品协议、同时只允许一路说话、培训课堂、客服转人工和直播带货脚本都不要加进 `app.py` 或 `server/routes.py`。

三个应用是适配层的客户端：

| 应用 | 仓库 | 自己保留的业务 |
| --- | --- | --- |
| Teachora | `C:\Coding\BixingAI\Teachora` | 企业培训、讲稿、举手答疑 |
| Helpora | `C:\Coding\BixingAI\Helpora` | 客服收件箱、知识、转人工 |
| Shopora | `C:\Coding\BixingAI\Shopora` | 直播带货、商品口播稿 |

当前本地 MVP 仍可能由浏览器直接访问端口 `5555`。那是临时路径。适配层开始提供协议之后，应用只连接适配层，引擎端口留在私有网络。
