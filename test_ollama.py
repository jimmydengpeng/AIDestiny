from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import requests
import json
from rich.console import Console
from utils.display_util import display_model_response

console = Console()

print(console.width, console.height)

def test_remote_model():
    try:
        # 远程Ollama服务配置
        import platform
        REMOTE_HOST = "192.168.11.8" if platform.system() == "Linux" else "127.0.0.1"
        OLLAMA_PORT = 11434
        
        # 检查 Ollama 服务是否在运行
        try:
            response = requests.get(f"http://{REMOTE_HOST}:{OLLAMA_PORT}/api/version", 
                                  timeout=5)
            console.print(f"[green]Ollama服务状态: {response.status_code}[/green]")
            console.print(f"版本信息: {response.json()['version']}")
        except requests.exceptions.ConnectionError as e:
            console.print("[red]错误：无法连接到远程 Ollama 服务。[/red]")
            console.print(f"[red]详细错误: {str(e)}[/red]")
            return
        except Exception as e:
            console.print(f"[red]检查服务时发生错误: {str(e)}[/red]")
            return

        # 初始化ChatOllama
        llm = ChatOllama(
            base_url=f"http://{REMOTE_HOST}:{OLLAMA_PORT}",
            model="deepseek-r1:8b",
            temperature=0.7,
            timeout=30
        )
        
        # 创建测试消息
        # message = HumanMessage(content="你是谁")
        message = HumanMessage(content="9.11和9.8哪个大")
        
        # 调用模型并获取响应
        console.print("\n[yellow]正在调用模型...[/yellow]")
        response = llm.invoke([message])
        
        # 使用显示工具显示响应
        display_model_response(
            content=response.content,
            metadata=response.response_metadata,
            debug=True  # 在测试时启用调试信息
        )

    except requests.exceptions.RequestException as e:
        console.print(f"[red]API 请求错误: {str(e)}[/red]")
    except Exception as e:
        console.print(f"[red]发生错误: {str(e)}[/red]")
        # 打印完整的错误堆栈（调试用）
        import traceback
        console.print("[dim]" + traceback.format_exc() + "[/dim]")

if __name__ == "__main__":
    test_remote_model() 