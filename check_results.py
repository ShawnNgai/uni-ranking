#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析邮箱收集结果
"""

import json
import pandas as pd

def analyze_results():
    """分析邮箱收集结果"""
    
    # 读取测试结果
    try:
        with open('universities_emails_test.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        print("=== 邮箱收集结果分析 ===")
        print(f"测试大学总数: {len(test_data)}")
        
        # 统计成功获取邮箱的大学
        with_emails = [u for u in test_data if u['official_email']]
        success_rate = len(with_emails) / len(test_data) * 100
        
        print(f"成功获取邮箱的大学: {len(with_emails)}")
        print(f"成功率: {success_rate:.1f}%")
        
        print("\n=== 成功获取邮箱的大学 ===")
        for uni in with_emails:
            print(f"排名 {uni['rank']}: {uni['university']} ({uni['country']})")
            print(f"  官方邮箱: {uni['official_email']}")
            if uni['contact_email']:
                print(f"  联系邮箱: {uni['contact_email']}")
            print()
        
        # 按国家统计
        countries = {}
        for uni in with_emails:
            country = uni['country']
            if country not in countries:
                countries[country] = 0
            countries[country] += 1
        
        print("=== 按国家统计 ===")
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
            print(f"{country}: {count} 所大学")
        
        # 分析邮箱域名
        domains = {}
        for uni in with_emails:
            if uni['official_email']:
                domain = uni['official_email'].split('@')[1]
                if domain not in domains:
                    domains[domain] = 0
                domains[domain] += 1
        
        print("\n=== 邮箱域名统计 ===")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
            print(f"{domain}: {count} 个邮箱")
        
    except FileNotFoundError:
        print("未找到测试结果文件")
    
    # 读取最新进度文件
    try:
        with open('progress_simple_50_150.json', 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        
        print(f"\n=== 最新进度分析 ===")
        print(f"已处理大学总数: {len(progress_data)}")
        
        # 统计成功获取邮箱的大学
        with_emails_progress = [u for u in progress_data if u['official_email']]
        success_rate_progress = len(with_emails_progress) / len(progress_data) * 100
        
        print(f"成功获取邮箱的大学: {len(with_emails_progress)}")
        print(f"成功率: {success_rate_progress:.1f}%")
        
        # 显示最近成功的例子
        recent_success = [u for u in progress_data[-20:] if u['official_email']]
        if recent_success:
            print(f"\n=== 最近成功的例子 ===")
            for uni in recent_success:
                print(f"排名 {uni['rank']}: {uni['university']} - {uni['official_email']}")
        
    except FileNotFoundError:
        print("未找到进度文件")

def export_summary():
    """导出汇总报告"""
    try:
        # 读取所有进度文件
        all_data = []
        
        # 读取测试结果
        with open('universities_emails_test.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
            all_data.extend(test_data)
        
        # 读取最新进度
        with open('progress_simple_50_150.json', 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
            all_data.extend(progress_data)
        
        # 去重
        unique_data = []
        seen_ranks = set()
        for uni in all_data:
            if uni['rank'] not in seen_ranks:
                unique_data.append(uni)
                seen_ranks.add(uni['rank'])
        
        # 统计
        total = len(unique_data)
        with_emails = [u for u in unique_data if u['official_email']]
        success_rate = len(with_emails) / total * 100
        
        # 创建汇总报告
        summary = {
            "总处理大学数": total,
            "成功获取邮箱数": len(with_emails),
            "成功率": f"{success_rate:.1f}%",
            "成功获取邮箱的大学": [
                {
                    "排名": uni['rank'],
                    "大学名称": uni['university'],
                    "国家": uni['country'],
                    "官方邮箱": uni['official_email'],
                    "联系邮箱": uni['contact_email'],
                    "网站": uni['website']
                }
                for uni in with_emails
            ]
        }
        
        # 保存汇总报告
        with open('email_collection_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        # 导出CSV
        df = pd.DataFrame(with_emails)
        df = df[['rank', 'university', 'country', 'official_email', 'contact_email', 'website']]
        df.to_csv('successful_emails.csv', index=False, encoding='utf-8-sig')
        
        print(f"\n=== 汇总报告已生成 ===")
        print(f"总处理大学数: {total}")
        print(f"成功获取邮箱数: {len(with_emails)}")
        print(f"成功率: {success_rate:.1f}%")
        print(f"汇总报告: email_collection_summary.json")
        print(f"成功邮箱CSV: successful_emails.csv")
        
    except Exception as e:
        print(f"导出汇总报告失败: {e}")

if __name__ == "__main__":
    analyze_results()
    export_summary() 