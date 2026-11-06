# 滚动转场 / 11 种分区边缘变化

- 作者：@codrops
- 分类：网页实验
- 状态：ai_recreated
- 原文：https://x.com/codrops/status/2116144602465931717
- 素材 ID：2116144602465931717
- 版本：1.1.0

## 复刻说明

单文件、自包含的滚动转场演示。顶部 `01`–`11` 控件对应 Codrops SeamTransitions 展示的 11 种边缘处理：ink bleeding、tiles crumbling、blanket fraying、photograph in type、contour map、marbling、mist、kintsugi cracks、roots、sediment 和 wood shavings。选择样式后向下滚动，固定的首屏会按滚动进度揭开下一章节；不是自动播放。适配桌面、窄屏和手机横屏。

改脚本顶部的 `BRAND` 可更换标题、章节文案和条目。实现使用 Canvas 与原生滚动，不引用外部资源；系统开启「减少动态效果」时，揭示在滚动中点切换为静态完成态。素材构想与原始演示的排列对应；示例森林为程序绘制，11 种边缘纹理是对原演示技法的自包含重绘，不载入 Codrops 源码或图像资产。
