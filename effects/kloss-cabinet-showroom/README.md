# 霓虹机柜展厅

- 作者：@kloss_xyz
- 分类：品牌 · 网页交互
- 状态：ai_recreated
- 原文：https://x.com/kloss_xyz/status/2118145838568661278
- 素材 ID：2118145838568661278
- 版本：1.0.0

## 复刻说明

自包含单文件，无外链。对照站点海报和 8 秒 preview：竖版发售页、顶部两行大字、深色反光地面上的机柜、Arcade / Claw / Vending 三种外形可切换、镜头自动环绕，底部按钮点选，拖动改角度。

原帖没有公开源码。站点没有完整长视频（台账里的 `video.mp4` 未发布），所以范围停在这份预览能核对的展厅骨架。机柜用原创几何体，不使用原品牌字标、海报插画或产品贴图。

改脚本顶部 `const BRAND`：`kicker` / `line1` / `line2` 换文案，`accent` / `cyan` / `violet` 换霓虹色。`?mode=arcade|claw|vending` 指定机型，`?freeze=1` 停住自动切换和环绕。
