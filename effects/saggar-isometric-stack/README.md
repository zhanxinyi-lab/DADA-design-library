# Saggar 等轴测技术栈

- 作者：@sonia_axion
- 分类：品牌 · 网页交互
- 状态：ai_recreated
- 原文：https://x.com/sonia_axion/status/2119521404857254112
- 素材 ID：2119521404857254112
- 版本：1.0.0

给 Saggar 做的网站区块复刻。帖文只说用它代替大段文字讲技术栈。无源码、无许可证、无标志文件。页面不嵌图片、字体或标志图形。

## 实际看到的画面

1080p 帧的背景是浅冷灰，约 `#f3f4f9`，不是深色页。角点像素约为 `(243, 244, 249)`，正文比背景更暗。先前「深色七层叠板」是看图描述看反了，本页按帧像素来做。

高亮是一块饱和蓝（约 `#4f5cf6`）的扁椭圆，大约 360×180。约 10.3 秒里它自上而下停 5 次，每次大约 2 秒，相邻中心间距约 175px，并左右交替偏移：

1. Scenarios（偏右，右上卡片同时被浅蓝洗亮）
2. Personas（偏左，左上卡片）
3. The firing（偏右，右中卡片）
4. Traces（偏左，左下卡片）
5. The cone（偏右，右下卡片）

全帧 Windows OCR 没有读出 Platform、Design System、Evals、The model、Retrieval、Data。叠层上的深色笔画框得很小，单独放大后 OCR 仍是空的，所以没有把这些词写进页面。五层标签用的是和该层同步点亮的卡片标题。这是从同步关系推出来的，不是从斜置层名里逐字母读出来的。

## 卡片全文

左上 Personas

Impatient, confused, adversarial, multilingual. Simulated users that behave like your worst Tuesday.

左下 Traces

Every regression comes with the exact turn, the tool call and a diff against the last release that passed.

右上 Scenarios

Plain files in your repo. A goal, a persona and what must never happen. Saggar writes the variations.

右中 The firing

Thousands of conversations run in parallel against sandboxed tools. Nothing touches real data.

右下 The cone

Below the bar you set, the merge is held.

Above it, ship with proof instead of hope.

## 相对 OCR 改过的空格和字母

只改了断词、大小写和明显的字形误读：

- lmpatient → Impatient
- confu sed → confused
- m uttilingual → multilingual
- li ke / WO rst / ?uesday → like your worst Tuesday
- Eve ry → Every
- th e → the
- t00l → tool
- ag ai nst → against
- re PO → repo
- g oa l → goal
- n ever → never
- hap pen → happen
- write S → writes
- Th e firing → The firing
- Thousands Of → Thousands of
- ru n → run
- tOOls → tools
- re al d ata → real data
- BeIow / th e b ar / YO u → Below the bar you
- i n stead Of → instead of

The cone 用阈值裁切逐字母核对过，是 T-h-e-c-o-n-e，不是 The score。The firing 后面没有再读出第二个词。末行 Above it, ship with proof instead of hope 来自加对比后的全帧 OCR 词框；提示里只有碎片「Above it, shi」，后续单词是这次 OCR 补全的，没有另造句子。

没有采用看图误读「Adversarial personas that behave like the exact user」。

## 触发

录像里没有鼠标，也看不出页面在滚动。高亮按约 2 秒一层自动往下循环，到最底层后回到顶层。不是滚动劫持。

## 验收补上的可达性

下面这些原帖画面里看不到，是按验收补的：

- 上下或左右方向键移动高亮层。按钮和每一层、每一张卡片也能切。焦点用 `:focus-visible` 描边。
- 窄屏改成单列：叠层在上，五张卡片按高亮顺序排在下面，避免横向溢出。
- `prefers-reduced-motion: reduce` 时不自动播放，停在第一层 Scenarios，文案保持可读。键盘和按钮仍可切换。
