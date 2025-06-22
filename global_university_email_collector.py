#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球大学官方邮箱收集器
专业版本 - 多源数据收集策略
目标：获取5000+全球大学的官方邮箱
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
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('global_email_collector.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GlobalUniversityEmailCollector:
    def __init__(self):
        self.session = None
        self.results = []
        self.processed_urls = set()
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%+-]+\[at\][A-Za-z0-9.-]+\[dot\][A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.\s*[A-Z|a-z]{2,}\b'
        ]
        
        # 优先级邮箱关键词
        self.priority_keywords = [
            'international', 'global', 'cooperation', 'partnership', 'info', 
            'contact', 'general', 'office', 'administration', 'admissions'
        ]
        
        # 全球大学数据源
        self.university_sources = {
            'times_higher_education': 'https://www.timeshighereducation.com/world-university-rankings',
            'qs_rankings': 'https://www.topuniversities.com/world-university-rankings',
            'shanghai_rankings': 'http://www.shanghairanking.com/rankings/arwu/2023',
            'us_news': 'https://www.usnews.com/best-colleges/rankings/national-universities',
            'cwur': 'http://cwur.org/2023.php'
        }
        
        # 预定义的全球知名大学列表（部分）
        self.global_universities = [
            # 美国
            {'name': 'Harvard University', 'country': 'USA', 'website': 'https://www.harvard.edu'},
            {'name': 'Stanford University', 'country': 'USA', 'website': 'https://www.stanford.edu'},
            {'name': 'Massachusetts Institute of Technology', 'country': 'USA', 'website': 'https://www.mit.edu'},
            {'name': 'University of California, Berkeley', 'country': 'USA', 'website': 'https://www.berkeley.edu'},
            {'name': 'Yale University', 'country': 'USA', 'website': 'https://www.yale.edu'},
            {'name': 'Princeton University', 'country': 'USA', 'website': 'https://www.princeton.edu'},
            {'name': 'Columbia University', 'country': 'USA', 'website': 'https://www.columbia.edu'},
            {'name': 'University of Chicago', 'country': 'USA', 'website': 'https://www.uchicago.edu'},
            {'name': 'University of Pennsylvania', 'country': 'USA', 'website': 'https://www.upenn.edu'},
            {'name': 'California Institute of Technology', 'country': 'USA', 'website': 'https://www.caltech.edu'},
            
            # 英国
            {'name': 'University of Oxford', 'country': 'UK', 'website': 'https://www.ox.ac.uk'},
            {'name': 'University of Cambridge', 'country': 'UK', 'website': 'https://www.cam.ac.uk'},
            {'name': 'Imperial College London', 'country': 'UK', 'website': 'https://www.imperial.ac.uk'},
            {'name': 'University College London', 'country': 'UK', 'website': 'https://www.ucl.ac.uk'},
            {'name': 'London School of Economics', 'country': 'UK', 'website': 'https://www.lse.ac.uk'},
            {'name': 'King\'s College London', 'country': 'UK', 'website': 'https://www.kcl.ac.uk'},
            {'name': 'University of Edinburgh', 'country': 'UK', 'website': 'https://www.ed.ac.uk'},
            {'name': 'University of Manchester', 'country': 'UK', 'website': 'https://www.manchester.ac.uk'},
            {'name': 'University of Bristol', 'country': 'UK', 'website': 'https://www.bristol.ac.uk'},
            {'name': 'University of Warwick', 'country': 'UK', 'website': 'https://www.warwick.ac.uk'},
            
            # 加拿大
            {'name': 'University of Toronto', 'country': 'Canada', 'website': 'https://www.utoronto.ca'},
            {'name': 'University of British Columbia', 'country': 'Canada', 'website': 'https://www.ubc.ca'},
            {'name': 'McGill University', 'country': 'Canada', 'website': 'https://www.mcgill.ca'},
            {'name': 'University of Alberta', 'country': 'Canada', 'website': 'https://www.ualberta.ca'},
            {'name': 'University of Waterloo', 'country': 'Canada', 'website': 'https://uwaterloo.ca'},
            
            # 澳大利亚
            {'name': 'University of Melbourne', 'country': 'Australia', 'website': 'https://www.unimelb.edu.au'},
            {'name': 'Australian National University', 'country': 'Australia', 'website': 'https://www.anu.edu.au'},
            {'name': 'University of Sydney', 'country': 'Australia', 'website': 'https://www.sydney.edu.au'},
            {'name': 'University of Queensland', 'country': 'Australia', 'website': 'https://www.uq.edu.au'},
            {'name': 'Monash University', 'country': 'Australia', 'website': 'https://www.monash.edu'},
            
            # 德国
            {'name': 'Technical University of Munich', 'country': 'Germany', 'website': 'https://www.tum.de'},
            {'name': 'Ludwig Maximilian University of Munich', 'country': 'Germany', 'website': 'https://www.lmu.de'},
            {'name': 'Heidelberg University', 'country': 'Germany', 'website': 'https://www.uni-heidelberg.de'},
            {'name': 'Humboldt University of Berlin', 'country': 'Germany', 'website': 'https://www.hu-berlin.de'},
            {'name': 'Free University of Berlin', 'country': 'Germany', 'website': 'https://www.fu-berlin.de'},
            
            # 法国
            {'name': 'Sorbonne University', 'country': 'France', 'website': 'https://www.sorbonne-universite.fr'},
            {'name': 'École Normale Supérieure', 'country': 'France', 'website': 'https://www.ens.psl.eu'},
            {'name': 'Paris Sciences et Lettres University', 'country': 'France', 'website': 'https://www.psl.eu'},
            {'name': 'École Polytechnique', 'country': 'France', 'website': 'https://www.polytechnique.edu'},
            
            # 荷兰
            {'name': 'Delft University of Technology', 'country': 'Netherlands', 'website': 'https://www.tudelft.nl'},
            {'name': 'University of Amsterdam', 'country': 'Netherlands', 'website': 'https://www.uva.nl'},
            {'name': 'Leiden University', 'country': 'Netherlands', 'website': 'https://www.universiteitleiden.nl'},
            {'name': 'Erasmus University Rotterdam', 'country': 'Netherlands', 'website': 'https://www.eur.nl'},
            
            # 瑞士
            {'name': 'ETH Zurich', 'country': 'Switzerland', 'website': 'https://www.ethz.ch'},
            {'name': 'University of Zurich', 'country': 'Switzerland', 'website': 'https://www.uzh.ch'},
            {'name': 'EPFL', 'country': 'Switzerland', 'website': 'https://www.epfl.ch'},
            
            # 瑞典
            {'name': 'Karolinska Institute', 'country': 'Sweden', 'website': 'https://ki.se'},
            {'name': 'Uppsala University', 'country': 'Sweden', 'website': 'https://www.uu.se'},
            {'name': 'Lund University', 'country': 'Sweden', 'website': 'https://www.lu.se'},
            
            # 丹麦
            {'name': 'University of Copenhagen', 'country': 'Denmark', 'website': 'https://www.ku.dk'},
            {'name': 'Technical University of Denmark', 'country': 'Denmark', 'website': 'https://www.dtu.dk'},
            
            # 挪威
            {'name': 'University of Oslo', 'country': 'Norway', 'website': 'https://www.uio.no'},
            {'name': 'Norwegian University of Science and Technology', 'country': 'Norway', 'website': 'https://www.ntnu.no'},
            
            # 芬兰
            {'name': 'University of Helsinki', 'country': 'Finland', 'website': 'https://www.helsinki.fi'},
            {'name': 'Aalto University', 'country': 'Finland', 'website': 'https://www.aalto.fi'},
            
            # 日本
            {'name': 'University of Tokyo', 'country': 'Japan', 'website': 'https://www.u-tokyo.ac.jp'},
            {'name': 'Kyoto University', 'country': 'Japan', 'website': 'https://www.kyoto-u.ac.jp'},
            {'name': 'Osaka University', 'country': 'Japan', 'website': 'https://www.osaka-u.ac.jp'},
            {'name': 'Tohoku University', 'country': 'Japan', 'website': 'https://www.tohoku.ac.jp'},
            
            # 韩国
            {'name': 'Seoul National University', 'country': 'South Korea', 'website': 'https://www.snu.ac.kr'},
            {'name': 'Korea Advanced Institute of Science and Technology', 'country': 'South Korea', 'website': 'https://www.kaist.ac.kr'},
            {'name': 'Yonsei University', 'country': 'South Korea', 'website': 'https://www.yonsei.ac.kr'},
            
            # 中国
            {'name': 'Tsinghua University', 'country': 'China', 'website': 'https://www.tsinghua.edu.cn'},
            {'name': 'Peking University', 'country': 'China', 'website': 'https://www.pku.edu.cn'},
            {'name': 'Fudan University', 'country': 'China', 'website': 'https://www.fudan.edu.cn'},
            {'name': 'Shanghai Jiao Tong University', 'country': 'China', 'website': 'https://www.sjtu.edu.cn'},
            {'name': 'Zhejiang University', 'country': 'China', 'website': 'https://www.zju.edu.cn'},
            
            # 新加坡
            {'name': 'National University of Singapore', 'country': 'Singapore', 'website': 'https://www.nus.edu.sg'},
            {'name': 'Nanyang Technological University', 'country': 'Singapore', 'website': 'https://www.ntu.edu.sg'},
            
            # 香港
            {'name': 'University of Hong Kong', 'country': 'Hong Kong', 'website': 'https://www.hku.hk'},
            {'name': 'Hong Kong University of Science and Technology', 'country': 'Hong Kong', 'website': 'https://www.ust.hk'},
            {'name': 'Chinese University of Hong Kong', 'country': 'Hong Kong', 'website': 'https://www.cuhk.edu.hk'},
            
            # 台湾
            {'name': 'National Taiwan University', 'country': 'Taiwan', 'website': 'https://www.ntu.edu.tw'},
            {'name': 'National Tsing Hua University', 'country': 'Taiwan', 'website': 'https://www.nthu.edu.tw'},
            
            # 印度
            {'name': 'Indian Institute of Technology Bombay', 'country': 'India', 'website': 'https://www.iitb.ac.in'},
            {'name': 'Indian Institute of Technology Delhi', 'country': 'India', 'website': 'https://www.iitd.ac.in'},
            {'name': 'University of Delhi', 'country': 'India', 'website': 'https://www.du.ac.in'},
            
            # 巴西
            {'name': 'University of São Paulo', 'country': 'Brazil', 'website': 'https://www.usp.br'},
            {'name': 'State University of Campinas', 'country': 'Brazil', 'website': 'https://www.unicamp.br'},
            
            # 墨西哥
            {'name': 'National Autonomous University of Mexico', 'country': 'Mexico', 'website': 'https://www.unam.mx'},
            {'name': 'Monterrey Institute of Technology', 'country': 'Mexico', 'website': 'https://www.tec.mx'},
            
            # 阿根廷
            {'name': 'University of Buenos Aires', 'country': 'Argentina', 'website': 'https://www.uba.ar'},
            
            # 智利
            {'name': 'Pontifical Catholic University of Chile', 'country': 'Chile', 'website': 'https://www.uc.cl'},
            {'name': 'University of Chile', 'country': 'Chile', 'website': 'https://www.uchile.cl'},
            
            # 南非
            {'name': 'University of Cape Town', 'country': 'South Africa', 'website': 'https://www.uct.ac.za'},
            {'name': 'University of the Witwatersrand', 'country': 'South Africa', 'website': 'https://www.wits.ac.za'},
            
            # 埃及
            {'name': 'Cairo University', 'country': 'Egypt', 'website': 'https://cu.edu.eg'},
            {'name': 'Ain Shams University', 'country': 'Egypt', 'website': 'https://www.asu.edu.eg'},
            
            # 以色列
            {'name': 'Hebrew University of Jerusalem', 'country': 'Israel', 'website': 'https://www.huji.ac.il'},
            {'name': 'Tel Aviv University', 'country': 'Israel', 'website': 'https://www.tau.ac.il'},
            {'name': 'Technion - Israel Institute of Technology', 'country': 'Israel', 'website': 'https://www.technion.ac.il'},
            
            # 土耳其
            {'name': 'Middle East Technical University', 'country': 'Turkey', 'website': 'https://www.metu.edu.tr'},
            {'name': 'Bogazici University', 'country': 'Turkey', 'website': 'https://www.boun.edu.tr'},
            
            # 俄罗斯
            {'name': 'Lomonosov Moscow State University', 'country': 'Russia', 'website': 'https://www.msu.ru'},
            {'name': 'Saint Petersburg State University', 'country': 'Russia', 'website': 'https://spbu.ru'},
            
            # 波兰
            {'name': 'University of Warsaw', 'country': 'Poland', 'website': 'https://www.uw.edu.pl'},
            {'name': 'Jagiellonian University', 'country': 'Poland', 'website': 'https://www.uj.edu.pl'},
            
            # 捷克
            {'name': 'Charles University', 'country': 'Czech Republic', 'website': 'https://www.cuni.cz'},
            
            # 匈牙利
            {'name': 'Eötvös Loránd University', 'country': 'Hungary', 'website': 'https://www.elte.hu'},
            
            # 奥地利
            {'name': 'University of Vienna', 'country': 'Austria', 'website': 'https://www.univie.ac.at'},
            
            # 比利时
            {'name': 'KU Leuven', 'country': 'Belgium', 'website': 'https://www.kuleuven.be'},
            {'name': 'Ghent University', 'country': 'Belgium', 'website': 'https://www.ugent.be'},
            
            # 意大利
            {'name': 'University of Bologna', 'country': 'Italy', 'website': 'https://www.unibo.it'},
            {'name': 'Sapienza University of Rome', 'country': 'Italy', 'website': 'https://www.uniroma1.it'},
            {'name': 'University of Milan', 'country': 'Italy', 'website': 'https://www.unimi.it'},
            
            # 西班牙
            {'name': 'University of Barcelona', 'country': 'Spain', 'website': 'https://www.ub.edu'},
            {'name': 'Autonomous University of Madrid', 'country': 'Spain', 'website': 'https://www.uam.es'},
            {'name': 'Complutense University of Madrid', 'country': 'Spain', 'website': 'https://www.ucm.es'},
            {'name': 'University of Valencia', 'country': 'Spain', 'website': 'https://www.uv.es'},
            {'name': 'University of Granada', 'country': 'Spain', 'website': 'https://www.ugr.es'},
            
            # 葡萄牙
            {'name': 'University of Lisbon', 'country': 'Portugal', 'website': 'https://www.ulisboa.pt'},
            {'name': 'University of Porto', 'country': 'Portugal', 'website': 'https://www.up.pt'},
            
            # 爱尔兰
            {'name': 'Trinity College Dublin', 'country': 'Ireland', 'website': 'https://www.tcd.ie'},
            {'name': 'University College Dublin', 'country': 'Ireland', 'website': 'https://www.ucd.ie'},
            
            # 新西兰
            {'name': 'University of Auckland', 'country': 'New Zealand', 'website': 'https://www.auckland.ac.nz'},
            {'name': 'University of Otago', 'country': 'New Zealand', 'website': 'https://www.otago.ac.nz'},
        ]

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
                # 清理邮箱地址
                email = email.strip()
                email = email.replace('[at]', '@').replace('[dot]', '.')
                email = re.sub(r'\s+', '', email)
                
                # 验证邮箱格式
                if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email):
                    emails.append(email.lower())
        
        return list(set(emails))  # 去重

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

    async def extract_emails_from_url(self, url: str) -> List[str]:
        """从URL中提取邮箱地址"""
        content = await self.fetch_page_content(url)
        if not content:
            return []
        
        # 从HTML中提取邮箱
        emails = self.extract_emails_from_text(content)
        
        # 尝试从页面中查找更多邮箱链接
        soup = BeautifulSoup(content, 'html.parser')
        
        # 查找包含邮箱的链接
        email_links = soup.find_all('a', href=re.compile(r'mailto:'))
        for link in email_links:
            href = link.get('href', '')
            if href.startswith('mailto:'):
                email = href[7:]  # 移除 'mailto:'
                if email and '@' in email:
                    emails.append(email.lower())
        
        return list(set(emails))  # 去重

    async def find_contact_pages(self, base_url: str) -> List[str]:
        """查找联系页面"""
        contact_urls = []
        
        try:
            content = await self.fetch_page_content(base_url)
            if not content:
                return contact_urls
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # 查找联系页面链接
            contact_keywords = ['contact', 'about', 'info', 'international', 'global', 'admissions']
            
            for link in soup.find_all('a', href=True):
                href = link.get('href', '').lower()
                text = link.get_text().lower()
                
                # 检查链接文本和URL是否包含联系相关关键词
                if any(keyword in href or keyword in text for keyword in contact_keywords):
                    full_url = urljoin(base_url, link['href'])
                    if full_url.startswith('http'):
                        contact_urls.append(full_url)
            
            # 限制联系页面数量
            return contact_urls[:10]
            
        except Exception as e:
            logger.error(f"Error finding contact pages for {base_url}: {str(e)}")
            return contact_urls

    async def collect_university_emails(self, university: Dict) -> Dict:
        """收集单个大学的邮箱"""
        university_name = university['name']
        website = university['website']
        country = university['country']
        
        logger.info(f"正在处理: {university_name} ({country})")
        
        all_emails = []
        
        try:
            # 1. 从主页提取邮箱
            main_emails = await self.extract_emails_from_url(website)
            all_emails.extend(main_emails)
            
            # 2. 查找并访问联系页面
            contact_pages = await self.find_contact_pages(website)
            
            for contact_url in contact_pages[:5]:  # 限制联系页面数量
                contact_emails = await self.extract_emails_from_url(contact_url)
                all_emails.extend(contact_emails)
                await asyncio.sleep(0.5)  # 避免请求过快
            
            # 去重并排序
            unique_emails = list(set(all_emails))
            prioritized_emails = self.prioritize_emails(unique_emails)
            
            # 选择最佳邮箱
            best_email = prioritized_emails[0] if prioritized_emails else None
            
            result = {
                'university_name': university_name,
                'country': country,
                'website': website,
                'emails_found': len(unique_emails),
                'best_email': best_email,
                'all_emails': prioritized_emails[:3]  # 保存前3个最佳邮箱
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
                'emails_found': 0,
                'best_email': None,
                'all_emails': [],
                'error': str(e)
            }

    async def collect_all_emails(self, max_universities: int = None) -> List[Dict]:
        """收集所有大学的邮箱"""
        await self.init_session()
        
        universities = self.global_universities
        if max_universities:
            universities = universities[:max_universities]
        
        logger.info(f"开始收集 {len(universities)} 所大学的邮箱...")
        
        # 使用信号量限制并发数
        semaphore = asyncio.Semaphore(10)
        
        async def collect_with_semaphore(university):
            async with semaphore:
                return await self.collect_university_emails(university)
        
        # 并发收集邮箱
        tasks = [collect_with_semaphore(uni) for uni in universities]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 过滤掉异常结果
        valid_results = []
        for result in results:
            if isinstance(result, dict):
                valid_results.append(result)
            else:
                logger.error(f"收集过程中出现异常: {result}")
        
        await self.close_session()
        return valid_results

    def export_to_csv(self, results: List[Dict], filename: str = None):
        """导出结果到CSV文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'global_universities_emails_{timestamp}.csv'
        
        # 准备CSV数据
        csv_data = []
        for result in results:
            if result.get('best_email'):
                csv_data.append({
                    'university_name': result['university_name'],
                    'email': result['best_email']
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
        universities_with_emails = len([r for r in results if r.get('best_email')])
        total_emails_found = sum(r.get('emails_found', 0) for r in results)
        
        # 按国家统计
        country_stats = {}
        for result in results:
            country = result.get('country', 'Unknown')
            if country not in country_stats:
                country_stats[country] = {'total': 0, 'with_emails': 0}
            country_stats[country]['total'] += 1
            if result.get('best_email'):
                country_stats[country]['with_emails'] += 1
        
        # 生成报告
        report = f"""
=== 全球大学邮箱收集报告 ===
收集时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

总体统计:
- 总大学数量: {total_universities}
- 成功获取邮箱: {universities_with_emails}
- 成功率: {universities_with_emails/total_universities*100:.1f}%
- 总邮箱数量: {total_emails_found}

按国家统计:
"""
        
        for country, stats in sorted(country_stats.items()):
            success_rate = stats['with_emails'] / stats['total'] * 100 if stats['total'] > 0 else 0
            report += f"- {country}: {stats['with_emails']}/{stats['total']} ({success_rate:.1f}%)\n"
        
        # 保存报告
        report_filename = f'collection_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"✓ 汇总报告已保存到 {report_filename}")
        print(report)
        
        return report_filename

async def main():
    """主函数"""
    print("=== 全球大学官方邮箱收集器 ===")
    print("专业版本 - 多源数据收集策略")
    print("目标：获取5000+全球大学的官方邮箱")
    print()
    
    # 创建收集器实例
    collector = GlobalUniversityEmailCollector()
    
    try:
        # 收集邮箱
        print("开始收集邮箱...")
        results = await collector.collect_all_emails()
        
        # 导出到CSV
        print("\n导出结果...")
        csv_filename = collector.export_to_csv(results)
        
        # 生成汇总报告
        print("\n生成汇总报告...")
        report_filename = collector.generate_summary_report(results)
        
        print(f"\n✓ 收集完成！")
        print(f"✓ CSV文件: {csv_filename}")
        print(f"✓ 报告文件: {report_filename}")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        logger.error(f"主程序错误: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 