from datetime import datetime
import sxtwl  # 使用寿星天文历库计算农历和八字
from typing import Dict, Tuple, List

class BaziChartEngine:
    """八字排盘引擎"""
    
    # 天干
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    
    # 地支
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 五行
    FIVE_ELEMENTS = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }

    # 五行生克关系
    FIVE_ELEMENTS_RELATIONS = {
        "木": {"木": "比", "火": "生", "土": "财", "金": "官", "水": "印"},
        "火": {"木": "印", "火": "比", "土": "生", "金": "财", "水": "官"},
        "土": {"木": "官", "火": "印", "土": "比", "金": "生", "水": "财"},
        "金": {"木": "财", "火": "官", "土": "印", "金": "比", "水": "生"},
        "水": {"木": "生", "火": "财", "土": "官", "金": "印", "水": "比"}
    }

    # 阴阳
    YIN_YANG = {
        "甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳",
        "己": "阴", "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴"
    }

    # 十神名称
    TEN_GODS = {
        ("阳", "比"): "比肩",
        ("阴", "比"): "劫财",
        ("阳", "印"): "偏印",
        ("阴", "印"): "正印",
        ("阳", "官"): "七杀",
        ("阴", "官"): "正官",
        ("阳", "财"): "偏财",
        ("阴", "财"): "正财",
        ("阳", "生"): "食神",
        ("阴", "生"): "伤官"
    }

    def __init__(self):
        pass
    
    def calculate_bazi(self, birth_time: datetime) -> Dict:
        """
        计算八字
        Args:
            birth_time: 出生时间
        Returns:
            包含八字信息的字典
        """
        # 获取农历日期
        lunar_date = sxtwl.fromSolar(
            birth_time.year,
            birth_time.month,
            birth_time.day
        )
        
        # 计算年月日时的天干地支
        year_gz = lunar_date.getYearGZ()
        month_gz = lunar_date.getMonthGZ()
        day_gz = lunar_date.getDayGZ()
        hour_gz = self._get_hour_gz(day_gz.tg, birth_time.hour)
        
        # 获取日干（命主）
        day_stem = self.HEAVENLY_STEMS[day_gz.tg]
        
        # 组装八字
        bazi = {
            "year": {
                "heavenly_stem": self.HEAVENLY_STEMS[year_gz.tg],
                "earthly_branch": self.EARTHLY_BRANCHES[year_gz.dz]
            },
            "month": {
                "heavenly_stem": self.HEAVENLY_STEMS[month_gz.tg],
                "earthly_branch": self.EARTHLY_BRANCHES[month_gz.dz]
            },
            "day": {
                "heavenly_stem": self.HEAVENLY_STEMS[day_gz.tg],
                "earthly_branch": self.EARTHLY_BRANCHES[day_gz.dz]
            },
            "hour": {
                "heavenly_stem": self.HEAVENLY_STEMS[hour_gz[0]],
                "earthly_branch": self.EARTHLY_BRANCHES[hour_gz[1]]
            }
        }
        
        # 计算五行属性
        bazi["five_elements"] = self._calculate_five_elements(bazi)
        
        # 计算十神
        bazi["ten_gods"] = self._calculate_ten_gods(bazi, day_stem)
        
        return bazi
    
    def _calculate_ten_gods(self, bazi: Dict, day_stem: str) -> Dict[str, Dict[str, str]]:
        """
        计算十神
        Args:
            bazi: 八字信息字典
            day_stem: 日干
        Returns:
            十神信息字典
        """
        result = {}
        day_element = self.FIVE_ELEMENTS[day_stem]
        day_yin_yang = self.YIN_YANG[day_stem]
        
        for pillar in ["year", "month", "day", "hour"]:
            result[pillar] = {}
            
            # 计算天干十神
            stem = bazi[pillar]["heavenly_stem"]
            if stem != day_stem:  # 不计算日干的十神
                stem_element = self.FIVE_ELEMENTS[stem]
                relation = self.FIVE_ELEMENTS_RELATIONS[day_element][stem_element]
                stem_yin_yang = self.YIN_YANG[stem]
                result[pillar]["heavenly_stem"] = self.TEN_GODS[(
                    "阳" if stem_yin_yang == day_yin_yang else "阴",
                    relation
                )]
            
            # 计算地支藏干的十神（简化处理，只计算地支本气）
            branch = bazi[pillar]["earthly_branch"]
            result[pillar]["earthly_branch"] = self._get_branch_ten_god(branch, day_stem)
        
        return result
    
    def _get_branch_ten_god(self, branch: str, day_stem: str) -> str:
        """
        获取地支藏干的十神（简化处理，只返回地支本气的十神）
        Args:
            branch: 地支
            day_stem: 日干
        Returns:
            十神名称
        """
        # 地支藏干对应表（简化，只列出本气）
        BRANCH_HIDDEN_STEM = {
            "子": "癸", "丑": "己", "寅": "甲",
            "卯": "乙", "辰": "戊", "巳": "丙",
            "午": "丁", "未": "己", "申": "庚",
            "酉": "辛", "戌": "戊", "亥": "壬"
        }
        
        hidden_stem = BRANCH_HIDDEN_STEM[branch]
        day_element = self.FIVE_ELEMENTS[day_stem]
        hidden_element = self.FIVE_ELEMENTS[hidden_stem]
        relation = self.FIVE_ELEMENTS_RELATIONS[day_element][hidden_element]
        
        return self.TEN_GODS[(
            "阳" if self.YIN_YANG[hidden_stem] == self.YIN_YANG[day_stem] else "阴",
            relation
        )]
    
    def _get_hour_gz(self, day_stem: int, hour: int) -> Tuple[int, int]:
        """
        计算时柱天干地支
        Args:
            day_stem: 日柱天干
            hour: 小时
        Returns:
            时柱天干地支的索引元组
        """
        # 将24小时制转换为12地支时辰
        branch_index = (hour + 1) // 2 % 12
        
        # 根据日干推算时干
        stem_index = ((day_stem % 10) * 2 + branch_index) % 10
        
        return (stem_index, branch_index)
    
    def _calculate_five_elements(self, bazi: Dict) -> List[str]:
        """
        计算八字中的五行属性
        Args:
            bazi: 八字信息字典
        Returns:
            五行属性列表
        """
        five_elements = []
        for pillar in ["year", "month", "day", "hour"]:
            stem = bazi[pillar]["heavenly_stem"]
            five_elements.append(self.FIVE_ELEMENTS[stem])
        return five_elements

    def get_bazi_string(self, bazi: Dict) -> str:
        """
        将八字转换为字符串格式
        Args:
            bazi: 八字信息字典
        Returns:
            格式化的八字字符串
        """
        result = []
        for pillar in ["year", "month", "day", "hour"]:
            stem = bazi[pillar]["heavenly_stem"]
            branch = bazi[pillar]["earthly_branch"]
            result.append(f"{stem}{branch}")
        return " ".join(result)

def main():
    try:
        # 从终端获取输入
        print("请输入出生年份（如1990）：")
        year = int(input().strip())
        
        print("请输入出生月份（1-12）：")
        month = int(input().strip())
        
        print("请输入出生日期（1-31）：")
        day = int(input().strip())
        
        print("请输入出生时间（24小时制，0-23）：")
        hour = int(input().strip())
        
        # 验证输入
        if not (1900 <= year <= 2100):
            raise ValueError("年份必须在1900-2100之间")
        if not (1 <= month <= 12):
            raise ValueError("月份必须在1-12之间")
        if not (1 <= day <= 31):
            raise ValueError("日期必须在1-31之间")
        if not (0 <= hour <= 23):
            raise ValueError("小时必须在0-23之间")
        
        # 创建日期对象
        birth_time = datetime(year, month, day, hour, 0)
        
        # 计算八字
        engine = BaziChartEngine()
        bazi = engine.calculate_bazi(birth_time)
        
        # 输出结果
        print("\n=== 八字排盘结果 ===")
        print(f"阳历：{year}年{month}月{day}日 {hour:02d}时")
        print("八字：", engine.get_bazi_string(bazi))
        print("五行：", " ".join(bazi["five_elements"]))
        
    except ValueError as e:
        print(f"输入错误：{str(e)}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    main()
