"""自定义工具集。新工具在此目录新增模块并在 __init__.py 注册。"""
from capabilities.agents.tools.calculator import add

# 注册到 ALL_TOOLS 后即可被 Agent 绑定
ALL_TOOLS = [add]
