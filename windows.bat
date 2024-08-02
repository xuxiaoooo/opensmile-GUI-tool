@echo off
REM 初始化 conda 环境
CALL conda init

REM 激活指定的 conda 环境
CALL conda activate base

REM 运行 Python 脚本
python opensmile-GUI-tool.py

REM 提示完成
echo Script execution completed!
pause