#!/usr/bin/env python3
"""Report perceptual separation for bundled publication palettes.

The script uses CIE76 color distance and simple protanopia/deuteranopia
simulations. The results are diagnostics, not a substitute for inspecting the
final chart and using non-color redundancy.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


PROTANOPIA = (
    (0.152286, 1.052583, -0.204868),
    (0.114503, 0.786281, 0.099216),
    (-0.003882, -0.048116, 1.051998),
)

DEUTERANOPIA = (
    (0.367322, 0.860646, -0.227968),
    (0.280085, 0.672501, 0.047413),
    (-0.011820, 0.042940, 0.968881),
)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Expected six-digit hex color, got #{value}")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    channels = [max(0, min(255, round(channel * 255))) for channel in rgb]
    return "#" + "".join(f"{channel:02X}" for channel in channels)


def srgb_to_linear(channel: float) -> float:
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def linear_to_srgb(channel: float) -> float:
    channel = max(0.0, min(1.0, channel))
    if channel <= 0.0031308:
        return 12.92 * channel
    return 1.055 * (channel ** (1 / 2.4)) - 0.055


def simulate(rgb: tuple[int, int, int], matrix) -> tuple[float, float, float]:
    linear = [srgb_to_linear(channel / 255) for channel in rgb]
    transformed = [sum(row[index] * linear[index] for index in range(3)) for row in matrix]
    return tuple(linear_to_srgb(channel) for channel in transformed)


def linear_rgb(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    return tuple(srgb_to_linear(channel / 255) for channel in rgb)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    red, green, blue = linear_rgb(rgb)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_with_white(rgb: tuple[int, int, int]) -> float:
    return 1.05 / (relative_luminance(rgb) + 0.05)


def rgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    red, green, blue = linear_rgb(rgb)
    x = 0.4124564 * red + 0.3575761 * green + 0.1804375 * blue
    y = 0.2126729 * red + 0.7151522 * green + 0.0721750 * blue
    z = 0.0193339 * red + 0.1191920 * green + 0.9503041 * blue

    def pivot(value: float) -> float:
        delta = 6 / 29
        return value ** (1 / 3) if value > delta**3 else value / (3 * delta**2) + 4 / 29

    fx = pivot(x / 0.95047)
    fy = pivot(y / 1.00000)
    fz = pivot(z / 1.08883)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(rgb_a: tuple[float, float, float], rgb_b: tuple[float, float, float]) -> float:
    a = rgb_to_lab(tuple(round(channel * 255) for channel in rgb_a))
    b = rgb_to_lab(tuple(round(channel * 255) for channel in rgb_b))
    return math.sqrt(sum((left - right) ** 2 for left, right in zip(a, b)))


def minimum_pair_distance(
    colors: list[tuple[int, int, int]],
    matrix=None,
) -> tuple[float, str]:
    transformed = [simulate(color, matrix) if matrix else tuple(channel / 255 for channel in color) for color in colors]
    best = (float("inf"), "")
    for left in range(len(transformed)):
        for right in range(left + 1, len(transformed)):
            distance = delta_e(transformed[left], transformed[right])
            pair = f"{rgb_to_hex(tuple(channel / 255 for channel in colors[left]))} / {rgb_to_hex(tuple(channel / 255 for channel in colors[right]))}"
            if distance < best[0]:
                best = (distance, pair)
    return best


def audit_palette(name: str, definition: dict) -> dict[str, object]:
    colors = [hex_to_rgb(value) for value in definition["colors"]]
    normal = minimum_pair_distance(colors)
    deuteranopia = minimum_pair_distance(colors, DEUTERANOPIA)
    protanopia = minimum_pair_distance(colors, PROTANOPIA)
    minimum_contrast = min((contrast_with_white(color), rgb_to_hex(tuple(channel / 255 for channel in color))) for color in colors)
    return {
        "name": name,
        "label": definition["label"],
        "normal": normal,
        "deuteranopia": deuteranopia,
        "protanopia": protanopia,
        "minimum_contrast": minimum_contrast,
    }


def make_preview(data: dict, path: Path) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise RuntimeError("Pillow is required for --preview") from exc

    row_height = 78
    label_width = 170
    width = 1180
    palettes = data["palettes"]
    height = 42 + len(palettes) * row_height * 4
    image = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.load_default(size=14)
        small = ImageFont.load_default(size=11)
    except TypeError:
        font = ImageFont.load_default()
        small = font
    draw.text((18, 12), "Publication palette audit: normal, deuteranopia, protanopia, grayscale", fill="#111111", font=font)

    y = 42
    for key, definition in palettes.items():
        colors = [hex_to_rgb(value) for value in definition["colors"]]
        variants = [
            ("normal", colors, None),
            ("deuteranopia", colors, DEUTERANOPIA),
            ("protanopia", colors, PROTANOPIA),
            ("grayscale", colors, "gray"),
        ]
        for variant_name, source, matrix in variants:
            draw.text((14, y + 10), f"{key} / {variant_name}", fill="#334155", font=font)
            swatch_width = (width - label_width - 18) // len(source)
            for index, color in enumerate(source):
                if matrix == "gray":
                    luminance = relative_luminance(color)
                    value = round(linear_to_srgb(luminance) * 255)
                    transformed = (value, value, value)
                    fill = f"#{value:02X}{value:02X}{value:02X}"
                elif matrix:
                    transformed_srgb = simulate(color, matrix)
                    fill = rgb_to_hex(transformed_srgb)
                else:
                    fill = rgb_to_hex(tuple(channel / 255 for channel in color))

                left = label_width + index * swatch_width
                draw.rectangle((left, y, left + swatch_width - 2, y + row_height - 4), fill=fill)
                text = "#FFFFFF" if contrast_with_white(hex_to_rgb(fill)) > 4.5 else "#111111"
                draw.text((left + 7, y + 7), fill.upper(), fill=text, font=small)
            y += row_height

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--palette", default="all", help="Palette name or 'all'")
    parser.add_argument("--palettes-file", type=Path)
    parser.add_argument("--preview", type=Path, help="Write a PNG contact sheet")
    args = parser.parse_args()

    palette_file = args.palettes_file
    if palette_file is None:
        palette_file = Path(__file__).resolve().parents[1] / "assets" / "palettes.json"
    data = json.loads(palette_file.read_text(encoding="utf-8"))
    palettes = data["palettes"]
    selected = palettes if args.palette == "all" else {args.palette: palettes[args.palette]}

    warnings = 0
    for name, definition in selected.items():
        result = audit_palette(name, definition)
        normal, normal_pair = result["normal"]
        deuter, deuter_pair = result["deuteranopia"]
        protan, protan_pair = result["protanopia"]
        contrast, contrast_color = result["minimum_contrast"]
        print(f"\n{name}: {definition['label']}")
        print(f"  Normal min Delta E:      {normal:5.1f}  ({normal_pair})")
        print(f"  Deuteranopia min Delta E:{deuter:5.1f}  ({deuter_pair})")
        print(f"  Protanopia min Delta E:  {protan:5.1f}  ({protan_pair})")
        print(f"  Minimum white contrast:  {contrast:4.1f}:1 ({contrast_color})")
        if normal < 12 or deuter < 8 or protan < 8:
            warnings += 1
            print("  WARN Use shape, marker, line style, or direct labels as redundancy.")
        if contrast < 1.5:
            warnings += 1
            print("  WARN The lightest color has weak white contrast; avoid it for thin marks or text.")

    if args.preview:
        make_preview(data, args.preview)
        print(f"\nPreview: {args.preview.resolve()}")

    print("\nColor separation does not prove accessibility or visual quality.")
    print("Inspect the final-size figure in grayscale and with redundant encodings.")
    return 0 if warnings == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
