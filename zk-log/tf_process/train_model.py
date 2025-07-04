# ===== 导入必要的模块 =====
import os
import numpy as np
import tensorflow as tf
from prepare_dataset import load_dataset            # 加载自定义数据集加载函数
from tensorflow.keras.callbacks import EarlyStopping
import random

# ===== 固定随机种子，确保结果可复现 =====
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)
random.seed(SEED)

# ===== 可调参数区域 =====
DATA_DIR = "aug_data"           # 数据所在目录
EPOCHS = 50                     # 最大训练轮数
BATCH_SIZE = 2                  # 每批训练样本数量
VALIDATION_SPLIT = 0.2          # 验证集比例（20%）
LEARNING_RATE = 0.0005          # 学习率，影响收敛速度  0.0005    
HIDDEN_UNITS = 30              # 全连接层神经元个数（用于分类决策） 30
PATIENCE = 5                    # 验证集早停耐心轮数
# ==========================

# ===== 加载数据集 =====
X, y = load_dataset(DATA_DIR)   # 加载图像和对应标签
print(f"\n📦 数据集加载完毕：{X.shape}, 标签：{y.shape}")

# 输出标签分布统计
unique, counts = np.unique(y, return_counts=True)
print("🎯 标签统计：")
for u, c in zip(unique, counts):
    print(f"  类别 {u}: {c} 个样本")

# ===== 构建模型结构 =====
def build_model():
    model = tf.keras.Sequential([

        # 输入层（64x64 单通道图像）
        tf.keras.layers.Input(shape=(64, 64, 1)),

        # 卷积层1：提取低阶特征
        tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(),

        # 卷积层2：提取更复杂的模式
        tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(),

        # 扁平化输出，为全连接层准备输入
        tf.keras.layers.Flatten(),

        # 全连接层：提取全局特征并用于判别
        tf.keras.layers.Dense(HIDDEN_UNITS, activation='relu'),

        # Dropout 层：防止过拟合
        tf.keras.layers.Dropout(0.3),

        # 输出层：1 个神经元 + sigmoid 激活，输出概率（用于二分类）
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # 编译模型
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='binary_crossentropy',   # 二分类损失函数
        metrics=['accuracy']          # 评估指标为准确率
    )
    return model

# 创建模型
model = build_model()

# 设置 EarlyStopping：验证集 loss 多次不提升就提前停止训练
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=PATIENCE,
    restore_best_weights=True,
    verbose=1
)

# ===== 模型训练 =====
print("\n🚀 开始训练模型...")
history = model.fit(
    X, y,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=VALIDATION_SPLIT,
    callbacks=[early_stop],
    verbose=1
)

# ===== 保存 Keras 原始模型 =====
model.save("model.h5")
print("✅ 模型已保存为 model.h5")

# ===== 导出未量化的 TFLite 模型（float32） =====
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open("model.tflite", "wb") as f:
    f.write(tflite_model)
print("✅ 模型已保存为 model.tflite")

# ===== int8 量化版本（完整整数量化） =====

# 提供用于量化校准的代表性数据生成器（只要几百个样本即可）
def representative_data_gen():
    for i in range(min(100, len(X))):             # 用前100个样本进行校准
        data = X[i]
        data = np.expand_dims(data, axis=0).astype(np.float32)  # 添加 batch 维度
        yield [data]

# 创建量化转换器
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]                  # 启用默认优化（包括量化）
converter.representative_dataset = representative_data_gen           # 设置代表性数据
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]  # 使用完整 int8 量化
converter.inference_input_type = tf.uint8                            # 输入类型
converter.inference_output_type = tf.uint8                           # 输出类型

# 转换并保存 int8 量化模型
tflite_quant_model = converter.convert()
with open("model_int8.tflite", "wb") as f:
    f.write(tflite_quant_model)
print("✅ int8 量化模型已保存为 model_int8.tflite")




# 混合 int16 权重 + int8 激活（较少使用）
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,  # 支持 int8 + 部分 int16
]
# 注意：不能设置 input/output 为 int16，还是 uint8 或 float32
tflite_mixed_model = converter.convert()

with open("model_mixed.tflite", "wb") as f:
    f.write(tflite_mixed_model)

print("✅ 混合 int16 权重 模型已保存为 model_mixed.tflite")









