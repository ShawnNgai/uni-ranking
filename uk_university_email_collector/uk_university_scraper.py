#!/usr/bin/env python3
"""
英国大学邮箱收集器
专门收集英国所有正规大学的邮箱信息
"""

import asyncio
import aiohttp
import re
import csv
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from loguru import logger
from datetime import datetime
from urllib.parse import urljoin, urlparse
from email_validator import validate_email, EmailNotValidError

class UKUniversityScraper:
    """英国大学邮箱收集器"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.universities = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def collect_uk_universities(self) -> List[Dict]:
        """收集英国大学邮箱信息"""
        logger.info("开始收集英国大学邮箱信息...")
        
        # 从Wikipedia获取英国大学列表
        uk_universities = await self._get_uk_universities_from_wikipedia()
        
        # 为每个大学收集邮箱信息
        for uni in uk_universities:
            await self._collect_university_emails(uni)
            await asyncio.sleep(1)  # 避免请求过快
        
        logger.info(f"收集完成，共处理 {len(self.universities)} 所大学")
        return self.universities
    
    async def _get_uk_universities_from_wikipedia(self) -> List[Dict]:
        """从Wikipedia获取英国大学列表"""
        logger.info("从Wikipedia获取英国大学列表...")
        
        # 英国大学列表（基于Wikipedia数据）
        uk_universities = [
            {"name": "University of Aberdeen", "website": "https://www.abdn.ac.uk/"},
            {"name": "Abertay University", "website": "https://www.abertay.ac.uk/"},
            {"name": "Aberystwyth University", "website": "https://www.aber.ac.uk/"},
            {"name": "Anglia Ruskin University", "website": "https://www.aru.ac.uk/"},
            {"name": "University of the Arts London", "website": "https://www.arts.ac.uk/"},
            {"name": "Aston University", "website": "https://www.aston.ac.uk/"},
            {"name": "Bangor University", "website": "https://www.bangor.ac.uk/"},
            {"name": "University of Bath", "website": "https://www.bath.ac.uk/"},
            {"name": "Bath Spa University", "website": "https://www.bathspa.ac.uk/"},
            {"name": "University of Bedfordshire", "website": "https://www.beds.ac.uk/"},
            {"name": "University of Birmingham", "website": "https://www.birmingham.ac.uk/"},
            {"name": "Birmingham City University", "website": "https://www.bcu.ac.uk/"},
            {"name": "University College Birmingham", "website": "https://www.ucb.ac.uk/"},
            {"name": "Bishop Grosseteste University", "website": "https://www.bishopg.ac.uk/"},
            {"name": "University of Bolton", "website": "https://www.bolton.ac.uk/"},
            {"name": "Arts University Bournemouth", "website": "https://aub.ac.uk/"},
            {"name": "Bournemouth University", "website": "https://www.bournemouth.ac.uk/"},
            {"name": "BPP University", "website": "https://www.bpp.com/"},
            {"name": "University of Bradford", "website": "https://www.bradford.ac.uk/"},
            {"name": "University of Brighton", "website": "https://www.brighton.ac.uk/"},
            {"name": "University of Bristol", "website": "https://www.bristol.ac.uk/"},
            {"name": "Brunel University London", "website": "https://www.brunel.ac.uk/"},
            {"name": "University of Buckingham", "website": "https://www.buckingham.ac.uk/"},
            {"name": "Buckinghamshire New University", "website": "https://www.bucks.ac.uk/"},
            {"name": "University of Cambridge", "website": "https://www.cam.ac.uk/"},
            {"name": "Canterbury Christ Church University", "website": "https://www.canterbury.ac.uk/"},
            {"name": "Cardiff Metropolitan University", "website": "https://www.cardiffmet.ac.uk/"},
            {"name": "Cardiff University", "website": "https://www.cardiff.ac.uk/"},
            {"name": "University of Central Lancashire", "website": "https://www.uclan.ac.uk/"},
            {"name": "University of Chester", "website": "https://www.chester.ac.uk/"},
            {"name": "University of Chichester", "website": "https://www.chi.ac.uk/"},
            {"name": "City, University of London", "website": "https://www.city.ac.uk/"},
            {"name": "Coventry University", "website": "https://www.coventry.ac.uk/"},
            {"name": "Cranfield University", "website": "https://www.cranfield.ac.uk/"},
            {"name": "University for the Creative Arts", "website": "https://www.uca.ac.uk/"},
            {"name": "University of Cumbria", "website": "https://www.cumbria.ac.uk/"},
            {"name": "De Montfort University", "website": "https://www.dmu.ac.uk/"},
            {"name": "University of Derby", "website": "https://www.derby.ac.uk/"},
            {"name": "University of Dundee", "website": "https://www.dundee.ac.uk/"},
            {"name": "Durham University", "website": "https://www.durham.ac.uk/"},
            {"name": "University of East Anglia", "website": "https://www.uea.ac.uk/"},
            {"name": "University of East London", "website": "https://www.uel.ac.uk/"},
            {"name": "Edge Hill University", "website": "https://www.edgehill.ac.uk/"},
            {"name": "University of Edinburgh", "website": "https://www.ed.ac.uk/"},
            {"name": "Edinburgh Napier University", "website": "https://www.napier.ac.uk/"},
            {"name": "University of Essex", "website": "https://www.essex.ac.uk/"},
            {"name": "University of Exeter", "website": "https://www.exeter.ac.uk/"},
            {"name": "Falmouth University", "website": "https://www.falmouth.ac.uk/"},
            {"name": "University of Glasgow", "website": "https://www.gla.ac.uk/"},
            {"name": "Glasgow Caledonian University", "website": "https://www.gcu.ac.uk/"},
            {"name": "University of Gloucestershire", "website": "https://www.glos.ac.uk/"},
            {"name": "University of Greenwich", "website": "https://www.gre.ac.uk/"},
            {"name": "Harper Adams University", "website": "https://www.harper-adams.ac.uk/"},
            {"name": "Hartpury University", "website": "https://www.hartpury.ac.uk/"},
            {"name": "Heriot-Watt University", "website": "https://www.hw.ac.uk/"},
            {"name": "University of Hertfordshire", "website": "https://www.herts.ac.uk/"},
            {"name": "University of the Highlands and Islands", "website": "https://www.uhi.ac.uk/"},
            {"name": "University of Huddersfield", "website": "https://www.hud.ac.uk/"},
            {"name": "University of Hull", "website": "https://www.hull.ac.uk/"},
            {"name": "Imperial College London", "website": "https://www.imperial.ac.uk/"},
            {"name": "Keele University", "website": "https://www.keele.ac.uk/"},
            {"name": "University of Kent", "website": "https://www.kent.ac.uk/"},
            {"name": "King's College London", "website": "https://www.kcl.ac.uk/"},
            {"name": "Kingston University", "website": "https://www.kingston.ac.uk/"},
            {"name": "Lancaster University", "website": "https://www.lancaster.ac.uk/"},
            {"name": "University of Leeds", "website": "https://www.leeds.ac.uk/"},
            {"name": "Leeds Arts University", "website": "https://www.leeds-art.ac.uk/"},
            {"name": "Leeds Beckett University", "website": "https://www.leedsbeckett.ac.uk/"},
            {"name": "Leeds Trinity University", "website": "https://www.leedstrinity.ac.uk/"},
            {"name": "University of Leicester", "website": "https://www.le.ac.uk/"},
            {"name": "University of Lincoln", "website": "https://www.lincoln.ac.uk/"},
            {"name": "University of Liverpool", "website": "https://www.liverpool.ac.uk/"},
            {"name": "Liverpool Hope University", "website": "https://www.hope.ac.uk/"},
            {"name": "Liverpool John Moores University", "website": "https://www.ljmu.ac.uk/"},
            {"name": "University of London", "website": "https://www.london.ac.uk/"},
            {"name": "London Metropolitan University", "website": "https://www.londonmet.ac.uk/"},
            {"name": "London School of Economics and Political Science", "website": "https://www.lse.ac.uk/"},
            {"name": "London South Bank University", "website": "https://www.lsbu.ac.uk/"},
            {"name": "Loughborough University", "website": "https://www.lboro.ac.uk/"},
            {"name": "University of Manchester", "website": "https://www.manchester.ac.uk/"},
            {"name": "Manchester Metropolitan University", "website": "https://www.mmu.ac.uk/"},
            {"name": "Middlesex University", "website": "https://www.mdx.ac.uk/"},
            {"name": "Newcastle University", "website": "https://www.ncl.ac.uk/"},
            {"name": "Newman University", "website": "https://www.newman.ac.uk/"},
            {"name": "University of Northampton", "website": "https://www.northampton.ac.uk/"},
            {"name": "Northumbria University", "website": "https://www.northumbria.ac.uk/"},
            {"name": "Norwich University of the Arts", "website": "https://www.nua.ac.uk/"},
            {"name": "University of Nottingham", "website": "https://www.nottingham.ac.uk/"},
            {"name": "Nottingham Trent University", "website": "https://www.ntu.ac.uk/"},
            {"name": "Open University", "website": "https://www.open.ac.uk/"},
            {"name": "University of Oxford", "website": "https://www.ox.ac.uk/"},
            {"name": "Oxford Brookes University", "website": "https://www.brookes.ac.uk/"},
            {"name": "Plymouth University", "website": "https://www.plymouth.ac.uk/"},
            {"name": "University of Portsmouth", "website": "https://www.port.ac.uk/"},
            {"name": "Queen Margaret University", "website": "https://www.qmu.ac.uk/"},
            {"name": "Queen's University Belfast", "website": "https://www.qub.ac.uk/"},
            {"name": "University of Reading", "website": "https://www.reading.ac.uk/"},
            {"name": "Regent's University London", "website": "https://www.regents.ac.uk/"},
            {"name": "Robert Gordon University", "website": "https://www.rgu.ac.uk/"},
            {"name": "University of Roehampton", "website": "https://www.roehampton.ac.uk/"},
            {"name": "Royal Agricultural University", "website": "https://www.rau.ac.uk/"},
            {"name": "Royal Holloway, University of London", "website": "https://www.royalholloway.ac.uk/"},
            {"name": "University of Salford", "website": "https://www.salford.ac.uk/"},
            {"name": "University of Sheffield", "website": "https://www.sheffield.ac.uk/"},
            {"name": "Sheffield Hallam University", "website": "https://www.shu.ac.uk/"},
            {"name": "University of South Wales", "website": "https://www.southwales.ac.uk/"},
            {"name": "University of Southampton", "website": "https://www.southampton.ac.uk/"},
            {"name": "Solent University", "website": "https://www.solent.ac.uk/"},
            {"name": "University of St Andrews", "website": "https://www.st-andrews.ac.uk/"},
            {"name": "St George's, University of London", "website": "https://www.sgul.ac.uk/"},
            {"name": "St Mary's University, Twickenham", "website": "https://www.stmarys.ac.uk/"},
            {"name": "Staffordshire University", "website": "https://www.staffs.ac.uk/"},
            {"name": "University of Stirling", "website": "https://www.stir.ac.uk/"},
            {"name": "University of Strathclyde", "website": "https://www.strath.ac.uk/"},
            {"name": "University of Suffolk", "website": "https://www.uos.ac.uk/"},
            {"name": "University of Sunderland", "website": "https://www.sunderland.ac.uk/"},
            {"name": "University of Surrey", "website": "https://www.surrey.ac.uk/"},
            {"name": "University of Sussex", "website": "https://www.sussex.ac.uk/"},
            {"name": "Swansea University", "website": "https://www.swansea.ac.uk/"},
            {"name": "Teesside University", "website": "https://www.tees.ac.uk/"},
            {"name": "University of the West of England", "website": "https://www.uwe.ac.uk/"},
            {"name": "University of the West of Scotland", "website": "https://www.uws.ac.uk/"},
            {"name": "University of Westminster", "website": "https://www.westminster.ac.uk/"},
            {"name": "University of Winchester", "website": "https://www.winchester.ac.uk/"},
            {"name": "University of Wolverhampton", "website": "https://www.wlv.ac.uk/"},
            {"name": "University of Worcester", "website": "https://www.worcester.ac.uk/"},
            {"name": "University of York", "website": "https://www.york.ac.uk/"},
            {"name": "York St John University", "website": "https://www.yorksj.ac.uk/"}
        ]
        
        logger.info(f"获取到 {len(uk_universities)} 所英国大学")
        return uk_universities
    
    async def _collect_university_emails(self, university: Dict):
        """收集单个大学的邮箱信息"""
        try:
            website = university.get('website', '')
            if not website:
                return
            
            logger.info(f"正在处理: {university['name']}")
            
            # 尝试获取邮箱信息
            emails = await self._extract_emails_from_website(website)
            
            # 构建大学数据
            uni_data = {
                "university_name": university['name'],
                "website": website,
                "all_emails": '; '.join(emails) if emails else ''
            }
            
            self.universities.append(uni_data)
            
        except Exception as e:
            logger.error(f"处理 {university['name']} 时出错: {str(e)}")
    
    async def _extract_emails_from_website(self, website: str) -> List[str]:
        """从大学网站提取邮箱信息"""
        all_emails = []
        
        try:
            # 尝试访问联系页面
            contact_urls = [
                f"{website}/contact",
                f"{website}/contact-us",
                f"{website}/about/contact",
                f"{website}/en/contact",
                f"{website}/contact-us/",
                f"{website}/contact/",
                f"{website}/enquiries",
                f"{website}/admissions",
                f"{website}/international"
            ]
            
            for contact_url in contact_urls:
                try:
                    async with self.session.get(contact_url, timeout=10) as response:
                        if response.status == 200:
                            html = await response.text()
                            found_emails = self._extract_emails_from_html(html)
                            
                            # 添加所有找到的邮箱
                            for email in found_emails:
                                if self._validate_email(email) and email not in all_emails:
                                    all_emails.append(email)
                            
                            if len(all_emails) >= 3:  # 如果已经有3个邮箱，就停止
                                break
                except:
                    continue
            
            # 如果联系页面没有找到足够的邮箱，尝试主页
            if len(all_emails) < 3:
                async with self.session.get(website, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        found_emails = self._extract_emails_from_html(html)
                        
                        for email in found_emails:
                            if self._validate_email(email) and email not in all_emails:
                                all_emails.append(email)
                                if len(all_emails) >= 3:  # 限制最多3个邮箱
                                    break
            
            # 优先选择重要的邮箱（包含关键词的邮箱排在前面）
            priority_keywords = ['admissions', 'international', 'contact', 'info', 'enquiries']
            sorted_emails = []
            
            # 先添加包含优先关键词的邮箱
            for keyword in priority_keywords:
                for email in all_emails:
                    if keyword in email.lower() and email not in sorted_emails:
                        sorted_emails.append(email)
                        if len(sorted_emails) >= 3:
                            break
                if len(sorted_emails) >= 3:
                    break
            
            # 再添加其他邮箱
            for email in all_emails:
                if email not in sorted_emails:
                    sorted_emails.append(email)
                    if len(sorted_emails) >= 3:
                        break
            
            return sorted_emails[:3]  # 确保最多返回3个邮箱
            
        except Exception as e:
            logger.error(f"提取邮箱失败 {website}: {str(e)}")
        
        return all_emails[:3]  # 确保最多返回3个邮箱
    
    def _extract_emails_from_html(self, html: str) -> List[str]:
        """从HTML中提取邮箱地址"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html)
        
        # 过滤掉明显的无效邮箱
        excluded_patterns = ['noreply', 'no-reply', 'donotreply', 'example', 'test']
        filtered_emails = []
        
        for email in emails:
            if not any(pattern in email.lower() for pattern in excluded_patterns):
                filtered_emails.append(email)
        
        return list(set(filtered_emails))  # 去重
    
    def _validate_email(self, email: str) -> bool:
        """验证邮箱地址"""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    def export_to_csv(self, filename: str = None):
        """导出为CSV格式"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"uk_universities_emails_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'university_name', 'website', 'emails'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for uni in self.universities:
                writer.writerow({
                    'university_name': uni['university_name'],
                    'website': uni['website'],
                    'emails': uni['all_emails']
                })
        
        logger.info(f"数据已导出到: {filename}")
        return filename 