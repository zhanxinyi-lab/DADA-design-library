# Geist Serif 与字体家族连字样例

- 作者：@vikingmute
- 字体版权：Vercel，与 basement.studio 合作
- 许可证：SIL Open Font License 1.1（全文随附）
- 分类：字体排印
- 状态：has_code
- 原文：https://x.com/vikingmute/status/2116499499548045336
- 素材 ID：2116499499548045336
- 版本：1.0.0

## 说明

此单页同时展示两种明确标注的 Geist 字体能力：

- `GeistSerif.woff2` 的真实 `ELSH` 轴用于点号、标点等受影响字形的实时样例；页面同时以真实 `ss01` OpenType 特性并排展示 `aR` 默认 / 替代字形。
- 连字对照使用同一字体家族的 `GeistSans.woff2`。它的 GSUB `liga` 特性含有 `f+i`、`f+l` 和 `f+f` 替代规则；页面将开关打开与关闭的相同文本并排展示。

随附 Geist Serif 文件的 GSUB 不含标准 `liga` 特性；因此页面不声称 fi/fl 连字属于 Serif 字体，而是把实际连字清楚标为 Geist Sans。两份 Vercel 官方 WOFF2 字体以原始字节内嵌在 `code/index.html`，使素材保持单页、自包含；本 README 与单页内可展开的“字体许可”区域均附有完整 SIL Open Font License 1.1。来源：https://github.com/vercel/geist-font。该页展示静态字形与字体特性，不推断或声称复刻原帖动画。

## 字体来源与核验

来源仓库：<https://github.com/vercel/geist-font>（Vercel × basement.studio）。内嵌 WOFF2 的 SHA-256：

- Geist Serif VF · 49,036 bytes · `022e59b139ab2ce6962d91fe08539ea9e5f4a734d1bdffbf6fbbb9bc46921e96`
- Geist Sans VF · 69,760 bytes · `2ffebe993e969069a9789d15164b7715d42491b5835516c5e3b935d5f81b05f1`

FontTools 对上述字节核验：Geist Serif 的 `fvar` 轴为 `ELSH` 0/0/100，GSUB 特性列表不含 `liga`；Geist Sans 的 GSUB `liga` 查找含 `fi`、`fl`、`ff` 替代。

## 字体许可

```text
Copyright (c) 2023 Vercel, in collaboration with basement.studio

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
http://scripts.sil.org/OFL

-----------------------------------------------------------
SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
-----------------------------------------------------------

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font creation
efforts of academic and linguistic communities, and to provide a free and
open framework in which fonts may be shared and improved in partnership
with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded,
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply
to any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software components as
distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to, deleting,
or substituting -- in part or in whole -- any of the components of the
Original Version, by changing formats or by porting the Font Software to a
new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION AND CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed, modify,
redistribute, and sell modified and unmodified copies of the Font
Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components,
in Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the corresponding
Copyright Holder. This restriction only applies to the primary font name as
presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created
using the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
OTHER DEALINGS IN THE FONT SOFTWARE.
```
