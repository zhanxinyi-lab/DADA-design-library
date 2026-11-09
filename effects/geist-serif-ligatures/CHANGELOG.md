# 更新记录

## 1.0.0 — 2026-11-06
- 新增交互字体样例：使用内嵌的 Geist Serif 官方 WOFF2 展示真实 ELSH 轴与 `ss01` 替代字形；另以同家族 Geist Sans 官方 WOFF2 展示经 GSUB 核验的 fi、fl、ff 连字开 / 关对照。
- 字体文件以原始字节内嵌于单页；SIL OFL 1.1 全文写入素材 README。注明 Geist Serif 的 GSUB 不含标准 `liga` 特性，不把 Geist Sans 连字误标为 Serif 特性，也不声称复刻未证实动画。
- 追加字体字节 SHA-256 与 FontTools 的 GSUB/fvar 核验记录；单页也提供可展开的完整 OFL 1.1 文本，并将滑块停靠名写入 `aria-valuetext`。
