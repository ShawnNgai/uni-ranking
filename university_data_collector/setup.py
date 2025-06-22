#!/usr/bin/env python3
"""
环境设置脚本
用于检查和安装必要的依赖
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("   需要Python 3.8或更高版本")
        return False
    else:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True

def install_requirements():
    """安装依赖包"""
    print("\n📦 安装依赖包...")
    
    requirements = [
        "pandas",
        "openpyxl", 
        "aiohttp",
        "beautifulsoup4",
        "loguru",
        "email-validator"
    ]
    
    for package in requirements:
        try:
            print(f"   安装 {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ {package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"   ❌ {package} 安装失败")
            return False
    
    return True

def create_directories():
    """创建必要的目录"""
    print("\n📁 创建目录结构...")
    
    directories = [
        "data",
        "data/exports",
        "data/backups", 
        "logs",
        "temp"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ 创建目录: {directory}")

def main():
    """主函数"""
    print("="*60)
    print("🔧 西班牙大学数据收集器 - 环境设置")
    print("="*60)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not install_requirements():
        print("❌ 依赖安装失败")
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    print("\n✅ 环境设置完成!")
    print("\n💡 接下来您可以运行:")
    print("   python demo_export.py     # 演示导出功能")
    print("   python quick_export.py    # 快速导出数据")
    print("   python run_spain_collection.py  # 收集西班牙大学数据")

if __name__ == "__main__":
    main() 