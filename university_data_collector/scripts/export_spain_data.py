#!/usr/bin/env python3
"""
西班牙大学数据导出脚本
支持导出为CSV和Excel格式
"""

import sys
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import argparse
from typing import List, Dict, Optional

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def load_latest_data(data_dir: str = "data") -> List[Dict]:
    """加载最新的数据文件"""
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"❌ 数据目录不存在: {data_dir}")
        return []
    
    # 查找最新的数据文件
    data_files = list(data_path.glob("spain_universities_*.json"))
    
    if not data_files:
        print(f"❌ 在 {data_dir} 目录中未找到数据文件")
        return []
    
    # 按修改时间排序，获取最新的文件
    latest_file = max(data_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 找到最新数据文件: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 成功加载 {len(data)} 条记录")
        return data
    except Exception as e:
        print(f"❌ 加载数据失败: {str(e)}")
        return []

def clean_data_for_export(data: List[Dict]) -> List[Dict]:
    """清理数据，准备导出"""
    cleaned_data = []
    
    for uni in data:
        # 创建清理后的记录
        cleaned_uni = {
            # 基本信息
            "英文名称": uni.get('name_en', ''),
            "本地名称": uni.get('name_local', ''),
            "国家": uni.get('country', 'Spain'),
            "地区": uni.get('region', ''),
            "城市": uni.get('city', ''),
            
            # 联系信息
            "官方网站": uni.get('website', ''),
            "官方邮箱": uni.get('official_email', ''),
            "联系邮箱": uni.get('contact_email', ''),
            "校长邮箱": uni.get('president_email', ''),
            "行政邮箱": uni.get('admin_email', ''),
            "电话": uni.get('phone', ''),
            "地址": uni.get('address', ''),
            
            # 地理信息
            "纬度": uni.get('latitude', ''),
            "经度": uni.get('longitude', ''),
            
            # 基本信息
            "成立年份": uni.get('founded_year', ''),
            "学生数量": uni.get('student_count', ''),
            "教职工数量": uni.get('staff_count', ''),
            "大学类型": uni.get('university_type', ''),
            "认证机构": uni.get('accreditation', ''),
            
            # 排名信息
            "国内排名": uni.get('ranking_national', ''),
            "世界排名": uni.get('ranking_world', ''),
            
            # 元数据
            "数据来源": uni.get('data_source', ''),
            "最后验证时间": uni.get('last_verified', ''),
            "备注": uni.get('notes', '')
        }
        
        cleaned_data.append(cleaned_uni)
    
    return cleaned_data

def export_to_csv(data: List[Dict], output_dir: str = "data/exports") -> str:
    """导出为CSV格式"""
    if not data:
        print("❌ 没有数据可导出")
        return ""
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"spain_universities_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)
    
    try:
        # 导出为CSV
        df.to_csv(filepath, index=False, encoding='utf-8-sig')  # 使用utf-8-sig支持中文
        print(f"✅ CSV文件已导出: {filepath}")
        print(f"   记录数量: {len(data)}")
        print(f"   文件大小: {os.path.getsize(filepath) / 1024:.1f} KB")
        return filepath
    except Exception as e:
        print(f"❌ CSV导出失败: {str(e)}")
        return ""

def export_to_excel(data: List[Dict], output_dir: str = "data/exports") -> str:
    """导出为Excel格式"""
    if not data:
        print("❌ 没有数据可导出")
        return ""
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"spain_universities_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    
    try:
        # 创建Excel写入器
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 主数据表
            df.to_excel(writer, sheet_name='大学数据', index=False)
            
            # 统计信息表
            stats_data = generate_statistics(data)
            stats_df = pd.DataFrame(stats_data)
            stats_df.to_excel(writer, sheet_name='统计信息', index=False)
            
            # 地区分布表
            region_data = generate_region_stats(data)
            region_df = pd.DataFrame(region_data)
            region_df.to_excel(writer, sheet_name='地区分布', index=False)
            
            # 城市分布表
            city_data = generate_city_stats(data)
            city_df = pd.DataFrame(city_data)
            city_df.to_excel(writer, sheet_name='城市分布', index=False)
        
        print(f"✅ Excel文件已导出: {filepath}")
        print(f"   记录数量: {len(data)}")
        print(f"   文件大小: {os.path.getsize(filepath) / 1024:.1f} KB")
        print(f"   包含工作表: 大学数据, 统计信息, 地区分布, 城市分布")
        return filepath
    except Exception as e:
        print(f"❌ Excel导出失败: {str(e)}")
        return ""

def generate_statistics(data: List[Dict]) -> List[Dict]:
    """生成统计信息"""
    total_count = len(data)
    with_official_email = len([u for u in data if u.get('官方邮箱')])
    with_president_email = len([u for u in data if u.get('校长邮箱')])
    with_admin_email = len([u for u in data if u.get('行政邮箱')])
    with_ranking = len([u for u in data if u.get('世界排名')])
    
    # 按大学类型统计
    public_count = len([u for u in data if 'public' in u.get('大学类型', '').lower()])
    private_count = len([u for u in data if 'private' in u.get('大学类型', '').lower()])
    
    stats = [
        {"统计项目": "总大学数量", "数值": total_count},
        {"统计项目": "有官方邮箱", "数值": with_official_email, "百分比": f"{with_official_email/total_count*100:.1f}%"},
        {"统计项目": "有校长邮箱", "数值": with_president_email, "百分比": f"{with_president_email/total_count*100:.1f}%"},
        {"统计项目": "有行政邮箱", "数值": with_admin_email, "百分比": f"{with_admin_email/total_count*100:.1f}%"},
        {"统计项目": "有世界排名", "数值": with_ranking, "百分比": f"{with_ranking/total_count*100:.1f}%"},
        {"统计项目": "公立大学", "数值": public_count, "百分比": f"{public_count/total_count*100:.1f}%"},
        {"统计项目": "私立大学", "数值": private_count, "百分比": f"{private_count/total_count*100:.1f}%"},
    ]
    
    return stats

def generate_region_stats(data: List[Dict]) -> List[Dict]:
    """生成地区分布统计"""
    regions = {}
    for uni in data:
        region = uni.get('地区', '未知')
        regions[region] = regions.get(region, 0) + 1
    
    region_stats = []
    for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
        region_stats.append({
            "地区": region,
            "大学数量": count,
            "占比": f"{count/len(data)*100:.1f}%"
        })
    
    return region_stats

def generate_city_stats(data: List[Dict]) -> List[Dict]:
    """生成城市分布统计"""
    cities = {}
    for uni in data:
        city = uni.get('城市', '未知')
        cities[city] = cities.get(city, 0) + 1
    
    city_stats = []
    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
        city_stats.append({
            "城市": city,
            "大学数量": count,
            "占比": f"{count/len(data)*100:.1f}%"
        })
    
    return city_stats

def print_data_summary(data: List[Dict]):
    """打印数据摘要"""
    print("\n" + "="*60)
    print("📊 数据摘要")
    print("="*60)
    
    total_count = len(data)
    print(f"总大学数量: {total_count}")
    
    # 邮箱统计
    with_official = len([u for u in data if u.get('官方邮箱')])
    with_president = len([u for u in data if u.get('校长邮箱')])
    with_admin = len([u for u in data if u.get('行政邮箱')])
    
    print(f"有官方邮箱: {with_official} ({with_official/total_count*100:.1f}%)")
    print(f"有校长邮箱: {with_president} ({with_president/total_count*100:.1f}%)")
    print(f"有行政邮箱: {with_admin} ({with_admin/total_count*100:.1f}%)")
    
    # 地区分布
    regions = {}
    for uni in data:
        region = uni.get('地区', '未知')
        regions[region] = regions.get(region, 0) + 1
    
    print(f"\n地区分布 (前5):")
    for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {region}: {count}")
    
    # 城市分布
    cities = {}
    for uni in data:
        city = uni.get('城市', '未知')
        cities[city] = cities.get(city, 0) + 1
    
    print(f"\n城市分布 (前5):")
    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {city}: {count}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='导出西班牙大学数据')
    parser.add_argument('--format', choices=['csv', 'excel', 'both'], default='both',
                       help='导出格式 (默认: both)')
    parser.add_argument('--data-dir', default='data',
                       help='数据目录 (默认: data)')
    parser.add_argument('--output-dir', default='data/exports',
                       help='输出目录 (默认: data/exports)')
    
    args = parser.parse_args()
    
    print("="*60)
    print("📤 西班牙大学数据导出工具")
    print("="*60)
    
    # 加载数据
    print("\n📁 加载数据...")
    data = load_latest_data(args.data_dir)
    
    if not data:
        print("❌ 无法加载数据，程序退出")
        sys.exit(1)
    
    # 清理数据
    print("\n🧹 清理数据...")
    cleaned_data = clean_data_for_export(data)
    
    # 打印数据摘要
    print_data_summary(cleaned_data)
    
    # 导出数据
    print(f"\n📤 导出数据 (格式: {args.format})...")
    
    exported_files = []
    
    if args.format in ['csv', 'both']:
        csv_file = export_to_csv(cleaned_data, args.output_dir)
        if csv_file:
            exported_files.append(csv_file)
    
    if args.format in ['excel', 'both']:
        excel_file = export_to_excel(cleaned_data, args.output_dir)
        if excel_file:
            exported_files.append(excel_file)
    
    # 总结
    print("\n" + "="*60)
    print("✅ 导出完成!")
    print("="*60)
    
    for file in exported_files:
        print(f"📄 {file}")
    
    print(f"\n💡 提示:")
    print(f"   - CSV文件可以用Excel打开")
    print(f"   - Excel文件包含多个工作表")
    print(f"   - 建议定期备份导出的数据")

if __name__ == "__main__":
    main() 