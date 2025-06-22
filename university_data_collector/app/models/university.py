from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, HttpUrl

Base = declarative_base()

class University(Base):
    """大学数据库模型"""
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(500), nullable=False, index=True)  # 英文名称
    name_local = Column(String(500))  # 本地语言名称
    country = Column(String(100), nullable=False, index=True)  # 国家
    region = Column(String(200))  # 地区/省份
    city = Column(String(200))  # 城市
    website = Column(String(500))  # 官方网站
    official_email = Column(String(200))  # 官方邮箱
    contact_email = Column(String(200))  # 联系邮箱
    president_email = Column(String(200))  # 校长邮箱
    admin_email = Column(String(200))  # 行政邮箱
    phone = Column(String(50))  # 电话
    address = Column(Text)  # 地址
    latitude = Column(Float)  # 纬度
    longitude = Column(Float)  # 经度
    founded_year = Column(Integer)  # 成立年份
    student_count = Column(Integer)  # 学生数量
    staff_count = Column(Integer)  # 教职工数量
    university_type = Column(String(100))  # 大学类型（公立/私立）
    accreditation = Column(String(200))  # 认证机构
    ranking_national = Column(Integer)  # 国内排名
    ranking_world = Column(Integer)  # 世界排名
    data_source = Column(String(200))  # 数据来源
    last_verified = Column(DateTime, default=datetime.utcnow)  # 最后验证时间
    is_active = Column(Boolean, default=True)  # 是否活跃
    notes = Column(Text)  # 备注
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic模型用于API
class UniversityBase(BaseModel):
    name_en: str
    name_local: Optional[str] = None
    country: str
    region: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    official_email: Optional[str] = None
    contact_email: Optional[str] = None
    president_email: Optional[str] = None
    admin_email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    founded_year: Optional[int] = None
    student_count: Optional[int] = None
    staff_count: Optional[int] = None
    university_type: Optional[str] = None
    accreditation: Optional[str] = None
    ranking_national: Optional[int] = None
    ranking_world: Optional[int] = None
    data_source: Optional[str] = None
    notes: Optional[str] = None

class UniversityCreate(UniversityBase):
    pass

class UniversityUpdate(BaseModel):
    name_en: Optional[str] = None
    name_local: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None
    official_email: Optional[str] = None
    contact_email: Optional[str] = None
    president_email: Optional[str] = None
    admin_email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    founded_year: Optional[int] = None
    student_count: Optional[int] = None
    staff_count: Optional[int] = None
    university_type: Optional[str] = None
    accreditation: Optional[str] = None
    ranking_national: Optional[int] = None
    ranking_world: Optional[int] = None
    data_source: Optional[str] = None
    notes: Optional[str] = None

class UniversityResponse(UniversityBase):
    id: int
    last_verified: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UniversitySearch(BaseModel):
    query: str
    country: Optional[str] = None
    limit: int = 50
    offset: int = 0

class UniversityList(BaseModel):
    universities: List[UniversityResponse]
    total: int
    page: int
    limit: int 