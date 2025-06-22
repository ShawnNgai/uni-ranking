from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # 数据库配置
    database_url: str = "sqlite:///./university_data.db"
    database_echo: bool = False
    
    # API配置
    api_title: str = "全球大学数据收集器"
    api_version: str = "1.0.0"
    api_description: str = "收集和管理全球大学信息的API服务"
    
    # 爬虫配置
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    request_delay: float = 1.0  # 请求间隔（秒）
    max_retries: int = 3
    timeout: int = 30
    
    # 数据源配置
    spain_education_api: Optional[str] = None
    world_university_api: Optional[str] = None
    
    # 邮件验证配置
    email_validation_enabled: bool = True
    domain_validation_enabled: bool = True
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/university_collector.log"
    
    # 安全配置
    secret_key: str = "your-secret-key-here"
    access_token_expire_minutes: int = 30
    
    # 数据收集配置
    countries_to_collect: List[str] = ["spain", "france", "germany", "italy", "uk"]
    max_universities_per_country: int = 1000
    
    # 代理配置（可选）
    use_proxy: bool = False
    proxy_list: List[str] = []
    
    # 存储配置
    data_export_path: str = "data/exports"
    backup_path: str = "data/backups"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 创建全局设置实例
settings = Settings()

# 确保必要的目录存在
def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        "data",
        "data/exports", 
        "data/backups",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# 西班牙大学数据源配置
SPAIN_DATA_SOURCES = {
    "official_sources": [
        {
            "name": "西班牙教育部",
            "url": "https://www.educacionyfp.gob.es/",
            "type": "government"
        },
        {
            "name": "西班牙大学校长会议(CRUE)",
            "url": "https://www.crue.org/",
            "type": "association"
        }
    ],
    "university_directories": [
        {
            "name": "Study in Spain",
            "url": "https://www.studyinspain.info/",
            "type": "directory"
        },
        {
            "name": "Universia",
            "url": "https://www.universia.net/",
            "type": "portal"
        }
    ],
    "ranking_sources": [
        {
            "name": "QS World Rankings",
            "url": "https://www.topuniversities.com/",
            "type": "ranking"
        },
        {
            "name": "Times Higher Education",
            "url": "https://www.timeshighereducation.com/",
            "type": "ranking"
        }
    ]
}

# 邮箱验证规则
EMAIL_VALIDATION_RULES = {
    "common_domains": [
        "edu", "ac", "university", "uni", "college", "institute"
    ],
    "spain_domains": [
        "es", "edu.es", "university.es", "uni.es"
    ],
    "excluded_patterns": [
        "noreply", "no-reply", "donotreply", "info", "contact"
    ]
}

# 大学名称映射（西班牙语到英语）
SPAIN_UNIVERSITY_NAMES = {
    "Universidad Complutense de Madrid": "Complutense University of Madrid",
    "Universidad de Barcelona": "University of Barcelona", 
    "Universidad Autónoma de Madrid": "Autonomous University of Madrid",
    "Universidad de Valencia": "University of Valencia",
    "Universidad de Granada": "University of Granada",
    "Universidad de Sevilla": "University of Seville",
    "Universidad Politécnica de Madrid": "Technical University of Madrid",
    "Universidad de Salamanca": "University of Salamanca",
    "Universidad de Navarra": "University of Navarra",
    "Universidad Pompeu Fabra": "Pompeu Fabra University"
} 