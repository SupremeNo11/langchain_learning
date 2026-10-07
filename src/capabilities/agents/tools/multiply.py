"""工具：整数乘法。—— 阶段2 任务 2.4 示范

@tool 装饰器会读取函数签名和 docstring，生成给模型看的"工具说明书"。
docstring 直接决定模型什么时候调用它、参数传什么。
"""
from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """将两个整数相乘。任何乘法计算都必须使用这个工具。"""
    return a * b
