from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

import requests
import json
from rich import print
from utils.display_util import display_model_response


# 远程Ollama服务ip
import platform
REMOTE_HOST = "192.168.11.8" if platform.system() == "Linux" else "127.0.0.1"
# Ollama服务端口
OLLAMA_PORT = 11434

STREAM_OUTPUT = False


def init_model(host: str, port: int) -> ChatOllama:
    """初始化LLM模型
    
    Args:
        host: Ollama服务主机地址
        port: Ollama服务端口
        
    Returns:
        初始化好的ChatOllama实例
    """
    return ChatOllama(
        base_url=f"http://{host}:{port}",
        model="deepseek-r1:8b",
        temperature=0.7,
        timeout=30
    )


def get_messages():
    """初始化消息
    
    Returns:
        初始化好的消息
    """
    # message = HumanMessage(content="你是谁")
    # message = HumanMessage(content="9.8和9.11哪个大")

    # messages = [
    #     SystemMessage("Translate the following from English into Chinese"),
    #     HumanMessage("hi!"),
    # ]

    # messages = [
    #     SystemMessage("你是一个数学家"),
    #     HumanMessage("9.8和9.11哪个大"),
    # ]


    system_template = "Translate the following from English into {language}. Be casual, colloquial, witty."

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )

    messages = prompt_template.invoke({"language": "Chinese", "text": "Give you some color see see!"})


    return messages



def invoke_model(model, messages):
    """调用模型
    
    Args:
        model: 模型
        messages: 消息
        
    Returns:
        模型响应，如果调用失败返回None
    """
    # 调用模型并获取响应
    print("\n[yellow]正在调用模型...[/yellow]")
    return model.invoke(messages)



def main():
    try:
        # 检查 Ollama 服务是否在运行
        try:
            response = requests.get(f"http://{REMOTE_HOST}:{OLLAMA_PORT}/api/version", timeout=5)
            print(f"Ollama服务状态: [green]{response.status_code}[/green]")
            print(f"版本信息: {response.json()['version']}")
        except requests.exceptions.ConnectionError as e:
            print("[red]错误：无法连接到远程 Ollama 服务。[/red]")
            print(f"[red]详细错误: {str(e)}[/red]")
            return
        except Exception as e:
            print(f"[red]检查服务时发生错误: {str(e)}[/red]")
            return

            
        
        # 初始化ChatOllama
        model = init_model(REMOTE_HOST, OLLAMA_PORT)

        messages = get_messages()

        if STREAM_OUTPUT:
            for token in model.stream(messages):
                print(token.content, end='')

        else:
            response = invoke_model(model, messages)
            # print(response)
            if response:
                display_model_response(
                    content=response.content,
                    response_metadata=response.response_metadata,
                    usage_metadata=response.usage_metadata,
                    debug=False  # 在测试时启用调试信息
                )


    except requests.exceptions.RequestException as e:
        print(f"[red]API 请求错误: {str(e)}[/red]")
    except Exception as e:
        print(f"[red]发生错误: {str(e)}[/red]")
        # 打印完整的错误堆栈（调试用）
        import traceback
        print("[dim]" + traceback.format_exc() + "[/dim]")

if __name__ == "__main__":
    main() 