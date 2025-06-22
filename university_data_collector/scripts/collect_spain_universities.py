#!/usr/bin/env python3
"""
西班牙大学数据收集脚本
用于收集西班牙大学的英文名称、官方邮箱和管理层邮箱信息
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.scrapers.spain_scraper import SpainUniversityScraper
from loguru import logger

async def collect_spain_data():
    """收集西班牙大学数据"""
    logger.info("开始收集西班牙大学数据...")
    
    try:
        async with SpainUniversityScraper() as scraper:
            # 收集大学数据
            universities = await scraper.collect_spain_universities()
            
            # 保存数据到JSON文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"data/spain_universities_{timestamp}.json"
            
            # 确保数据目录存在
            os.makedirs("data", exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(universities, f, ensure_ascii=False, indent=2)
            
            logger.info(f"数据已保存到: {output_file}")
            
            # 生成统计报告
            generate_report(universities, output_file)
            
            return universities
            
    except Exception as e:
        logger.error(f"数据收集失败: {str(e)}")
        return []

def generate_report(universities, data_file):
    """生成数据收集报告"""
    logger.info("生成数据收集报告...")
    
    total_count = len(universities)
    with_emails = len([u for u in universities if u.get('official_email')])
    with_president_email = len([u for u in universities if u.get('president_email')])
    with_admin_email = len([u for u in universities if u.get('admin_email')])
    
    # 按地区统计
    regions = {}
    for uni in universities:
        region = uni.get('region', 'Unknown')
        regions[region] = regions.get(region, 0) + 1
    
    # 按城市统计
    cities = {}
    for uni in universities:
        city = uni.get('city', 'Unknown')
        cities[city] = cities.get(city, 0) + 1
    
    report = {
        "collection_date": datetime.now().isoformat(),
        "data_file": data_file,
        "summary": {
            "total_universities": total_count,
            "with_official_email": with_emails,
            "with_president_email": with_president_email,
            "with_admin_email": with_admin_email,
            "email_coverage": round(with_emails / total_count * 100, 2) if total_count > 0 else 0
        },
        "regions": regions,
        "cities": cities,
        "sample_data": universities[:5] if universities else []
    }
    
    # 保存报告
    report_file = f"data/spain_universities_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告摘要
    print("\n" + "="*60)
    print("西班牙大学数据收集报告")
    print("="*60)
    print(f"收集时间: {report['collection_date']}")
    print(f"总大学数量: {total_count}")
    print(f"有官方邮箱: {with_emails} ({report['summary']['email_coverage']}%)")
    print(f"有校长邮箱: {with_president_email}")
    print(f"有行政邮箱: {with_admin_email}")
    print(f"数据文件: {data_file}")
    print(f"报告文件: {report_file}")
    
    print("\n地区分布:")
    for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region}: {count}")
    
    print("\n城市分布 (前10):")
    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {city}: {count}")
    
    print("\n样本数据:")
    for i, uni in enumerate(report['sample_data'], 1):
        print(f"  {i}. {uni['name_en']}")
        print(f"     网站: {uni['website']}")
        print(f"     官方邮箱: {uni['official_email'] or 'N/A'}")
        print(f"     校长邮箱: {uni['president_email'] or 'N/A'}")
        print()

def main():
    """主函数"""
    logger.info("启动西班牙大学数据收集器")
    
    # 运行数据收集
    universities = asyncio.run(collect_spain_data())
    
    if universities:
        logger.info(f"成功收集 {len(universities)} 所大学的数据")
    else:
        logger.error("数据收集失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 