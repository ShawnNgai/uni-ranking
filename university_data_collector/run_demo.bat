@echo off
chcp 65001 >nul
echo ============================================================
echo 📤 西班牙大学数据收集器 - 演示运行
echo ============================================================
echo.

echo 🔧 步骤1: 环境设置...
python setup.py
if %errorlevel% neq 0 (
    echo ❌ 环境设置失败
    pause
    exit /b 1
)

echo.
echo 📤 步骤2: 运行演示...
python demo_export.py
if %errorlevel% neq 0 (
    echo ❌ 演示运行失败
    pause
    exit /b 1
)

echo.
echo 📁 步骤3: 查看结果...
if exist "data\exports\*.csv" (
    echo ✅ 找到CSV文件:
    dir /b data\exports\*.csv
) else (
    echo ❌ 未找到CSV文件
)

if exist "data\exports\*.xlsx" (
    echo ✅ 找到Excel文件:
    dir /b data\exports\*.xlsx
) else (
    echo ❌ 未找到Excel文件
)

echo.
echo 🎉 演示完成!
echo 💡 提示: 您可以在 data\exports 目录中找到导出的文件
echo.
pause 