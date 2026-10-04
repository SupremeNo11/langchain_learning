# LangChain + LangGraph 工业级项目学习脚手架

从零系统学习 LangChain / LangGraph，配合工业级实战项目的项目骨架。

> **学习方式**：本项目是"框架 + 教学模板"，核心业务模块均为待实现的 TODO，
> 你需要按 [docs/00-learning-roadmap.md](docs/00-learning-roadmap.md) 的学习路线
> 逐步完成 [docs/01](docs/01-phase1-langchain-core.md)、[docs/02](docs/02-phase2-langgraph.md)、[docs/03](docs/03-phase3-industrial.md) 三个阶段的任务，
> 用 `pytest` 验收自己的实现。**先自己动手，再对照参考实现。**

## 目录结构

```
config/            配置中心（pydantic-settings + 模型供应商表）
src/
  core/            Layer1 基础层：LLM 工厂、日志、Prompt、向量库、检索、缓存
  capabilities/    Layer2 能力层：RAG、Agent 工具、记忆、路由
  graphs/          Layer3 编排层：LangGraph 状态、节点、工作流
  api/             Layer4 应用层：FastAPI 入口、路由、Schema
  utils/           工具函数
  quick_start/     阶段0 入门脚本(first_chat.py)
data/              raw 原始文档 / processed 清洗后 / vector_db 向量库持久化
tests/             unit 单测(不调LLM) / integration 集成(调真实LLM) / eval 评测
```

## 快速开始

```bash
# 1. 激活 conda 环境（示例: ai）
conda activate ai

# 2. 安装项目本身 + 补全依赖（langchain/langgraph 已装则跳过升级）
pip install -e ".[dev]"

# 3. 配置密钥
cp .env.example .env
# 编辑 .env 填入 LLM_API_KEY / ARK_API_KEY

# 4. 验证 LLM 连通
python src/quick_start/first_chat.py

# 5. 启动 API
uvicorn api.main:app --reload
# 健康检查: http://localhost:8000/health

# 6. 运行测试
pytest
```

## 学习路线

1. **阶段 0 基础**：LLM 连通、消息类型、invoke/stream/batch
2. **阶段 1 LangChain Core**：Prompt、OutputParser、LCEL、RAG 检索链路
3. **阶段 2 LangGraph**：StateGraph、节点/条件边、Agent、记忆持久化
4. **阶段 3 工业级**：混合检索+重排序、评估体系、可观测性、安全护栏
