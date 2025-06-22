#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看排名501名开始的大学数据
"""

import sqlite3
import json

def check_rankings_501():
    """查看排名501名开始的大学数据"""
    try:
        # 连接数据库
        conn = sqlite3.connect('database/rankings.db')
        cursor = conn.cursor()
        
        # 获取排名501-600的大学
        cursor.execute('''
            SELECT rank, university, country, research, reputation, employment, international, total_score, star_rating, year 
            FROM universities 
            WHERE year = 2025 AND rank >= 501 AND rank <= 600
            ORDER BY rank
        ''')
        
        universities_501_600 = cursor.fetchall()
        
        print(f"排名501-600的大学数量: {len(universities_501_600)}")
        print("\n排名501-600的大学列表:")
        print("-" * 100)
        print(f"{'排名':<6} {'大学名称':<50} {'国家':<20} {'总分':<6}")
        print("-" * 100)
        
        for row in universities_501_600:
            rank, university, country, research, reputation, employment, international, total_score, star_rating, year = row
            print(f"{rank:<6} {university:<50} {country:<20} {total_score:<6.1f}")
        
        # 获取排名501-1000的大学
        cursor.execute('''
            SELECT rank, university, country, research, reputation, employment, international, total_score, star_rating, year 
            FROM universities 
            WHERE year = 2025 AND rank >= 501 AND rank <= 1000
            ORDER BY rank
        ''')
        
        universities_501_1000 = cursor.fetchall()
        
        print(f"\n排名501-1000的大学总数: {len(universities_501_1000)}")
        
        # 按国家统计
        countries = {}
        for row in universities_501_1000:
            country = row[2]
            if country not in countries:
                countries[country] = 0
            countries[country] += 1
        
        print(f"\n排名501-1000各国大学数量统计:")
        print("-" * 50)
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
            print(f"{country:<25} {count}")
        
        # 导出501-1000名大学数据
        universities_data = []
        for row in universities_501_1000:
            universities_data.append({
                'rank': row[0],
                'university': row[1],
                'country': row[2],
                'research': row[3],
                'reputation': row[4],
                'employment': row[5],
                'international': row[6],
                'total_score': row[7],
                'star_rating': row[8],
                'year': row[9],
                'official_email': '',  # 预留邮箱字段
                'contact_email': '',   # 预留联系邮箱字段
                'website': ''          # 预留网站字段
            })
        
        with open('universities_501_1000.json', 'w', encoding='utf-8') as f:
            json.dump(universities_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n已导出排名501-1000大学数据到: universities_501_1000.json")
        print(f"总共包含 {len(universities_data)} 所大学")
        
        conn.close()
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    check_rankings_501() 