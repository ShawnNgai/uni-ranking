#!/usr/bin/env python3
"""
测试西班牙大学数据收集器
"""

import asyncio
import json
from app.scrapers.spain_scraper import SpainUniversityScraper

async def test_spain_scraper():
    """测试西班牙大学爬虫"""
    print("开始测试西班牙大学数据收集器...")
    
    try:
        async with SpainUniversityScraper() as scraper:
            # 测试数据收集
            universities = await scraper.collect_spain_universities()
            
            print(f"\n成功收集到 {len(universities)} 所大学的数据")
            
            # 显示前5个结果
            print("\n前5所大学信息:")
            print("-" * 80)
            
            for i, uni in enumerate(universities[:5], 1):
                print(f"{i}. {uni['name_en']}")
                print(f"   本地名称: {uni['name_local']}")
                print(f"   网站: {uni['website']}")
                print(f"   城市: {uni.get('city', 'N/A')}")
                print(f"   地区: {uni.get('region', 'N/A')}")
                print(f"   官方邮箱: {uni.get('official_email', 'N/A')}")
                print(f"   联系邮箱: {uni.get('contact_email', 'N/A')}")
                print(f"   校长邮箱: {uni.get('president_email', 'N/A')}")
                print(f"   行政邮箱: {uni.get('admin_email', 'N/A')}")
                print(f"   世界排名: {uni.get('ranking_world', 'N/A')}")
                print(f"   大学类型: {uni.get('university_type', 'N/A')}")
                print("-" * 80)
            
            # 统计信息
            with_emails = len([u for u in universities if u.get('official_email')])
            with_president = len([u for u in universities if u.get('president_email')])
            with_admin = len([u for u in universities if u.get('admin_email')])
            
            print(f"\n统计信息:")
            print(f"总大学数量: {len(universities)}")
            print(f"有官方邮箱: {with_emails} ({with_emails/len(universities)*100:.1f}%)")
            print(f"有校长邮箱: {with_president} ({with_president/len(universities)*100:.1f}%)")
            print(f"有行政邮箱: {with_admin} ({with_admin/len(universities)*100:.1f}%)")
            
            # 保存测试结果
            with open('test_results.json', 'w', encoding='utf-8') as f:
                json.dump(universities, f, ensure_ascii=False, indent=2)
            
            print(f"\n测试结果已保存到: test_results.json")
            
            return True
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("西班牙大学数据收集器测试")
    print("=" * 60)
    
    success = asyncio.run(test_spain_scraper())
    
    if success:
        print("\n✅ 测试成功完成!")
    else:
        print("\n❌ 测试失败!")
        exit(1)

if __name__ == "__main__":
    main() 