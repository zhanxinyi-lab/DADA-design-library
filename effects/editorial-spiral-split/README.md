# 左右分屏与螺旋文字隧道

- 作者：Edo (@edo_lunardi)
- 分类：品牌 · 网页交互
- 状态：ai_recreated
- 原文：https://x.com/edo_lunardi/status/2117757773018792447
- 素材 ID：2117757773018792447
- 版本：1.0.1

## 复刻说明

自包含单文件，无外链。对照原帖 2.5 秒视频、站点 `poster0.jpg` / `img1.jpg` / `preview.mp4`，以及 [contentarchitecture.dev](https://www.contentarchitecture.dev/) 首屏滚动能直接看到的三段：

1. 左暖纸、右黑底的分屏。左侧是可换的衬线叠字，右侧是同一句话绕成的螺旋。
2. 继续滚动后，螺旋铺满画面，文字旋向中心亮孔。
3. 再落到反向分屏：左侧无衬线大写叠字，右侧一句话。

原站商品文案、导航和字标没有搬过来。画面上的句子写在 `code/index.html` 的 `#mark` 和 `#statement` 里，改那里即可换字；螺旋会跟着 `#mark` 重画。底部四个词滚的是上面这三段，不是四章：Index 回到开场分屏，Notes 进入螺旋，Atlas 和 Signal 都落在反向分屏里，Atlas 更早，Signal 到这段的末尾。

系统开启减少动态效果时，螺旋不再自行旋转，滚动仍可切换三段，并停在当前段的静止画面。
