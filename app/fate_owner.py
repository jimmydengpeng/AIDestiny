from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class Gender(str, Enum):
    """性别枚举"""
    MALE = "male"
    FEMALE = "female"


class BirthInfo(BaseModel):
    """生日信息数据结构"""
    year: int = Field(..., ge=1900, le=2100, description="出生年份，范围1900-2100")
    month: int = Field(..., ge=1, le=12, description="出生月份，范围1-12")
    day: int = Field(..., ge=1, le=31, description="出生日期，范围1-31")
    hour: int = Field(..., ge=0, le=23, description="出生小时，范围0-23")
    minute: int = Field(0, ge=0, le=59, description="出生分钟，范围0-59")
    gender: str = Field("male", description="性别，male或female")
    
    def to_datetime(self) -> datetime:
        """转换为datetime对象"""
        return datetime(
            self.year, self.month, self.day, 
            self.hour, self.minute
        )
    
    def __str__(self) -> str:
        """返回格式化的生日字符串"""
        return f"{self.year}年{self.month}月{self.day}日 {self.hour:02d}:{self.minute:02d}"


class PillarInfo(BaseModel):
    """单柱信息（天干地支）"""
    heavenly_stem: str = Field(..., description="天干")
    earthly_branch: str = Field(..., description="地支")
    
    def __str__(self) -> str:
        """返回天干地支组合"""
        return f"{self.heavenly_stem}{self.earthly_branch}"


class TenGodInfo(BaseModel):
    """十神信息"""
    heavenly_stem: str = Field(..., description="天干十神")
    earthly_branch: str = Field(..., description="地支十神")


class BaziInfo(BaseModel):
    """八字信息数据结构"""
    year: PillarInfo = Field(..., description="年柱")
    month: PillarInfo = Field(..., description="月柱")
    day: PillarInfo = Field(..., description="日柱")
    hour: PillarInfo = Field(..., description="时柱")
    
    lunar_year: Optional[int] = Field(None, description="农历年")
    lunar_month: Optional[int] = Field(None, description="农历月")
    lunar_day: Optional[int] = Field(None, description="农历日")
    
    five_elements: List[str] = Field([], description="五行属性")
    ten_gods: Optional[Dict[str, TenGodInfo]] = Field(None, description="十神信息")
    
    def get_bazi_string(self) -> str:
        """返回八字字符串，如'甲子 乙丑 丙寅 丁卯'"""
        return f"{self.year} {self.month} {self.day} {self.hour}"
    
    def get_five_elements_string(self) -> str:
        """返回五行字符串，如'木 火 土 金'"""
        return " ".join(self.five_elements)
    
    def get_lunar_date_string(self) -> str:
        """返回农历日期字符串"""
        if None in (self.lunar_year, self.lunar_month, self.lunar_day):
            return "农历信息不完整"
        return f"农历{self.lunar_year}年{self.lunar_month}月{self.lunar_day}日"


class FateOwner(BaseModel):
    """命主类，包含生日信息和八字信息"""
    name: Optional[str] = Field(None, description="命主姓名")
    gender: Gender = Field(..., description="性别")
    birth_info: BirthInfo = Field(..., description="生日信息")
    bazi_info: Optional[BaziInfo] = Field(None, description="八字信息")
    
    def calculate_bazi(self, engine=None):
        """计算八字信息
        
        如果没有提供排盘引擎，会自动导入并创建一个
        """
        if engine is None:
            # 延迟导入，避免循环引用
            from app.paipan_engine import BaziPaipanEngine
            engine = BaziPaipanEngine()
        
        # 使用排盘引擎计算八字
        bazi_dict = engine.calculate_bazi(self.birth_info.to_datetime())
        
        # 构建PillarInfo对象
        year_pillar = PillarInfo(
            heavenly_stem=bazi_dict["year"]["heavenly_stem"],
            earthly_branch=bazi_dict["year"]["earthly_branch"]
        )
        month_pillar = PillarInfo(
            heavenly_stem=bazi_dict["month"]["heavenly_stem"],
            earthly_branch=bazi_dict["month"]["earthly_branch"]
        )
        day_pillar = PillarInfo(
            heavenly_stem=bazi_dict["day"]["heavenly_stem"],
            earthly_branch=bazi_dict["day"]["earthly_branch"]
        )
        hour_pillar = PillarInfo(
            heavenly_stem=bazi_dict["hour"]["heavenly_stem"],
            earthly_branch=bazi_dict["hour"]["earthly_branch"]
        )
        
        # 构建十神信息
        ten_gods = {}
        if "ten_gods" in bazi_dict:
            for pillar_name, gods in bazi_dict["ten_gods"].items():
                ten_gods[pillar_name] = TenGodInfo(
                    heavenly_stem=gods["heavenly_stem"],
                    earthly_branch=gods["earthly_branch"]
                )
        
        # 创建八字信息
        self.bazi_info = BaziInfo(
            year=year_pillar,
            month=month_pillar,
            day=day_pillar,
            hour=hour_pillar,
            five_elements=bazi_dict.get("five_elements", []),
            ten_gods=ten_gods
        )
        
        return self.bazi_info
    
    def get_summary(self) -> str:
        """获取命主信息摘要"""
        gender_str = "男" if self.gender == Gender.MALE else "女"
        summary = [
            f"姓名: {self.name or '未知'}",
            f"性别: {gender_str}",
            f"出生: {self.birth_info}"
        ]
        
        if self.bazi_info:
            summary.extend([
                f"八字: {self.bazi_info.get_bazi_string()}",
                f"五行: {self.bazi_info.get_five_elements_string()}"
            ])
        
        return "\n".join(summary)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "FateOwner":
        """从字典创建FateOwner实例"""
        birth_info = BirthInfo(
            year=data["year"],
            month=data["month"],
            day=data["day"],
            hour=data["hour"],
            minute=data.get("minute", 0),
            gender=data["gender"]
        )
        
        return cls(
            name=data.get("name"),
            gender=data["gender"],
            birth_info=birth_info
        ) 