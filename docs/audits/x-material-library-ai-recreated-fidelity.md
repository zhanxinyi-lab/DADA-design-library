# x-material-library：AI 复刻效果还原度审计

> 审计基线：`zhanxinyi-lab/DADA-design-library` 的 `origin/main`，`c1c258ba89a54a8603725dba9f23534684b51511`（2026-11-06 fetch 后）。站点预览来自 <https://x-material-library.workers.xd-sites.com/>。本文件只记录审计结果，不改效果代码。

## 方法与口径

逐项核对 issue #9 列出的来源链接、随静态站点导出的原帖海报/短视频副本（只读）、远端主线 `effects/<slug>/README.md` / `code/index.html` 映射，以及对应的线上代码预览。线上代码路由均可打开；视觉核查以桌面默认视口的预览截图为主，不代表移动端、跨浏览器或音频 QA。X/XHS 原站页面未在本轮验证登录态，原帖画面证据取自站点静态导出中的媒体副本；不能从文案推断副本未呈现的内容。

结论分为“确认偏差 / 基本一致 / 证据不足”。影响级别：P1 = 核心视觉或效果明显不符；P2 = 重要构成/范围不符；P3 = 轻微差异或可接受的限定范围。建议仅界定单效果修复边界，不代表本报告创建了后续任务。

## 逐项记录

### 1. 液态玻璃字 / 泡泡成字转场

- **素材 ID / 来源：** `2116612471880610054` · [@kloss_xyz 原帖](https://x.com/kloss_xyz/status/2116612471880610054)
- **DADA 源码：** 有，[`effects/kloss-liquid-glass-type/`](../../effects/kloss-liquid-glass-type/)，主线 README 版本 `1.1.0`。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/2116612471880610054/code/index.html)
- **对照：** 导出短片可见液面线、透明泡状主体及其后续成字；预览实现了对应的液面、带虹彩边缘的泡泡和文字形变。README 明确限定为原片的 “LIQUID” 段；原片其余片段、HUD 和音效未复刻。当前可见的核心泡泡成字段基本吻合，未发现足以要求返工的有据差异。
- **结论 / 影响：** **基本一致 · P3（仅针对已声明的 LIQUID 段）**。
- **建议修复边界：** 暂无必需修复。若以后要求覆盖整支原片，应另限于补齐有来源证据的其它镜头/HUD/音效，不扩大到本效果以外。

### 2. little after effects exercise

- **素材 ID / 来源：** `2116583457438761319` · [@sebiiweby 原帖](https://x.com/sebiiweby/status/2116583457438761319)
- **DADA 源码：** **未发现**对应 `effects/<slug>/` 目录或 README；当前代码仅能在静态导出副本中找到。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/2116583457438761319/code/index.html)
- **对照：** 原帖海报/短片帧以白色网格底上的超大黑色排印和图形构成为主；线上预览则是粉色网格上的像素块人物、星形和放射线。核心轮廓、色彩关系和画面主题均不同，不是同一排印效果的轻微样式偏差。
- **结论 / 影响：** **确认偏差 · P1**。
- **建议修复边界：** 只修这一条：先把站点副本迁成 DADA 仓可追溯的 `effects/<slug>/` 源码，再按原帖可见的排印主体、背景网格和形变节奏复刻；不顺带改其它动画。

### 3. Geist Serif

- **素材 ID / 来源：** `2116499499548045336` · [@vikingmute 原帖](https://x.com/vikingmute/status/2116499499548045336)，并链接 [Vercel 的 Geist Serif 介绍](https://vercel.com/blog/introducing-geist-serif)。
- **DADA 源码：** **未发现**对应 `effects/<slug>/` 目录或 README；站点静态导出中有独立代码页及一张源页面图片。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/2116499499548045336/code/index.html)
- **对照：** 导出源图展示的是多栏字体 specimen（Sans / Serif / Mono / Pixel、样例段落）；线上预览只展示一枚大字形，并提供“元素形状”滑杆及 `G / a / R` 替代字形按钮。可确认两边的展示范围和交互不同；仅凭现有截图不足以断言字形轮廓是否准确复现了 Geist Serif。
- **结论 / 影响：** **确认偏差 · P2（展示与交互范围）；字形轮廓准确度证据不足**。
- **建议修复边界：** 只处理 Geist Serif 这一项：先纳入可追溯 DADA 源码，再以来源 specimen 校准真实 Serif 样字和版式；不要把无法从来源证实的可变轴行为当成既定规格。

### 4. Noel 动态排印

- **素材 ID / 来源：** `xhs-noel-mosyenboy` · [小红书原帖](https://xhslink.cn/o/xnJJ91oNTA)
- **DADA 源码：** 有，[`effects/noel-kinetic-type/`](../../effects/noel-kinetic-type/)；README 版本 `1.0.0`。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/xhs-noel-mosyenboy/code/index.html)
- **对照：** 导出原帖视频抽帧可见高对比箭头、文字与贴纸/UI 图形的拼贴画面；线上预览是浅灰底、DADA 标记和几块静态感较强的抽象矩形。来源与预览的主体图形、色彩和构图明显不一致，现有预览没有呈现来源中最醒目的箭头/排印组合。
- **结论 / 影响：** **确认偏差 · P1**。
- **建议修复边界：** 只重做此动态排印：以来源可见的箭头/文字/贴纸构成和镜头节奏为边界；不要把通用 DADA 品牌占位图形当作来源视觉。

### 5. 滚动分区边缘溶解

- **素材 ID / 来源：** `2116144602465931717` · [@codrops 原帖](https://x.com/codrops/status/2116144602465931717)，链接其 [Seam Transitions 演示](https://tympanus.net/Demos/SeamTransitions/)。
- **DADA 源码：** 有，[`effects/codrops-scroll-dissolve/`](../../effects/codrops-scroll-dissolve/)；README 版本 `1.0.0`。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/2116144602465931717/code/index.html)
- **对照：** 原帖明确介绍 11 种滚动驱动的分区边缘动画；预览只有 `Torn` / `Dissolve` 两个切换项，当前画面是 DADA “pandahi” 森林 Hero。相较来源演示，边缘样式/变化范围明显收窄；所见源视频画面与预览的森林场景也不相同。没有据此推断每一种源转场的内部实现。
- **结论 / 影响：** **确认偏差 · P2**。
- **建议修复边界：** 只修该滚动边缘效果：按来源选定且能由原帖/演示验证的边缘形态与滚动时序，避免把两种按钮状态误当作完整来源效果集；不扩展成通用转场库。

### 6. Hero 水墨流体文字

- **素材 ID / 来源：** `2116042685043888269` · [@nickbakeddesign 原帖](https://x.com/nickbakeddesign/status/2116042685043888269)；站点另记录了作者的 [说明链接](https://twitter.com/nickbakeddesign/status/2115688643344093499)。
- **DADA 源码：** 有，[`effects/nickbaked-ink-type/`](../../effects/nickbaked-ink-type/)；README 版本 `1.0.0`。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/2116042685043888269/code/index.html)
- **对照：** 导出源视频抽帧是白色书页式排版（“De Dracone”标题、段落文字及右侧彩色插画）；预览换成 PANda 标题、另一组占位段落和左侧红色墨团。书页/墨迹概念仍可辨认，但内容、插画位置与主要构图不一致。
- **结论 / 影响：** **确认偏差 · P2**。
- **建议修复边界：** 限定为此 Hero：以来源可见的文字层级、插画/墨迹位置和画面流动方式校准；不需重做通用文章排版系统。

### 7. 3D 折叠滚动

- **素材 ID / 来源：** `2115816197266477213` · [@enesozturkdev 原帖](https://x.com/enesozturkdev/status/2115816197266477213)
- **DADA 源码：** 有，[`effects/enes-folded-scroll/`](../../effects/enes-folded-scroll/)；README 版本 `1.0.0`。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/2115816197266477213/code/index.html)
- **对照：** 原帖海报为深色 emoji picker（“Search emoji…”、分类标题和多行彩色 emoji 网格）；线上预览为“Search panda…”和 Lookbook / Night rack 等文字列表，主要图标为单色符号。可见内容及列表密度明显不同；预览首屏截图没有直接呈现折叠边缘的滚动过程，因此本结论针对当前可见构成，不推断未观测到的 3D 变形参数。
- **结论 / 影响：** **确认偏差 · P2**。
- **建议修复边界：** 只校准此效果：恢复来源的 emoji 网格/分类内容，并在滚动时让边缘折叠成为可观察的主要效果；不改其它菜单或表情库。

### 8. Hero 3D 元素环绕标题 / 礼品卡

- **素材 ID / 来源：** `2115447175400276149` · [@marina_uiux 原帖](https://x.com/marina_uiux/status/2115447175400276149)
- **DADA 源码：** 有，[`effects/marina-orbit-hero/`](../../effects/marina-orbit-hero/)；README 版本 `1.0.0`。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/2115447175400276149/code/index.html)
- **对照：** 源视频/海报展示明亮的花束/礼品卡 Hero 与具有体积感的花朵元素；预览使用黑底、居中的 “Gift Card” 字样和几朵简单平面花形。来源的明亮背景、立体质感与环绕主体在预览中均未保留。
- **结论 / 影响：** **确认偏差 · P1**。
- **建议修复边界：** 仅重做该 3D 礼品卡 Hero：恢复来源中的花束/卡片体积、空间关系及标题环绕；不要把其它 3D 商品展示一起纳入。

### 9. 发光 3D Hero

- **素材 ID / 来源：** `2115433719183864058` · [@guicolombel 原帖](https://x.com/guicolombel/status/2115433719183864058)
- **DADA 源码：** 有，[`effects/gui-glow-card-hero/`](../../effects/gui-glow-card-hero/)；README 版本 `1.0.0`。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/2115433719183864058/code/index.html)
- **对照：** 源海报是居中的半透明粉橙色发光体，内部透出文字并落在反射地面上；线上预览截图呈现为几块彼此分离的红色矩形/扇形切片，文字模糊且没有源图的连续玻璃体与镜面关系。主体轮廓和材质是核心差异。
- **结论 / 影响：** **确认偏差 · P1**。
- **建议修复边界：** 仅修复此 Hero 的单一主体：按来源恢复连续的半透明发光体、可读文字层和反射地面，不扩大到整个作品集站点。

### 10. 列表 / 网格切换

- **素材 ID / 来源：** issue 写作 `2115412490378019`；原 issue 链接是 [@osmosupply 原帖（issue 提供的 ID）](https://x.com/osmosupply/status/2115412490378019)。DADA README 与站点实际使用的规范 ID 是 **`2115412490372678019`** · [原帖（DADA 规范 ID）](https://x.com/osmosupply/status/2115412490372678019)。两处 ID 不一致，建议看板确认并更正记录。
- **DADA 源码：** 有，[`effects/osmo-list-grid-toggle/`](../../effects/osmo-list-grid-toggle/)；README 记录规范 ID `2115412490372678019`，版本 `1.0.0`。
- **站点预览：** [实时预览（规范 ID）](https://x-material-library.workers.xd-sites.com/assets/2115412490372678019/code/index.html)
- **对照：** 原帖展示项目照片从列表与网格之间做 FLIP 位置转换，并在移动时淡出标题/分隔线；预览有 `List` / `Grid` 控制和对应布局转换，核心交互基本一致。预览卡片使用几何色块占位，没有来源中的摄影缩略图，因而整体视觉内容较简化。
- **结论 / 影响：** **基本一致 · P3**（有低影响的素材占位差异）。
- **建议修复边界：** 如需补齐，只替换此预览的占位卡片内容/缩略图，不重写已匹配的 List/Grid 转换。

### 11. Shader 点阵显现

- **素材 ID / 来源：** `2115263887667069027` · [@threejs 原帖](https://x.com/threejs/status/2115263887667069027)，另有 [原演示链接](https://playfulground.work/exp/flip-sequin/)。
- **DADA 源码：** 有，[`effects/threejs-sequin-field/`](../../effects/threejs-sequin-field/)；README 版本 `1.0.0`。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/2115263887667069027/code/index.html)
- **对照：** 来源海报显示带有明暗反射的密集亮片/圆片表面和局部高亮；预览是均匀灰色圆点场，局部区域变亮，但圆片基本保持扁平、均一，未见来源的物体/图像质感。点阵与局部亮度响应方向相符，材质和输入画面则明显简化。
- **结论 / 影响：** **确认偏差 · P2**。
- **建议修复边界：** 只修此 shader：以来源可见的亮片反射、明暗结构和图像内容为边界；不改其它 Three.js 背景效果。

### 12. TLG Fluted Glass

- **素材 ID / 来源：** `tlg-fluted-glass` · [the-lazy-god 原始仓库](https://github.com/the-lazy-god/tlg-fluted-glass)
- **DADA 源码：** 有，[`effects/tlg-fluted-glass/`](../../effects/tlg-fluted-glass/)。该目录 README 状态是 `has_code`，而线上站点数据将其标为 `ai_recreated`，两者状态不一致。
- **站点预览：** [实时预览](https://x-material-library.workers.xd-sites.com/assets/tlg-fluted-glass/code/index.html)
- **对照：** 上游 README 定义了输入图像上的棱纹玻璃效果，并提供交互模式、棱纹数量、旋转、运动与叠层参数；DADA 预览具有相应控制项及鼠标/滚动/静止模式，核心棱纹和交互能力基本吻合。当前预览用彩色渐变作为演示底图，而非上游示例中的实际图像纹理，导致折射/图像细节无法直接比对。
- **结论 / 影响：** **基本一致 · P3**（演示纹理与站点状态标签待校准）。
- **建议修复边界：** 无高优先级视觉返工；如需补齐，仅验证一张实际图像纹理的折射效果，并统一该素材的 `has_code` / `ai_recreated` 状态定义。

## 汇总

- **确认偏差：** #2 little after effects exercise、#3 Geist Serif（展示/交互范围）、#4 Noel 动态排印、#5 Codrops 边缘转场、#6 水墨流体文字、#7 Enes 折叠滚动、#8 Marina 3D Hero、#9 发光 3D Hero、#11 Three.js 点阵。
- **基本一致：** #1 液态玻璃字（仅 README 声明的 LIQUID 段）、#10 列表/网格切换、#12 TLG Fluted Glass。
- **证据不足事项：** #3 的 Geist Serif 字形轮廓准确度；#7 的完整滚动折叠运动参数；#12 用真实图片时的折射细节。上述项目不据此扩大差异结论。
- **源码映射异常：** #2、#3 只有静态站点导出里的代码，没有当前远端主线 `effects/` 源目录；#10 issue ID 与 DADA 规范 ID 不同；#12 站点与 DADA README 的状态标签不同。

## PR 自查

- 本次变更仅新增本审计报告；未修改 `effects/`、静态导出或其它文件。
- 未部署、未合并、未创建/修改/关闭看板 issue。
- 执行 `git diff --check`：报告提交前通过（无空白错误）。
- 按 DADA 仓库 PR 模板：类型选“其他”，说明仅新增审计文档，未涉及效果版本变化；代码打开/动效检查、版本号及 CHANGELOG 检查不适用于本次纯文档变更。
