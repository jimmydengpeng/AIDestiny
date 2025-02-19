from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import requests
import json
from rich.console import Console
from rich import print

from utils.display_util import display_model_response

console = Console()

print(f"console size: ({console.width}, {console.height})")

# 远程Ollama服务ip
import platform
REMOTE_HOST = "192.168.11.8" if platform.system() == "Linux" else "127.0.0.1"
# Ollama服务端口
OLLAMA_PORT = 11434



def call_llm_model(host: str, port: int):
    """初始化并调用LLM模型
    
    Args:
        host: Ollama服务主机地址
        port: Ollama服务端口
        
    Returns:
        模型响应，如果调用失败返回None
    """
    # 初始化ChatOllama
    llm = ChatOllama(
        base_url=f"http://{host}:{port}",
        model="deepseek-r1:8b",
        temperature=0.7,
        timeout=30
    )
    
    # 创建测试消息
    # message = HumanMessage(content="你是谁")
    message = HumanMessage(content="9.8和9.11哪个大")
    
    # 调用模型并获取响应
    console.print("\n[yellow]正在调用模型...[/yellow]")
    return llm.invoke([message])



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

        response = call_llm_model(REMOTE_HOST, OLLAMA_PORT)

        if response:
            display_model_response(
                content=response.content,
                metadata=response.response_metadata,
                debug=True  # 在测试时启用调试信息
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