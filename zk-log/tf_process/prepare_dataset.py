import os
import numpy as np

def load_data_from_folder(folder, label):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            arr = np.loadtxt(path, dtype=np.uint16)
            arr = arr.reshape((64, 64)) / 65535.0  # 归一化到 0~1
            data.append((arr, label))
    return data

def load_dataset(data_dir):
    dataset = []
    dataset += load_data_from_folder(os.path.join(data_dir, "positive"), 1)
    dataset += load_data_from_folder(os.path.join(data_dir, "negative"), 0)

    np.random.shuffle(dataset)
    X = np.array([d[0] for d in dataset])
    y = np.array([d[1] for d in dataset])
    X = X[..., np.newaxis]  # 加通道维度 (64, 64, 1)
    return X, y