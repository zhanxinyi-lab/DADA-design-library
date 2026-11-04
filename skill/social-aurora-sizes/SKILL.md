---
name: social-aurora-sizes
description: 将用户提供的完整 SVG 母版批量导出为微信和 X 的五种社媒尺寸，背景等比裁切，字标与小字独立居中，输出 JPG 和可编辑 SVG。适用于“给 SVG 出社媒尺寸”、HARKEN 全媒体适配；不把单独字标当成完整背景母版。
metadata:
  short-description: HARKEN 蓝绿极光社媒尺寸制作
---

# HARKEN 蓝绿极光社媒尺寸

默认任务是：用户只提供完整 SVG，直接制作以下五种尺寸，无需用户手工拆图层或填写参数。沿用 SVG 的背景颜色、字标、标语和图形标，不重新生成背景，不擅自删标或改色。只有明确要求重新设计时，才使用后面的视觉建议和提示词；提示词是整理后的建议，不是历史生成原文。

## 批量导出入口

使用随 Skill 提供的 scripts/export_social.py。要求 Python 3.9+、Pillow 和 resvg_py。先用现有环境，不自动安装依赖。脚本支持 --python-path 指向已经存在的依赖目录。缺少依赖时告知用户；用户授权安装后，可运行 python -m pip install -r requirements.txt。

执行示例（将路径换成实际输入和新的输出目录）：

    python scripts/export_social.py input.svg --output output/Set1

需要指定已有依赖目录时增加：

    --python-path /path/to/existing/python-packages

从 Skill 文件夹运行，或使用脚本绝对路径。输出目录必须尚不存在；保留输入和以前交付。两份 SVG 分别导出到 Set1 和 Set2。不要默认使用旧临时文件作为用户这次的输入。

每份输入生成 5 个 JPG、5 个 SVG、preview.jpg 和 report.json。JPG 上限默认 1,000,000 字节，SVG 内嵌背景时不受这个上限约束。JSON 记录尺寸、质量、体积和前景外框。

## 自动拆分和边界

- 自动识别第一个铺满画布的 image 或 rect 作为背景，保留 defs、渐变、裁切和祖先变换。其余可见图层作为完整前景。不要把整个 SVG 直接 cover 裁切，否则会截掉字标。
- 若背景由多层组成，先查看 XML 和渲染预览，在工作副本把背景组织成一个组，再传 --background-id 对应组 ID。不要修改原文件；仅有模板规则无法可靠识别任意 SVG 的语义。
- 默认保留全部前景，包括图形标和标语。用户要“只有字标”时先在副本中准确移除图形标，再导出；不要凭颜色猜测。当前字标版方形也保留标语，不沿用早期方形只放 HARKEN 的规则。
- 文字已转曲、图片已内嵌时可只给一份 SVG。活文字、外链资源、仅字标文件、或整图压成一张位图时，先检查现有素材是否能补齐。缺少背景或无法分离前景时明确说明需要什么，不声称自动完成。
- 背景等比铺满居中裁切。前景按可见外框居中，默认保留母版坐标尺寸，过大时等比缩小，左右至少留 7%。X_2000x800 使用项目约定 y=20%–85% 的安全带；这不是平台实时规范，用户指定新安全区时调整脚本或布局。
- 本脚本是通用等比裁切，不复刻旧脚本的轻微非等比缩放和按竖条边界裁切。需要与历史成品逐像素一致时应读取对应旧布局参数再适配，不能承诺现默认规则会完全相同。
- 渲染 SVG 后生成 JPG；前景仍保留矢量。SVG 内嵌位图背景不能变成可编辑矢量，转曲标语也不是可改字的文本层。

## 每次交付检查

读取 report.json，验证五个尺寸、字节数和前景外框；打开 preview.jpg 检查每张的裁切、视觉中心、文字对比和标语完整性。放大至少检查一张字标边缘及背景渐变。若有明显白字落亮部等问题，在本次副本调整布局后重导；不要未经要求改变定稿颜色。输出链接和实际验证结果，不把格式校验等同于出图验收。

## 视觉基准

- 背景接近黑色的深蓝；主体是一条宽厚、连续、平面化的极光带。
- 主色是天蓝，向青蓝和正常绿色平滑过渡；绿色出现在光带较亮的末端或消散处，不要压在最暗边缘。
- 转折主要放在左右三分之一；画面中央保持相对稳定、较暗，为白色文字留出安全区。
- 使用等宽垂直平涂条纹，条内只有轻微明暗过渡。不得出现斑驳、木纹、树纹、摩尔纹、细碎发丝光束、颗粒噪点或过强霓虹光晕。

## 推荐提示词

中文：

近黑色深蓝背景上的抽象蓝绿色极光光带，一整条宽厚、连续、半透明的平面光带从左侧进入，在左侧三分之一处柔和弯折，经过中央较暗的留白区域，再在右侧三分之一处弯折并向边缘消散。主体以清晰天蓝色为主，向青蓝和自然绿色平滑过渡，绿色只出现在有亮度的光带末端。使用等宽垂直平面色条，条内有非常轻的明暗过渡，几何、克制、现代、干净，适合叠加白色品牌文字。

English:

Abstract blue-green aurora on a near-black deep navy background, formed by one broad, continuous, translucent planar ribbon. The ribbon enters from the left, bends softly around the left third, passes through a darker central area reserved for white typography, bends again around the right third, and fades toward the edges. Dominant clear sky blue, smoothly transitioning through teal into natural green only near the brighter fading ends. Evenly spaced vertical flat color ribs with subtle tonal variation inside each rib, clean restrained contemporary identity design, smooth planar gradients, quiet center, suitable for white brand typography.

Negative prompt: photographic sky, stars, clouds, lightning, mottled texture, marbled texture, wood grain, tree grain, moiré, noisy vertical streaks, hair-like rays, thin laser beams, random light spots, excessive bloom, harsh neon glow, high-frequency detail, text, logo, watermark.

提示词只负责建立大形；最终颜色、竖条宽度和文字安全区需要在设计软件或脚本中复核和校正。

## 社媒尺寸

默认从同一张母版裁切，不为每个平台重新画一条光带。当前常用输出：

- WeChat_2350x1000.jpg
- WeChat_1000x1000.jpg
- WeChat_1080x1440.jpg
- X_2000x800.jpg
- X_1600x900.jpg

文件名使用英文“平台_尺寸”。新的平台先确定画布比例和文字安全区，再沿用母版的光带方向、蓝绿关系和暗部结构。

## 制作流程

1. 确认已批准的母版，以及图形标、字标或纯背景版本。
2. 以母版为底做 cover crop；保持光带连续性和中央文字安全区，不要拉伸背景。
3. 检查中央区域，白字应避开最亮转折和高饱和绿色。
4. 仅在重新设计背景任务中调整蓝绿关系；仅适配尺寸时保持输入颜色。
5. 检查垂直条纹是否等宽、连续、平滑。发现树纹或摩尔纹时回到平涂和低频处理，不要靠锐化补细节。
6. JPG 控制在目标平台体积限制内；需要继续编辑时另外输出 SVG，背景可内嵌位图，文字和标志保持独立矢量层。

## 验收

- 尺寸和文件名符合目标平台。
- 各尺寸来自同一母版，裁切没有拉伸或明显断裂。
- 中央白字有足够对比度和连续安全区。
- 蓝色是主体，绿色是受控的亮部过渡，不阴森、不脏、不发灰。
- 放大检查没有树纹、摩尔纹、重复噪点、明显接缝或高频竖向波纹。
- SVG 渲染后应与 JPG 内容一致；JPG 用于发布，SVG 用于编辑。
