#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大学官方邮箱收集系统
支持多种策略获取大学官方邮箱
"""

import json
import time
import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_collection.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class UniversityEmailCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ]
        self.contact_keywords = [
            'contact', 'contact us', 'get in touch', 'reach us',
            'admissions', 'admission', 'enquiry', 'inquiry',
            'info', 'information', 'office', 'department',
            'academic', 'student', 'faculty', 'staff'
        ]
        
    def load_universities(self, json_file):
        """加载大学数据"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载大学数据失败: {e}")
            return []
    
    def search_google_for_website(self, university_name, country):
        """通过Google搜索大学官网"""
        try:
            search_query = f'"{university_name}" "{country}" official website'
            url = f"https://www.google.com/search?q={search_query}"
            
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 查找搜索结果中的链接
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if href.startswith('/url?q='):
                        # 提取实际URL
                        actual_url = href.split('/url?q=')[1].split('&')[0]
                        if self.is_university_website(actual_url, university_name):
                            return actual_url
            return None
        except Exception as e:
            logging.error(f"Google搜索失败 {university_name}: {e}")
            return None
    
    def is_university_website(self, url, university_name):
        """判断是否为大学官网"""
        try:
            domain = urlparse(url).netloc.lower()
            university_words = university_name.lower().split()
            
            # 检查域名是否包含大学名称的关键词
            for word in university_words:
                if len(word) > 3 and word in domain:
                    return True
            
            # 检查常见的大学域名模式
            edu_patterns = ['.edu', '.ac.', 'university', 'college', 'institute']
            for pattern in edu_patterns:
                if pattern in domain:
                    return True
                    
            return False
        except:
            return False
    
    def extract_emails_from_website(self, website_url, university_name):
        """从大学官网提取邮箱"""
        emails = set()
        
        try:
            # 获取主页
            response = self.session.get(website_url, timeout=15)
            if response.status_code == 200:
                emails.update(self.extract_emails_from_text(response.text))
                
                # 解析HTML查找联系页面链接
                soup = BeautifulSoup(response.content, 'html.parser')
                contact_links = self.find_contact_links(soup, website_url)
                
                # 访问联系页面
                for link in contact_links[:3]:  # 限制访问数量
                    try:
                        contact_response = self.session.get(link, timeout=10)
                        if contact_response.status_code == 200:
                            emails.update(self.extract_emails_from_text(contact_response.text))
                    except:
                        continue
                        
        except Exception as e:
            logging.error(f"提取邮箱失败 {website_url}: {e}")
        
        return list(emails)
    
    def find_contact_links(self, soup, base_url):
        """查找联系页面链接"""
        contact_links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            
            # 检查链接文本和URL是否包含联系关键词
            for keyword in self.contact_keywords:
                if keyword in href or keyword in text:
                    full_url = urljoin(base_url, link['href'])
                    contact_links.append(full_url)
                    break
        
        return contact_links
    
    def extract_emails_from_text(self, text):
        """从文本中提取邮箱"""
        emails = set()
        
        for pattern in self.email_patterns:
            found_emails = re.findall(pattern, text)
            for email in found_emails:
                # 过滤掉明显的非官方邮箱
                if self.is_official_email(email):
                    emails.add(email.lower())
        
        return emails
    
    def is_official_email(self, email):
        """判断是否为官方邮箱"""
        # 过滤掉明显的非官方邮箱
        exclude_patterns = [
            'example.com', 'test.com', 'sample.com', 'demo.com',
            'noreply', 'no-reply', 'donotreply', 'do-not-reply',
            'webmaster', 'postmaster', 'admin@localhost'
        ]
        
        email_lower = email.lower()
        for pattern in exclude_patterns:
            if pattern in email_lower:
                return False
        
        return True
    
    def search_emails_with_selenium(self, university_name, country):
        """使用Selenium进行更深入的邮箱搜索"""
        emails = set()
        
        try:
            # 配置Chrome选项
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(options=chrome_options)
            
            # 搜索策略1: 大学名 + official email
            search_queries = [
                f'"{university_name}" official email contact',
                f'"{university_name}" "{country}" contact email',
                f'"{university_name}" admissions office email',
                f'"{university_name}" international office email'
            ]
            
            for query in search_queries:
                try:
                    driver.get(f"https://www.google.com/search?q={query}")
                    time.sleep(2)
                    
                    # 提取页面文本中的邮箱
                    page_text = driver.page_source
                    emails.update(self.extract_emails_from_text(page_text))
                    
                except Exception as e:
                    logging.error(f"Selenium搜索失败: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            logging.error(f"Selenium初始化失败: {e}")
        
        return list(emails)
    
    def collect_emails_for_universities(self, universities_data, start_index=0, end_index=None):
        """为大学收集邮箱"""
        if end_index is None:
            end_index = len(universities_data)
        
        results = []
        
        for i in range(start_index, end_index):
            university = universities_data[i]
            rank = university['rank']
            name = university['university']
            country = university['country']
            
            logging.info(f"处理第 {i+1}/{end_index} 所大学: {name} (排名 {rank})")
            
            # 策略1: 搜索官网
            website = self.search_google_for_website(name, country)
            website_emails = []
            
            if website:
                logging.info(f"找到官网: {website}")
                website_emails = self.extract_emails_from_website(website, name)
            
            # 策略2: 使用Selenium搜索
            selenium_emails = self.search_emails_with_selenium(name, country)
            
            # 合并邮箱
            all_emails = list(set(website_emails + selenium_emails))
            
            # 选择最佳邮箱
            official_email = self.select_best_email(all_emails, name)
            contact_email = self.select_contact_email(all_emails, official_email)
            
            # 更新大学数据
            university['website'] = website or ''
            university['official_email'] = official_email or ''
            university['contact_email'] = contact_email or ''
            university['all_emails'] = all_emails
            
            results.append(university)
            
            # 保存进度
            if (i + 1) % 10 == 0:
                self.save_progress(results, f"progress_{start_index}_{i+1}.json")
            
            # 避免请求过于频繁
            time.sleep(2)
        
        return results
    
    def select_best_email(self, emails, university_name):
        """选择最佳官方邮箱"""
        if not emails:
            return ""
        
        # 优先级排序
        priority_patterns = [
            'admissions@', 'admission@', 'info@', 'contact@',
            'international@', 'global@', 'office@', 'admin@'
        ]
        
        for pattern in priority_patterns:
            for email in emails:
                if pattern in email:
                    return email
        
        # 如果没有找到优先级邮箱，返回第一个
        return emails[0]
    
    def select_contact_email(self, emails, official_email):
        """选择联系邮箱"""
        if not emails:
            return ""
        
        # 如果只有一个邮箱，返回空
        if len(emails) == 1:
            return ""
        
        # 返回不同于官方邮箱的另一个邮箱
        for email in emails:
            if email != official_email:
                return email
        
        return ""
    
    def save_progress(self, data, filename):
        """保存进度"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"进度已保存到: {filename}")
        except Exception as e:
            logging.error(f"保存进度失败: {e}")
    
    def export_to_csv(self, data, filename):
        """导出为CSV格式"""
        try:
            df = pd.DataFrame(data)
            # 移除all_emails列（因为包含列表）
            if 'all_emails' in df.columns:
                df = df.drop('all_emails', axis=1)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logging.info(f"数据已导出到: {filename}")
        except Exception as e:
            logging.error(f"导出CSV失败: {e}")

def main():
    """主函数"""
    collector = UniversityEmailCollector()
    
    # 加载大学数据
    universities = collector.load_universities('universities_501_1000.json')
    
    if not universities:
        logging.error("无法加载大学数据")
        return
    
    logging.info(f"开始处理 {len(universities)} 所大学")
    
    # 分批处理，避免内存问题
    batch_size = 50
    all_results = []
    
    for i in range(0, len(universities), batch_size):
        end_idx = min(i + batch_size, len(universities))
        logging.info(f"处理批次 {i//batch_size + 1}: {i+1}-{end_idx}")
        
        batch_results = collector.collect_emails_for_universities(
            universities, i, end_idx
        )
        all_results.extend(batch_results)
        
        # 保存批次结果
        collector.save_progress(all_results, f"universities_with_emails_{end_idx}.json")
        collector.export_to_csv(all_results, f"universities_with_emails_{end_idx}.csv")
    
    # 保存最终结果
    collector.save_progress(all_results, "universities_with_emails_final.json")
    collector.export_to_csv(all_results, "universities_with_emails_final.csv")
    
    # 统计结果
    with_emails = sum(1 for u in all_results if u['official_email'])
    logging.info(f"收集完成! 成功获取邮箱的大学: {with_emails}/{len(all_results)}")

if __name__ == "__main__":
    main() 