from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from datetime import datetime
from app.paipan_engine import BaziPaipanEngine
from typing import Dict, List, AsyncGenerator, Union
import logging
import os
from app.model import get_chat_model
from langchain.schema import HumanMessage
from app.fate_owner import FateOwner, Gender, BaziInfo, SolarBirthInfo, LunarBirthInfo
from app.prompt_templates import get_bazi_report_prompt
import json

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
app.mount("/", StaticFiles(directory="frontend/ai-destiny-vue/dist", html=True), name="static")

class BaziResponse(BaseModel):
    solar_date: str
    lunar_date: str
    bazi_string: str
    five_elements: List[str]
    pillars: Dict[str, Dict[str, str]]
    ten_gods: Dict[str, Dict[str, str]]

@app.post("/api/calculate_bazi", response_model=BaziResponse)
async def calculate_bazi(birth_info: SolarBirthInfo):
    try:
        # 验证输入已经由Pydantic模型完成
        
        # 创建命主对象
        fate_owner = FateOwner(
            gender=Gender.MALE if birth_info.gender == "male" else Gender.FEMALE,
            solar_birth_info=birth_info
        )
        
        # 计算八字
        engine = BaziPaipanEngine()
        bazi_info = fate_owner.calculate_bazi(engine)
        
        # 构造响应
        response = {
            "solar_date": str(birth_info),
            "lunar_date": str(fate_owner.lunar_birth_info) if fate_owner.lunar_birth_info else None,
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

async def generate_report_stream(birth_info: Union[SolarBirthInfo, LunarBirthInfo]) -> AsyncGenerator[str, None]:
    """生成流式命理报告"""
    try:
        # 创建命主对象
        fate_owner = FateOwner(
            gender=Gender.MALE if birth_info.gender == "male" else Gender.FEMALE,
            solar_birth_info=birth_info if isinstance(birth_info, SolarBirthInfo) else None,
            lunar_birth_info=birth_info if isinstance(birth_info, LunarBirthInfo) else None
        )
        
        # 计算八字
        engine = BaziPaipanEngine()
        bazi_info = fate_owner.calculate_bazi(engine)
        
        # 准备提示词数据
        prompt_data = {
            "gender": birth_info.gender,
            "birth_date": str(birth_info),
            "lunar_date": str(fate_owner.lunar_birth_info) if fate_owner.lunar_birth_info else None,
            "bazi": bazi_info.get_bazi_string(),
            "five_elements": " ".join(bazi_info.five_elements)
        }
        
        # 获取提示词
        prompt = get_bazi_report_prompt(prompt_data)
        
        # 使用LLM生成解读
        llm = get_chat_model(model_source=os.environ.get("MODEL_SOURCE", "local"))
        
        # 创建消息
        messages = [HumanMessage(content=prompt)]
        
        # 流式生成报告
        logger.info("开始生成命理报告...")
        
        # 发送开始事件
        yield f"event: start\ndata: {{}}\n\n"
        
        # 使用流式输出 - 直接使用astream方法
        buffer = ""
        async for chunk in llm.astream(messages):
            if hasattr(chunk, 'content') and chunk.content:
                content = chunk.content
                logger.debug(f"收到内容块: {content}")
                
                # 将内容添加到缓冲区
                buffer += content
                
                # 逐字符发送，以实现更好的流式效果
                for char in content:
                    # 使用SSE格式发送数据
                    yield f"event: message\ndata: {json.dumps({'text': char})}\n\n"
        
        # 发送完成事件
        yield f"event: end\ndata: {{}}\n\n"
        
        logger.info("命理报告生成完成")
        
    except Exception as e:
        logger.error(f"生成命理报告时发生错误：{str(e)}", exc_info=True)
        # 发送错误事件
        yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

@app.post("/api/fate_report")
@app.get("/api/fate_report")  # 添加GET方法支持
async def get_fate_report(birth_info: Union[SolarBirthInfo, LunarBirthInfo] = None, data: str = None):
    """获取流式命理报告"""
    # 如果通过查询参数传递数据，则解析数据
    if birth_info is None and data:
        try:
            birth_data = json.loads(data)
            # 判断是否为农历数据
            if "lunar_year" in birth_data:
                birth_info = LunarBirthInfo(**birth_data)
            else:
                birth_info = SolarBirthInfo(**birth_data)
        except Exception as e:
            logger.error(f"解析查询参数失败：{str(e)}")
            raise HTTPException(status_code=400, detail=f"无效的请求数据: {str(e)}")
    
    # 如果仍然没有birth_info，则返回错误
    if birth_info is None:
        raise HTTPException(status_code=400, detail="缺少必要的出生信息")
    
    return StreamingResponse(
        generate_report_stream(birth_info),
        media_type="text/event-stream"
    )

@app.post("/api/basic_report")
async def get_basic_report(birth_info: SolarBirthInfo):
    """获取基本命盘解读"""
    try:
        # 创建命主对象
        fate_owner = FateOwner(
            gender=Gender.MALE if birth_info.gender == "male" else Gender.FEMALE,
            solar_birth_info=birth_info
        )
        
        # 计算八字
        engine = BaziPaipanEngine()
        bazi_info = fate_owner.calculate_bazi(engine)
        
        # 使用LLM生成解读
        llm = get_chat_model(model_source=os.environ.get("MODEL_SOURCE", "local"))
        prompt = f"请对以下八字进行命理解读：{bazi_info.get_bazi_string()}"
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        
        return {
            "bazi": bazi_info.get_bazi_string(),
            "reading": response.content
        }
    except Exception as e:
        logger.error(f"生成命盘解读时发生错误：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

