#!/usr/bin/env python3
"""Export each item inside a Figma node link into a local folder."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.figma.com/v1"
USER_AGENT = "figma-export-skill/1.0"
IMAGE_BATCH = 40
MAX_SEGMENT = 80
GENERIC_PRIMITIVE = re.compile(
    r"^(Vector|Ellipse|Rectangle|Polygon|Star|Line|Boolean|Group|Text)(?:\s+\d+)?$",
    re.I,
)
UNWRAP_TYPES = {"CANVAS", "SECTION", "COMPONENT_SET"}
ALWAYS_ITEMS = {"FRAME", "COMPONENT", "INSTANCE", "SLICE"}
MAYBE_ITEMS = {
    "GROUP",
    "VECTOR",
    "BOOLEAN_OPERATION",
    "STAR",
    "LINE",
    "ELLIPSE",
    "REGULAR_POLYGON",
    "RECTANGLE",
    "TEXT",
}
WIN_ILLEGAL = re.compile(r'[<>:"|?*\x00-\x1f]')
URL_RE = re.compile(
    r"https?://(?:www\.)?figma\.com/(?:design|file|proto|board|deck)/([A-Za-z0-9]+)"
)


def fail(message, extra=None, code=1):
    payload = {"ok": False, "error": message}
    if extra:
        payload.update(extra)
    emit(payload)
    return code


def emit(payload):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def parse_figma_url(url):
    raw = (url or "").strip()
    match = URL_RE.search(raw)
    if not match:
        raise ValueError("不是可识别的 Figma 链接。需要 figma.com/design 或 /file 链接，并带 node-id。")
    file_key = match.group(1)
    parsed = urllib.parse.urlparse(raw)
    query = urllib.parse.parse_qs(parsed.query)
    node_raw = (query.get("node-id") or query.get("node_id") or [""])[0]
    node_id = normalize_node_id(node_raw)
    return file_key, node_id


def normalize_node_id(value):
    text = urllib.parse.unquote(value or "").strip()
    if not text:
        return ""
    return text.replace("-", ":")


def read_token(start_dir):
    for key in ("FIGMA_TOKEN", "FIGMA_ACCESS_TOKEN"):
        value = (os.environ.get(key) or "").strip()
        if value:
            return value
    directory = Path(start_dir).resolve()
    for _ in range(8):
        env_path = directory / ".env"
        if env_path.is_file():
            token = token_from_env_file(env_path)
            if token:
                return token
        parent = directory.parent
        if parent == directory:
            break
        directory = parent
    return ""


def token_from_env_file(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"^\s*(?:FIGMA_TOKEN|FIGMA_ACCESS_TOKEN)\s*=\s*(.+?)\s*$",
        text,
        re.M,
    )
    if not match:
        return ""
    value = match.group(1).strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        value = value[1:-1]
    return value.strip()


def iter_visible(node):
    for child in node.get("children") or []:
        if child.get("visible") is False:
            continue
        name = (child.get("name") or "").strip()
        if name.startswith(".") or name.startswith("_"):
            continue
        yield child


def expand_unwrap(node):
    node_type = node.get("type")
    if node_type in UNWRAP_TYPES:
        out = []
        for child in iter_visible(node):
            if child.get("type") in UNWRAP_TYPES:
                out.extend(expand_unwrap(child))
            else:
                out.append(child)
        return out
    out = []
    for child in iter_visible(node):
        if child.get("type") in UNWRAP_TYPES:
            out.extend(expand_unwrap(child))
        else:
            out.append(child)
    return out


def is_export_item(node):
    node_type = node.get("type")
    if node_type in ALWAYS_ITEMS:
        return True
    if node_type in MAYBE_ITEMS:
        return not GENERIC_PRIMITIVE.match((node.get("name") or "").strip())
    return False


def collect_items(root):
    pool = expand_unwrap(root)
    items = [node for node in pool if is_export_item(node)]
    if items:
        return items
    if root.get("type") not in {"DOCUMENT", "CANVAS"}:
        return [root]
    return []


def sanitize_segment(value, fallback="item"):
    text = (value or "").strip()
    text = text.replace("\\", "-").replace("/", "-")
    text = WIN_ILLEGAL.sub("-", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    text = text.replace("..", ".")
    if not text:
        text = fallback
    lowered = text.rstrip(".").upper()
    if lowered in {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "LPT1",
        "LPT2",
        "LPT3",
    }:
        text = f"{text}_"
    return text[:MAX_SEGMENT]


def flatten_name(value, fallback="item"):
    text = re.sub(r"[\\/]+", "-", value or "")
    text = re.sub(r"-{2,}", "-", text)
    return sanitize_segment(text, fallback=fallback)


def path_from_layer(value, fallback="item"):
    parts = [part for part in re.split(r"[\\/]+", value or "") if part.strip()]
    if not parts:
        return Path(fallback)
    return Path(*(sanitize_segment(part, fallback=fallback) for part in parts))


def split_ext(path_str):
    path = Path(path_str)
    suffix = path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".svg", ".pdf", ".webp"}:
        return path.with_suffix(""), suffix.lstrip(".")
    return path, ""


def render_template(template, item, index, parent_name, fmt, scale):
    node_id = item.get("id") or ""
    layer = item.get("name") or ""
    values = {
        "name": flatten_name(layer, fallback=f"node-{node_id.replace(':', '-')}"),
        "parent": flatten_name(parent_name, fallback="export"),
        "index": str(index),
        "id": node_id.replace(":", "-"),
        "ext": fmt,
        "scale": str(scale).rstrip("0").rstrip(".") if isinstance(scale, float) else str(scale),
    }
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{" + key + "}", value)
    if "{path}" in template:
        rendered = rendered.replace(
            "{path}",
            str(path_from_layer(layer, fallback=values["name"])).replace("\\", "/"),
        )
    return rendered


def apply_naming(item, index, parent_name, fmt, scale, template, prefix, names, mapping):
    node_id = item.get("id") or ""
    layer = item.get("name") or ""
    fallback = flatten_name(layer, fallback=f"node-{node_id.replace(':', '-')}")
    chosen = None
    source = "layer"

    if names:
        if index <= len(names):
            chosen = names[index - 1].strip()
            source = "names"
        else:
            chosen = fallback
            source = "layer-fallback"
    elif mapping:
        matched = match_mapping(layer, mapping)
        if matched:
            chosen = matched
            source = "map"
        else:
            chosen = fallback
            source = "layer-fallback"
    elif template:
        chosen = render_template(template, item, index, parent_name, fmt, scale)
        source = "template"
    elif prefix:
        chosen = str(Path(prefix) / fallback) if prefix.endswith(("/", "\\")) else f"{prefix}{fallback}"
        source = "prefix"
    else:
        chosen = fallback

    stem_path, _ext_in_name = split_ext(chosen)
    if template and "{ext}" in template:
        rel = Path(chosen)
    else:
        rel = Path(str(stem_path) + "." + fmt)

    parts = [sanitize_segment(part) for part in rel.parts[:-1]]
    filename = sanitize_segment(rel.name, fallback=f"{fallback}.{fmt}")
    rel = Path(*parts, filename) if parts else Path(filename)
    return rel, source


def match_mapping(layer, mapping):
    if layer in mapping:
        return mapping[layer]
    folded = {key.casefold(): value for key, value in mapping.items()}
    if layer.casefold() in folded:
        return folded[layer.casefold()]
    hits = [value for key, value in mapping.items() if key and key in layer]
    if len(hits) == 1:
        return hits[0]
    return ""


def uniquify(rel_path, used):
    key = str(rel_path).replace("\\", "/").casefold()
    if key not in used:
        used.add(key)
        return rel_path
    stem, ext = rel_path.stem, rel_path.suffix
    n = 2
    while True:
        candidate = rel_path.with_name(f"{stem}-{n}{ext}")
        key = str(candidate).replace("\\", "/").casefold()
        if key not in used:
            used.add(key)
            return candidate
        n += 1


def parse_sizes(value):
    if not value:
        return []
    sizes = []
    for part in value.split(","):
        part = part.strip().lower().replace("px", "")
        if not part:
            continue
        if not part.isdigit():
            raise ValueError(f"--sizes 必须是正整数像素，收到：{part}")
        number = int(part)
        if number <= 0 or number > 8192:
            raise ValueError(f"--sizes 超出范围：{number}")
        if number not in sizes:
            sizes.append(number)
    sizes.sort(reverse=True)
    return sizes


def path_with_size(rel, size, fmt=None):
    rel = Path(rel)
    stem = re.sub(r"\s+\d+$", "", rel.stem).rstrip() or rel.stem
    ext = fmt or (rel.suffix.lstrip(".") if rel.suffix else "png")
    name = f"{stem} {size}.{ext}"
    return rel.with_name(name) if rel.parent != Path(".") else Path(name)


def is_non_integer(value, eps=0.02):
    if value is None:
        return False
    number = float(value)
    return abs(number - round(number)) > eps


def index_nodes(node, acc=None):
    acc = {} if acc is None else acc
    node_id = node.get("id")
    if node_id:
        acc[node_id] = node
    for child in node.get("children") or []:
        index_nodes(child, acc)
    return acc


def pixel_risks_for(node, limit=12):
    risks = []

    def walk(current):
        if len(risks) >= limit:
            return
        box = current.get("absoluteBoundingBox") or {}
        bad = [key for key in ("x", "y", "width", "height") if is_non_integer(box.get(key))]
        if bad:
            risks.append(
                {
                    "id": current.get("id"),
                    "name": current.get("name") or "",
                    "type": current.get("type") or "",
                    "fields": bad,
                    "box": {
                        key: box.get(key)
                        for key in ("x", "y", "width", "height")
                        if box.get(key) is not None
                    },
                }
            )
        for child in current.get("children") or []:
            walk(child)

    if node:
        walk(node)
    return risks


def collect_pixel_risks(root, items):
    tree = index_nodes(root)
    risks = []
    seen = set()
    for item in items:
        node = tree.get(item.get("id"))
        if node is None and root.get("id") == item.get("id"):
            node = root
        for risk in pixel_risks_for(node):
            if risk["id"] in seen:
                continue
            seen.add(risk["id"])
            risks.append(risk)
            if len(risks) >= 40:
                return risks
    return risks


def expand_size_plan(planned, sizes):
    if not sizes:
        return planned
    used = set()
    expanded = []
    for item in planned:
        if item.get("format") != "png":
            rel = uniquify(Path(item["path"]), used)
            expanded.append({**item, "path": str(rel).replace("\\", "/")})
            continue
        for size in sizes:
            rel = uniquify(path_with_size(item["path"], size, "png"), used)
            expanded.append(
                {
                    **item,
                    "path": str(rel).replace("\\", "/"),
                    "outSize": size,
                }
            )
    return expanded


def sample_pad_rgba(image):
    pixel = image.getpixel((0, 0))
    if image.mode == "RGBA":
        return pixel
    if image.mode == "RGB":
        return pixel + (255,)
    converted = image.convert("RGBA")
    return converted.getpixel((0, 0))


def fit_square_png(png_bytes, target):
    from io import BytesIO

    from PIL import Image

    image = Image.open(BytesIO(png_bytes)).convert("RGBA")
    width, height = image.size
    if width == target and height == target:
        return image
    if width > target or height > target:
        image.thumbnail((target, target), Image.Resampling.LANCZOS)
        width, height = image.size
        if width == target and height == target:
            return image
    canvas = Image.new("RGBA", (target, target), sample_pad_rgba(image))
    canvas.paste(image, ((target - width) // 2, (target - height) // 2), image)
    return canvas


def raster_size_variants(png_bytes, sizes):
    from io import BytesIO

    from PIL import Image

    if not sizes:
        return []
    master_size = max(sizes)
    master = fit_square_png(png_bytes, master_size)
    variants = []
    for size in sizes:
        frame = master if size == master_size else master.resize(
            (size, size), Image.Resampling.LANCZOS
        )
        buffer = BytesIO()
        frame.save(buffer, format="PNG")
        variants.append((size, buffer.getvalue()))
    return variants


def fetch_bytes(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read()


def atomic_write(dest, data):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp")
    try:
        tmp.write_bytes(data)
        tmp.replace(dest)
    except Exception:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    return len(data)


def parse_names(names_arg, name_args):
    values = []
    if name_args:
        values.extend(item.strip() for item in name_args if item and item.strip())
    if names_arg:
        splitter = "|" if "|" in names_arg else ","
        values.extend(part.strip() for part in names_arg.split(splitter) if part.strip())
    return values


def parse_mapping(map_args):
    mapping = {}
    for raw in map_args or []:
        if "=" not in raw:
            raise ValueError(f"--map 需要 layer=filename，收到：{raw}")
        key, value = raw.split("=", 1)
        key, value = key.strip(), value.strip()
        if not key or not value:
            raise ValueError(f"--map 需要 layer=filename，收到：{raw}")
        mapping[key] = value
    return mapping


def parse_formats(value):
    formats = []
    for part in (value or "png").split(","):
        fmt = part.strip().lower()
        if fmt == "jpeg":
            fmt = "jpg"
        if fmt not in {"png", "jpg", "svg", "pdf"}:
            raise ValueError(f"不支持的格式：{part}")
        if fmt not in formats:
            formats.append(fmt)
    return formats or ["png"]


def figma_request(url, token, timeout=60):
    req = urllib.request.Request(
        url,
        headers={
            "X-Figma-Token": token,
            "User-Agent": USER_AGENT,
        },
    )
    last_error = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as res:
                body = res.read()
                return res.status, body
        except urllib.error.HTTPError as err:
            body = err.read() if err.fp else b""
            if err.code == 429 or err.code >= 500:
                wait = 1.5 * (attempt + 1)
                retry_after = err.headers.get("Retry-After") if err.headers else None
                if retry_after:
                    try:
                        wait = max(wait, float(retry_after))
                    except ValueError:
                        pass
                last_error = err
                time.sleep(wait)
                continue
            return err.code, body
        except urllib.error.URLError as err:
            last_error = err
            time.sleep(1.5 * (attempt + 1))
    if last_error:
        raise last_error
    raise RuntimeError("Figma 请求失败")


def figma_json(path, token, query=None):
    url = API + path
    if query:
        url += "?" + urllib.parse.urlencode(query, safe=":,")
    status, body = figma_request(url, token)
    try:
        data = json.loads(body.decode("utf-8"))
    except ValueError as err:
        raise RuntimeError(f"Figma 返回非 JSON（HTTP {status}）") from err
    if status >= 400 or (isinstance(data.get("status"), int) and data["status"] >= 400):
        message = data.get("err") or data.get("message") or body.decode("utf-8", "replace")[:300]
        raise RuntimeError(f"Figma API HTTP {status}：{message}")
    return data


def fetch_node(file_key, node_id, token):
    if node_id:
        data = figma_json(f"/files/{file_key}/nodes", token, {"ids": node_id})
        entry = (data.get("nodes") or {}).get(node_id)
        if not entry or not entry.get("document"):
            raise RuntimeError(f"找不到 node-id {node_id}。确认链接指向的图层仍在文件里，且 token 有权读这个文件。")
        return {
            "fileName": data.get("name") or "",
            "lastModified": data.get("lastModified") or "",
            "version": data.get("version") or "",
            "document": entry["document"],
        }
    data = figma_json(f"/files/{file_key}", token, {"depth": "2"})
    pages = data.get("document", {}).get("children") or []
    raise RuntimeError(
        "链接没有 node-id。请在 Figma 里选中要导出的那一块，右键 Copy link。文件里的页面："
        + "；".join(f"{page.get('name')} ({page.get('id')})" for page in pages[:20])
    )


def fetch_images(file_key, ids, token, fmt, scale):
    urls = {}
    for start in range(0, len(ids), IMAGE_BATCH):
        chunk = ids[start : start + IMAGE_BATCH]
        query = {"ids": ",".join(chunk), "format": fmt}
        if fmt in {"png", "jpg"}:
            query["scale"] = str(scale)
        data = figma_json(f"/images/{file_key}", token, query)
        if data.get("err"):
            raise RuntimeError(f"Figma 出图失败：{data['err']}")
        urls.update(data.get("images") or {})
    return urls


def download(url, dest, timeout=90):
    return atomic_write(dest, fetch_bytes(url, timeout=timeout))


def plan_exports(root, formats, scale, template, prefix, names, mapping, items=None):
    if items is None:
        items = collect_items(root)
    parent_name = root.get("name") or "export"
    used = set()
    planned = []
    for index, item in enumerate(items, start=1):
        for fmt in formats:
            rel, source = apply_naming(
                item,
                index,
                parent_name,
                fmt,
                scale,
                template,
                prefix,
                names,
                mapping,
            )
            rel = uniquify(rel, used)
            planned.append(
                {
                    "id": item.get("id"),
                    "layerName": item.get("name") or "",
                    "type": item.get("type") or "",
                    "path": str(rel).replace("\\", "/"),
                    "format": fmt,
                    "scale": scale if fmt in {"png", "jpg"} else None,
                    "naming": source,
                }
            )
    return items, planned


def build_parser():
    parser = argparse.ArgumentParser(description="Export Figma node children into a folder")
    parser.add_argument("--url", help="Figma design/file link with node-id")
    parser.add_argument("--file-key", dest="file_key")
    parser.add_argument("--node-id", dest="node_id")
    parser.add_argument("--out", help="Output folder. Default: exports/<node-name>")
    parser.add_argument("--format", default="png", help="png, svg, pdf, or comma list. Default png")
    parser.add_argument(
        "--scale",
        type=float,
        default=None,
        help="PNG/JPG scale. Default 2, or 1 when --sizes is set",
    )
    parser.add_argument(
        "--sizes",
        help="e.g. 1024,512,256,128,64. Fetch the largest PNG once, then integer-resize. Off by default.",
    )
    parser.add_argument("--template", help="e.g. logo/{name}@2x.png")
    parser.add_argument("--prefix", help="e.g. Harken_  or logo/")
    parser.add_argument("--names", help="Ordered names, split by | or comma")
    parser.add_argument("--name", action="append", dest="name_args", help="Repeatable ordered filename")
    parser.add_argument("--map", action="append", dest="map_args", help="layer=filename, repeatable")
    parser.add_argument(
        "--id",
        action="append",
        dest="export_ids",
        help="Export these node ids as-is (repeatable). Skips child picking.",
    )
    parser.add_argument(
        "--self",
        action="store_true",
        help="Export the linked node itself, not its children",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        formats = parse_formats(args.format)
        names = parse_names(args.names, args.name_args)
        mapping = parse_mapping(args.map_args)
        sizes = parse_sizes(args.sizes)
        if args.url:
            file_key, node_id = parse_figma_url(args.url)
        else:
            file_key, node_id = args.file_key or "", normalize_node_id(args.node_id or "")
        if not file_key:
            return fail("需要 --url，或同时提供 --file-key 和 --node-id。")
    except ValueError as err:
        return fail(str(err))

    scale = args.scale if args.scale is not None else (1.0 if sizes else 2.0)
    if scale <= 0 or scale > 4:
        return fail("--scale 必须在 0 到 4 之间（Figma PNG/JPG 限制）。")
    args.scale = scale

    token = read_token(Path.cwd())
    if not token:
        return fail(
            "找不到 FIGMA_TOKEN。在系统环境变量或当前项目 .env 里设置 FIGMA_TOKEN=figd_...；"
            "不要把 token 发到对话里。Figma → Settings → Security → Personal access tokens，"
            "权限只要 File content 和 File metadata 的读权限。",
            extra={"hint": "https://help.figma.com/hc/en-us/articles/8085703771159"},
            code=3,
        )

    try:
        meta = fetch_node(file_key, node_id, token)
    except RuntimeError as err:
        return fail(str(err), extra={"fileKey": file_key, "nodeId": node_id})

    root = meta["document"]
    if args.export_ids:
        export_ids = [normalize_node_id(item_id) for item_id in args.export_ids]
        if names and len(names) != len(export_ids):
            return fail(
                f"命名数量是 {len(names)}，--id 数量是 {len(export_ids)}，对不上。",
                extra={"ids": export_ids, "names": names},
            )
        items = [
            {
                "id": item_id,
                "name": names[index] if names else item_id,
                "type": "EXPLICIT",
            }
            for index, item_id in enumerate(export_ids)
        ]
    elif args.self:
        items = [root]
    else:
        items = None
    items, planned = plan_exports(
        root,
        formats,
        args.scale,
        args.template,
        args.prefix,
        names,
        mapping,
        items=items,
    )
    planned = expand_size_plan(planned, sizes)
    if names and len(names) != len(items):
        return fail(
            f"命名数量是 {len(names)}，可导出项是 {len(items)}，对不上。先核对图层，或改用模板/前缀。",
            extra={
                "fileKey": file_key,
                "source": {"id": root.get("id"), "name": root.get("name"), "type": root.get("type")},
                "layerNames": [item.get("name") for item in items],
                "names": names,
            },
        )
    if not planned:
        return fail(
            "这个节点下面没有可分开导出的项。选中包含各帧/组件的那一层再 Copy link。",
            extra={"source": {"id": root.get("id"), "name": root.get("name"), "type": root.get("type")}},
        )

    parent_name = flatten_name(root.get("name") or "export")
    out_dir = Path(args.out).expanduser() if args.out else Path("exports") / parent_name
    if not out_dir.is_absolute():
        out_dir = Path.cwd() / out_dir

    result = {
        "ok": True,
        "dryRun": bool(args.dry_run),
        "fileKey": file_key,
        "fileName": meta.get("fileName") or "",
        "version": meta.get("version") or "",
        "source": {
            "id": root.get("id"),
            "name": root.get("name"),
            "type": root.get("type"),
        },
        "outDir": str(out_dir),
        "format": formats,
        "scale": args.scale,
        "count": len(items),
        "items": planned,
    }
    if sizes:
        result["sizes"] = sizes
    pixel_risks = collect_pixel_risks(root, items)
    if pixel_risks:
        result["pixelRisks"] = pixel_risks
    if args.dry_run:
        emit(result)
        return 0

    if sizes and "png" in formats:
        try:
            from PIL import Image  # noqa: F401
        except ImportError:
            return fail(
                "多尺寸导出需要 Pillow。安装：py -3 -m pip install Pillow",
                extra=result,
                code=4,
            )

    id_list = []
    seen = set()
    for item in planned:
        if item["id"] not in seen:
            seen.add(item["id"])
            id_list.append(item["id"])

    written = []
    errors = []
    missing_url = "Figma 没有返回这张图的地址（图层可能太大、空，或当前格式导不出）"
    for fmt in formats:
        try:
            urls = fetch_images(file_key, id_list, token, fmt, args.scale)
        except RuntimeError as err:
            return fail(str(err), extra=result)
        rasters = {}
        for item in planned:
            if item["format"] != fmt:
                continue
            dest = out_dir / item["path"]
            url = urls.get(item["id"])
            if sizes and fmt == "png":
                node_id = item["id"]
                if node_id not in rasters:
                    if not url:
                        rasters[node_id] = None
                    else:
                        try:
                            rasters[node_id] = dict(
                                raster_size_variants(fetch_bytes(url), sizes)
                            )
                        except Exception as err:
                            rasters[node_id] = err
                payload = rasters[node_id]
                if payload is None:
                    errors.append({"id": node_id, "path": item["path"], "error": missing_url})
                    continue
                if isinstance(payload, Exception):
                    errors.append({"id": node_id, "path": item["path"], "error": str(payload)})
                    continue
                data = payload.get(item.get("outSize"))
                if not data:
                    errors.append(
                        {
                            "id": node_id,
                            "path": item["path"],
                            "error": f"没有生成 {item.get('outSize')}px",
                        }
                    )
                    continue
                try:
                    nbytes = atomic_write(dest, data)
                except Exception as err:
                    errors.append({"id": node_id, "path": item["path"], "error": str(err)})
                    continue
                written.append({**item, "bytes": nbytes, "absPath": str(dest)})
                continue
            if not url:
                errors.append({"id": item["id"], "path": item["path"], "error": missing_url})
                continue
            try:
                nbytes = download(url, dest)
            except Exception as err:
                errors.append({"id": item["id"], "path": item["path"], "error": str(err)})
                continue
            written.append({**item, "bytes": nbytes, "absPath": str(dest)})

    result["ok"] = not errors
    result["written"] = written
    if errors:
        result["errors"] = errors
        result["error"] = f"{len(errors)} 个文件导出失败，{len(written)} 个成功。"
        emit(result)
        return 1
    emit(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
