#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
FateOwner类和BaziPaipanEngine类的使用示例
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.fate_owner import (
    SolarBirthInfo, LunarBirthInfo, FateOwner, Gender,
    HeavenlyStem, EarthlyBranch, TenGodType
)
from app.paipan_engine import BaziPaipanEngine 
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# 创建控制台对象
console = Console()

def print_birth_info(fate_owner: FateOwner):
    """打印生日信息"""
    console.print("\n[bold cyan]生日信息[/bold cyan]")
    if fate_owner.solar_birth_info:
        console.print(f"阳历: {fate_owner.solar_birth_info}")
    if fate_owner.lunar_birth_info:
        console.print(f"农历: {fate_owner.lunar_birth_info}")

def print_pillar_info(pillar_name: str, pillar, ten_god_info=None):
    """打印单柱信息"""
    table = Table(show_header=False, show_lines=True)
    table.add_column("项目", style="cyan")
    table.add_column("内容", style="green")
    
    table.add_row("天干", pillar.heavenly_stem.value)
    if ten_god_info:
        table.add_row("天干十神", ten_god_info.heavenly_stem.value)
    
    table.add_row("地支", pillar.earthly_branch.value)
    if ten_god_info:
        table.add_row("地支十神", ten_god_info.earthly_branch.value)
    
    if pillar.hidden_stem:
        hidden_stems_str = ", ".join(stem.value for stem in pillar.hidden_stem)
        table.add_row("藏干", hidden_stems_str)
        if ten_god_info and ten_god_info.hidden_stems:
            hidden_gods_str = ", ".join(god.value for god in ten_god_info.hidden_stems)
            table.add_row("藏干十神", hidden_gods_str)
    
    console.print(Panel(table, title=f"[bold]{pillar_name}[/bold]"))

def print_bazi_info(fate_owner: FateOwner):
    """打印八字信息"""
    if not fate_owner.bazi_info:
        console.print("[red]未计算八字信息[/red]")
        return
    
    console.print("\n[bold cyan]八字信息[/bold cyan]")
    
    # 打印四柱
    pillars = [
        ("年柱", fate_owner.bazi_info.year_pillar, "year"),
        ("月柱", fate_owner.bazi_info.month_pillar, "month"),
        ("日柱", fate_owner.bazi_info.day_pillar, "day"),
        ("时柱", fate_owner.bazi_info.hour_pillar, "hour")
    ]
    
    for pillar_name, pillar, key in pillars:
        ten_god_info = fate_owner.bazi_info.ten_gods.get(key) if fate_owner.bazi_info.ten_gods else None
        print_pillar_info(pillar_name, pillar, ten_god_info)
    
    # 打印五行
    if fate_owner.bazi_info.five_elements:
        console.print("\n[bold cyan]五行[/bold cyan]")
        console.print(fate_owner.bazi_info.get_five_elements_string())

def print_destiny_cycle_info(fate_owner: FateOwner):
    """打印大运信息"""
    if not fate_owner.bazi_info or not fate_owner.bazi_info.destiny_cycle:
        console.print("[red]未计算大运信息[/red]")
        return
    
    console.print("\n[bold cyan]大运信息[/bold cyan]")
    
    # 创建大运信息表格
    table = Table(show_header=True)
    table.add_column("序", style="cyan", justify="center")
    table.add_column("干支", style="green")
    table.add_column("藏干", style="yellow")
    table.add_column("年龄", style="magenta")
    
    # 添加大运数据
    start_age = fate_owner.bazi_info.destiny_cycle.start_age
    for i, cycle in enumerate(fate_owner.bazi_info.destiny_cycle.cycles, 1):
        age = (i * 10) + start_age.years
        hidden_stems = ", ".join(str(stem) for stem in cycle.hidden_stem) if cycle.hidden_stem else ""
        table.add_row(
            str(i),
            f"{cycle}",
            hidden_stems,
            f"{age}岁"
        )
    
    # 打印起运信息
    direction = "顺" if fate_owner.bazi_info.destiny_cycle.is_forward else "逆"
    console.print(f"[cyan]起运年龄:[/cyan] {start_age}")
    console.print(f"[cyan]大运方向:[/cyan] {direction}行")
    
    # 打印大运表格
    console.print(table)

def test_solar_birth():
    """测试阳历生日信息"""
    console.print("\n=== 测试阳历生日信息 ===")
    
    # 创建阳历生日信息
    solar_birth_info = SolarBirthInfo(
        year=2025,
        month=2,
        day=27,
        hour=22,
        minute=27
    )
    
    # 创建命主对象（使用阳历）
    fate_owner = FateOwner(
        name="张三",
        gender=Gender.MALE,
        solar_birth_info=solar_birth_info
    )
    
    # 计算八字
    fate_owner.calculate_bazi()
    
    # 打印命主信息摘要
    console.print(Panel(
        fate_owner.get_summary(),
        title="命主信息（阳历）",
        border_style="cyan"
    ))
    
    # 打印详细信息
    print_birth_info(fate_owner)
    print_bazi_info(fate_owner)
    print_destiny_cycle_info(fate_owner)

def test_lunar_birth():
    """测试农历生日信息"""
    console.print("\n=== 测试农历生日信息 ===")
    
    # 创建农历生日信息
    lunar_birth_info = LunarBirthInfo(
        year=2024,
        month=12,
        day=30,
        hour=23,
        minute=0,
        is_leap_month=False
    )
    
    # 创建命主对象（使用农历）
    fate_owner = FateOwner(
        name="李四",
        gender=Gender.FEMALE,
        lunar_birth_info=lunar_birth_info
    )
    
    # 计算八字
    fate_owner.calculate_bazi()
    
    # 打印命主信息摘要
    console.print(Panel(
        fate_owner.get_summary(),
        title="命主信息（农历）",
        border_style="magenta"
    ))
    
    # 打印详细信息
    print_birth_info(fate_owner)
    print_bazi_info(fate_owner)
    print_destiny_cycle_info(fate_owner)

def test_date_conversion():
    """测试日期转换"""
    console.print("\n=== 测试日期转换 ===")
    
    # 创建排盘引擎
    engine = BaziPaipanEngine()
    
    # 测试阳历转农历
    solar_date = {"year": 1992, "month": 8, "day": 25}
    lunar_date = engine.solar_to_lunar(**solar_date)
    
    console.print("[cyan]阳历转农历:[/cyan]")
    console.print(f"阳历: {solar_date['year']}年{solar_date['month']}月{solar_date['day']}日")
    console.print(f"农历: {lunar_date['year']}年{lunar_date['month']}月{lunar_date['day']}日")
    
    # 测试农历转阳历
    lunar_date = {"year": 1992, "month": 7, "day": 27, "is_leap_month": False}
    solar_date = engine.lunar_to_solar(**lunar_date)
    
    console.print("\n[cyan]农历转阳历:[/cyan]")
    console.print(f"农历: {lunar_date['year']}年{lunar_date['month']}月{lunar_date['day']}日")
    console.print(f"阳历: {solar_date['year']}年{solar_date['month']}月{solar_date['day']}日")

def test_special_cases():
    """测试特殊情况"""
    console.print("\n=== 测试特殊情况 ===")
    
    # 测试闰月
    lunar_birth_info = LunarBirthInfo(
        year=1990,
        month=6,
        day=1,
        hour=12,
        is_leap_month=True
    )
    
    fate_owner = FateOwner(
        name="王五",
        gender=Gender.MALE,
        lunar_birth_info=lunar_birth_info
    )
    
    fate_owner.calculate_bazi()
    
    console.print(Panel(
        fate_owner.get_summary(),
        title="闰月测试",
        border_style="yellow"
    ))
    print_destiny_cycle_info(fate_owner)
    
    # 测试子时（夜里23-1点）
    solar_birth_info = SolarBirthInfo(
        year=1990,
        month=7,
        day=15,
        hour=0
    )
    
    fate_owner = FateOwner(
        name="赵六",
        gender=Gender.FEMALE,
        solar_birth_info=solar_birth_info
    )
    
    fate_owner.calculate_bazi()
    
    console.print(Panel(
        fate_owner.get_summary(),
        title="子时测试",
        border_style="yellow"
    ))
    print_destiny_cycle_info(fate_owner)
    
    # 测试1996年农历三月二十六日下午2点
    lunar_birth_info = LunarBirthInfo(
        year=1996,
        month=3,
        day=26,
        hour=14,
        is_leap_month=False
    )
    
    fate_owner = FateOwner(
        name="测试大运",
        gender=Gender.MALE,  # 测试男性
        lunar_birth_info=lunar_birth_info
    )
    
    fate_owner.calculate_bazi()
    
    console.print(Panel(
        fate_owner.get_summary(),
        title="1996年大运测试",
        border_style="yellow"
    ))
    print_destiny_cycle_info(fate_owner)

def test_gender_cases():
    """测试不同性别和年干阴阳组合的情况"""
    console.print("\n=== 测试性别和年干阴阳组合 ===")
    
    # 测试数据
    test_cases = [
        ("男阳年", Gender.MALE, 1984),    # 甲子年，阳年
        ("男阴年", Gender.MALE, 1985),    # 乙丑年，阴年
        ("女阳年", Gender.FEMALE, 1984),  # 甲子年，阳年
        ("女阴年", Gender.FEMALE, 1985)   # 乙丑年，阴年
    ]
    
    for case_name, gender, year in test_cases:
        solar_birth_info = SolarBirthInfo(
            year=year,
            month=7,
            day=1,
            hour=12
        )
        
        fate_owner = FateOwner(
            name=f"测试_{case_name}",
            gender=gender,
            solar_birth_info=solar_birth_info
        )
        
        fate_owner.calculate_bazi()
        
        console.print(Panel(
            fate_owner.get_summary(),
            title=f"{case_name}测试",
            border_style="blue"
        ))
        print_destiny_cycle_info(fate_owner)

def main():
    """主函数"""
    console.print("[bold]八字排盘系统测试[/bold]")
    
    try:
        # 测试阳历生日
        test_solar_birth()
        
        # 测试农历生日
        test_lunar_birth()
        
        # 测试日期转换
        test_date_conversion()
        
        # 测试特殊情况
        test_special_cases()
        
        # 测试性别和年干阴阳组合
        test_gender_cases()
        
    except Exception as e:
        console.print(f"[red]发生错误：{str(e)}[/red]")

if __name__ == "__main__":
    main() 