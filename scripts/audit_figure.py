#!/usr/bin/env python3
"""Audit basic properties of exported publication figures.

The checks cover file integrity, page count, physical dimensions, and obvious
font or rasterization risks. They do not establish statistical correctness or
visual legibility, so the final exported figure still needs inspection.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def _result(level: str, message: str) -> dict[str, str]:
    return {"level": level, "message": message}


def audit_pdf(path: Path) -> list[dict[str, str]]:
    data = path.read_bytes()
    results: list[dict[str, str]] = []

    if not data.startswith(b"%PDF-"):
        return [_result("error", "Missing PDF header")]

    page_count = len(re.findall(rb"/Type\s*/Page\b", data))
    font_count = len(re.findall(rb"/Type\s*/Font\b", data))
    embedded_count = len(re.findall(rb"/FontFile[23]?\s", data))
    base_fonts = sorted(
        {
            match.decode("latin-1", errors="replace")
            for match in re.findall(rb"/BaseFont\s*/([^\s/<>\[\]()]+)", data)
        }
    )
    media_box = re.search(
        rb"/MediaBox\s*\[\s*([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s*\]",
        data,
    )

    results.append(_result("ok", f"PDF pages: {page_count}"))
    results.append(_result("ok", f"Font objects: {font_count}; embedded font streams: {embedded_count}"))
    if media_box:
        x0, y0, x1, y1 = (float(value) for value in media_box.groups())
        width = abs(x1 - x0) / 72
        height = abs(y1 - y0) / 72
        results.append(_result("ok", f"First-page physical size: {width:.2f} x {height:.2f} in"))
    else:
        results.append(_result("warn", "No MediaBox found; physical page size could not be verified"))
    if base_fonts:
        results.append(_result("ok", "Fonts: " + ", ".join(base_fonts[:8])))
    if page_count != 1:
        results.append(_result("warn", "Expected one page for a standalone figure"))
    if font_count and embedded_count == 0:
        results.append(_result("warn", "Font objects found but no embedded Type 1/TrueType/CFF streams were detected"))

    return results


def audit_svg(path: Path) -> list[dict[str, str]]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [_result("error", f"Invalid SVG XML: {exc}")]

    results: list[dict[str, str]] = []
    width = root.attrib.get("width")
    height = root.attrib.get("height")
    view_box = root.attrib.get("viewBox")
    results.append(_result("ok", f"SVG dimensions: width={width or 'unset'}, height={height or 'unset'}"))
    if not view_box:
        results.append(_result("warn", "SVG has no viewBox; downstream scaling may be less predictable"))

    image_count = sum(1 for element in root.iter() if element.tag.rsplit("}", 1)[-1] == "image")
    text_count = sum(1 for element in root.iter() if element.tag.rsplit("}", 1)[-1] == "text")
    results.append(_result("ok", f"SVG text nodes: {text_count}; embedded raster images: {image_count}"))
    if image_count:
        results.append(_result("warn", "SVG contains raster image elements; verify they meet the target resolution"))

    return results


def audit_png(path: Path) -> list[dict[str, str]]:
    try:
        from PIL import Image
    except ImportError:
        return [_result("warn", "Pillow is unavailable; skipped PNG resolution and DPI checks")]

    results: list[dict[str, str]] = []
    with Image.open(path) as image:
        width, height = image.size
        dpi = image.info.get("dpi")
        results.append(_result("ok", f"PNG pixels: {width} x {height}; mode: {image.mode}"))
        if image.mode in {"RGBA", "LA"}:
            alpha = image.getchannel("A")
            if alpha.getextrema()[0] < 255:
                results.append(_result("warn", "PNG contains transparent pixels; verify transparency is intentional"))

        if dpi:
            dpi_x = round(float(dpi[0]), 1)
            dpi_y = round(float(dpi[1]), 1)
            inches_x = width / float(dpi[0])
            inches_y = height / float(dpi[1])
            results.append(
                _result(
                    "ok",
                    f"PNG DPI: {dpi_x} x {dpi_y}; physical size: {inches_x:.2f} x {inches_y:.2f} in",
                )
            )
            if min(float(dpi[0]), float(dpi[1])) < 299:
                results.append(_result("warn", "PNG is below 300 dpi at the declared physical size"))
        else:
            results.append(_result("warn", "PNG has no DPI metadata; verify final-size resolution manually"))

        if min(width, height) < 600:
            results.append(_result("warn", "PNG is unusually small for a print figure; inspect text legibility"))

    return results


def audit_file(path: Path) -> list[dict[str, str]]:
    if not path.exists() or not path.is_file():
        return [_result("error", "File does not exist")]
    if path.stat().st_size == 0:
        return [_result("error", "File is empty")]

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return audit_pdf(path)
    if suffix == ".svg":
        return audit_svg(path)
    if suffix == ".png":
        return audit_png(path)
    return [_result("warn", f"No format-specific checks for {suffix or 'a file without an extension'}")]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="Exported PDF, SVG, or PNG files")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures, useful in automated workflows",
    )
    args = parser.parse_args()

    total_errors = 0
    total_warnings = 0

    for path in args.files:
        print(f"\n{path}")
        for item in audit_file(path):
            print(f"  {item['level'].upper():5} {item['message']}")
            total_errors += item["level"] == "error"
            total_warnings += item["level"] == "warn"

    print("\nAutomated checks do not verify the statistical claim or visual legibility.")
    print("Inspect the final-size render, including a grayscale copy.")

    if total_errors or (args.strict and total_warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
