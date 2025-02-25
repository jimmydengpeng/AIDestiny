from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from app.paipan_engine import BaziPaipanEngine
from typing import Dict, List
import logging
import os
from app.model import get_chat_model
from langchain.schema import HumanMessage
from app.fate_owner import BirthInfo, FateOwner, Gender, BaziInfo

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

class BaziResponse(BaseModel):
    solar_date: str
    bazi_string: str
    five_elements: List[str]
    pillars: Dict[str, Dict[str, str]]
    ten_gods: Dict[str, Dict[str, str]]

@app.post("/api/calculate_bazi", response_model=BaziResponse)
async def calculate_bazi(birth_info: BirthInfo):
    try:
        # 验证输入已经由Pydantic模型完成
        
        # 创建命主对象
        fate_owner = FateOwner(
            gender=Gender.MALE if birth_info.gender == "male" else Gender.FEMALE,
            birth_info=birth_info
        )
        
        # 计算八字
        engine = BaziPaipanEngine()
        bazi_info = fate_owner.calculate_bazi(engine)
        
        # 构造响应
        response = {
            "solar_date": str(birth_info),
            "bazi_string": bazi_info.get_bazi_string(),
            "five_elements": bazi_info.five_elements,
            "pillars": {
                "year": {"heavenly_stem": bazi_info.year.heavenly_stem, "earthly_branch": bazi_info.year.earthly_branch},
                "month": {"heavenly_stem": bazi_info.month.heavenly_stem, "earthly_branch": bazi_info.month.earthly_branch},
                "day": {"heavenly_stem": bazi_info.day.heavenly_stem, "earthly_branch": bazi_info.day.earthly_branch},
                "hour": {"heavenly_stem": bazi_info.hour.heavenly_stem, "earthly_branch": bazi_info.hour.earthly_branch}
            },
            "ten_gods": {
                pillar: {"heavenly_stem": god.heavenly_stem, "earthly_branch": god.earthly_branch}
                for pillar, god in bazi_info.ten_gods.items()
            } if bazi_info.ten_gods else {}
        }

        return response

    except Exception as e:
        logger.error(f"发生错误：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/basic_report")
async def get_basic_report(birth_info: BirthInfo):
    """获取基本命盘解读"""
    # 创建命主对象
    fate_owner = FateOwner(
        gender=Gender.MALE if birth_info.gender == "male" else Gender.FEMALE,
        birth_info=birth_info
    )
    
    # 计算八字
    fate_owner.calculate_bazi()
    
    # 使用LLM生成解读
    llm = get_chat_model(model_source=os.environ.get("MODEL_SOURCE", "local"))
    prompt = f"请对以下八字进行命理解读：{fate_owner.bazi_info.get_bazi_string()}"
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    return {
        "bazi": fate_owner.bazi_info.get_bazi_string(),
        "reading": response.content
    }

@app.get("/")
async def root():
    return FileResponse("frontend/index.html", media_type="text/html; charset=utf-8")
