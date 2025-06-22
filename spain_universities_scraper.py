#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
维基百科西班牙大学列表抓取器
获取西班牙所有96所大学的信息
"""

import requests
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime

def get_spain_universities():
    """从维基百科获取西班牙大学列表"""
    
    # 西班牙大学列表页面
    url = "https://en.wikipedia.org/wiki/List_of_universities_in_Spain"
    
    try:
        print("正在获取西班牙大学列表...")
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        universities = []
        
        # 方法1：查找所有表格
        tables = soup.find_all('table')
        
        print(f"找到 {len(tables)} 个表格")
        
        for i, table in enumerate(tables):
            print(f"处理表格 {i+1}...")
            
            # 查找表格中的所有链接
            links = table.find_all('a')
            
            for link in links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                # 检查是否是大学链接
                if (text and len(text) > 5 and 
                    any(keyword in text.lower() for keyword in ['university', 'universidad', 'college', 'institute']) and
                    not text.startswith('[') and
                    not text.startswith('http')):
                    
                    # 获取父行信息
                    row = link.find_parent('tr')
                    if row:
                        cells = row.find_all(['td', 'th'])
                        
                        # 提取城市信息
                        city = ""
                        founded = ""
                        website = ""
                        
                        if len(cells) > 1:
                            city = cells[1].get_text().strip()
                        if len(cells) > 2:
                            founded = cells[2].get_text().strip()
                        
                        # 查找网站链接
                        for cell in cells:
                            cell_links = cell.find_all('a')
                            for cell_link in cell_links:
                                cell_href = cell_link.get('href', '')
                                if cell_href.startswith('http') and not cell_href.startswith('https://en.wikipedia.org'):
                                    website = cell_href
                                    break
                            if website:
                                break
                        
                        # 检查是否已存在
                        existing = [u for u in universities if u['name'] == text]
                        if not existing:
                            universities.append({
                                'name': text,
                                'city': city,
                                'founded': founded,
                                'website': website
                            })
                            print(f"  ✓ {text}")
        
        # 方法2：查找列表项
        lists = soup.find_all(['ul', 'ol'])
        
        for ul in lists:
            items = ul.find_all('li')
            for item in items:
                text = item.get_text().strip()
                
                if (text and len(text) > 10 and 
                    any(keyword in text.lower() for keyword in ['university', 'universidad', 'college', 'institute'])):
                    
                    # 提取大学名称
                    university_name = text.split('(')[0].split('[')[0].strip()
                    
                    # 查找网站链接
                    website = ""
                    links = item.find_all('a')
                    for link in links:
                        href = link.get('href', '')
                        if href.startswith('http') and not href.startswith('https://en.wikipedia.org'):
                            website = href
                            break
                    
                    # 检查是否已存在
                    existing = [u for u in universities if u['name'] == university_name]
                    if not existing and len(university_name) > 5:
                        universities.append({
                            'name': university_name,
                            'city': '',
                            'founded': '',
                            'website': website
                        })
                        print(f"  ✓ {university_name}")
        
        print(f"找到 {len(universities)} 所西班牙大学")
        return universities
        
    except Exception as e:
        print(f"获取数据时出错: {e}")
        return []

def save_to_csv(universities, filename=None):
    """保存大学信息到CSV文件"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'spain_universities_{timestamp}.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'city', 'founded', 'website']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for uni in universities:
            writer.writerow(uni)
    
    print(f"✓ 已保存到 {filename}")
    return filename

def print_universities(universities):
    """打印大学列表"""
    print(f"\n=== 西班牙大学列表 (共{len(universities)}所) ===")
    print()
    
    for i, uni in enumerate(universities, 1):
        print(f"{i:2d}. {uni['name']}")
        if uni['city']:
            print(f"    城市: {uni['city']}")
        if uni['founded']:
            print(f"    成立: {uni['founded']}")
        if uni['website']:
            print(f"    网站: {uni['website']}")
        print()

def main():
    """主函数"""
    print("=== 维基百科西班牙大学列表抓取器 ===")
    print()
    
    # 获取大学列表
    universities = get_spain_universities()
    
    if universities:
        # 打印列表
        print_universities(universities)
        
        # 保存到CSV
        csv_filename = save_to_csv(universities)
        
        print(f"✓ 完成！共获取 {len(universities)} 所西班牙大学")
        print(f"✓ CSV文件: {csv_filename}")
    else:
        print("❌ 未能获取到大学数据")

if __name__ == "__main__":
    main() 