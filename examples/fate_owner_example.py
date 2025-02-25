#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
FateOwner类使用示例
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.fate_owner import BirthInfo, FateOwner, Gender
from rich.console import Console
from rich.panel import Panel

# 创建控制台对象
console = Console()

def main():
    # 创建生日信息
    birth_info = BirthInfo(
        year=1992,
        month=8,
        day=25,
        hour=8,
        minute=0
    )
    
    # 创建命主对象
    fate_owner = FateOwner(
        name="张三",
        gender=Gender.MALE,
        birth_info=birth_info
    )
    
    # 计算八字
    fate_owner.calculate_bazi()
    
    # 打印命主信息摘要
    console.print(Panel(
        fate_owner.get_summary(),
        title="命主信息",
        border_style="cyan",
        expand=False,
        padding=(1, 2)
    ))
    
    # 打印详细的八字信息
    if fate_owner.bazi_info:
        console.print("\n[bold]详细八字信息:[/bold]")
        
        # 打印四柱
        console.print("\n[cyan]四柱:[/cyan]")
        pillars = [
            ("年柱", fate_owner.bazi_info.year),
            ("月柱", fate_owner.bazi_info.month),
            ("日柱", fate_owner.bazi_info.day),
            ("时柱", fate_owner.bazi_info.hour)
        ]
        
        for name, pillar in pillars:
            console.print(f"{name}: {pillar.heavenly_stem}{pillar.earthly_branch}")
        
        # 打印五行
        console.print("\n[cyan]五行:[/cyan]")
        console.print(" ".join(fate_owner.bazi_info.five_elements))
        
        # 打印十神
        if fate_owner.bazi_info.ten_gods:
            console.print("\n[cyan]十神:[/cyan]")
            for pillar_name, god in fate_owner.bazi_info.ten_gods.items():
                pillar_name_cn = {
                    "year": "年柱",
                    "month": "月柱",
                    "day": "日柱",
                    "hour": "时柱"
                }.get(pillar_name, pillar_name)
                
                console.print(f"{pillar_name_cn}: 天干-{god.heavenly_stem}, 地支-{god.earthly_branch}")

if __name__ == "__main__":
    main() 