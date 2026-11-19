# 动效六参数控制台

- 作者：frontman (@frontm_an)
- 分类：AI工具/工作流
- 状态：video_recreated
- 原文：https://x.com/frontm_an/status/2118971398173409489
- 素材 ID：2118971398173409489
- 版本：1.1.0

## 复刻说明

自包含单文件，无外链。对照原帖正文，以及原帖视频（约 15.125 秒，可读的 720×916、每秒 1 帧抽了 15 张）。素材库条目 `https://x-material-library.workers.xd-sites.com/s/rjqagsc0hcqp/assets/2118971398173409489/preview.mp4` 现在返回 404；当前站点清单里这条是 `code_only_preview`，没有 poster、video 或 license，`code_links` 只指向本目录。

原帖列出的 6 个名字都能在画面里对上，但它们不是 1.0.0 那种深色滑杆。15 秒里实际看到的是一张竖版说明页：

- 标题是 OPUS 5.5 / YOUR F*CKING MOTION DESIGN LAB，副行写着 Claude Code + Remotion + GSAP / six editable controls。
- 提示行打出 `build a motion lab. expose six controls. keep every scene editable.`
- 中间预览窗有自己的时间码、场景名，以及一条带菱形刻度的时间轴。
- 下方是 6 张控制卡：spacing、typography、motion blur、easing、follow-through、anticipation。当前场景会给对应的卡加橙色描边。
- 再下面是 directing prompt、一段只展示的 frame-driven code，以及三张交付缩略图。
- 页脚是 THE LOOP：BUILD > RENDER > SCRUB > TUNE > REPEAT。

按抽帧，场景大致是：0–2.2s spacing（弹跳的蓝点和 squash），2.2–3.6s 标题字，3.6–4.6s motion blur 注释，4.6–6.2s 仍是 typography（STRETCH / SNAP），6.2–8.6s easing（先直线后 ease in-out），8.6–11.2s follow-through 拖尾，11.2–13.2s anticipation 的百分比刻度，13.2–15s FINAL DELIVERY。时间码没有做机器 OCR，秒数来自画面上的 `00.0s / 15.0s`。

页面只复刻这些看得见的交互：播放/暂停或逐步前进、拖动 15 秒时间轴、点 6 张卡跳到对应场景、方向键改时间、数字键 1–6 跳卡。系统开启减少动态效果时不自动播放，播放键改为 Step，每次前进 0.5 秒。

明确不做：不接 Claude Code，不加载 Remotion 或 GSAP，不生成、不渲染、也不和帧时钟同步。预览里的代码和命令是画面上的文字，不会执行。不包含原视频、海报、字体文件、商标图片或第三方源码。

许可：原帖没有附开源许可证，站点目录条目也没有 license 字段。
