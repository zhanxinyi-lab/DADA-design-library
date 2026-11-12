# 甩动卡片

- 作者：Vansh (@vansh1029)
- 分类：品牌 · 网页交互
- 状态：ai_recreated
- 原文：https://x.com/vansh1029/status/2116523080931475887
- 素材 ID：2116523080931475887
- 版本：1.1.0

按住浅色圆角卡片再甩出去。甩得越快，卡片沿甩出的方向拱得越厉害；慢下来以后恢复平直。页面是单文件 WebGL，不引用外网。

## 对照了什么

原帖原文是 “fling it. the cards bend based on how fast you throw them. live WebGL, every vertex.” 帖里只有这段话和一条视频，没有源码、仓库或代码链接。作者主页 [vanshnagar.com](https://www.vanshnagar.com/) 也不是这个演示。

已发布站点上的预览和原片是同一条视频的低清版本：

- 站点：https://x-material-library.workers.xd-sites.com/s/rjqagsc0hcqp/assets/2116523080931475887/preview.mp4 （720×406，8 秒，与本地发布稿 SHA-256 一致）
- 海报：同目录 `poster0.jpg`
- 原片：1280×720、60fps、约 10.8 秒。近黑底、浅色圆角卡片、深色字。能读到的句子就是 “fling it.” 和 “the cards bend based on how fast you throw them.” 静止时卡片是平的；光标拖着甩出时，卡片沿运动方向拱起，并带有运动模糊，停下后回到平直。

低清预览看不清拱起有多大。弯曲方向和「越快越弯」来自原片。卡片之间不相撞，也不会弹回原来的位置；飞出画面时只从边缘挡回来。

## 许可

原帖、作者介绍和已发布条目都没有许可证。这里没有复制作者的页面或着色器，只按公开视频里能核对到的抛掷和弯曲做了独立实现。

## 用在哪些项目

| 项目 | 用的版本 | 什么时候 | 负责人 | 备注 |
|---|---|---|---|---|
| — | — | — | — | 还没有项目用过 |
