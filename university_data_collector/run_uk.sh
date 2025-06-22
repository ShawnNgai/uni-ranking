#!/bin/bash

echo "============================================================"
echo "🇬🇧 英国大学邮箱收集器 - Mac/Linux一键运行"
echo "============================================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.8或更高版本"
    echo "📖 Mac安装: brew install python"
    echo "📖 Linux安装: sudo apt-get install python3"
    exit 1
fi

echo "✅ Python已安装"
python3 --version

# 检查依赖包
echo
echo "🔍 检查依赖包..."
if ! python3 -c "import aiohttp, loguru, email_validator" &> /dev/null; then
    echo "📦 安装依赖包..."
    pip3 install aiohttp loguru email-validator
    if [ $? -ne 0 ]; then
        echo "❌ 依赖包安装失败"
        exit 1
    fi
fi

echo "✅ 依赖包已安装"

# 创建数据目录
mkdir -p data/exports

# 运行演示脚本
echo
echo "🚀 运行英国大学邮箱收集演示..."
python3 run_uk_demo.py

if [ $? -ne 0 ]; then
    echo "❌ 演示运行失败"
    exit 1
fi

echo
echo "✅ 演示完成！"
echo
echo "💡 要收集真实数据，请运行:"
echo "   python3 run_uk_collection.py"
echo
echo "📁 导出的CSV文件位于: data/exports/"
echo 