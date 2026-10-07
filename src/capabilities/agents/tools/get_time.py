"""工具：获取时间。

@tool 装饰器会读取函数签名和 docstring，生成给模型看的"工具说明书"。
docstring 直接决定模型什么时候调用它、参数传什么。
"""
from langchain_core.tools import tool
from datetime import datetime

@tool
def get_current_time() -> str:
    """获取当前时间，返回格式为 YYYY-MM-DD HH:MM:SS 的本地时间字符串。"""
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time_str
