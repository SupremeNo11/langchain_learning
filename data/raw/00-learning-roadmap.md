# LangChain / LangGraph 学习路线（总体开发文档）

> 目标：从零系统掌握 LangChain 与 LangGraph，以工业级项目为载体，边学边做。
> 原则：**文档驱动、任务制、测试验收**——每个模块先由你亲手实现，跑通测试后再进入下一任务。

---

## 1. 项目是什么

一个"RAG + Agent"的工业级问答系统骨架，四层架构：

```
Layer4 应用层  api/       FastAPI 入口、路由、Schema
Layer3 编排层  graphs/    LangGraph 状态、节点、工作流
Layer2 能力层  capabilities/  RAG、Agent 工具、记忆、路由
Layer1 基础层  core/      LLM 工厂、日志、Prompt、向量库、检索、缓存
```

框架已搭好，所有核心业务模块均为**待实现的教学模板**（见下文目录地图），每个文件头部标注了所属阶段与任务编号。

## 2. 阶段总览

| 阶段 | 主题 | 核心产出 | 验收标准 |
|---|---|---|---|
| 阶段0 | 环境与连通性 | 能调用 LLM | `python src/quick_start/first_chat.py` 输出中文回答 |
| 阶段1 | LangChain Core | 基础 RAG 链路（LCEL） | 单测通过 + CLI 文档问答可运行 |
| 阶段2 | LangGraph | RAG Graph + 带工具 Agent | `rag_flow` 跑通 + Agent 可调工具 |
| 阶段3 | 工业级模式 | 完整 API + 缓存/路由/评估 | `/chat` 全链路 + 评测报告 |

## 3. 学习方法（务必先读）

1. **先读对应阶段的文档**（`docs/01|02|03-*.md`），理解概念。
2. **自己动手实现**模板文件中的 TODO，不确定时可向我提问。
3. **用测试验收**：`pytest tests/unit -v`，测试通过即达标。
4. **对照检查**：实现完成后可向我要"参考实现"进行对照，加深理解。
5. **每阶段结束时**完成该阶段文档末尾的"综合任务"。

## 4. 目录地图（哪个阶段学哪个目录）

```
config/                 基础设施，已就绪（供应商注册表 + 统一配置）
src/
  core/
    llm.py              阶段1-1.1   LLM 工厂
    prompts.py          阶段1-1.2   Prompt 模板
    vectorstore.py      阶段1-1.3   向量库封装
    retriever.py        阶段1-1.4   检索器封装
    log.py              基础设施，已就绪
    cache.py            阶段3-3.1   TTL 缓存
  capabilities/
    rag/loader.py       阶段1-1.5   文档加载
    rag/splitter.py     阶段1-1.5   文档切分
    rag/embedding.py    阶段1-1.3   向量化
    rag/qa_chain.py     阶段1-1.6   LCEL 问答链
    agents/tools/       阶段2-2.4   工具集（示例已就绪）
    agents/prompt.py    阶段2-2.4   Agent 提示词
    memory/conversation.py  阶段2-2.5  会话记忆
    memory/longterm.py  阶段2-2.5   长期记忆（占位）
    routing/router.py   阶段3-3.2   意图路由
  graphs/
    state.py            阶段2-2.1   状态定义
    nodes/              阶段2-2.2   检索/生成节点
    workflows/rag_flow.py  阶段2-2.3  RAG 工作流
  api/
    main.py / schemas.py   基础设施，已就绪
    routers/chat.py     阶段3-3.3   对话路由
tests/
  unit/                 离线单测（验收标准）
  integration/          集成测试（需真实 LLM）
  eval/                 评测（阶段3）
data/
  raw/                  放你的原始文档（PDF/MD/TXT）
```

## 5. 环境准备

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # 填入 LLM_API_KEY / ARK_API_KEY
python src/quick_start/first_chat.py    # 阶段0 验收
```

## 6. 常见问题

- **导入报错**：本框架将 `config/core/capabilities/graphs/api` 注册为顶层包，`pip install -e .` 后即可直接 `from core.llm import ...`。
- **`tests/unit` 报 ERROR（NotImplementedError）**：这是正常的——对应的 TODO 还没实现，实现后即通过。
- **不知道下一步做什么**：看本文件第 4 节地图 + 各阶段文档的任务编号，按顺序推进。
