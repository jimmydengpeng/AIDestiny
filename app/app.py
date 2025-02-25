from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from app.paipan_engine import BaziChartEngine
from typing import Dict, List
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="八字排盘系统",
    description="基于Python的八字排盘API服务",
    version="1.0.0"
)

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class BirthInfo(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    gender: str  # 添加性别字段

class BaziResponse(BaseModel):
    solar_date: str
    bazi_string: str
    five_elements: List[str]
    pillars: Dict[str, Dict[str, str]]
    ten_gods: Dict[str, Dict[str, str]]

@app.post("/api/calculate_bazi", response_model=BaziResponse)
async def calculate_bazi(birth_info: BirthInfo):
    try:
        # logger.info(f"收到请求：{birth_info}")
        
        # 验证输入
        if not (1900 <= birth_info.year <= 2100):
            raise HTTPException(status_code=400, detail="年份必须在1900-2100之间")
        if not (1 <= birth_info.month <= 12):
            raise HTTPException(status_code=400, detail="月份必须在1-12之间")
        if not (1 <= birth_info.day <= 31):
            raise HTTPException(status_code=400, detail="日期必须在1-31之间")
        if not (0 <= birth_info.hour <= 23):
            raise HTTPException(status_code=400, detail="小时必须在0-23之间")
        if birth_info.gender not in ["male", "female"]:
            raise HTTPException(status_code=400, detail="性别必须为male或female")

        # 创建日期对象
        birth_time = datetime(
            birth_info.year,
            birth_info.month,
            birth_info.day,
            birth_info.hour,
            0
        )

        # 计算八字
        engine = BaziChartEngine()
        bazi = engine.calculate_bazi(birth_time)
        
        # logger.info(f"计算结果：{bazi}")

        # 构造响应
        response = {
            "solar_date": f"{birth_info.year}年{birth_info.month}月{birth_info.day}日 {birth_info.hour:02d}时",
            "bazi_string": engine.get_bazi_string(bazi),
            "five_elements": bazi["five_elements"],
            "pillars": {
                "year": bazi["year"],
                "month": bazi["month"],
                "day": bazi["day"],
                "hour": bazi["hour"]
            },
            "ten_gods": bazi["ten_gods"]
        }

        return response

    except Exception as e:
        logger.error(f"发生错误：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return FileResponse("frontend/index.html", media_type="text/html; charset=utf-8")
