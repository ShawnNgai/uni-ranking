#!/usr/bin/env python3
"""
英国大学邮箱收集演示脚本
使用示例数据快速演示功能
"""

import csv
import json
from datetime import datetime
from pathlib import Path

def create_sample_uk_data():
    """创建英国大学示例数据"""
    sample_data = [
        {
            "university_name": "University of Oxford",
            "website": "https://www.ox.ac.uk/",
            "general_email": "admissions@ox.ac.uk",
            "admissions_email": "admissions@ox.ac.uk",
            "international_email": "international.office@ox.ac.uk",
            "contact_email": "contact@ox.ac.uk",
            "info_email": "info@ox.ac.uk",
            "all_emails": "admissions@ox.ac.uk; international.office@ox.ac.uk; contact@ox.ac.uk; info@ox.ac.uk"
        },
        {
            "university_name": "University of Cambridge",
            "website": "https://www.cam.ac.uk/",
            "general_email": "admissions@cam.ac.uk",
            "admissions_email": "admissions@cam.ac.uk",
            "international_email": "international@cam.ac.uk",
            "contact_email": "contact@cam.ac.uk",
            "info_email": "info@cam.ac.uk",
            "all_emails": "admissions@cam.ac.uk; international@cam.ac.uk; contact@cam.ac.uk; info@cam.ac.uk"
        },
        {
            "university_name": "Imperial College London",
            "website": "https://www.imperial.ac.uk/",
            "general_email": "admissions@imperial.ac.uk",
            "admissions_email": "admissions@imperial.ac.uk",
            "international_email": "international@imperial.ac.uk",
            "contact_email": "contact@imperial.ac.uk",
            "info_email": "info@imperial.ac.uk",
            "all_emails": "admissions@imperial.ac.uk; international@imperial.ac.uk; contact@imperial.ac.uk; info@imperial.ac.uk"
        },
        {
            "university_name": "University College London",
            "website": "https://www.ucl.ac.uk/",
            "general_email": "admissions@ucl.ac.uk",
            "admissions_email": "admissions@ucl.ac.uk",
            "international_email": "international@ucl.ac.uk",
            "contact_email": "contact@ucl.ac.uk",
            "info_email": "info@ucl.ac.uk",
            "all_emails": "admissions@ucl.ac.uk; international@ucl.ac.uk; contact@ucl.ac.uk; info@ucl.ac.uk"
        },
        {
            "university_name": "London School of Economics and Political Science",
            "website": "https://www.lse.ac.uk/",
            "general_email": "admissions@lse.ac.uk",
            "admissions_email": "admissions@lse.ac.uk",
            "international_email": "international@lse.ac.uk",
            "contact_email": "contact@lse.ac.uk",
            "info_email": "info@lse.ac.uk",
            "all_emails": "admissions@lse.ac.uk; international@lse.ac.uk; contact@lse.ac.uk; info@lse.ac.uk"
        },
        {
            "university_name": "University of Edinburgh",
            "website": "https://www.ed.ac.uk/",
            "general_email": "admissions@ed.ac.uk",
            "admissions_email": "admissions@ed.ac.uk",
            "international_email": "international@ed.ac.uk",
            "contact_email": "contact@ed.ac.uk",
            "info_email": "info@ed.ac.uk",
            "all_emails": "admissions@ed.ac.uk; international@ed.ac.uk; contact@ed.ac.uk; info@ed.ac.uk"
        },
        {
            "university_name": "King's College London",
            "website": "https://www.kcl.ac.uk/",
            "general_email": "admissions@kcl.ac.uk",
            "admissions_email": "admissions@kcl.ac.uk",
            "international_email": "international@kcl.ac.uk",
            "contact_email": "contact@kcl.ac.uk",
            "info_email": "info@kcl.ac.uk",
            "all_emails": "admissions@kcl.ac.uk; international@kcl.ac.uk; contact@kcl.ac.uk; info@kcl.ac.uk"
        },
        {
            "university_name": "University of Manchester",
            "website": "https://www.manchester.ac.uk/",
            "general_email": "admissions@manchester.ac.uk",
            "admissions_email": "admissions@manchester.ac.uk",
            "international_email": "international@manchester.ac.uk",
            "contact_email": "contact@manchester.ac.uk",
            "info_email": "info@manchester.ac.uk",
            "all_emails": "admissions@manchester.ac.uk; international@manchester.ac.uk; contact@manchester.ac.uk; info@manchester.ac.uk"
        },
        {
            "university_name": "University of Bristol",
            "website": "https://www.bristol.ac.uk/",
            "general_email": "admissions@bristol.ac.uk",
            "admissions_email": "admissions@bristol.ac.uk",
            "international_email": "international@bristol.ac.uk",
            "contact_email": "contact@bristol.ac.uk",
            "info_email": "info@bristol.ac.uk",
            "all_emails": "admissions@bristol.ac.uk; international@bristol.ac.uk; contact@bristol.ac.uk; info@bristol.ac.uk"
        },
        {
            "university_name": "University of Warwick",
            "website": "https://www.warwick.ac.uk/",
            "general_email": "admissions@warwick.ac.uk",
            "admissions_email": "admissions@warwick.ac.uk",
            "international_email": "international@warwick.ac.uk",
            "contact_email": "contact@warwick.ac.uk",
            "info_email": "info@warwick.ac.uk",
            "all_emails": "admissions@warwick.ac.uk; international@warwick.ac.uk; contact@warwick.ac.uk; info@warwick.ac.uk"
        }
    ]
    return sample_data

def export_to_csv(data, filename):
    """导出数据到CSV文件"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'university_name', 'website', 'general_email', 
            'admissions_email', 'international_email', 
            'contact_email', 'info_email', 'all_emails'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for uni in data:
            writer.writerow(uni)

def main():
    """主函数"""
    print("="*60)
    print("🇬🇧 英国大学邮箱收集演示")
    print("="*60)
    
    # 创建示例数据
    sample_data = create_sample_uk_data()
    
    # 创建导出目录
    export_dir = Path("data/exports")
    export_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = export_dir / f"demo_uk_universities_{timestamp}.csv"
    
    # 导出CSV
    export_to_csv(sample_data, csv_filename)
    
    # 显示统计信息
    total_count = len(sample_data)
    with_emails = len([u for u in sample_data if u.get('all_emails')])
    
    print(f"📁 使用示例数据文件")
    print(f"✅ 成功加载 {total_count} 条记录")
    print(f"✅ CSV文件已导出: {csv_filename}")
    
    print(f"\n📊 数据统计:")
    print(f"   总大学数量: {total_count}")
    print(f"   有邮箱信息: {with_emails} ({with_emails/total_count*100:.1f}%)")
    
    print(f"\n🌍 大学列表:")
    for i, uni in enumerate(sample_data, 1):
        print(f"   {i:2d}. {uni['university_name']}")
        if uni.get('all_emails'):
            emails = uni['all_emails'].split('; ')
            for email in emails[:2]:  # 只显示前2个邮箱
                print(f"       📧 {email}")
        print()
    
    print(f"💡 提示: 完整数据已保存到 {csv_filename}")
    print(f"📖 要收集真实数据，请运行: python run_uk_collection.py")

if __name__ == "__main__":
    main() 