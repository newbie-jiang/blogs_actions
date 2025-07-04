#!/usr/bin/env python3
"""
batch_header_generator.py

读取 `png_pix_log/` 目录下所有 .txt 文件（每行格式 x,y），
将坐标转换成 C 头文件，每个文件对应一个 .h，保存到 `output_src/` 目录。

依赖：
    无（标准库）
"""

import os
import sys
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch convert coordinate logs to C header files.")
    parser.add_argument(
        "--input-dir", default="png_pix_log",
        help="目录，读取其中的 .txt 文件 (默认 png_pix_log)")
    parser.add_argument(
        "--output-dir", default="output_src",
        help="目录，保存生成的 .h 文件 (默认 output_src)")
    parser.add_argument(
        "--extension", default=".txt",
        help="日志文件扩展名 (默认 .txt)")
    return parser.parse_args()


def read_coords(path):
    coords = []
    with open(path, 'r') as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                x_str, y_str = line.split(',')
                coords.append((int(x_str), int(y_str)))
            except ValueError:
                print(f"Warning: cannot parse line {lineno} in {path}: '{line}'", file=sys.stderr)
    return coords


def write_header(coords, header_path, array_name):
    count = len(coords)
    with open(header_path, 'w') as out:
        out.write(f"// {header_path.name}\n")
        out.write("#pragma once\n")
        out.write("#include <stdint.h>\n\n")
        out.write(f"#define {array_name.upper()}_COUNT {count}\n\n")
        out.write(f"static const uint16_t {array_name}[{count}][2] = {{\n")
        per_line = 10
        for i in range(0, count, per_line):
            chunk = coords[i:i+per_line]
            line_elems = [f"{{{x}, {y}}}" for x, y in chunk]
            comma = ',' if i + per_line < count else ''
            out.write("    " + ", ".join(line_elems) + comma + "\n")
        out.write("};\n")


def slugify(name):
    # 生成合法的 C 标识符
    slug = ''.join(c if c.isalnum() else '_' for c in name)
    if slug and slug[0].isdigit():
        slug = '_' + slug
    return slug


def main():
    args = parse_args()
    in_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = list(in_dir.glob(f"*{args.extension}"))
    if not files:
        print(f"No '{args.extension}' files found in '{in_dir}'")
        return

    for file in files:
        coords = read_coords(file)
        if not coords:
            print(f"Skipping '{file.name}', no valid coordinates.")
            continue
        stem = file.stem
        array_name = slugify(stem) + '_pts'
        header_name = stem + '.h'
        header_path = out_dir / header_name
        write_header(coords, header_path, array_name)
        print(f"Generated header: {header_path} ({len(coords)} points)")

if __name__ == '__main__':
    main()
