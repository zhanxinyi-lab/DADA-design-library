# 命名写法

用户每次怎么说就怎么落到文件名。脚本用 `--template`、`--prefix`、`--name` / `--names`、`--map`。

## 模板 `--template`

图层名填进占位符，路径里的 `/` 会建文件夹。

| 占位符 | 含义 |
|---|---|
| `{name}` | 图层名，斜杠压成 `-` |
| `{path}` | 图层名里的 `/` 当成子文件夹 |
| `{parent}` | 链接那一层的名字 |
| `{index}` | 从 1 开始的序号 |
| `{id}` | 节点 id，冒号改成 `-` |
| `{ext}` | 当前格式 |
| `{scale}` | PNG/JPG 倍率 |

例子：

- `logo/{name}.png` → `logo/主标.png`
- `{parent}/{name}@2x.png` → `Logos/Inverse@2x.png`
- `{path}.png` 且图层叫 `Logo/Primary` → `Logo/Primary.png`

没写扩展名时，按本次格式补上。

## 前缀 `--prefix`

- `Harken_` → `Harken_主标.png`
- `logo/` → `logo/主标.png`（末尾斜杠当文件夹）

## 逐个指定 `--name` / `--names`

按导出顺序对齐，数量必须等于可导出项。对不上就停，不要猜。

```text
--name Harken_Logo_Primary --name Harken_Logo_Inverse
--names "Harken_Logo_Primary|Harken_Logo_Inverse"
```

## 对照表 `--map`

```text
--map 主标=Harken_Logo_Primary --map 组合=Harken_Lockup_Studio
```

先精确匹配图层名，再忽略大小写，再在唯一包含关系时采用。匹配不到的项退回图层名，并在 JSON 的 `naming` 里标 `layer-fallback`。

## 默认

用户没给命名规则时，用消毒后的图层名：`{name}.png`。
Windows 非法字符会替换；重名自动加 `-2`、`-3`。
默认 PNG 2x 只提高像素密度，文件名不加 `@2x`，除非模板里写了。

## 多尺寸 `--sizes`

传了 `--sizes 1024,512,256` 时，脚本按每个尺寸各写一份 PNG。若文件名（或模板结果）末尾已有尺寸数字，换成当前尺寸；没有就补上：

- `Hub/Hub light 1024.png` → `Hub/Hub light 1024.png`、`Hub/Hub light 512.png`
- `Hub light.png` → `Hub light 1024.png`、`Hub light 512.png`

不传 `--sizes` 时文件名逻辑不变。
