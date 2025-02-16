import uvicorn
from app import app

if __name__ == "__main__":
    print("=== 八字排盘系统服务启动 ===")
    print("系统访问地址: http://localhost:8000")
    print("API文档地址: http://localhost:8000/docs")
    print("========================")
    uvicorn.run(app, host="0.0.0.0", port=8000) 