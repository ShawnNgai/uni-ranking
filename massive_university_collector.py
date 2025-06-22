#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大规模全球大学邮箱收集器
目标：采集前1万所大学的官方邮箱
特性：支持断点续抓，自动保存进度
"""

import asyncio
import aiohttp
import pandas as pd
import re
import json
import time
import logging
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set, Optional
import csv
from datetime import datetime
import random
from bs4 import BeautifulSoup
import os
import pickle

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('massive_collector.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MassiveUniversityCollector:
    def __init__(self, max_universities=10000):
        self.session = None
        self.max_universities = max_universities
        self.processed_urls = set()
        self.progress_file = 'progress_universities.pkl'
        self.results_file = 'universities_emails.csv'
        
        # 邮箱匹配模式
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.\s*[A-Z|a-z]{2,}\b'
        ]
        
        # 优先级邮箱关键词
        self.priority_keywords = [
            'international', 'global', 'cooperation', 'partnership', 'info', 
            'contact', 'general', 'office', 'administration', 'admissions'
        ]
        
        # 数据源配置
        self.data_sources = {
            '4icu': {
                'base_url': 'https://www.4icu.org/top-universities-world/',
                'pages': 50,  # 4ICU前50页，每页约200所大学
                'pattern': r'https://www\.4icu\.org/reviews/universities/\d+\.htm'
            },
            'webometrics': {
                'base_url': 'https://www.webometrics.info/en/world',
                'pages': 50,  # Webometrics前50页
                'pattern': r'https://www\.webometrics\.info/en/Detail/\d+'
            }
        }
        
        # 加载进度
        self.load_progress()

    def load_progress(self):
        """加载进度"""
        self.completed_universities = set()
        self.universities_list = []
        
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'rb') as f:
                    data = pickle.load(f)
                    self.completed_universities = data.get('completed', set())
                    self.universities_list = data.get('universities', [])
                logger.info(f"加载进度：已完成 {len(self.completed_universities)} 所大学")
            except Exception as e:
                logger.error(f"加载进度文件失败: {e}")

    def save_progress(self):
        """保存进度"""
        try:
            data = {
                'completed': self.completed_universities,
                'universities': self.universities_list,
                'timestamp': datetime.now().isoformat()
            }
            with open(self.progress_file, 'wb') as f:
                pickle.dump(data, f)
            logger.info(f"保存进度：已完成 {len(self.completed_universities)} 所大学")
        except Exception as e:
            logger.error(f"保存进度失败: {e}")

    async def init_session(self):
        """初始化异步会话"""
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )

    async def close_session(self):
        """关闭会话"""
        if self.session:
            await self.session.close()

    def extract_emails_from_text(self, text: str) -> List[str]:
        """从文本中提取邮箱地址"""
        emails = []
        for pattern in self.email_patterns:
            found_emails = re.findall(pattern, text, re.IGNORECASE)
            for email in found_emails:
                email = email.strip()
                email = re.sub(r'\s+', '', email)
                if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email):
                    emails.append(email.lower())
        return list(set(emails))

    def prioritize_emails(self, emails: List[str]) -> List[str]:
        """根据关键词优先级排序邮箱"""
        if not emails:
            return []
        
        prioritized = []
        others = []
        
        for email in emails:
            email_lower = email.lower()
            is_priority = any(keyword in email_lower for keyword in self.priority_keywords)
            
            if is_priority:
                prioritized.append(email)
            else:
                others.append(email)
        
        return prioritized + others

    async def fetch_page_content(self, url: str) -> Optional[str]:
        """异步获取页面内容"""
        if url in self.processed_urls:
            return None
        
        self.processed_urls.add(url)
        
        try:
            async with self.session.get(url, allow_redirects=True) as response:
                if response.status == 200:
                    content = await response.text()
                    return content
                else:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    async def collect_universities_from_4icu(self) -> List[Dict]:
        """从4ICU收集大学信息"""
        universities = []
        
        for page in range(1, self.data_sources['4icu']['pages'] + 1):
            if len(universities) >= self.max_universities:
                break
                
            url = f"{self.data_sources['4icu']['base_url']}page-{page}.htm"
            logger.info(f"正在采集4ICU第{page}页: {url}")
            
            try:
                content = await self.fetch_page_content(url)
                if not content:
                    continue
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # 查找大学链接
                university_links = soup.find_all('a', href=re.compile(r'/reviews/universities/\d+\.htm'))
                
                for link in university_links:
                    if len(universities) >= self.max_universities:
                        break
                    
                    href = link.get('href', '')
                    name = link.get_text().strip()
                    
                    if name and href:
                        # 获取大学详情页
                        detail_url = urljoin(url, href)
                        detail_content = await self.fetch_page_content(detail_url)
                        
                        if detail_content:
                            detail_soup = BeautifulSoup(detail_content, 'html.parser')
                            
                            # 查找官网链接
                            website = ""
                            website_links = detail_soup.find_all('a', href=True)
                            for web_link in website_links:
                                web_href = web_link.get('href', '')
                                if (web_href.startswith('http') and 
                                    not web_href.startswith('https://www.4icu.org') and
                                    any(keyword in web_link.get_text().lower() for keyword in ['website', 'official', 'homepage'])):
                                    website = web_href
                                    break
                            
                            # 如果没有找到明确的官网链接，尝试从页面中提取
                            if not website:
                                for web_link in website_links:
                                    web_href = web_link.get('href', '')
                                    if (web_href.startswith('http') and 
                                        not web_href.startswith('https://www.4icu.org') and
                                        '.edu' in web_href or '.ac.' in web_href or '.university' in web_href):
                                        website = web_href
                                        break
                            
                            if website:
                                universities.append({
                                    'name': name,
                                    'website': website,
                                    'source': '4icu',
                                    'country': self.extract_country_from_url(website)
                                })
                                logger.info(f"✓ 4ICU: {name} -> {website}")
                        
                        await asyncio.sleep(0.5)  # 避免请求过快
                
                await asyncio.sleep(1)  # 页面间暂停
                
            except Exception as e:
                logger.error(f"处理4ICU第{page}页时出错: {e}")
                continue
        
        logger.info(f"从4ICU收集到 {len(universities)} 所大学")
        return universities

    async def collect_universities_from_webometrics(self) -> List[Dict]:
        """从Webometrics收集大学信息"""
        universities = []
        
        for page in range(1, self.data_sources['webometrics']['pages'] + 1):
            if len(universities) >= self.max_universities:
                break
                
            url = f"{self.data_sources['webometrics']['base_url']}?page={page}"
            logger.info(f"正在采集Webometrics第{page}页: {url}")
            
            try:
                content = await self.fetch_page_content(url)
                if not content:
                    continue
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # 查找大学链接
                university_links = soup.find_all('a', href=re.compile(r'/en/Detail/\d+'))
                
                for link in university_links:
                    if len(universities) >= self.max_universities:
                        break
                    
                    href = link.get('href', '')
                    name = link.get_text().strip()
                    
                    if name and href:
                        # 获取大学详情页
                        detail_url = urljoin(url, href)
                        detail_content = await self.fetch_page_content(detail_url)
                        
                        if detail_content:
                            detail_soup = BeautifulSoup(detail_content, 'html.parser')
                            
                            # 查找官网链接
                            website = ""
                            website_links = detail_soup.find_all('a', href=True)
                            for web_link in website_links:
                                web_href = web_link.get('href', '')
                                if (web_href.startswith('http') and 
                                    not web_href.startswith('https://www.webometrics.info') and
                                    any(keyword in web_link.get_text().lower() for keyword in ['website', 'official', 'homepage'])):
                                    website = web_href
                                    break
                            
                            if website:
                                universities.append({
                                    'name': name,
                                    'website': website,
                                    'source': 'webometrics',
                                    'country': self.extract_country_from_url(website)
                                })
                                logger.info(f"✓ Webometrics: {name} -> {website}")
                        
                        await asyncio.sleep(0.5)
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"处理Webometrics第{page}页时出错: {e}")
                continue
        
        logger.info(f"从Webometrics收集到 {len(universities)} 所大学")
        return universities

    def extract_country_from_url(self, url: str) -> str:
        """从URL推断国家"""
        url_lower = url.lower()
        
        country_mapping = {
            '.edu': 'USA',
            '.ac.uk': 'UK',
            '.ca': 'Canada',
            '.au': 'Australia',
            '.de': 'Germany',
            '.fr': 'France',
            '.jp': 'Japan',
            '.cn': 'China',
            '.in': 'India',
            '.br': 'Brazil',
            '.mx': 'Mexico',
            '.es': 'Spain',
            '.it': 'Italy',
            '.nl': 'Netherlands',
            '.se': 'Sweden',
            '.no': 'Norway',
            '.dk': 'Denmark',
            '.fi': 'Finland',
            '.ch': 'Switzerland',
            '.at': 'Austria',
            '.be': 'Belgium',
            '.ie': 'Ireland',
            '.nz': 'New Zealand',
            '.za': 'South Africa',
            '.kr': 'South Korea',
            '.sg': 'Singapore',
            '.my': 'Malaysia',
            '.th': 'Thailand',
            '.vn': 'Vietnam',
            '.id': 'Indonesia',
            '.ph': 'Philippines',
            '.pk': 'Pakistan',
            '.bd': 'Bangladesh',
            '.lk': 'Sri Lanka',
            '.np': 'Nepal',
            '.mm': 'Myanmar',
            '.kh': 'Cambodia',
            '.la': 'Laos',
            '.mn': 'Mongolia',
            '.kz': 'Kazakhstan',
            '.uz': 'Uzbekistan',
            '.kg': 'Kyrgyzstan',
            '.tj': 'Tajikistan',
            '.tm': 'Turkmenistan',
            '.af': 'Afghanistan',
            '.ir': 'Iran',
            '.iq': 'Iraq',
            '.sa': 'Saudi Arabia',
            '.ae': 'UAE',
            '.kw': 'Kuwait',
            '.qa': 'Qatar',
            '.bh': 'Bahrain',
            '.om': 'Oman',
            '.ye': 'Yemen',
            '.jo': 'Jordan',
            '.lb': 'Lebanon',
            '.sy': 'Syria',
            '.ps': 'Palestine',
            '.il': 'Israel',
            '.tr': 'Turkey',
            '.cy': 'Cyprus',
            '.gr': 'Greece',
            '.bg': 'Bulgaria',
            '.ro': 'Romania',
            '.hu': 'Hungary',
            '.cz': 'Czech Republic',
            '.sk': 'Slovakia',
            '.pl': 'Poland',
            '.lt': 'Lithuania',
            '.lv': 'Latvia',
            '.ee': 'Estonia',
            '.ru': 'Russia',
            '.ua': 'Ukraine',
            '.by': 'Belarus',
            '.md': 'Moldova',
            '.ge': 'Georgia',
            '.am': 'Armenia',
            '.az': 'Azerbaijan',
            '.rs': 'Serbia',
            '.hr': 'Croatia',
            '.si': 'Slovenia',
            '.ba': 'Bosnia and Herzegovina',
            '.me': 'Montenegro',
            '.mk': 'North Macedonia',
            '.al': 'Albania',
            '.xk': 'Kosovo',
            '.pt': 'Portugal',
            '.mt': 'Malta',
            '.is': 'Iceland',
            '.fo': 'Faroe Islands',
            '.gl': 'Greenland',
            '.cl': 'Chile',
            '.ar': 'Argentina',
            '.pe': 'Peru',
            '.co': 'Colombia',
            '.ve': 'Venezuela',
            '.ec': 'Ecuador',
            '.bo': 'Bolivia',
            '.py': 'Paraguay',
            '.uy': 'Uruguay',
            '.gy': 'Guyana',
            '.sr': 'Suriname',
            '.gf': 'French Guiana',
            '.fk': 'Falkland Islands',
            '.gs': 'South Georgia',
            '.br': 'Brazil',
            '.mx': 'Mexico',
            '.gt': 'Guatemala',
            '.bz': 'Belize',
            '.sv': 'El Salvador',
            '.hn': 'Honduras',
            '.ni': 'Nicaragua',
            '.cr': 'Costa Rica',
            '.pa': 'Panama',
            '.cu': 'Cuba',
            '.jm': 'Jamaica',
            '.ht': 'Haiti',
            '.do': 'Dominican Republic',
            '.pr': 'Puerto Rico',
            '.tt': 'Trinidad and Tobago',
            '.bb': 'Barbados',
            '.gd': 'Grenada',
            '.lc': 'Saint Lucia',
            '.vc': 'Saint Vincent and the Grenadines',
            '.ag': 'Antigua and Barbuda',
            '.kn': 'Saint Kitts and Nevis',
            '.dm': 'Dominica',
            '.bs': 'Bahamas',
            '.bz': 'Belize',
            '.bz': 'Belize',
        }
        
        for domain, country in country_mapping.items():
            if domain in url_lower:
                return country
        
        return "Unknown"

    async def collect_all_universities(self) -> List[Dict]:
        """收集所有大学信息"""
        all_universities = []
        
        # 如果已有大学列表，直接使用
        if self.universities_list:
            all_universities = self.universities_list
            logger.info(f"使用已保存的大学列表: {len(all_universities)} 所")
        else:
            # 从4ICU收集
            logger.info("开始从4ICU收集大学信息...")
            universities_4icu = await self.collect_universities_from_4icu()
            all_universities.extend(universities_4icu)
            
            # 如果不足1万，从Webometrics补充
            if len(all_universities) < self.max_universities:
                logger.info("开始从Webometrics收集大学信息...")
                universities_webometrics = await self.collect_universities_from_webometrics()
                all_universities.extend(universities_webometrics)
            
            # 去重并限制数量
            unique_universities = []
            seen_names = set()
            
            for uni in all_universities:
                if len(unique_universities) >= self.max_universities:
                    break
                name_key = uni['name'].lower().strip()
                if name_key not in seen_names:
                    seen_names.add(name_key)
                    unique_universities.append(uni)
            
            all_universities = unique_universities
            self.universities_list = all_universities
            self.save_progress()
        
        logger.info(f"总共收集到 {len(all_universities)} 所大学")
        return all_universities

    async def collect_emails_for_universities(self, universities: List[Dict]) -> List[Dict]:
        """为大学收集邮箱地址"""
        results = []
        
        # 使用信号量限制并发数
        semaphore = asyncio.Semaphore(10)
        
        async def collect_email_for_university(university):
            async with semaphore:
                return await self.collect_single_university_email(university)
        
        # 分批处理
        batch_size = 50
        for i in range(0, len(universities), batch_size):
            batch = universities[i:i+batch_size]
            logger.info(f"处理第 {i//batch_size + 1} 批大学 ({len(batch)} 所)")
            
            tasks = []
            for uni in batch:
                # 跳过已完成的大学
                if uni['name'] in self.completed_universities:
                    continue
                tasks.append(collect_email_for_university(uni))
            
            if tasks:
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # 过滤有效结果
                for result in batch_results:
                    if isinstance(result, dict):
                        results.append(result)
                        self.completed_universities.add(result['university_name'])
                    else:
                        logger.error(f"收集邮箱时出现异常: {result}")
                
                # 保存进度
                self.save_progress()
            
            # 批次间暂停
            await asyncio.sleep(2)
        
        return results

    async def collect_single_university_email(self, university: Dict) -> Dict:
        """收集单个大学的邮箱"""
        university_name = university['name']
        website = university.get('website', '')
        country = university.get('country', 'Unknown')
        
        if not website:
            return {
                'university_name': university_name,
                'country': country,
                'website': '',
                'email': '',
                'emails_found': 0,
                'source': university.get('source', 'unknown')
            }
        
        try:
            # 尝试从主页获取邮箱
            content = await self.fetch_page_content(website)
            if not content:
                return {
                    'university_name': university_name,
                    'country': country,
                    'website': website,
                    'email': '',
                    'emails_found': 0,
                    'source': university.get('source', 'unknown')
                }
            
            # 提取邮箱
            emails = self.extract_emails_from_text(content)
            prioritized_emails = self.prioritize_emails(emails)
            
            best_email = prioritized_emails[0] if prioritized_emails else ''
            
            result = {
                'university_name': university_name,
                'country': country,
                'website': website,
                'email': best_email,
                'emails_found': len(emails),
                'source': university.get('source', 'unknown')
            }
            
            if best_email:
                logger.info(f"✓ {university_name}: {best_email}")
            else:
                logger.warning(f"✗ {university_name}: 未找到邮箱")
            
            return result
            
        except Exception as e:
            logger.error(f"处理 {university_name} 时出错: {str(e)}")
            return {
                'university_name': university_name,
                'country': country,
                'website': website,
                'email': '',
                'emails_found': 0,
                'source': university.get('source', 'unknown'),
                'error': str(e)
            }

    def export_to_csv(self, results: List[Dict], filename: str = None):
        """导出结果到CSV文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'global_universities_emails_{timestamp}.csv'
        
        # 准备CSV数据
        csv_data = []
        for result in results:
            if result.get('email'):
                csv_data.append({
                    'university_name': result['university_name'],
                    'email': result['email']
                })
        
        # 写入CSV文件
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['university_name', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in csv_data:
                writer.writerow(row)
        
        logger.info(f"✓ 成功导出 {len(csv_data)} 条记录到 {filename}")
        return filename

    def generate_summary_report(self, results: List[Dict]):
        """生成汇总报告"""
        total_universities = len(results)
        universities_with_emails = len([r for r in results if r.get('email')])
        total_emails_found = sum(r.get('emails_found', 0) for r in results)
        
        # 按国家统计
        country_stats = {}
        for result in results:
            country = result.get('country', 'Unknown')
            if country not in country_stats:
                country_stats[country] = {'total': 0, 'with_emails': 0}
            country_stats[country]['total'] += 1
            if result.get('email'):
                country_stats[country]['with_emails'] += 1
        
        # 按数据源统计
        source_stats = {}
        for result in results:
            source = result.get('source', 'unknown')
            if source not in source_stats:
                source_stats[source] = {'total': 0, 'with_emails': 0}
            source_stats[source]['total'] += 1
            if result.get('email'):
                source_stats[source]['with_emails'] += 1
        
        # 生成报告
        report = f"""
=== 大规模全球大学邮箱收集报告 ===
收集时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
目标数量: {self.max_universities}

总体统计:
- 总大学数量: {total_universities}
- 成功获取邮箱: {universities_with_emails}
- 成功率: {universities_with_emails/total_universities*100:.1f}%
- 总邮箱数量: {total_emails_found}

按国家统计 (前20):
"""
        
        sorted_countries = sorted(country_stats.items(), key=lambda x: x[1]['total'], reverse=True)
        for country, stats in sorted_countries[:20]:
            success_rate = stats['with_emails'] / stats['total'] * 100 if stats['total'] > 0 else 0
            report += f"- {country}: {stats['with_emails']}/{stats['total']} ({success_rate:.1f}%)\n"
        
        report += "\n按数据源统计:\n"
        for source, stats in source_stats.items():
            success_rate = stats['with_emails'] / stats['total'] * 100 if stats['total'] > 0 else 0
            report += f"- {source}: {stats['with_emails']}/{stats['total']} ({success_rate:.1f}%)\n"
        
        # 保存报告
        report_filename = f'massive_collection_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"✓ 汇总报告已保存到 {report_filename}")
        print(report)
        
        return report_filename

async def main():
    """主函数"""
    print("=== 大规模全球大学邮箱收集器 ===")
    print("目标：采集前1万所大学的官方邮箱")
    print("特性：支持断点续抓，自动保存进度")
    print()
    
    # 创建收集器实例
    collector = MassiveUniversityCollector(max_universities=10000)
    
    try:
        # 初始化会话
        await collector.init_session()
        
        # 收集大学信息
        print("第一步：收集大学信息...")
        universities = await collector.collect_all_universities()
        
        print(f"收集到 {len(universities)} 所大学信息")
        
        # 收集邮箱
        print("\n第二步：收集邮箱地址...")
        results = await collector.collect_emails_for_universities(universities)
        
        # 关闭会话
        await collector.close_session()
        
        # 导出到CSV
        print("\n第三步：导出结果...")
        csv_filename = collector.export_to_csv(results)
        
        # 生成汇总报告
        print("\n第四步：生成汇总报告...")
        report_filename = collector.generate_summary_report(results)
        
        print(f"\n✓ 收集完成！")
        print(f"✓ CSV文件: {csv_filename}")
        print(f"✓ 报告文件: {report_filename}")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
        collector.save_progress()
        await collector.close_session()
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        logger.error(f"主程序错误: {str(e)}")
        collector.save_progress()
        await collector.close_session()

if __name__ == "__main__":
    asyncio.run(main()) 