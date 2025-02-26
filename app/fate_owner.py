from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from app.paipan_engine import BaziPaipanEngine

class Gender(str, Enum):
    """性别枚举"""
    MALE   = "男"
    FEMALE = "女"

    def __str__(self) -> str:
        """返回性别汉字"""
        return self.value

class HeavenlyStem(str, Enum):
    """十天干枚举"""
    JIA  = "甲"
    YI   = "乙"
    BING = "丙"
    DING = "丁"
    WU   = "戊"
    JI   = "己"
    GENG = "庚"
    XIN  = "辛"
    REN  = "壬"
    GUI  = "癸"

    def __str__(self) -> str:
        """返回天干汉字"""
        return self.value

class EarthlyBranch(str, Enum):
    """十二地支枚举"""
    ZI   = "子"
    CHOU = "丑"
    YIN  = "寅"
    MAO  = "卯"
    CHEN = "辰"
    SI   = "巳"
    WU   = "午"
    WEI  = "未"
    SHEN = "申"
    YOU  = "酉"
    XU   = "戌"
    HAI  = "亥"

    def __str__(self) -> str:
        """返回地支汉字"""
        return self.value

class TenGodType(str, Enum):
    """十神枚举"""
    BI_JIAN    = "比肩"
    JIE_CAI    = "劫财"
    SHI_SHEN   = "食神"
    SHANG_GUAN = "伤官"
    ZHENG_CAI  = "正财"
    PIAN_CAI   = "偏财"
    ZHENG_GUAN = "正官"
    QI_SHA     = "七杀"
    ZHENG_YIN  = "正印"
    PIAN_YIN   = "偏印"

    def __str__(self) -> str:
        """返回十神汉字"""
        return self.value

# 地支藏干对应表（简化，只列出本气）
BRANCH_HIDDEN_STEM = {
    "子": ["癸", "癸"], 
    "丑": ["己", "辛", "癸"], 
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"], 
    "辰": ["戊", "乙", "癸"], 
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"], 
    "未": ["己", "丁", "乙"], 
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"], 
    "戌": ["戊", "辛", "丁"], 
    "亥": ["壬", "甲"]
}


class SolarBirthInfo(BaseModel):
    """阳历生日信息数据结构"""
    year  : int = Field(..., ge=1900, le=2100, description="出生年份，范围1900-2100")
    month : int = Field(..., ge=1, le=12, description="出生月份，范围1-12")
    day   : int = Field(..., ge=1, le=31, description="出生日期，范围1-31")
    hour  : int = Field(..., ge=0, le=23, description="出生小时，范围0-23")
    minute: int = Field(0,   ge=0, le=59, description="出生分钟，范围0-59")
    
    def __str__(self) -> str:
        """返回格式化的生日字符串"""
        return f"{self.year}年{self.month}月{self.day}日 {self.hour:02d}:{self.minute:02d}"


class LunarBirthInfo(BaseModel):
    """农历生日信息数据结构"""
    year         : int  = Field(..., ge=1900, le=2100, description="农历年份，范围1900-2100")
    month        : int  = Field(..., ge=1, le=12, description="农历月份，范围1-12")
    day          : int  = Field(..., ge=1, le=30, description="农历日期，范围1-30")
    hour         : int  = Field(..., ge=0, le=23, description="出生小时，范围0-23")
    minute       : int  = Field(0,   ge=0, le=59, description="出生分钟，范围0-59")
    is_leap_month: bool = Field(False, description="是否闰月")
    
    def __str__(self) -> str:
        """返回格式化的农历生日字符串"""
        # 月份特殊处理
        month_map = {
            1: "正月",
            11: "冬月", 
            12: "腊月"
        }
        # 处理2-10月
        if 2 <= self.month <= 10:
            month_str = f"{self._to_chinese_num(self.month)}月"
        else:
            month_str = month_map.get(self.month, "")  # 1,11,12月使用特殊名称
        
        # 日期特殊处理
        if self.day <= 10:
            day_str = f"初{self._to_chinese_num(self.day)}"
        else:
            if self.day < 20:
                day_str = f"十{self._to_chinese_num(self.day - 10)}"
            elif self.day == 20:
                day_str = "二十"
            elif self.day < 30:
                day_str = f"廿{self._to_chinese_num(self.day - 20)}"
            else:
                day_str = "三十"
        
        leap_str = "闰" if self.is_leap_month else ""
        return f"农历{self.year}年{leap_str}{month_str}{day_str} {self.hour:02d}:{self.minute:02d}"
    
    def _to_chinese_num(self, num: int) -> str:
        """将数字转换为中文数字"""
        chinese_nums = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
        return chinese_nums[num]


class PillarInfo(BaseModel):
    """单柱信息（天干地支）"""
    heavenly_stem : HeavenlyStem  = Field(..., description="天干")
    earthly_branch: EarthlyBranch = Field(..., description="地支")
    hidden_stem: Optional[List[HeavenlyStem]] = Field(None, description="地支藏干")
    
    def __init__(self, **data):
        super().__init__(**data)
        # 如果没有提供hidden_stem，根据地支查找藏干
        if not self.hidden_stem and self.earthly_branch:
            branch_str = self.earthly_branch.value
            if branch_str in BRANCH_HIDDEN_STEM:
                self.hidden_stem = [HeavenlyStem(stem) for stem in BRANCH_HIDDEN_STEM[branch_str]]

    def __str__(self) -> str:
        """返回天干地支的汉字组合"""
        return f"{self.heavenly_stem}{self.earthly_branch}"


class TenGodInfo(BaseModel):
    """十神信息"""
    heavenly_stem: TenGodType = Field(..., description="天干十神")
    earthly_branch: TenGodType = Field(..., description="地支十神")
    hidden_stems: List[TenGodType] = Field(default_factory=list, description="藏干十神")


class BaziInfo(BaseModel):
    """八字信息数据结构"""
    
    '''四柱'''
    year_pillar : PillarInfo = Field(..., description="年柱")
    month_pillar: PillarInfo = Field(..., description="月柱")
    day_pillar  : PillarInfo = Field(..., description="日柱")
    hour_pillar : PillarInfo = Field(..., description="时柱")
    
    '''五行'''
    five_elements: List[str] = Field(default_factory=list, description="五行")
    
    '''十神'''
    ten_gods: Dict[str, TenGodInfo] = Field(default_factory=dict, description="十神")
    
    def get_bazi_string(self) -> str:
        """返回八字字符串，如'甲子 乙丑 丙寅 丁卯'"""
        return f"{self.year_pillar} {self.month_pillar} {self.day_pillar} {self.hour_pillar}"
    
    def get_bazi_string_with_hidden_stem(self) -> str:
        """返回带藏干的八字字符串"""
        pillars = []
        for pillar in [self.year_pillar, self.month_pillar, self.day_pillar, self.hour_pillar]:
            hidden_stems = f"（{', '.join(str(stem) for stem in pillar.hidden_stem)}）" if pillar.hidden_stem else ""
            pillars.append(f"{pillar}{hidden_stems}")
        return " ".join(pillars)
    
    def get_five_elements_string(self) -> str:
        """返回五行字符串"""
        return " ".join(self.five_elements)


class FateOwner(BaseModel):
    """命主类，包含生日信息和八字信息"""
    name: Optional[str] = Field(None, description="命主姓名")
    gender: Gender = Field(..., description="性别")
    solar_birth_info: Optional[SolarBirthInfo] = Field(None, description="阳历生日信息")
    lunar_birth_info: Optional[LunarBirthInfo] = Field(None, description="农历生日信息")
    bazi_info: Optional[BaziInfo] = Field(None, description="八字信息")
    
    def __init__(self, **data):
        super().__init__(**data)
        # 如果只提供了一种生日信息，自动转换生成另一种
        if self.solar_birth_info and not self.lunar_birth_info:
            self._convert_solar_to_lunar()
        elif self.lunar_birth_info and not self.solar_birth_info:
            self._convert_lunar_to_solar()
    
    def _convert_solar_to_lunar(self):
        """将阳历转换为农历"""
        if not self.solar_birth_info:
            return
            
        # 使用排盘引擎进行转换
        engine = BaziPaipanEngine()
        lunar_info = engine.solar_to_lunar(
            self.solar_birth_info.year,
            self.solar_birth_info.month,
            self.solar_birth_info.day
        )
        
        # 获取农历信息
        self.lunar_birth_info = LunarBirthInfo(
            year=lunar_info["year"],
            month=lunar_info["month"],
            day=lunar_info["day"],
            hour=self.solar_birth_info.hour,
            minute=self.solar_birth_info.minute,
            is_leap_month=lunar_info["is_leap_month"]
        )
    
    def _convert_lunar_to_solar(self):
        """将农历转换为阳历"""
        if not self.lunar_birth_info:
            return
            
        # 使用排盘引擎进行转换
        engine = BaziPaipanEngine()
        solar_info = engine.lunar_to_solar(
            self.lunar_birth_info.year,
            self.lunar_birth_info.month,
            self.lunar_birth_info.day,
            self.lunar_birth_info.is_leap_month
        )
        
        # 获取阳历信息
        self.solar_birth_info = SolarBirthInfo(
            year=solar_info["year"],
            month=solar_info["month"],
            day=solar_info["day"],
            hour=self.lunar_birth_info.hour,
            minute=self.lunar_birth_info.minute
        )
    
    def calculate_bazi(self) -> BaziInfo:
        """计算八字信息"""
        engine = BaziPaipanEngine()
        
        # 确保有农历信息用于计算
        if not self.lunar_birth_info:
            if self.solar_birth_info:
                self._convert_solar_to_lunar()
            else:
                raise ValueError("需要阳历或农历生日信息才能计算八字")
        
        # 使用排盘引擎计算八字
        bazi_dict = engine.calculate_bazi(
            lunar_year    = self.lunar_birth_info.year,
            lunar_month   = self.lunar_birth_info.month,
            lunar_day     = self.lunar_birth_info.day,
            hour          = self.lunar_birth_info.hour,
            is_leap_month = self.lunar_birth_info.is_leap_month
        )
        
        # 构建PillarInfo对象
        year_pillar = PillarInfo(
            heavenly_stem=HeavenlyStem(bazi_dict["year"]["heavenly_stem"]),
            earthly_branch=EarthlyBranch(bazi_dict["year"]["earthly_branch"]),
            hidden_stem=[HeavenlyStem(stem) for stem in bazi_dict["year"]["hidden_stems"]]
        )
        month_pillar = PillarInfo(
            heavenly_stem=HeavenlyStem(bazi_dict["month"]["heavenly_stem"]),
            earthly_branch=EarthlyBranch(bazi_dict["month"]["earthly_branch"]),
            hidden_stem=[HeavenlyStem(stem) for stem in bazi_dict["month"]["hidden_stems"]]
        )
        day_pillar = PillarInfo(
            heavenly_stem=HeavenlyStem(bazi_dict["day"]["heavenly_stem"]),
            earthly_branch=EarthlyBranch(bazi_dict["day"]["earthly_branch"]),
            hidden_stem=[HeavenlyStem(stem) for stem in bazi_dict["day"]["hidden_stems"]]
        )
        hour_pillar = PillarInfo(
            heavenly_stem=HeavenlyStem(bazi_dict["hour"]["heavenly_stem"]),
            earthly_branch=EarthlyBranch(bazi_dict["hour"]["earthly_branch"]),
            hidden_stem=[HeavenlyStem(stem) for stem in bazi_dict["hour"]["hidden_stems"]]
        )
        
        # 构建十神信息
        ten_gods = {}
        if "ten_gods" in bazi_dict:
            for pillar_name, gods in bazi_dict["ten_gods"].items():
                ten_gods[pillar_name] = TenGodInfo(
                    heavenly_stem=TenGodType(gods["heavenly_stem"]),
                    earthly_branch=TenGodType(gods["earthly_branch"]),
                    hidden_stems=[TenGodType(god) for god in gods["hidden_stems"]]
                )
        
        # 创建八字信息
        self.bazi_info = BaziInfo(
            year_pillar=year_pillar,
            month_pillar=month_pillar,
            day_pillar=day_pillar,
            hour_pillar=hour_pillar,
            five_elements=bazi_dict["five_elements"],
            ten_gods=ten_gods
        )
        
        return self.bazi_info
    
    def get_summary(self) -> str:
        """获取命主信息摘要"""
        summary = [
            f"姓名: {self.name or '未知'}",
            f"性别: {self.gender}"
        ]
        
        if self.solar_birth_info:
            summary.append(f"阳历: {self.solar_birth_info}")
        if self.lunar_birth_info:
            summary.append(f"农历: {self.lunar_birth_info}")
        
        if self.bazi_info:
            summary.extend([
                f"八字: {self.bazi_info.get_bazi_string()}",
                f"八字(含藏干): {self.bazi_info.get_bazi_string_with_hidden_stem()}",
                f"五行: {self.bazi_info.get_five_elements_string()}"
            ])
        
        return "\n".join(summary)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "FateOwner":
        """从字典创建FateOwner实例"""
        # 判断是否包含农历信息
        has_lunar = all(key in data for key in ["lunar_year", "lunar_month", "lunar_day"])
        # 判断是否包含阳历信息
        has_solar = all(key in data for key in ["year", "month", "day"])
        
        if not (has_lunar or has_solar):
            raise ValueError("需要提供阳历或农历生日信息")
        
        # 构建阳历信息
        solar_birth_info = None
        if has_solar:
            solar_birth_info = SolarBirthInfo(
                year=data["year"],
                month=data["month"],
                day=data["day"],
                hour=data.get("hour", 0),
                minute=data.get("minute", 0)
            )
        
        # 构建农历信息
        lunar_birth_info = None
        if has_lunar:
            lunar_birth_info = LunarBirthInfo(
                year=data["lunar_year"],
                month=data["lunar_month"],
                day=data["lunar_day"],
                hour=data.get("hour", 0),
                minute=data.get("minute", 0),
                is_leap_month=data.get("is_leap_month", False)
            )
        
        return cls(
            name=data.get("name"),
            gender=data["gender"],
            solar_birth_info=solar_birth_info,
            lunar_birth_info=lunar_birth_info
        ) 