#!/usr/bin/env python3
"""
演示西班牙大学数据导出功能
"""

import sys
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

def demo_export():
    """演示导出功能"""
    print("="*60)
    print("📤 西班牙大学数据导出演示")
    print("="*60)
    
    # 检查示例数据文件
    sample_file = "data/sample_spain_universities.json"
    
    if not os.path.exists(sample_file):
        print(f"❌ 示例数据文件不存在: {sample_file}")
        print("请先运行数据收集脚本或检查文件路径")
        return False
    
    print(f"📁 使用示例数据文件: {sample_file}")
    
    # 加载数据
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 成功加载 {len(data)} 条记录")
    except Exception as e:
        print(f"❌ 加载数据失败: {str(e)}")
        return False
    
    # 准备导出数据
    export_data = []
    for uni in data:
        export_uni = {
            "英文名称": uni.get('name_en', ''),
            "本地名称": uni.get('name_local', ''),
            "国家": uni.get('country', 'Spain'),
            "地区": uni.get('region', ''),
            "城市": uni.get('city', ''),
            "官方网站": uni.get('website', ''),
            "官方邮箱": uni.get('official_email', ''),
            "联系邮箱": uni.get('contact_email', ''),
            "校长邮箱": uni.get('president_email', ''),
            "行政邮箱": uni.get('admin_email', ''),
            "电话": uni.get('phone', ''),
            "地址": uni.get('address', ''),
            "成立年份": uni.get('founded_year', ''),
            "学生数量": uni.get('student_count', ''),
            "教职工数量": uni.get('staff_count', ''),
            "大学类型": uni.get('university_type', ''),
            "世界排名": uni.get('ranking_world', ''),
            "数据来源": uni.get('data_source', ''),
            "备注": uni.get('notes', '')
        }
        export_data.append(export_uni)
    
    # 创建输出目录
    os.makedirs("data/exports", exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 导出CSV
    csv_filename = f"data/exports/demo_spain_universities_{timestamp}.csv"
    try:
        df = pd.DataFrame(export_data)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"✅ CSV文件已导出: {csv_filename}")
    except Exception as e:
        print(f"❌ CSV导出失败: {str(e)}")
    
    # 导出Excel
    excel_filename = f"data/exports/demo_spain_universities_{timestamp}.xlsx"
    try:
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            # 主数据表
            df.to_excel(writer, sheet_name='大学数据', index=False)
            
            # 统计信息
            stats = [
                {"项目": "总大学数量", "数值": len(data)},
                {"项目": "有官方邮箱", "数值": len([u for u in export_data if u.get('官方邮箱')])},
                {"项目": "有校长邮箱", "数值": len([u for u in export_data if u.get('校长邮箱')])},
                {"项目": "有行政邮箱", "数值": len([u for u in export_data if u.get('行政邮箱')])},
            ]
            stats_df = pd.DataFrame(stats)
            stats_df.to_excel(writer, sheet_name='统计信息', index=False)
            
            # 地区分布
            regions = {}
            for uni in export_data:
                region = uni.get('地区', '未知')
                regions[region] = regions.get(region, 0) + 1
            
            region_data = [{"地区": k, "数量": v} for k, v in regions.items()]
            region_df = pd.DataFrame(region_data)
            region_df.to_excel(writer, sheet_name='地区分布', index=False)
        
        print(f"✅ Excel文件已导出: {excel_filename}")
    except Exception as e:
        print(f"❌ Excel导出失败: {str(e)}")
    
    # 显示统计信息
    print("\n📊 数据统计:")
    print(f"   总大学数量: {len(data)}")
    print(f"   有官方邮箱: {len([u for u in export_data if u.get('官方邮箱')])}")
    print(f"   有校长邮箱: {len([u for u in export_data if u.get('校长邮箱')])}")
    print(f"   有行政邮箱: {len([u for u in export_data if u.get('行政邮箱')])}")
    
    # 显示地区分布
    regions = {}
    for uni in export_data:
        region = uni.get('地区', '未知')
        regions[region] = regions.get(region, 0) + 1
    
    print(f"\n🌍 地区分布:")
    for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
        print(f"   {region}: {count}")
    
    # 显示样本数据
    print(f"\n📋 样本数据 (前3条):")
    for i, uni in enumerate(export_data[:3], 1):
        print(f"   {i}. {uni['英文名称']}")
        print(f"      网站: {uni['官方网站']}")
        print(f"      官方邮箱: {uni['官方邮箱']}")
        print(f"      校长邮箱: {uni['校长邮箱']}")
        print()
    
    print(f"📄 导出文件:")
    print(f"   CSV: {csv_filename}")
    print(f"   Excel: {excel_filename}")
    
    print(f"\n💡 使用提示:")
    print(f"   - 可以使用Excel打开CSV文件")
    print(f"   - Excel文件包含多个工作表")
    print(f"   - 文件已保存在 data/exports 目录中")
    print(f"   - 可以运行 python quick_export.py 进行完整导出")
    
    return True

def main():
    """主函数"""
    success = demo_export()
    
    if success:
        print("\n✅ 演示完成!")
    else:
        print("\n❌ 演示失败!")
        sys.exit(1)

if __name__ == "__main__":
    main() 