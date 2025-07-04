import numpy as np
import tensorflow as tf
import glob
import os

interpreter = tf.lite.Interpreter(model_path="model_mixed.tflite")  # 使用量化模型
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 获取输入/输出的量化参数（zero point 和 scale）
input_scale, input_zero_point = input_details[0]['quantization']
output_scale, output_zero_point = output_details[0]['quantization']

def run_inference(txt_path):
    arr = np.loadtxt(txt_path, dtype=np.uint16).reshape((64, 64)) / 65535.0
    input_tensor = np.expand_dims(arr, axis=(0, -1)).astype(np.float32)  # float32

    # 量化：float32 -> uint8（或 int8）
    input_dtype = input_details[0]['dtype']
    if input_dtype == np.uint8 or input_dtype == np.int8:
        input_tensor = input_tensor / input_scale + input_zero_point
        input_tensor = np.clip(input_tensor, np.iinfo(input_dtype).min, np.iinfo(input_dtype).max)
        input_tensor = input_tensor.astype(input_dtype)

    interpreter.set_tensor(input_details[0]['index'], input_tensor)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])

    # 去量化：int -> float32
    output_dtype = output_details[0]['dtype']
    if output_dtype == np.uint8 or output_dtype == np.int8:
        output = (output.astype(np.float32) - output_zero_point) * output_scale

    return output[0][0]  # 单输出

# 统计函数
def evaluate_category(category, label):
    correct = 0
    total = 0
    files = sorted(glob.glob(f"aug_data/{category}/*.txt"))

    print(f"\n📂 分类: {category}（实际标签: {label}）")
    for path in files:
        prob = run_inference(path)
        pred = int(prob > 0.5)
        result = '✅' if pred == label else '❌'
        if pred == label:
            correct += 1
        total += 1
        print(f"{path} -> 概率: {prob:.4f} -> 预测: {pred} {result}")
    acc = correct / total if total > 0 else 0
    print(f"📊 分类 [{category}] 准确率: {acc*100:.2f}% ({correct}/{total})")
    return correct, total

# 主流程
def main():
    total_correct, total_total = 0, 0
    for cat, label in [("positive", 1), ("negative", 0)]:
        c, t = evaluate_category(cat, label)
        total_correct += c
        total_total += t
    print(f"\n🎯 总体准确率: {total_correct}/{total_total} = {total_correct/total_total*100:.2f}%")

main()
