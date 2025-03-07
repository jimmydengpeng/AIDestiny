import ephem
from datetime import datetime, timedelta
from typing import Tuple

def get_jieqi_date(year: int, angle: float) -> datetime:
    """
    计算指定年份中太阳到达某黄经角度的时间
    Args:
        year: 年份
        angle: 角度 (0-360)
    Returns:
        datetime对象
    """
    date = ephem.Date(datetime(year, 1, 1))
    sun = ephem.Sun()
    earth = ephem.Date(date)
    
    # 计算太阳到达指定角度的时间
    while True:
        sun.compute(earth)
        # 将弧度转换为角度
        sun_lon = sun.hlong * 180 / ephem.pi
        if sun_lon >= angle:
            break
        earth = ephem.Date(earth + 1)
    
    # 精确计算（二分法）
    earth_start = earth - 1
    earth_end = earth
    
    while earth_end - earth_start > 0.000001:  # 精确到秒级
        earth_mid = (earth_start + earth_end) / 2
        sun.compute(earth_mid)
        sun_lon = sun.hlong * 180 / ephem.pi
        
        if sun_lon > angle:
            earth_end = earth_mid
        else:
            earth_start = earth_mid
    
    return ephem.Date(earth_start).datetime()

def get_nearest_jieqi(date: datetime) -> Tuple[str, datetime, float]:
    """
    获取最近的节气信息
    Args:
        date: 待查询的日期时间
    Returns:
        (节气名称, 节气时间, 相差小时数)
    """
    # 24节气对应的黄经角度
    JIEQI_ANGLES = {
        "春分": 0, "清明": 15, "谷雨": 30, "立夏": 45,
        "小满": 60, "芒种": 75, "夏至": 90, "小暑": 105,
        "大暑": 120, "立秋": 135, "处暑": 150, "白露": 165,
        "秋分": 180, "寒露": 195, "霜降": 210, "立冬": 225,
        "小雪": 240, "大雪": 255, "冬至": 270, "小寒": 285,
        "大寒": 300, "立春": 315, "雨水": 330, "惊蛰": 345
    }
    
    year = date.year
    nearest_jieqi = None
    nearest_time = None
    min_diff = float('inf')
    
    # 检查前一年最后一个节气到下一年第一个节气
    for year_offset in [-1, 0, 1]:
        check_year = year + year_offset
        for jieqi, angle in JIEQI_ANGLES.items():
            jieqi_time = get_jieqi_date(check_year, angle)
            time_diff = abs((date - jieqi_time).total_seconds() / 3600)  # 转换为小时
            
            if time_diff < min_diff:
                min_diff = time_diff
                nearest_jieqi = jieqi
                nearest_time = jieqi_time
    
    return nearest_jieqi, nearest_time, min_diff

# 使用示例
if __name__ == "__main__":
    # 测试当前时间
    now = datetime.now()
    jieqi, jieqi_time, hours_diff = get_nearest_jieqi(now)
    print(f"最近的节气是：{jieqi}")
    print(f"节气时间：{jieqi_time}")
    print(f"相差小时数：{hours_diff:.2f}")
    

    
    
    