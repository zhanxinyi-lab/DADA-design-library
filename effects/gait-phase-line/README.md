# 步态拖线

- 作者：@techartist_
- 分类：教学 · 网页交互
- 状态：video_recreated
- 原文：https://x.com/techartist_/status/2119850623315456188
- 素材 ID：2119850623315456188
- 版本：1.0.0

## 复刻说明

自包含单页，无外链。侧身骨骼和肌肉色块是页面里画的，没有使用原视频、海报或解剖插图，页面上也不出现原片水印。

站点里的 `preview.mp4` 是 720×540、30fps、8.0 秒。条目写的时长约 26 秒，这份预览没有后半段。8 秒里先是步态页，大约 2 秒后翻到别的课（肋骨拉线、冠状面、一根长骨）。下面只做步态页这一件连续的事：拖页面下方那条线，腿跟着换成对应姿势，而不是把整段视频播一遍。

### 片中能对上的

- 一条可拖的进度线，刻度依次是 landing、push-off、swing up、reach、pull back。
- 拖动时，侧身的两条腿换姿势，不是整个人闪切。
- 停在某个刻度时，旁边列出这一下在做的动作和肌肉。片中能读到的是：
  - landing：髋伸 gluteals，膝屈 quadriceps（离心），踝背屈 gastrocnemius（离心）
  - push-off：髋伸 gluteals，膝伸 quadriceps，踝跖屈 gastrocnemius
  - swing up：髋屈 hip flexors，膝屈 hamstrings，踝背屈 tibialis anterior
  - reach：髋屈 hip flexors，膝伸 quadriceps，踝背屈 tibialis anterior
  - pull back：髋伸 gluteals，膝伸 hamstrings（离心），踝背屈 tibialis anterior
- 拖到线的末端，出现 turn the page。

原片左页的句子、书的装帧、刻度上的骨头形滑块和署名没有搬过来。肌肉名称用的是这一页上能读到的词，红块只标在正在发力的那条腿上。

### 操作

- 拖进度线，或点刻度之间。指针移动时，允许动态效果就把绘制合到下一帧；腿直接画在当前刻度，不沿时间播一段动画。
- 进度线获得焦点后，左右或上下方向键沿同一条线走，Home / End 到两端。焦点用轮廓标出。
- 读数、滑块位置、阶段名和 aria-valuetext 在同一次绘制里写成同一个位置。
- 系统开启减少动态效果时，拖动立刻跳到目标姿势并同步画一次，不排动画帧。
