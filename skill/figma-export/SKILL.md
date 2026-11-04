---
name: figma-export
description: >
  Export each item inside a Figma node link into a local folder using the
  user's naming scheme. 中文触发词：figma导出。Use when the user says
  figma导出, pastes a figma.com design or file URL, or asks to export Figma
  nodes into named folders. Do not use for renaming layers inside a web-UI
  repo, writing a Figma plugin, or screenshot visual QA.
---

# figma导出

中文触发词：`figma导出`。用户给 Figma 链接和命名方式时，导出**链接那一层里面的每一项**（不是整块一张图），按命名写入文件夹。默认 **PNG、2x、透明底**。用户口头改格式时才加 SVG/PDF 或改倍率。

不要手写 curl 或把 token 打进对话。用本 Skill 的脚本。

## 先凑齐输入

1. Figma 链接，必须带 `node-id`（在文件里选中那一块 → Copy link）。
2. 命名方式：模板、前缀、逐个文件名、图层对照表都可以。细节见 [references/naming.md](references/naming.md)。
3. 输出目录：用户指定就用指定的；没有就用当前工作目录下 `exports/<那一层的名字>/`。

链接指向的应是「装着要导出各项」的父级（画板、section、组件集）。脚本会：

- 导出直接子项里的 Frame / Component / Instance
- 展开 Component set 的变体、Section 里的帧
- 跳过隐藏图层，以及名字以 `_` 或 `.` 开头的图层
- 只有找不到可分项时，才退回导出链接节点自己
- 若链接是一整页、真正要导出的是里面的组合标，用 `--id` 指定节点（可重复），并与 `--name` 对齐；`--self` 则只导出链接节点本身

## Token

读 `FIGMA_TOKEN` 或 `FIGMA_ACCESS_TOKEN`，或从当前目录往上找 `.env`。不要打印、引用、提交 token。

没有 token 时停下，让用户自己去 Figma → Settings → Security → Personal access tokens 建一个**只读** token（File content + File metadata），写进环境变量或项目 `.env`。不要让用户把 token 粘贴到聊天里。

## 运行

Windows：

```text
py -3 "%USERPROFILE%\.agents\skills\figma-export\scripts\export.py" --url "FIGMA_URL" --out "输出目录" [命名参数]
```

macOS / Linux：

```text
python3 ~/.agents/skills/figma-export/scripts/export.py --url "FIGMA_URL" --out "输出目录" [命名参数]
```

命名参数三选一或组合（以脚本为准）：

- `--template "logo/{name}.png"`
- `--prefix "Harken_"`
- `--name 文件名` 可重复，或 `--names "a|b"`
- `--map 图层名=文件名` 可重复

其它常用参数：`--format png`（或 `png,svg`）、`--scale 2`、`--sizes 1024,512,256,128,64`、`--dry-run`。

逐个指定文件名时，若条数和可导出项不一致，脚本会失败并列出图层名。先改命名或换链接，不要凑合导出。

不确定会导出哪些图层时，先 `--dry-run`，看 JSON 里的 `items`，再去掉该参数真正下载。

## 多尺寸（避免小稿虚边）

不要在 Figma 里复制 1024 / 512 / 256 / 128 / 64 再逐个对齐。半像素边缘会虚；Figma REST 也不能帮你把图层吸到整像素。默认导出不变：不传 `--sizes` 时仍是 **PNG 2x 直接下载**。

App icon 这类需求：只链（或 `--id`）对齐好的 **最大稿**，然后：

```text
--sizes 1024,512,256,128,64
```

- 不传 `--scale` 时自动用 `1`（像素对齐画板）
- 每个节点只向 Figma 要一次 PNG，再用 Pillow 整数缩到其余尺寸
- 文件名末尾的尺寸数字会被替换：`Hub light 1024.png` → `Hub light 512.png`
- `--sizes` 的最大值应等于主稿画板边长，不要用小稿生成更大的图

JSON 若带 `pixelRisks`，说明主稿里仍有非整数 `absoluteBoundingBox`。最大尺寸本身也可能虚，需要在 Figma 里把 **最大稿** 对齐到整像素；其余尺寸交给脚本。

## 回报

成功后告诉用户输出目录和文件清单。有失败项就原样转述脚本 JSON 里的 `errors`，不要假装全部成功。

导出结果只落在用户指定或 `exports/` 下。不要提交这些图片，除非用户明确要求。
