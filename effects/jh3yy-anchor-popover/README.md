# 锚点变形 Popover 菜单

- 作者：jhey ʕ•ᴥ•ʔ (@jh3yy)
- 分类：品牌 · 网页交互
- 状态：ai_recreated
- 原文：https://x.com/jh3yy/status/2118488118257172710
- 素材 ID：2118488118257172710
- 版本：1.0.0

## 复刻说明

自包含单文件。深色页、顶栏锚点、圆角菜单。菜单盒子尺寸不变；里面的内容用 `scale` 从当前锚点 fallback 对应的角长出来。

原帖写明的机制：

`@container anchored(fallback: --top-left)`

弹出层保持全尺寸，内容从该 fallback 设定的网格原点生长。关联说明：https://x.com/jh3yy/status/2116202164896874710 （Chrome 里用 CSS 判断弹出层落在哪一侧）。

依据是原帖文字、25 秒原视频（540 画面）和已发布的 `preview.mp4` / `poster0.jpg`。画面里能确认：近黑底、顶栏左右有亮点、一张横向圆角卡片（左文右图），卡片会在中间或靠右出现，展开过程中内容先小于整张卡片。

看不清因此没有照搬的部分：品牌名、导航原文、产品图。菜单用「外观 / 结构 / 位置」和色块代替，页眉用 01–04。卡片角落的小字是当前生效的 fallback 名，用来看见锚点查询的结果，不是原片字幕。

基础定位故意溢出，让命名的 `@position-try`（`--top-left` / `--top-right` / `--bottom-left` / `--bottom-right`）始终成为生效项，这样 `@container anchored(fallback: …)` 才能匹配。不支持 `container-type: anchored` 时，脚本按按钮在视口里的位置选择同一套原点。
