# 扭曲波换卡

- 作者：Jakub Antalik (@Jakubantalik)
- 分类：品牌 · 网页交互
- 状态：video_recreated
- 原文：https://x.com/kombaiselects/status/2123400913314361760
- 素材 ID：2123400913314361760
- 版本：1.0.1

自包含单文件，无外链。对照的是约 13 秒、1600×1080 的预览，以及作者页上能看到的说明（https://libraries.dev/waves ，https://x.com/Jakubantalik/status/2120204589131870610）。npm 上有 MIT 包 `distortion-waves`。这里没有安装、复制或内嵌该包，页面也不声明拥有该许可。

黑底上四块界面，打开就能点，不会自己播完：

- 左上转账卡。底部 Confirm 发出向上拱的彩虹波，明细先朝按钮收一下，再被波扫过，出现边缘色差。白按钮和头像盖在波上面，保持清晰。扫完是绿勾、Sent 和 Done。
- 右上 Add credits。中间的 Buy $20 tokens 同样向上发一条偏绿的波，按钮先变成 Processing…，结束是 Credits added 和 Done。
- 左下 Sending USDC 条。点蓝色 $ 头像，波从圆心扩开，主要扫过文字；圆本身保持清晰，随后变成勾，并出现 View。
- 右下 Investor update。点卡片，从中部发出较淡的波，标题和正文换成下一条。

人名、备注、地址和投资者正文是自拟的，头像是字母圆标，不用原片照片。再点一次会用同样的波换回去。系统开启减少动态效果时不播波，立刻换状态。
