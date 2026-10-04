"""示例工具：安全计算器。"""
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """将两个整数相加。"""
    return a + b
