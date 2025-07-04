#!/usr/bin/env python3
"""
restore_images.py

读取 `png_pix_log/` 目录下所有日志文件，将像素坐标点恢复成黑白图像，
并将恢复后的图片保存到 `restore_the_picture/` 目录。

依赖：
    pip install pillow
"""

import os
from pathlib import Path
from PIL import Image


def main():
    input_log_dir = Path('png_pix_log')
    original_img_dir = Path('png')
    output_img_dir = Path('restore_the_picture')
    output_img_dir.mkdir(parents=True, exist_ok=True)

    log_files = list(input_log_dir.glob('*.txt'))
    if not log_files:
        print("No log files found in 'png_pix_log' directory.")
        return

    for log_file in log_files:
        # Determine original image path to get size
        stem = log_file.stem
        orig_img_path = original_img_dir / f"{stem}.png"
        if not orig_img_path.exists():
            print(f"Original image '{orig_img_path}' not found. Skipping.")
            continue

        # Open original to get dimensions
        orig_img = Image.open(orig_img_path)
        width, height = orig_img.size

        # Create white background
        restored = Image.new('RGB', (width, height), 'white')
        pixels = restored.load()

        # Read coordinates and plot black pixels
        count = 0
        with open(log_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    x_str, y_str = line.split(',')
                    x, y = int(x_str), int(y_str)
                    if 0 <= x < width and 0 <= y < height:
                        pixels[x, y] = (0, 0, 0)
                        count += 1
                except ValueError:
                    continue

        # Save restored image
        out_path = output_img_dir / f"{stem}.png"
        restored.save(out_path)
        print(f"Restored '{stem}.png' with {count} pixels saved to '{out_path}'")

if __name__ == '__main__':
    main()


    
