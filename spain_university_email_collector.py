#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西班牙大学官网邮箱批量抓取脚本
输入：spain_universities_*.csv
输出：spain_universities_emails_日期.csv（大学名称, 邮箱地址）
"""

import requests
from bs4 import BeautifulSoup
import re
import csv
from tqdm import tqdm
from time import sleep
from datetime import datetime

# 邮箱优先关键词
PRIORITY_KEYWORDS = [
    'international', 'cooperation', 'global', 'info', 'contact', 'admission', 'relaciones', 'cooperacion', 'relacionesinternacionales', 'internacional', 'oficina', 'office', 'general'
]

# 邮箱正则
EMAIL_REGEX = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

# 常见联系页面关键词
CONTACT_PATHS = [
    'contact', 'contacto', 'contact-us', 'contactar', 'contactos', 'international', 'internacional', 'info', 'about', 'relaciones', 'cooperacion', 'oficina', 'office'
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def load_universities(filename):
    universities = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['website'] and row['website'].startswith('http') and len(row['name']) > 3:
                universities.append({'name': row['name'], 'website': row['website']})
    return universities

def extract_emails(text):
    emails = re.findall(EMAIL_REGEX, text, re.IGNORECASE)
    return list(set([e.lower() for e in emails]))

def prioritize_email(emails):
    if not emails:
        return None
    for kw in PRIORITY_KEYWORDS:
        for email in emails:
            if kw in email.lower():
                return email
    return emails[0]

def find_contact_pages(base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)
    contact_pages = set()
    for link in links:
        href = link['href'].lower()
        for kw in CONTACT_PATHS:
            if kw in href:
                if href.startswith('http'):
                    contact_pages.add(href)
                elif href.startswith('/'):
                    contact_pages.add(base_url.rstrip('/') + href)
                else:
                    contact_pages.add(base_url.rstrip('/') + '/' + href)
    return list(contact_pages)

def fetch_url(url, timeout=10):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return ''

def collect_email_for_university(uni):
    name = uni['name']
    website = uni['website']
    # 1. 抓取首页
    html = fetch_url(website)
    emails = extract_emails(html)
    # 2. 查找联系页面
    contact_pages = find_contact_pages(website, html)
    for contact_url in contact_pages[:3]:  # 最多访问3个联系页
        contact_html = fetch_url(contact_url)
        emails += extract_emails(contact_html)
        sleep(0.5)
    emails = list(set(emails))
    best_email = prioritize_email(emails)
    return {'name': name, 'email': best_email or ''}

def main():
    # 自动查找最新的西班牙大学列表CSV
    import glob
    files = sorted(glob.glob('spain_universities_*.csv'))
    if not files:
        print('未找到西班牙大学列表CSV，请先运行spain_universities_scraper.py')
        return
    input_csv = files[-1]
    print(f'加载大学列表: {input_csv}')
    universities = load_universities(input_csv)
    print(f'共需抓取 {len(universities)} 所大学邮箱')
    results = []
    for uni in tqdm(universities, ncols=80):
        try:
            result = collect_email_for_university(uni)
            results.append(result)
        except Exception as e:
            results.append({'name': uni['name'], 'email': ''})
    # 导出结果
    out_csv = f'spain_universities_emails_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'email'])
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f'✓ 已导出: {out_csv}')

if __name__ == '__main__':
    main() 