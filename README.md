# DADA Design Library

DADA 的设计素材、可复用效果和设计工作流 Skill。站点：https://x-material-library.workers.xd-sites.com

站点按四种方式浏览：

- 设计：原画和概念图。只看图和原帖，并推荐类似内容，没有代码。
- 有代码：可以打开的交互或动效。
- 有提示词：静态对比。旁边放提示词，不放代码。
- 待复刻：还没做完，仓库里不再保留占位页面。

## 效果

每条效果使用 `effects/<效果名>/`。目录名只用小写字母、数字和横线，素材 ID 写在该目录的 README 里。

已经有可预览代码的：

- sonia-aurora-loader
- fluxora-glow-path
- tlg-fluted-glass（MIT，许可证见同目录 LICENSE）
- agent-robot-avatar（MIT lite 预览，许可证在 code/index.html）
- codrops-scroll-dissolve
- enes-folded-scroll
- gui-glow-card-hero
- marina-orbit-hero
- nickbaked-ink-type
- noel-kinetic-type
- osmo-list-grid-toggle
- light-progress-bar
- threejs-sequin-field

其余效果目录只保留说明。原先那套通用占位动画已删除，不能再当成复刻结果。

## 单独 fork 的头像仓库

这几个没有整仓并进本仓库。agent-robot-avatar 另有一份 lite 预览在效果目录里，其余还没放进效果目录。它们各自留在 zhanxinyi-lab 名下的 fork，网站「设计」分类只放预览和链接。

- [agent-robot-avatar](https://github.com/zhanxinyi-lab/agent-robot-avatar)：MIT，fork 自 [CX-ArtLab/BoopFace](https://github.com/CX-ArtLab/BoopFace)。`effects/agent-robot-avatar` 只收 v0.7.2 的 lite 预览，没有皮肤库，也没有嵌入式代码。
- [avatar-studio](https://github.com/zhanxinyi-lab/avatar-studio)：MIT，来自 ai-calypse/avatar-studio。
- [robo-face](https://github.com/zhanxinyi-lab/robo-face)、[animate-bot](https://github.com/zhanxinyi-lab/animate-bot)：MIT。bloub 与 animate-bot 的演示图相同，网站只保留 animate-bot，避免重复展示。
- [procedural-expression-library](https://github.com/zhanxinyi-lab/procedural-expression-library)、[mascots](https://github.com/zhanxinyi-lab/mascots)：GPL-3.0，只保留 fork，不把源码抄进本仓库。
- [openrive](https://github.com/zhanxinyi-lab/openrive)：MIT。

## Skill

设计工作流 Skill 放在 `skill/`。每个 Skill 一个目录，名称与 SKILL.md 的 name 一致。收录不等于已经安装。

| Skill | 用途 |
| --- | --- |
| [figma-export](skill/figma-export/SKILL.md) | 按 Figma 链接把节点导出到本地文件夹。触发词：figma导出。 |
| [social-aurora-sizes](skill/social-aurora-sizes/SKILL.md) | 把分层 SVG 导出成微信和 X 的五种社媒尺寸。 |

使用方式和依赖见 [skill/README.md](skill/README.md)。不要把 token、个人路径或未经许可的素材提交进仓库。
