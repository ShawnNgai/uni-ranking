#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版大学邮箱收集器
使用Google搜索和网页解析获取大学官方邮箱
"""

import json
import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from urllib.parse import urljoin, urlparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_collection_simple.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class SimpleEmailCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def load_universities(self, json_file):
        """加载大学数据"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载大学数据失败: {e}")
            return []
    
    def search_university_website(self, university_name, country):
        """搜索大学官网"""
        try:
            # 构建搜索查询
            search_queries = [
                f'"{university_name}" "{country}" official website',
                f'"{university_name}" "{country}" university website',
                f'"{university_name}" "{country}" .edu',
                f'"{university_name}" "{country}" .ac.'
            ]
            
            for query in search_queries:
                try:
                    # 使用Google搜索
                    url = f"https://www.google.com/search?q={query}"
                    response = self.session.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # 查找搜索结果中的链接
                        links = soup.find_all('a', href=True)
                        for link in links:
                            href = link['href']
                            if href.startswith('/url?q='):
                                actual_url = href.split('/url?q=')[1].split('&')[0]
                                if self.is_university_website(actual_url, university_name):
                                    return actual_url
                    
                    time.sleep(1)  # 避免请求过快
                    
                except Exception as e:
                    logging.error(f"搜索查询失败 {query}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            logging.error(f"搜索大学网站失败 {university_name}: {e}")
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
                
                # 解析HTML查找联系页面
                soup = BeautifulSoup(response.content, 'html.parser')
                contact_links = self.find_contact_links(soup, website_url)
                
                # 访问联系页面
                for link in contact_links[:2]:  # 限制访问数量
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
        contact_keywords = ['contact', 'admissions', 'enquiry', 'inquiry', 'info']
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            
            for keyword in contact_keywords:
                if keyword in href or keyword in text:
                    full_url = urljoin(base_url, link['href'])
                    contact_links.append(full_url)
                    break
        
        return contact_links
    
    def extract_emails_from_text(self, text):
        """从文本中提取邮箱"""
        emails = set()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        found_emails = re.findall(email_pattern, text)
        for email in found_emails:
            if self.is_official_email(email):
                emails.add(email.lower())
        
        return emails
    
    def is_official_email(self, email):
        """判断是否为官方邮箱"""
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
    
    def search_emails_google(self, university_name, country):
        """通过Google搜索邮箱"""
        emails = set()
        
        try:
            search_queries = [
                f'"{university_name}" official email contact',
                f'"{university_name}" "{country}" contact email',
                f'"{university_name}" admissions office email'
            ]
            
            for query in search_queries:
                try:
                    url = f"https://www.google.com/search?q={query}"
                    response = self.session.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        emails.update(self.extract_emails_from_text(response.text))
                    
                    time.sleep(1)
                    
                except Exception as e:
                    logging.error(f"Google搜索失败 {query}: {e}")
                    continue
            
        except Exception as e:
            logging.error(f"Google搜索邮箱失败 {university_name}: {e}")
        
        return list(emails)
    
    def collect_emails_batch(self, universities, start_idx, end_idx):
        """批量收集邮箱"""
        results = []
        
        for i in range(start_idx, end_idx):
            university = universities[i]
            rank = university['rank']
            name = university['university']
            country = university['country']
            
            logging.info(f"处理第 {i+1}/{end_idx} 所大学: {name} (排名 {rank})")
            
            # 策略1: 搜索官网并提取邮箱
            website = self.search_university_website(name, country)
            website_emails = []
            
            if website:
                logging.info(f"找到官网: {website}")
                website_emails = self.extract_emails_from_website(website, name)
            
            # 策略2: Google搜索邮箱
            google_emails = self.search_emails_google(name, country)
            
            # 合并邮箱
            all_emails = list(set(website_emails + google_emails))
            
            # 选择最佳邮箱
            official_email = self.select_best_email(all_emails)
            contact_email = self.select_contact_email(all_emails, official_email)
            
            # 更新大学数据
            university['website'] = website or ''
            university['official_email'] = official_email or ''
            university['contact_email'] = contact_email or ''
            university['all_emails_found'] = len(all_emails)
            
            results.append(university)
            
            # 保存进度
            if (i + 1) % 10 == 0:
                self.save_progress(results, f"progress_simple_{start_idx}_{i+1}.json")
            
            # 避免请求过于频繁
            time.sleep(2)
        
        return results
    
    def select_best_email(self, emails):
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
        
        return emails[0] if emails else ""
    
    def select_contact_email(self, emails, official_email):
        """选择联系邮箱"""
        if not emails or len(emails) == 1:
            return ""
        
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
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logging.info(f"数据已导出到: {filename}")
        except Exception as e:
            logging.error(f"导出CSV失败: {e}")

def main():
    """主函数"""
    collector = SimpleEmailCollector()
    
    # 加载大学数据
    universities = collector.load_universities('universities_501_1000.json')
    
    if not universities:
        logging.error("无法加载大学数据")
        return
    
    logging.info(f"开始处理 {len(universities)} 所大学")
    
    # 先处理前50所大学作为测试
    test_batch = 50
    logging.info(f"先处理前 {test_batch} 所大学作为测试")
    
    results = collector.collect_emails_batch(universities, 0, test_batch)
    
    # 统计结果
    with_emails = sum(1 for u in results if u['official_email'])
    logging.info(f"测试完成! 成功获取邮箱的大学: {with_emails}/{len(results)}")
    
    # 保存结果
    collector.save_progress(results, "universities_emails_test.json")
    collector.export_to_csv(results, "universities_emails_test.csv")
    
    # 询问是否继续处理剩余大学
    print(f"\n测试完成! 成功获取邮箱的大学: {with_emails}/{len(results)}")
    print("是否继续处理剩余大学? (y/n): ", end="")
    
    # 这里可以添加用户交互逻辑
    # 暂时自动继续处理
    if len(universities) > test_batch:
        logging.info("继续处理剩余大学...")
        remaining_results = collector.collect_emails_batch(
            universities, test_batch, len(universities)
        )
        results.extend(remaining_results)
        
        # 保存最终结果
        collector.save_progress(results, "universities_emails_final.json")
        collector.export_to_csv(results, "universities_emails_final.csv")
        
        final_with_emails = sum(1 for u in results if u['official_email'])
        logging.info(f"全部完成! 成功获取邮箱的大学: {final_with_emails}/{len(results)}")

if __name__ == "__main__":
    main() 