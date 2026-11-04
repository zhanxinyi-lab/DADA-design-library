# Design Skills

设计工作流 Skill 的统一存放目录。每个 Skill 使用一个独立文件夹，名称采用小写英文单词和连字符，并与 SKILL.md 中的 name 一致。后续 Skill 按同样方式加入本目录。

| Skill | 用途 |
| --- | --- |
| [social-aurora-sizes](social-aurora-sizes/SKILL.md) | 将分层 SVG 导出为微信、X 的五种尺寸，包含 JPG、SVG、预览及尺寸报告 |

## 使用

下载所需 Skill 的完整目录（不要只下载 SKILL.md），放到支持的 Agent 技能目录中。在 Cindy 本地可使用用户级 ~/.agents/skills/ 或项目级 .agents/skills/，新建或重启会话后加载。仓库收录不等于自动安装或发布到 SkillHub。

社媒导出 Skill 需要 Python 3.9+。按需在自己的 Python 环境安装其 requirements.txt 中的依赖，然后提供背景与字标分层、图片内嵌、文字已转曲的完整 SVG。复杂 SVG 可能需要先整理背景图层；详细限制及用法见各 Skill 的 SKILL.md。

只收录说明、必要脚本和依赖清单；不提交个人路径、凭据、临时测试输出或未经许可的素材。
