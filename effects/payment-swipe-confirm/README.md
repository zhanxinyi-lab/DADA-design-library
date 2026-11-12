# 支付确认滑动 / Payment swipe confirm

- 作者：stacked (@stackedlol)
- 分类：品牌 · 网页交互
- 状态：ai_recreated
- 原文：https://x.com/stackedlol/status/2118411290079011323
- 素材 ID：2118411290079011323
- 版本：1.0.0

## 复刻说明

自包含单文件，无外链。对照原帖约 7.3 秒、1780×2160 的视频，以及站点已发布的 `poster0.jpg` 和 `preview.mp4`（`/s/rjqagsc0hcqp/`，时长与原片一致）。站点 `preview.webm` 这次打开是 404，没有拿来当依据。

能核对到的画面：

- 浅色底上的白卡片。左上角秒表从 `0.00s` 起。
- 标题先是 `Review payment`。五行是 `You pay` / `You receive` / `Network` / `Fee` / `Status`。
- 金额读作 `0.8214 ETH`、`2,480.00 USDC`，网络 `Solana`，费用 `$0.12`，状态 `Awaiting approval`。ETH 小数点在画面里很淡，取这个读法是因为小数点落在首位和 `8214` 之间，并且和约 2,480 USDC 的兑换关系相符。
- 底部是 `Swipe to pay`。蓝色滑块从左侧出发，大约 1.7–2.4 秒把整条轨道涂成蓝色。
- 接着标题变成 `Confirming payment`，状态变成 `Pending`，按钮位置换成较小的 `Confirming...`。秒表从此开始走，卡片上半部有一小块循环运动。
- 大约 5.7 秒进入完成态：标题 `Payment confirmed`，秒表停在 `3.20s`，状态是带绿色底的 `Settled` 加上同一时间，底部是黑色 `View position`。

币种图标只用圆标里的字符，不描摹 ETH、USDC 或 Solana 的商标。上半部的转圈和完成勾是这块区域确实在动的简化，不是逐帧描图。`View position` 在原片里没有再打开新页面，这里也不另做一屏。

系统开启减少动态效果时停在当前一步，用「下一步」切换，不做自动滑动。
