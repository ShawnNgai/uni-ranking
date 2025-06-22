#!/usr/bin/env python3
"""
英国大学邮箱收集运行脚本（调试版）
增强日志输出，仅抓取前3所大学
"""

import asyncio
import sys
import os
from pathlib import Path
from loguru import logger

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from uk_university_scraper import UKUniversityScraper

async def main():
    """主函数"""
    print("🇬🇧 英国大学邮箱收集器（调试模式）")
    print("="*50)
    
    try:
        async with UKUniversityScraper() as scraper:
            # 只抓取前3所大学，便于调试
            all_universities = await scraper._get_uk_universities_from_wikipedia()
            test_universities = all_universities[:3]
            logger.info(f"本次仅抓取前3所大学：{[u['name'] for u in test_universities]}")
            for uni in test_universities:
                await scraper._collect_university_emails(uni)
                logger.info(f"已处理：{uni['name']}，当前结果：{scraper.universities[-1] if scraper.universities else '无'}")
                await asyncio.sleep(1)
            
            universities = scraper.universities
            if universities:
                # 导出为CSV
                csv_file = scraper.export_to_csv()
                
                # 显示统计信息
                total_count = len(universities)
                with_emails = len([u for u in universities if u.get('all_emails')])
                
                print(f"\n✅ 收集完成!")
                print(f"📊 统计信息:")
                print(f"   总大学数量: {total_count}")
                print(f"   有邮箱信息: {with_emails} ({with_emails/total_count*100:.1f}%)")
                print(f"   📁 CSV文件: {csv_file}")
                
                # 显示全部结果
                print(f"\n📋 结果:")
                for i, uni in enumerate(universities, 1):
                    print(f"   {i:2d}. {uni['university_name']}")
                    if uni.get('all_emails'):
                        emails = uni['all_emails'].split('; ')
                        for email in emails:
                            print(f"       📧 {email}")
                    else:
                        print(f"       ❌ 未找到邮箱")
                    print()
                
                print(f"💡 提示: 完整数据已保存到 {csv_file}")
                
            else:
                print("❌ 未收集到数据")
                
    except Exception as e:
        print(f"❌ 运行出错: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 