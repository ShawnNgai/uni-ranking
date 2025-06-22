#!/bin/bash

echo "============================================================"
echo "📤 西班牙大学数据收集器 - 演示运行"
echo "============================================================"
echo

echo "🔧 步骤1: 环境设置..."
python3 setup.py
if [ $? -ne 0 ]; then
    echo "❌ 环境设置失败"
    exit 1
fi

echo
echo "📤 步骤2: 运行演示..."
python3 demo_export.py
if [ $? -ne 0 ]; then
    echo "❌ 演示运行失败"
    exit 1
fi

echo
echo "📁 步骤3: 查看结果..."
if ls data/exports/*.csv 1> /dev/null 2>&1; then
    echo "✅ 找到CSV文件:"
    ls data/exports/*.csv
else
    echo "❌ 未找到CSV文件"
fi

if ls data/exports/*.xlsx 1> /dev/null 2>&1; then
    echo "✅ 找到Excel文件:"
    ls data/exports/*.xlsx
else
    echo "❌ 未找到Excel文件"
fi

echo
echo "🎉 演示完成!"
echo "💡 提示: 您可以在 data/exports 目录中找到导出的文件"
echo 