# AI算命系统 使用说明

这是一个基于Python的八字排盘系统，使用寿星天文历（sxtwl）库进行农历和八字的计算。

## 功能特点

- 支持公历日期转换为农历
- 计算八字（年柱、月柱、日柱、时柱）
- 计算五行属性
- 提供格式化的八字输出

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动系统

1.启动后端服务：

```bash
python run_server.py
```

2.访问系统：

- 后端服务地址：<http://localhost:8000>
- API文档地址：<http://localhost:8000/docs>
- 前端页面：使用浏览器直接打开 frontend/index.html

## 使用方法

```python
from datetime import datetime
from bazi_chart_engine import BaziChartEngine

# 创建八字排盘引擎实例
engine = BaziChartEngine()

# 设置出生时间（示例：1990年1月1日12点）
birth_time = datetime(1990, 1, 1, 12, 0)

# 计算八字
bazi = engine.calculate_bazi(birth_time)

# 打印结果
print("八字:", engine.get_bazi_string(bazi))
print("五行:", " ".join(bazi["five_elements"]))
```

## 系统要求

- Python 3.6+
- sxtwl 2.0.6
- python-dateutil 2.8.2+
