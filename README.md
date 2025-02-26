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

- 输入出生日期和时间，选择性别，点击"计算八字"按钮，即可获取八字排盘结果。

## Todos

- [x] 命主信息
- [x] 排盘引擎
- [x] 大运计算
- [ ] 前端环境 Dockerfile
- [ ] 后端环境 Dockerfile 
- [ ] 提示词模版优化

## 项目结构

```bash
.
├── app/                    # 核心应用目录
│   ├── app.py              # FastAPI应用主程序
│   ├── paipan_engine.py    # 八字排盘引擎
│   ├── fate_owner.py       # 命主信息处理
│   ├── model.py            # AI模型接口
│   └── prompt_templates.py # 提示词模板
├── examples/               # 示例/测试用例文件
├── frontend/               # 前端目录
│   └── index.html          # 前端页面
├── utils/                  # 工具函数
├── pdf/                    # PDF文档资源
├── txt/                    # 文本资源
├── run_server.py           # 服务器启动脚本
├── requirements.txt        # 项目依赖
├── ROADMAP.md              # 项目路线图
└── README.md               # 项目说明文档
```
