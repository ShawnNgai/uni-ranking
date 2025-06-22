import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Set
from loguru import logger
import time
from urllib.parse import urljoin, urlparse
from email_validator import validate_email, EmailNotValidError

class SpainUniversityScraper:
    """西班牙大学数据收集器"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.collected_emails: Set[str] = set()
        self.universities: List[Dict] = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def collect_spain_universities(self) -> List[Dict]:
        """收集西班牙大学数据的主方法"""
        logger.info("开始收集西班牙大学数据...")
        
        # 1. 从官方数据源收集
        await self._collect_from_official_sources()
        
        # 2. 从大学目录收集
        await self._collect_from_directories()
        
        # 3. 从排名网站收集
        await self._collect_from_rankings()
        
        # 4. 数据清洗和验证
        cleaned_data = await self._clean_and_validate_data()
        
        logger.info(f"收集完成，共获取 {len(cleaned_data)} 所大学信息")
        return cleaned_data
    
    async def _collect_from_official_sources(self):
        """从官方数据源收集大学信息"""
        logger.info("从官方数据源收集大学信息...")
        
        # 西班牙教育部和CRUE数据源
        official_sources = [
            {
                "name": "西班牙教育部",
                "url": "https://www.educacionyfp.gob.es/"
            },
            {
                "name": "西班牙大学校长会议(CRUE)",
                "url": "https://www.crue.org/"
            }
        ]
        
        for source in official_sources:
            try:
                logger.info(f"正在处理: {source['name']}")
                await self._scrape_official_source(source)
                await asyncio.sleep(1)  # 请求间隔
                
            except Exception as e:
                logger.error(f"处理 {source['name']} 时出错: {str(e)}")
    
    async def _scrape_official_source(self, source: Dict):
        """爬取官方数据源"""
        try:
            async with self.session.get(source['url'], timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 查找大学相关链接
                    university_links = soup.find_all('a', href=re.compile(r'universidad|universidad'))
                    
                    for link in university_links[:20]:  # 限制数量
                        university_name = link.get_text(strip=True)
                        university_url = urljoin(source['url'], link.get('href', ''))
                        
                        if university_name and "universidad" in university_name.lower():
                            await self._extract_university_details(university_name, university_url)
                            
        except Exception as e:
            logger.error(f"爬取 {source['name']} 失败: {str(e)}")
    
    async def _collect_from_directories(self):
        """从大学目录收集信息"""
        logger.info("从大学目录收集信息...")
        
        # 模拟从Study in Spain获取数据
        study_spain_data = [
            {
                "name_es": "Universidad Complutense de Madrid",
                "name_en": "Complutense University of Madrid",
                "website": "https://www.ucm.es/",
                "city": "Madrid",
                "region": "Madrid"
            },
            {
                "name_es": "Universidad de Barcelona",
                "name_en": "University of Barcelona", 
                "website": "https://www.ub.edu/",
                "city": "Barcelona",
                "region": "Catalonia"
            },
            {
                "name_es": "Universidad Autónoma de Madrid",
                "name_en": "Autonomous University of Madrid",
                "website": "https://www.uam.es/",
                "city": "Madrid",
                "region": "Madrid"
            },
            {
                "name_es": "Universidad de Valencia",
                "name_en": "University of Valencia",
                "website": "https://www.uv.es/",
                "city": "Valencia",
                "region": "Valencia"
            },
            {
                "name_es": "Universidad de Granada",
                "name_en": "University of Granada",
                "website": "https://www.ugr.es/",
                "city": "Granada",
                "region": "Andalusia"
            }
        ]
        
        for uni_data in study_spain_data:
            await self._extract_university_details(
                uni_data["name_es"], 
                uni_data["website"],
                english_name=uni_data["name_en"],
                city=uni_data["city"],
                region=uni_data["region"]
            )
    
    async def _collect_from_rankings(self):
        """从排名网站收集信息"""
        logger.info("从排名网站收集信息...")
        
        # 模拟QS排名数据
        qs_spain_data = [
            {
                "name_en": "Universitat Pompeu Fabra",
                "website": "https://www.upf.edu/",
                "city": "Barcelona",
                "ranking_world": 248
            },
            {
                "name_en": "Universitat Autònoma de Barcelona",
                "website": "https://www.uab.cat/",
                "city": "Barcelona", 
                "ranking_world": 312
            },
            {
                "name_en": "Universidad Carlos III de Madrid",
                "website": "https://www.uc3m.es/",
                "city": "Madrid",
                "ranking_world": 351
            }
        ]
        
        for uni_data in qs_spain_data:
            await self._extract_university_details(
                uni_data["name_en"],
                uni_data["website"],
                city=uni_data["city"],
                ranking_world=uni_data["ranking_world"]
            )
    
    async def _extract_university_details(self, name: str, website: str, 
                                        english_name: str = None, 
                                        city: str = None, 
                                        region: str = None,
                                        ranking_world: int = None):
        """提取大学详细信息"""
        try:
            # 如果网站可用，尝试获取更多信息
            emails = []
            if website and website.startswith('http'):
                emails = await self._extract_emails_from_website(website)
            
            # 构建大学数据
            university_data = {
                "name_en": english_name or self._translate_to_english(name),
                "name_local": name,
                "country": "Spain",
                "region": region,
                "city": city,
                "website": website,
                "official_email": emails[0] if emails else None,
                "contact_email": emails[1] if len(emails) > 1 else None,
                "president_email": self._find_president_email(emails),
                "admin_email": self._find_admin_email(emails),
                "ranking_world": ranking_world,
                "data_source": "Spain University Scraper",
                "university_type": "Public" if "pública" in name.lower() else "Private"
            }
            
            self.universities.append(university_data)
            logger.info(f"收集到大学: {university_data['name_en']}")
            
        except Exception as e:
            logger.error(f"提取大学详情失败 {name}: {str(e)}")
    
    async def _extract_emails_from_website(self, website: str) -> List[str]:
        """从大学网站提取邮箱地址"""
        emails = []
        
        try:
            # 尝试访问联系页面
            contact_urls = [
                f"{website}/contacto",
                f"{website}/contact",
                f"{website}/contacto.html",
                f"{website}/contact.html",
                f"{website}/about/contact",
                f"{website}/en/contact"
            ]
            
            for contact_url in contact_urls:
                try:
                    async with self.session.get(contact_url, timeout=10) as response:
                        if response.status == 200:
                            html = await response.text()
                            found_emails = self._extract_emails_from_html(html)
                            emails.extend(found_emails)
                            if emails:
                                break
                except:
                    continue
            
            # 如果联系页面没有找到，尝试主页
            if not emails:
                async with self.session.get(website, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        emails = self._extract_emails_from_html(html)
            
            # 去重并验证
            unique_emails = list(set(emails))
            valid_emails = []
            
            for email in unique_emails:
                if self._validate_email(email):
                    valid_emails.append(email)
            
            return valid_emails[:5]  # 限制返回数量
            
        except Exception as e:
            logger.error(f"提取邮箱失败 {website}: {str(e)}")
            return []
    
    def _extract_emails_from_html(self, html: str) -> List[str]:
        """从HTML中提取邮箱地址"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html)
        
        # 过滤掉明显的无效邮箱
        excluded_patterns = ['noreply', 'no-reply', 'donotreply', 'info', 'contact']
        filtered_emails = []
        for email in emails:
            if not any(pattern in email.lower() for pattern in excluded_patterns):
                filtered_emails.append(email)
        
        return filtered_emails
    
    def _validate_email(self, email: str) -> bool:
        """验证邮箱地址"""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    def _find_president_email(self, emails: List[str]) -> Optional[str]:
        """查找校长邮箱"""
        president_keywords = ['rector', 'president', 'rectorado', 'presidencia']
        for email in emails:
            if any(keyword in email.lower() for keyword in president_keywords):
                return email
        return None
    
    def _find_admin_email(self, emails: List[str]) -> Optional[str]:
        """查找行政邮箱"""
        admin_keywords = ['admin', 'administracion', 'secretaria', 'secretary']
        for email in emails:
            if any(keyword in email.lower() for keyword in admin_keywords):
                return email
        return None
    
    def _translate_to_english(self, spanish_name: str) -> str:
        """将西班牙语大学名称翻译为英语"""
        # 简单的翻译映射
        translations = {
            "universidad": "university",
            "universitat": "university",
            "pública": "public",
            "privada": "private",
            "politécnica": "technical",
            "autónoma": "autonomous",
            "complutense": "complutense"
        }
        
        english_name = spanish_name
        for es, en in translations.items():
            english_name = english_name.replace(es, en)
        
        return english_name
    
    async def _clean_and_validate_data(self) -> List[Dict]:
        """清洗和验证数据"""
        logger.info("开始数据清洗和验证...")
        
        cleaned_data = []
        seen_names = set()
        
        for uni in self.universities:
            # 去重
            if uni['name_en'] in seen_names:
                continue
            seen_names.add(uni['name_en'])
            
            # 基本验证
            if not uni['name_en'] or not uni['website']:
                continue
            
            # 确保必要字段存在
            uni.setdefault('country', 'Spain')
            uni.setdefault('data_source', 'Spain University Scraper')
            
            cleaned_data.append(uni)
        
        logger.info(f"数据清洗完成，保留 {len(cleaned_data)} 条有效记录")
        return cleaned_data

# 使用示例
async def main():
    """主函数示例"""
    async with SpainUniversityScraper() as scraper:
        universities = await scraper.collect_spain_universities()
        
        # 打印结果
        for uni in universities[:5]:  # 显示前5个
            print(f"大学: {uni['name_en']}")
            print(f"网站: {uni['website']}")
            print(f"官方邮箱: {uni['official_email']}")
            print(f"校长邮箱: {uni['president_email']}")
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main()) 