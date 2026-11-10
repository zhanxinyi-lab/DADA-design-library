# VoiceOrbs

- 作者：Alexis Munoz（amunozdev）
- 分类：网页实验
- 状态：has_code
- 许可证：MIT（Copyright (c) 2026 Alexis Munoz）。全文在 `code/index.html` 页脚，也在 `code/upstream.json` 的 `LICENSE`。
- 原文：https://github.com/amunozdev/voiceorbs
- 线上演示：https://voiceorbs.vercel.app/
- 上游提交：8b2799917734f52c9293a489e08982ca5b0187e9（main，2026-09-28，`show advanced controls without a disclosure`）
- 素材 ID：voice-orbs
- 版本：1.0.0

公开库 20 个光球，加上上游 `/drafts` 里已有实现、但没有放进首页的 3 个草稿（Radiance Orb、Dot Orbit、Duotone Flow）。预览不请求 voiceorbs.vercel.app。

本地打开 `code/index.html`。搜索、按技术 / 无第三方依赖 / Tailwind 源码筛选，卡片会自动走连接、聆听、思考、说话、待命。点「自定义与查看代码」可以改状态（含错误和停用）、播放演示、开关麦克风、调速度和尺寸、改颜色，并在光球和状态条之间切换。方向键可移动状态，Esc 关闭。系统开启「减少动态效果」时，演示停止，光球停在对应静止姿态。

`code/upstream.json` 是上述提交的源码快照：LICENSE、上游 README，以及 `src/registry` 里除测试和 Node 读文件脚本以外的实现。直接用文件协议打开时，浏览器可能拦截读取这份 JSON；用静态服务器打开 `code/` 后，详情里可以按文件查看。

和 DADA 单文件效果规范不一致的地方，只做了这些适配：

- 上游是 Next.js 应用。页面收成一个 `code/index.html`，没有带入工作流、锁文件、环境变量示例或 `examples/voice-assistant`。
- `@paper-design/shaders-react` 的许可不是 MIT（指向 paper-design/shaders 的 LICENSE），着色器本体没有复制。Plasma、Mercury、Dither、Grain、Radiance、Dot Orbit 仍运行上游 MIT 组件里的状态和 uniforms 计算；画面是本地画布按同一套 uniforms 画的近似，不是 Paper 的着色器。
- Nebula Orb 没有打包 three.js 和 React Three Fiber。片段/顶点着色器来自上游 MIT 的 `nebula-scene.tsx`，用原生 WebGL 绘制。网格细分用 5。上游把 icosahedron detail 设成 16，那会变成无法运行的网格。
- 卡片预览用 CSS Modules 版本。有 Tailwind 变体的源码留在快照里，不在预览里切换运行时。
