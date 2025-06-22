#!/usr/bin/env python3
"""
快速启动西班牙大学数据收集
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_environment():
    """设置环境"""
    print("🔧 设置环境...")
    
    # 创建必要的目录
    directories = ['data', 'logs', 'temp']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ 创建目录: {directory}")
    
    # 检查依赖
    try:
        import aiohttp
        import beautifulsoup4
        import loguru
        print("  ✓ 依赖检查通过")
    except ImportError as e:
        print(f"  ❌ 缺少依赖: {e}")
        print("  请运行: pip install -r requirements.txt")
        return False
    
    return True

async def main():
    """主函数"""
    print("=" * 60)
    print("🌍 西班牙大学数据收集器")
    print("=" * 60)
    
    # 设置环境
    if not setup_environment():
        sys.exit(1)
    
    try:
        # 导入爬虫
        from app.scrapers.spain_scraper import SpainUniversityScraper
        
        print("\n🚀 开始收集西班牙大学数据...")
        
        async with SpainUniversityScraper() as scraper:
            universities = await scraper.collect_spain_universities()
            
            if universities:
                print(f"\n✅ 成功收集 {len(universities)} 所大学的数据")
                
                # 显示样本数据
                print("\n📋 样本数据:")
                print("-" * 50)
                for i, uni in enumerate(universities[:3], 1):
                    print(f"{i}. {uni['name_en']}")
                    print(f"   网站: {uni['website']}")
                    print(f"   官方邮箱: {uni.get('official_email', 'N/A')}")
                    print(f"   校长邮箱: {uni.get('president_email', 'N/A')}")
                    print()
                
                # 统计信息
                with_emails = len([u for u in universities if u.get('official_email')])
                print(f"📊 统计信息:")
                print(f"   总大学数量: {len(universities)}")
                print(f"   有官方邮箱: {with_emails} ({with_emails/len(universities)*100:.1f}%)")
                
                print(f"\n💾 数据已收集完成，可以运行以下命令进行完整处理:")
                print(f"   python scripts/collect_spain_universities.py")
                
            else:
                print("❌ 数据收集失败")
                sys.exit(1)
                
    except Exception as e:
        print(f"❌ 运行失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 