

#!/usr/bin/env python3
"""
batch_pixel_logger.py

读取 `png/` 目录下所有 .png 文件，提取非白色像素坐标，并将每个图像的坐标日志分别保存到 `png_pix_log/` 目录中。

依赖：
    pip install pillow
"""

import os
from pathlib import Path
from PIL import Image

def main():
    # 输入、输出目录
    input_dir = Path('png')
    output_dir = Path('png_pix_log')
    output_dir.mkdir(parents=True, exist_ok=True)

    # 查找所有 PNG 文件
    png_files = list(input_dir.glob('*.png'))
    if not png_files:
        print("No PNG files found in 'png' directory.")
        return

    # 处理每个文件
    for img_path in png_files:
        img = Image.open(img_path).convert('RGB')
        width, height = img.size
        pixels = img.load()
        count = 0

        # 日志文件路径
        log_path = output_dir / f"{img_path.stem}.txt"
        with open(log_path, 'w') as log_file:
            for y in range(height):
                for x in range(width):
                    # 非白色像素
                    if pixels[x, y] != (255, 255, 255):
                        log_file.write(f"{x},{y}\n")
                        count += 1

        print(f"Processed {img_path.name}: {count} non-white pixels logged to {log_path}")

if __name__ == '__main__':
    main()
