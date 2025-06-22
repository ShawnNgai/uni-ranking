#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查2025年大学排名数据
"""

import sqlite3
import json

def check_2025_rankings():
    """检查2025年大学排名数据"""
    try:
        # 连接数据库
        conn = sqlite3.connect('database/rankings.db')
        cursor = conn.cursor()
        
        # 检查2025年大学数量
        cursor.execute('SELECT COUNT(*) FROM universities WHERE year = 2025')
        count_2025 = cursor.fetchone()[0]
        print(f"2025年大学数量: {count_2025}")
        
        # 获取2025年前10所大学
        cursor.execute('''
            SELECT rank, university, country, research, reputation, employment, international, total_score, star_rating, year 
            FROM universities 
            WHERE year = 2025 
            ORDER BY rank 
            LIMIT 10
        ''')
        
        print("\n2025年前10所大学:")
        print("-" * 80)
        print(f"{'排名':<4} {'大学名称':<35} {'国家':<15} {'总分':<6} {'星级'}")
        print("-" * 80)
        
        for row in cursor.fetchall():
            rank, university, country, research, reputation, employment, international, total_score, star_rating, year = row
            print(f"{rank:<4} {university:<35} {country:<15} {total_score:<6.1f} {star_rating}")
        
        # 获取所有2025年大学数据
        cursor.execute('''
            SELECT rank, university, country, research, reputation, employment, international, total_score, star_rating, year 
            FROM universities 
            WHERE year = 2025 
            ORDER BY rank
        ''')
        
        all_2025_data = cursor.fetchall()
        
        # 按国家统计
        countries = {}
        for row in all_2025_data:
            country = row[2]
            if country not in countries:
                countries[country] = 0
            countries[country] += 1
        
        print(f"\n2025年各国大学数量统计:")
        print("-" * 40)
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
            print(f"{country:<20} {count}")
        
        # 导出为JSON文件
        universities_2025 = []
        for row in all_2025_data:
            universities_2025.append({
                'rank': row[0],
                'university': row[1],
                'country': row[2],
                'research': row[3],
                'reputation': row[4],
                'employment': row[5],
                'international': row[6],
                'total_score': row[7],
                'star_rating': row[8],
                'year': row[9]
            })
        
        with open('2025_university_rankings.json', 'w', encoding='utf-8') as f:
            json.dump(universities_2025, f, ensure_ascii=False, indent=2)
        
        print(f"\n已导出2025年大学排名数据到: 2025_university_rankings.json")
        print(f"总共包含 {len(universities_2025)} 所大学")
        
        conn.close()
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    check_2025_rankings() 