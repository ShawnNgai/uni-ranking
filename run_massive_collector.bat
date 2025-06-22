@echo off
echo === 大规模全球大学邮箱收集器 ===
echo 目标：采集前1万所大学的官方邮箱
echo 特性：支持断点续抓，自动保存进度
echo.

echo 正在安装依赖...
pip install -r requirements.txt

echo.
echo 开始运行收集器...
python massive_university_collector.py

echo.
echo 程序执行完成！
pause 