@echo off
chcp 65001
echo 大学邮箱收集系统启动中...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo Python版本检查通过
echo.

REM 安装依赖
echo 正在安装依赖包...
pip install -r requirements_email_collector.txt

if errorlevel 1 (
    echo 警告: 部分依赖安装失败，尝试使用简化版本
    echo.
    echo 启动简化版邮箱收集器...
    python simple_email_collector.py
) else (
    echo 依赖安装完成
    echo.
    echo 启动完整版邮箱收集器...
    python university_email_collector.py
)

echo.
echo 邮箱收集完成！
pause 