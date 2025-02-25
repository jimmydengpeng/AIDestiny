from app.model import get_chat_model
from langchain_core.messages import HumanMessage


def test_langchain_api():
    # 加载环境变量
    llm = get_chat_model(model_source="aliyun")
    
    try:
        # 创建消息
        messages = [
            HumanMessage(content="9.9和9.11谁大")
        ]
        
        # 发送请求
        print("正在发送请求...")
        response = llm.invoke(messages)
        
        print("\n回答：")
        print(response.content)
        
    except Exception as e:
        print(f"调用过程中发生错误: {str(e)}")

if __name__ == "__main__":
    test_langchain_api() 