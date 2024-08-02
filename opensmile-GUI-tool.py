import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import opensmile
import librosa

# 初始化opensmile
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.ComParE_2016,
    feature_level=opensmile.FeatureLevel.Functionals,
)

def process_audio_files(input_folder, output_csv):
    # 创建一个空的DataFrame来存储所有特征
    all_features = pd.DataFrame()

    # 遍历文件夹中的所有音频文件
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.wav'):  # 只处理.wav文件
            # 构造完整文件路径
            file_path = os.path.join(input_folder, file_name)

            # 加载音频文件
            y, sr = librosa.load(file_path, sr=None)

            # 跳过时长小于30秒的文件
            duration = librosa.get_duration(y=y, sr=sr)
            if duration < 30:
                continue

            # 提取前30秒音频
            y_30s = y[:30*sr]

            # 提取音频特征
            features = smile.process_file(file_path)

            # 将文件名添加为一列
            features['file_name'] = file_name

            # 将特征添加到all_features DataFrame中
            all_features = pd.concat([all_features, features], ignore_index=True)

    # 将所有特征保存到CSV文件中
    all_features.to_csv(output_csv, index=False)
    messagebox.showinfo("完成", f"特征提取并保存到 {output_csv}")

def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_var.set(folder_selected)

def select_output_folder():
    file_selected = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    output_file_var.set(file_selected)

# 创建主窗口
root = tk.Tk()
root.title("音频特征提取")

# 输入文件夹选择
tk.Label(root, text="选择输入文件夹:").grid(row=0, column=0, padx=10, pady=10)
input_folder_var = tk.StringVar()
tk.Entry(root, textvariable=input_folder_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="浏览", command=select_input_folder).grid(row=0, column=2, padx=10, pady=10)

# 输出文件选择
tk.Label(root, text="选择输出文件:").grid(row=1, column=0, padx=10, pady=10)
output_file_var = tk.StringVar()
tk.Entry(root, textvariable=output_file_var, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="浏览", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

# 提取特征按钮
tk.Button(root, text="提取特征", command=lambda: process_audio_files(input_folder_var.get(), output_file_var.get())).grid(row=2, column=0, columnspan=3, padx=10, pady=20)

# 运行主循环
root.mainloop()