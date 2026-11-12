# Open Bot Avatar / 立体 Agent 头像

- 作者：M1nG (@ZJM330)
- 分类：AI工具/工作流
- 状态：ai_recreated
- 版本：1.0.1
- 原文：https://x.com/ZJM330/status/2117319107477737944
- 素材 ID：2117319107477737944

## 复刻说明

原帖介绍 Open Bot Avatar：一条 SVG 路径加上眼睛位置，渲染成能跟着指针看的立体小形象，并有 idle、thinking、happy。帖内链接指向 Dominik Scholz 的原帖；对应仓库是 [DominikScholz/open-bot-avatar](https://github.com/DominikScholz/open-bot-avatar) 0.2.0，MIT。

上游没有 git tag。固定点是提交 [`b59a73ac4be67d45a6756ef22309440b27d87682`](https://github.com/DominikScholz/open-bot-avatar/commit/b59a73ac4be67d45a6756ef22309440b27d87682)：npm 上 `open-bot-avatar@0.2.0` 的 gitHead 就是这一笔，`packages/core/package.json` 也是在这里第一次写成 `"version": "0.2.0"`。父提交 `8dd06351afb320045d07b5e3a47d71b9684907eb` 仍是 0.1.2；下一版 `6c42fc3b90f6fc92d2333807de775d0e9e48212f` 是 0.2.1。

页面只内嵌这一版的渲染器，没有拷贝 apps、assets、docs、gallery 目录、skills、锁文件或 CI。许可原文写在 `code/index.html` 的脚本注释里。

## 许可与来源文件

上述提交里，仓库根目录的 `LICENSE` 和 `packages/core/LICENSE` 是同一份文件，git blob 都是 `4ef1195fa75986acca3d8516541e557d566bdf1d`（1071 字节）。正文从单独一行的 `MIT License` 开始，接着 `Copyright (c) 2026 Dominik Scholz` 和标准许可、免责声明。页面注释逐行收录这一 blob，不是另写一份摘要。

| 页面里的轮廓 | 来源文件 | 是否上屏 |
|---|---|---|
| ghost | `gallery/ghost.json` | 是 |
| cat | `gallery/cat.json` | 是 |
| controller、sprout、mug | `packages/core/src/examples.ts` | 是 |
| barbell、lightbulb、chat、watering-can | `packages/core/src/examples.ts` | 否，只随渲染器里的示例一起留下 |

这些轮廓的路径和眼睛参数（`x`、`y`、`spacing`、`scale`）与上表文件逐字一致。它们随仓库以 MIT 发布，不是另行描摹的未授权图形。

指针在页面上移动时，头像转向指针；三个按钮切换闲着、思考和开心。系统开启减少动态效果时，沿用上游的 `reducedMotion: "system"`，身体停在静息姿态。

## 用在哪些项目

| 项目 | 用的版本 | 什么时候 | 负责人 | 备注 |
|---|---|---|---|---|
| — | — | — | — | 尚未被项目使用 |
