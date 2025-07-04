

#!/usr/bin/env python3
"""
draw_text_image.py

在一张指定尺寸的背景图上绘制指定的多行文字并保存，多张图分别命名为文字对应的文件名。

依赖：
    pip install pillow
"""

import argparse
import os
import platform
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def find_system_font():
    """
    Try a few common paths on different OSes for a default TrueType font.
    Returns a path or None.
    """
    sys_name = platform.system()
    if sys_name == "Windows":
        candidate = r"C:\Windows\Fonts\arial.ttf"
        if os.path.exists(candidate):
            return candidate
    elif sys_name == "Darwin":
        candidate = "/Library/Fonts/Arial.ttf"
        if os.path.exists(candidate):
            return candidate
    else:
        # Linux / Unix
        for path in (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ):
            if os.path.exists(path):
                return path
    return None


def slugify(text: str) -> str:
    """
    Convert text into a filename-friendly slug: lowercase, non-alphanumeric to underscore.
    """
    slug = text.strip().lower()
    # replace non-word characters with underscore
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    # trim underscores
    slug = slug.strip("_")
    return slug or "output"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate multiple images with different text overlays.")
    parser.add_argument(
        "--width", type=int, default=320,
        help="Image width in pixels (default: 320)")
    parser.add_argument(
        "--height", type=int, default=240,
        help="Image height in pixels (default: 240)")
    parser.add_argument(
        "--bg-color", default="white",
        help="Background color (name or hex, default: white)")
    parser.add_argument(
        "--texts", nargs='+',
        help="List of texts to draw; default five motion/position phrases.")
    parser.add_argument(
        "--font-path", default=None,
        help="Path to a .ttf font file (default: tries system fonts)")
    parser.add_argument(
        "--font-size", type=int, default=24,
        help="Font size in points (default: 16)")
    parser.add_argument(
        "--text-color", default="black",
        help="Text color (name or hex, default: black)")
    parser.add_argument(
        "--position", type=int, nargs=2, default=(0, 0),
        metavar=('X', 'Y'),
        help="Top-left corner where text starts (default: 0 0)")
    parser.add_argument(
        "--output-dir", default="png",
        help="Directory to save output images (default: png)")
    return parser.parse_args()


def main():
    args = parse_args()

    # Default phrases if none provided
    default_phrases = [
        "move left",
        "move right",
        "close to the camera",
        "far from the camera",
        "hold this position"
    ]

    # Determine texts to render
    texts = args.texts if args.texts else default_phrases

    # Prepare output directory
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load font
    font_file = args.font_path or find_system_font()
    if font_file:
        try:
            font = ImageFont.truetype(font_file, args.font_size)
        except IOError:
            print(f"Cannot load TTF font at {font_file}, falling back to default bitmap.")
            font = ImageFont.load_default()
    else:
        print("No TTF font found or specified, using default bitmap font (fixed size!).")
        font = ImageFont.load_default()

    # Generate images
    for text in texts:
        img = Image.new("RGB", (args.width, args.height), args.bg_color)
        draw = ImageDraw.Draw(img)
        draw.text(tuple(args.position), text, font=font, fill=args.text_color)

        # output filename based on text slug
        name = slugify(text) + ".png"
        out_path = out_dir / name
        img.save(out_path)
        print(f"Saved image: {out_path}")

if __name__ == "__main__":
    main()

