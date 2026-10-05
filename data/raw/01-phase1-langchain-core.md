# 阶段1：LangChain Core 基础

> 目标：掌握 LangChain 核心组件，交付一条可运行的"基础 RAG 问答链路"。
> 前置：阶段0 已跑通 [first_chat.py](../src/quick_start/first_chat.py)。

## 1.1 任务总览

| 任务 | 文件 | 核心知识点 |
|---|---|---|
| 1.1 | [core/llm.py](../src/core/llm.py) | ChatOpenAI、配置与密钥 |
| 1.2 | [core/prompts.py](../src/core/prompts.py) | PromptTemplate / ChatPromptTemplate |
| 1.3 | [core/vectorstore.py](../src/core/vectorstore.py)、[rag/embedding.py](../src/capabilities/rag/embedding.py) | Embeddings、Chroma |
| 1.4 | [core/retriever.py](../src/core/retriever.py) | as_retriever |
| 1.5 | [rag/loader.py](../src/capabilities/rag/loader.py)、[rag/splitter.py](../src/capabilities/rag/splitter.py) | DocumentLoader、TextSplitter |
| 1.6 | [rag/qa_chain.py](../src/capabilities/rag/qa_chain.py) | LCEL、StrOutputParser |

## 1.2 任务 1.1：LLM 工厂

**知识点**
- `ChatOpenAI(model, api_key, base_url, temperature, streaming)`——兼容所有 OpenAI 协议服务商。
- 供应商注册表在 [config/llm.py](../config/llm.py)（模型名 / 密钥环境变量 / base_url），统一配置在 [config/settings.py](../config/settings.py)。

**要求**：实现 `create_llm`，支持通过 `provider` 参数切换供应商。

**验收**：运行 `python -c "from core.llm import create_llm; print(create_llm().model_name)"` 能打印模型名。

## 1.3 任务 1.2：Prompt 模板

**知识点**
- `ChatPromptTemplate.from_template("{var} ...")` —— 单段模板，变量用 `{}` 占位。
- `ChatPromptTemplate.from_messages([("system", ...), ("human", "{question}")])` —— 多段消息模板。
- 模板调用：`prompt.format_messages(**kwargs)` 得到消息列表。

**要求**：实现 `rag_qa_prompt`（来自 `RAG_QA_TEMPLATE`）与 `chat_prompt`。

**验收**：`pytest tests/unit/test_prompts.py -v` 通过。

## 1.4 任务 1.3：向量化与向量库

**知识点**
- `Embeddings` 接口：`embed_query` / `embed_documents`，负责把文本转向量。
- `Chroma(collection_name, embedding_function, persist_directory)`：向量数据库，支持持久化。

**要求**：实现 `get_embeddings` 与 `get_vectorstore`。

**自测问题**
- 为什么 `collection_name` 和 `persist_dir` 两个参数都要保留？
> 答：`persist_dir`决定存在哪个物理位置；`collection_name`决定存在目录下的哪个集合里面
- 换了 embedding 模型后，向量库还能复用吗？（答案：不能，需要重建）
> 答：不能，embeding模型换了之后，向量空间更换，原来的索引全部报废，必须重建

## 1.5 任务 1.4：检索器

**知识点**
- `vectorstore.as_retriever(search_kwargs={"k": n})`：把向量库变成"可调用对象"，`invoke(question)` 返回文档列表。

**要求**：实现 `get_retriever`，支持 `k` 与 `score_threshold`。

## 1.6 任务 1.5：文档加载与切分

**知识点**
- `TextLoader` / `PyPDFLoader`：加载不同格式文件 → `Document` 列表（含 `page_content` 与 `metadata`）。
- `RecursiveCharacterTextSplitter`：按分隔符递归切分，`chunk_size`（块大小）与 `chunk_overlap`（重叠）影响检索质量。

**要求**：实现 `load_document` / `load_directory` / `get_text_splitter` / `split_documents`。

**自测问题**
- overlap 过大/过小会有什么影响？
> 答：overlap掌管不同chunk之间的相关性。overlap太小，能减少切片数量，但是不同chunk之间的相关性相对较弱。overlap太大，导致切片数量太大，不同chunk之间的相关性较强。因此chunk_overlap的大小取50-80字符之间较为合适。
- 为什么中文切分要加入 `。！？；` 作为分隔符？
> 答：因为这些分隔符往往代表一段局部语义的结束，让spliter更加精准的切分。

## 1.7 任务 1.6：LCEL 问答链（阶段产出）

**知识点**
- LCEL：用 `|` 把 Runnable 串成管道，如 `prompt | llm | parser`。
- `{"context": retriever | format_docs, "question": RunnablePassthrough()}`：把输入拆分注入模板变量。
- `StrOutputParser()`：把模型输出转成纯字符串。

**要求**：实现 `format_docs` 与 `build_rag_chain`。

**验收**：`pytest tests/unit -v` 全部通过。

## 1.8 综合任务：CLI 文档问答

写一个脚本 `src/cli_rag.py`（新建），完成：

1. 读取 `data/raw/` 下的文档（放 1-2 篇你熟悉的 Markdown）
2. 加载 → 切分 → 向量化 → 存入 Chroma
3. 用 `build_rag_chain` 对文档内容提问

**运行示例**：

```bash
python src/cli_rag.py "你的文档讲了什么核心内容？"
```

**验收标准**
- 能基于文档内容正确回答，且资料中不存在的内容会被拒绝（不编造）。

---

完成 1.1~1.6 与综合任务后，进入 [阶段2：LangGraph](./02-phase2-langgraph.md)。
