#!/usr/bin/env python3
"""
快速导出西班牙大学数据
"""

import sys
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def find_latest_data():
    """查找最新的数据文件"""
    data_dir = Path("data")
    
    if not data_dir.exists():
        print("❌ 数据目录不存在，请先运行数据收集脚本")
        return None
    
    # 查找数据文件
    data_files = list(data_dir.glob("spain_universities_*.json"))
    
    if not data_files:
        print("❌ 未找到数据文件，请先运行数据收集脚本")
        return None
    
    # 获取最新文件
    latest_file = max(data_files, key=lambda x: x.stat().st_mtime)
    return latest_file

def load_data(file_path):
    """加载数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ 加载数据失败: {str(e)}")
        return None

def prepare_data_for_export(data):
    """准备导出数据"""
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
    
    return export_data

def export_to_csv(data, filename):
    """导出为CSV"""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"✅ CSV文件已导出: {filename}")

def export_to_excel(data, filename):
    """导出为Excel"""
    df = pd.DataFrame(data)
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 主数据表
        df.to_excel(writer, sheet_name='大学数据', index=False)
        
        # 统计信息
        stats = [
            {"项目": "总大学数量", "数值": len(data)},
            {"项目": "有官方邮箱", "数值": len([u for u in data if u.get('官方邮箱')])},
            {"项目": "有校长邮箱", "数值": len([u for u in data if u.get('校长邮箱')])},
            {"项目": "有行政邮箱", "数值": len([u for u in data if u.get('行政邮箱')])},
        ]
        stats_df = pd.DataFrame(stats)
        stats_df.to_excel(writer, sheet_name='统计信息', index=False)
        
        # 地区分布
        regions = {}
        for uni in data:
            region = uni.get('地区', '未知')
            regions[region] = regions.get(region, 0) + 1
        
        region_data = [{"地区": k, "数量": v} for k, v in regions.items()]
        region_df = pd.DataFrame(region_data)
        region_df.to_excel(writer, sheet_name='地区分布', index=False)
    
    print(f"✅ Excel文件已导出: {filename}")

def main():
    """主函数"""
    print("="*60)
    print("📤 西班牙大学数据快速导出")
    print("="*60)
    
    # 查找数据文件
    data_file = find_latest_data()
    if not data_file:
        sys.exit(1)
    
    print(f"📁 找到数据文件: {data_file}")
    
    # 加载数据
    data = load_data(data_file)
    if not data:
        sys.exit(1)
    
    print(f"✅ 成功加载 {len(data)} 条记录")
    
    # 准备导出数据
    export_data = prepare_data_for_export(data)
    
    # 创建输出目录
    os.makedirs("data/exports", exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 导出CSV
    csv_filename = f"data/exports/spain_universities_{timestamp}.csv"
    export_to_csv(export_data, csv_filename)
    
    # 导出Excel
    excel_filename = f"data/exports/spain_universities_{timestamp}.xlsx"
    export_to_excel(export_data, excel_filename)
    
    # 统计信息
    print("\n📊 导出统计:")
    print(f"   总大学数量: {len(data)}")
    print(f"   有官方邮箱: {len([u for u in export_data if u.get('官方邮箱')])}")
    print(f"   有校长邮箱: {len([u for u in export_data if u.get('校长邮箱')])}")
    print(f"   有行政邮箱: {len([u for u in export_data if u.get('行政邮箱')])}")
    
    print(f"\n📄 导出文件:")
    print(f"   CSV: {csv_filename}")
    print(f"   Excel: {excel_filename}")
    
    print(f"\n💡 提示:")
    print(f"   - CSV文件可以用Excel打开")
    print(f"   - Excel文件包含多个工作表")
    print(f"   - 文件已保存在 data/exports 目录中")

if __name__ == "__main__":
    main() 