# 🧚‍♀️飞灵（Fatelling）- AI智能命运决策助手

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

- 后端服务地址：<http://localhost:8080>
- API文档地址：<http://localhost:8080/docs>
- 前端页面：使用浏览器直接打开 frontend/index.html

## 使用方法

### 模型部署

#### 远程模型调用

1. 在项目根目录创建 `.env` 文件
2. 输入你的API密钥，例如：`API_KEY=your_api_key_here`

#### 本地模型部署

1. 安装并使用Ollama下载模型
2. 启动本地模型，例如：`ollama run deepseek-r1:8b`

### 使用方法

- 输入出生日期和时间，选择性别，点击“计算八字”按钮，即可获取八字排盘结果。

## 系统要求

- Python 3.6+
- sxtwl 2.0.6
- python-dateutil 2.8.2+
