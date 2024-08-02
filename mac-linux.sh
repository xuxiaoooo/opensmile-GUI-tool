#!/bin/bash
# 初始化 conda 环境
source ~/miniconda3/etc/profile.d/conda.sh

# 激活指定的 conda 环境
conda activate base

# 运行 Python 脚本
python opensmile-GUI-tool.py

# 提示完成
echo "Script execution completed!"