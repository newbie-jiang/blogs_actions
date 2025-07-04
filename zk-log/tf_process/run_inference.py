# import numpy as np
# import tensorflow as tf
# import glob
# import os

# interpreter = tf.lite.Interpreter(model_path="model.tflite")
# interpreter.allocate_tensors()
# input_details = interpreter.get_input_details()
# output_details = interpreter.get_output_details()

# def run_inference(txt_path):
#     arr = np.loadtxt(txt_path, dtype=np.uint16).reshape((64, 64)) / 65535.0
#     input_tensor = np.expand_dims(arr, axis=(0, -1)).astype(np.float32)

#     interpreter.set_tensor(input_details[0]['index'], input_tensor)
#     interpreter.invoke()
#     output = interpreter.get_tensor(output_details[0]['index'])[0][0]
#     return output

# # 统计函数
# def evaluate_category(category, label):
#     correct = 0
#     total = 0
#     files = sorted(glob.glob(f"aug_data/{category}/*.txt"))

#     print(f"\n📂 分类: {category}（实际标签: {label}）")
#     for path in files:
#         prob = run_inference(path)
#         pred = int(prob > 0.5)
#         result = '✅' if pred == label else '❌'
#         if pred == label:
#             correct += 1
#         total += 1
#         print(f"{path} -> 概率: {prob:.4f} -> 预测: {pred} {result}")
#     acc = correct / total if total > 0 else 0
#     print(f"📊 分类 [{category}] 准确率: {acc*100:.2f}% ({correct}/{total})")
#     return correct, total

# # 主流程
# def main():
#     total_correct, total_total = 0, 0
#     for cat, label in [("positive", 1), ("negative", 0)]:
#         c, t = evaluate_category(cat, label)
#         total_correct += c
#         total_total += t
#     print(f"\n🎯 总体准确率: {total_correct}/{total_total} = {total_correct/total_total*100:.2f}%")

# main()


import numpy as np
import tensorflow as tf
import glob
import os
import time  # 引入 time 模块

# 初始化 interpreter
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def run_inference(txt_path):
    arr = np.loadtxt(txt_path, dtype=np.uint16).reshape((64, 64)) / 65535.0
    input_tensor = np.expand_dims(arr, axis=(0, -1)).astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], input_tensor)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])[0][0]
    return output

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
    start_time = time.time()  # 记录开始时间
    total_correct, total_total = 0, 0
    for cat, label in [("positive", 1), ("negative", 0)]:
        c, t = evaluate_category(cat, label)
        total_correct += c
        total_total += t
    end_time = time.time()  # 记录结束时间

    print(f"\n🎯 总体准确率: {total_correct}/{total_total} = {total_correct/total_total*100:.2f}%")
    print(f"⏱️ 总推理时间: {(end_time - start_time):.2f}秒")  # 输出整体推理时间

main()





