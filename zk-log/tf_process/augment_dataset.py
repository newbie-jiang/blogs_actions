

import os
import numpy as np

# 增强倍数：每张原图生成几张增强图
AUG_PER_IMAGE = 5

def augment_heatmap(arr):
    """对热图数组进行轻微扰动增强，保留结构"""
    # 添加非常轻微的高斯噪声（±0.0001）
    noise = np.random.normal(loc=0.0, scale=0.0001, size=arr.shape)
    result = arr + noise
    result = np.clip(result, 0.0, 1.0)  # 保持在 [0, 1]

    # 概率性左右/上下翻转（保持方向多样性）
    # if np.random.rand() < 0.5:
    #     result = np.flip(result, axis=1)  # 左右翻转
    # if np.random.rand() < 0.5:
    #     result = np.flip(result, axis=0)  # 上下翻转

    return result

def save_txt(path, arr):
   
    arr_uint16 = (arr * 65535).astype(np.uint16)
    corrected = arr_uint16               # ✅ 保持原向

    np.savetxt(path, corrected, fmt='%d', delimiter=' ')

def augment_folder(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    file_list = [f for f in os.listdir(src_dir) if f.endswith('.txt')]

    for file in file_list:
        base_name = os.path.splitext(file)[0]
        file_path = os.path.join(src_dir, file)

        try:
            arr = np.loadtxt(file_path, dtype=np.uint16).reshape((64, 64)) / 65535.0
        except Exception as e:
            print(f"❌ 跳过无效文件: {file} - {e}")
            continue

        # 保存原始图
        save_txt(os.path.join(dst_dir, f"{base_name}_orig.txt"), arr)

        # 保存增强图像
        for i in range(AUG_PER_IMAGE):
            aug_arr = augment_heatmap(arr)
            out_path = os.path.join(dst_dir, f"{base_name}_aug{i+1}.txt")
            save_txt(out_path, aug_arr)

        print(f"✅ 增强完成: {file} -> 共 {AUG_PER_IMAGE + 1} 张")

def main():
    os.makedirs("aug_data/positive", exist_ok=True)
    os.makedirs("aug_data/negative", exist_ok=True)

    print("📂 正在增强 positive 类数据...")
    augment_folder("data/positive", "aug_data/positive")

    print("📂 正在增强 negative 类数据...")
    augment_folder("data/negative", "aug_data/negative")

    print("🎉 增强完成！请使用 aug_data 作为新数据集进行训练。")

if __name__ == "__main__":
    main()




