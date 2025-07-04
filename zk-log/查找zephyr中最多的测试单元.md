.overlay 文件可以在原先配置的基础上更改

两个脚本，一个脚本列出所有.overlay 文件出现的次数，一个脚本列出最多的.overlay 文件测试单元目录



列出samples目录下 所有.overlay文件出现的次数

```python
import os
from collections import Counter

def find_overlay_files(root_dir):
    overlay_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.overlay'):
                overlay_files.append(filename)
    return overlay_files

def main():
    root_dir = 'samples'  # 修改为你的 Zephyr samples 目录路径
    overlay_files = find_overlay_files(root_dir)

    if not overlay_files:
        print("没有找到任何 .overlay 文件")
        return

    counter = Counter(overlay_files)
    most_common_file, count = counter.most_common(1)[0]

    print(f"出现次数最多的 .overlay 文件是: {most_common_file}")
    print(f"出现次数: {count}")

    print("\n所有 .overlay 文件出现次数统计：")
    for filename, cnt in counter.most_common():
        print(f"{filename}: {cnt}")

if __name__ == '__main__':
    main()

```



列出指定 .overlay samples目录下的所有的测试单元

```c
import os

def find_dirs_with_overlay(root_dir, target_overlay):
    matched_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if target_overlay in filenames:
            matched_dirs.append(dirpath)
    return matched_dirs

def main():
    root_dir = 'samples'  # 根据实际路径修改
    target_overlay = 'nrf52840dk_nrf52840.overlay'

    dirs = find_dirs_with_overlay(root_dir, target_overlay)
    if not dirs:
        print(f"未找到包含 {target_overlay} 的目录")
        return

    print(f"包含 {target_overlay} 的测试单元目录共 {len(dirs)} 个:")
    for d in dirs:
        print(d)

if __name__ == '__main__':
    main()

```

