#!/usr/bin/env python3
import unittest
from pathlib import Path

import export


def frame(node_id, name, children=None, node_type="FRAME", visible=True):
    node = {"id": node_id, "name": name, "type": node_type}
    if visible is False:
        node["visible"] = False
    if children is not None:
        node["children"] = children
    return node


class ParseUrlTests(unittest.TestCase):
    def test_design_link(self):
        key, node = export.parse_figma_url(
            "https://www.figma.com/design/AbC123xyz/Harken-Logo?node-id=12-34&m=dev"
        )
        self.assertEqual(key, "AbC123xyz")
        self.assertEqual(node, "12:34")

    def test_encoded_colon(self):
        key, node = export.parse_figma_url(
            "https://figma.com/file/AbC123xyz/Name?node-id=12%3A34"
        )
        self.assertEqual(key, "AbC123xyz")
        self.assertEqual(node, "12:34")

    def test_rejects_non_figma(self):
        with self.assertRaises(ValueError):
            export.parse_figma_url("https://xd.feishu.cn/wiki/abc")


class CollectItemsTests(unittest.TestCase):
    def test_direct_frames_skip_hidden_and_generic_vector(self):
        root = frame(
            "1:1",
            "Logos",
            [
                frame("1:2", "Primary"),
                frame("1:3", "Inverse"),
                frame("1:4", "_notes"),
                frame("1:5", ".guide"),
                frame("1:6", "hidden", visible=False),
                frame("1:7", "Vector", node_type="VECTOR"),
            ],
        )
        names = [item["name"] for item in export.collect_items(root)]
        self.assertEqual(names, ["Primary", "Inverse"])

    def test_component_set_unwraps_variants(self):
        root = frame(
            "2:1",
            "Icon",
            [
                frame("2:2", "Size=S", node_type="COMPONENT"),
                frame("2:3", "Size=M", node_type="COMPONENT"),
            ],
            node_type="COMPONENT_SET",
        )
        names = [item["name"] for item in export.collect_items(root)]
        self.assertEqual(names, ["Size=S", "Size=M"])

    def test_named_vectors_are_items(self):
        root = frame(
            "4:1",
            "Icons",
            [
                frame("4:2", "home", node_type="VECTOR"),
                frame("4:3", "search", node_type="BOOLEAN_OPERATION"),
            ],
        )
        names = [item["name"] for item in export.collect_items(root)]
        self.assertEqual(names, ["home", "search"])

    def test_single_mark_falls_back_to_itself(self):
        root = frame(
            "3:1",
            "Mark",
            [frame("3:2", "Vector", node_type="VECTOR")],
            node_type="COMPONENT",
        )
        items = export.collect_items(root)
        self.assertEqual([item["name"] for item in items], ["Mark"])

    def test_section_on_page_exports_frames(self):
        root = frame(
            "0:1",
            "Page 1",
            [
                frame(
                    "5:1",
                    "Logo pack",
                    [
                        frame("5:2", "Primary"),
                        frame("5:3", "Inverse"),
                    ],
                    node_type="SECTION",
                )
            ],
            node_type="CANVAS",
        )
        names = [item["name"] for item in export.collect_items(root)]
        self.assertEqual(names, ["Primary", "Inverse"])


class NamingTests(unittest.TestCase):
    def test_template_flattens_slash(self):
        item = frame("1:2", "主标 / Primary")
        rel, source = export.apply_naming(
            item, 1, "Logos", "png", 2, "logo/{name}@2x.png", None, None, None
        )
        self.assertEqual(source, "template")
        self.assertEqual(rel.as_posix(), "logo/主标 - Primary@2x.png")

    def test_prefix_and_explicit_names(self):
        item = frame("1:2", "主标")
        rel, source = export.apply_naming(item, 1, "Logos", "png", 2, None, "Harken_", None, None)
        self.assertEqual(source, "prefix")
        self.assertEqual(rel.as_posix(), "Harken_主标.png")

        rel, source = export.apply_naming(
            item, 1, "Logos", "png", 2, None, None, ["Harken_Logo_Primary"], None
        )
        self.assertEqual(source, "names")
        self.assertEqual(rel.as_posix(), "Harken_Logo_Primary.png")

    def test_template_png_suffix_follows_format(self):
        item = frame("1:2", "主标")
        rel, _source = export.apply_naming(
            item, 1, "Logos", "svg", 2, "logo/{name}.png", None, None, None
        )
        self.assertEqual(rel.as_posix(), "logo/主标.svg")

    def test_map_matches_layer(self):
        item = frame("1:2", "主标")
        rel, source = export.apply_naming(
            item, 1, "Logos", "png", 2, None, None, None, {"主标": "Harken_Logo_Primary"}
        )
        self.assertEqual(source, "map")
        self.assertEqual(rel.as_posix(), "Harken_Logo_Primary.png")

    def test_uniquify_collisions(self):
        used = set()
        first = export.uniquify(Path("a.png"), used)
        second = export.uniquify(Path("a.png"), used)
        self.assertEqual(first.as_posix(), "a.png")
        self.assertEqual(second.as_posix(), "a-2.png")


class SizeExportTests(unittest.TestCase):
    def test_parse_sizes(self):
        self.assertEqual(export.parse_sizes(""), [])
        self.assertEqual(export.parse_sizes(None), [])
        self.assertEqual(
            export.parse_sizes("1024,512,256,128,64"),
            [1024, 512, 256, 128, 64],
        )
        self.assertEqual(export.parse_sizes("64, 128px, 64"), [128, 64])
        with self.assertRaises(ValueError):
            export.parse_sizes("1024,foo")
        with self.assertRaises(ValueError):
            export.parse_sizes("0")

    def test_path_with_size_replaces_trailing_number(self):
        self.assertEqual(
            export.path_with_size("Hub/Hub light 1024.png", 512).as_posix(),
            "Hub/Hub light 512.png",
        )
        self.assertEqual(
            export.path_with_size("Hub light.png", 64).as_posix(),
            "Hub light 64.png",
        )
        self.assertEqual(
            export.path_with_size(Path("Search/Search dark 1024.png"), 256).as_posix(),
            "Search/Search dark 256.png",
        )

    def test_pixel_risks_non_integer_box(self):
        inner = frame("1:2", "inner", node_type="RECTANGLE")
        inner["absoluteBoundingBox"] = {
            "x": 1.3,
            "y": 0,
            "width": 1022.7,
            "height": 1024,
        }
        node = frame("1:1", "icon", [inner])
        node["absoluteBoundingBox"] = {"x": 0, "y": 0, "width": 1024, "height": 1024}
        risks = export.pixel_risks_for(node)
        self.assertTrue(any(risk["id"] == "1:2" for risk in risks))
        self.assertFalse(any(risk["id"] == "1:1" for risk in risks))
        self.assertIn("width", risks[0]["fields"])

    def test_expand_size_plan_png_only(self):
        planned = [
            {"id": "1:1", "path": "Hub/Hub light 1024.png", "format": "png"},
            {"id": "1:1", "path": "Hub/Hub light.svg", "format": "svg"},
        ]
        out = export.expand_size_plan(planned, [1024, 512])
        self.assertEqual(
            [item["path"] for item in out],
            ["Hub/Hub light 1024.png", "Hub/Hub light 512.png", "Hub/Hub light.svg"],
        )
        self.assertEqual([item.get("outSize") for item in out], [1024, 512, None])

    def test_raster_size_variants_square(self):
        from io import BytesIO

        from PIL import Image

        source = Image.new("RGBA", (64, 64), (12, 34, 56, 255))
        buffer = BytesIO()
        source.save(buffer, format="PNG")
        variants = dict(export.raster_size_variants(buffer.getvalue(), [64, 32, 16]))
        for size in (64, 32, 16):
            image = Image.open(BytesIO(variants[size]))
            self.assertEqual(image.size, (size, size))

    def test_fit_square_png_pads_short_side(self):
        from io import BytesIO

        from PIL import Image

        source = Image.new("RGBA", (60, 64), (9, 9, 9, 255))
        buffer = BytesIO()
        source.save(buffer, format="PNG")
        fitted = export.fit_square_png(buffer.getvalue(), 64)
        self.assertEqual(fitted.size, (64, 64))

    def test_scale_stays_unset_without_sizes(self):
        args = export.build_parser().parse_args(
            ["--url", "https://www.figma.com/design/Abc123xyz/Name?node-id=1-2"]
        )
        self.assertIsNone(args.scale)
        self.assertIsNone(args.sizes)


if __name__ == "__main__":
    unittest.main()
