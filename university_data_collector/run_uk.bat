@echo off
chcp 65001 >nul
echo ============================================================
echo 🇬🇧 英国大学邮箱收集器 - Windows一键运行
echo ============================================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8或更高版本
    echo 📖 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装
python --version

:: 检查依赖包
echo.
echo 🔍 检查依赖包...
python -c "import aiohttp, loguru, email_validator" >nul 2>&1
if errorlevel 1 (
    echo 📦 安装依赖包...
    pip install aiohttp loguru email-validator
    if errorlevel 1 (
        echo ❌ 依赖包安装失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖包已安装

:: 创建数据目录
if not exist "data\exports" mkdir "data\exports"

:: 运行演示脚本
echo.
echo 🚀 运行英国大学邮箱收集演示...
python run_uk_demo.py

if errorlevel 1 (
    echo ❌ 演示运行失败
    pause
    exit /b 1
)

echo.
echo ✅ 演示完成！
echo.
echo 💡 要收集真实数据，请运行:
echo    python run_uk_collection.py
echo.
echo 📁 导出的CSV文件位于: data\exports\
echo.
pause 