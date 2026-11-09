# 小规模群体演示（不是原帖百万体）

- 作者：@initcore
- 分类：3D
- 状态：ai_recreated
- 原文：https://x.com/initcore/status/2119198891086385568
- 素材 ID：2119198891086385568
- 版本：1.0.0

直接打开 `code/index.html`。单文件 Canvas 2D，没有外链、字体文件、视频或模型。

画面是深色尘土地、雾和朝镜头奔跑的简笔人形（圆头、躯干、两腿）。默认 2000 个。滑杆把模拟倍率调到 0.10–1.00，只缩放积分 dt。暂停冻结积分。一次冲击让车附近的一批进入整具翻滚。控件可用键盘聚焦。开启系统「减少动态效果」时只画一帧，不再持续请求动画帧；关掉之后会重新循环。

## 证据边界

原帖 https://x.com/initcore/status/2119198891086385568 作者 @initcore（maksym）的下列说法只是原文复述，没有随帖源码，不能当成已核验的实现：

- 用 Vork，在 Claude Code 的一次会话里做出。
- 约 1,000,000 个丧尸，每个有 GPU steering、crowd avoidance、ragdoll flight。
- 在 shader 里用 sim clock 做 bullet time。
- 12 秒 1080p，单张 RTX 5090 离线渲染 21 分钟。

这些性能和算法数字都没有源码可对。帖子引用的是 Ravi Parikh 的 Vork（Rust/Slang，Metal/Vulkan，voyager.so/vork）离线成片。帖子没有源码，也没有许可授权。本目录不拷贝视频、游戏模型、引擎 shader 或商标。

素材库预览 mp4 实测规格是 8.0 秒、30fps、720×406、240 帧。那不是帖子里的 12 秒 1080p 源片，文件也不在本仓库里。

本演示实际是：

- 个体数固定 2000，页面和 `window.__crowdProbe.count` 用的是同一个数。
- 算法是原创的：粗网格 BFS 流场寻路、空间哈希分离避让、整具的抛物线加俯仰/翻滚。不是 GPU 刚体 ragdoll，不是百万体，也不是 Vork。开场约 8% 已在空中；之后大约每 0.45 秒模拟时间，再从中距离跑者里抛起最多 4 个，避免翻滚马上归零。冲击按钮一次抛起车附近最多 150 个。落地后回到奔跑。
- 子弹时间只把积分 dt 乘上 0.10–1.00。渲染帧率不跟着变慢。
- 红色块状车和石块是原创占位几何，用来标出冲击和绕行，不是引用的游戏模型。
- 高分屏把 `devicePixelRatio` 上限压到 1.25，避免把画布像素放大到没有意义。

## 浏览器实测

2026-11-10，本机 Chrome headless（`--headless=new`，窗口 1280×800，`deviceScaleFactor` 1）打开 `code/index.html` 的 `file://` 地址。等约 3 秒读取 `window.__crowdProbe`。没有控制台异常，网络请求只有这一个本地文件。

约 3 秒时的读数：

- count：2000
- fps：33.9
- scale：1
- reduced：false

同一轮再过约 1.5 秒，滚动 FPS 是 31.8，个体数仍是 2000。33.9 不是稳定帧率承诺，只是这一次约 3 秒时的近 60 帧平均值。

`prefers-reduced-motion: reduce`：

- 加载前就打开减少动态：约 0.4 秒和再过 2 秒时，包过的 `requestAnimationFrame` 次数都是 0。`__crowdProbe` 为 `{ count: 2000, fps: 0, scale: 1, reduced: true }`。fps 为 0 是因为没有滚动帧可计，不是测到了 0 帧每秒的渲染上限。64×64 采样的颜色跨度是 553，不是纯色。静帧上的翻滚人数是 161。
- 动画过程中切到减少动态：之后 2 秒内动画帧次数停在 162，不再增加；`reduced` 为 true，页面 FPS 显示为「—」。此时点击「一次冲击」，翻滚从 24 变为 174，动画帧次数仍是 162。
- 再切回 `no-preference`：循环恢复，`reduced` 为 false，约 1.2 秒后 fps 为 32.5，动画帧次数从 162 增到 203。
