# Agent Robot Avatar

- 作者：CX ART Lab
- 分类：网页交互
- 状态：has_code
- 许可证：MIT（Copyright (c) 2026 CX ART Lab，全文在 code/index.html 的脚本注释里）
- 原文：https://github.com/CX-ArtLab/agent-robot-avatar
- 本地 fork：https://github.com/zhanxinyi-lab/agent-robot-avatar
- 素材 ID：agent-robot-avatar
- 版本：1.0.0

`code/index.html` 是单文件预览。组件来自 zhanxinyi-lab/agent-robot-avatar 的 v0.7.2（提交 6603a04）。GitHub 显示这个仓库 fork 自 CX-ArtLab/BoopFace；包里的仓库地址写的是 CX-ArtLab/agent-robot-avatar。这里只用 lite 入口，保留表情、视线和拖拽，不包含皮肤库，也不包含嵌入式移植。

预览页浅色底上放一个黑色头像。眼睛会跟着指针，按住头部可以拖，松手后弹回。下面的按钮调用组件自己的 `play()`，名称与上游 0.7 的动作表一致。系统开启减少动态效果时，沿用组件自己的处理。
