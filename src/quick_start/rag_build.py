from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.chat_models import ChatOpenAI
import os

model = ChatOpenAI(
    model = "deepseek-v4.1-flash",
    api_key = os.getenv("ARK_API_KEY"),
    base_url = "https://ark.cn-beijing.volces.com/api/coding/v3",
    temperature = 0,
)

loader = TextLoader("data/raw/lesson-4-kv-cache/README_CN.md")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, # 每个片段约500字符
    chunk_overlap=50, # 相邻片段保留50字符重叠，避免切断语义
)

chunks = splitter.split_documents(documents)
print(f"原始文档数：{len(documents)}, 切片后片段数：{len(chunks)}")


# 向量化存储
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore


embeddings = OpenAIEmbeddings(
    model="doubao-embedding-vision",
    api_key=os.environ.get("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    check_embedding_ctx_length=False,   # 关键：直接发送原始文本
    chunk_size = 10,
)

vectorstore = InMemoryVectorStore.from_documents(chunks, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})  # 每次召回 4 段

question = "简单的KV cache 怎么实现？"
docs = retriever.invoke(question)
for doc in docs:
    print("*" * 50)
    print(doc.page_content)


# 检索与生成
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是老师。只能依据提供的资料回答，资料中没有的信息就明确的说不知道。"),
        ("human", "资料:\n {context} \n\n 问题:\n {question}"),
    ]
)

def rag_answer(question:str) -> str:
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)
    return model.invoke(prompt.format(context=context, question=question)).content

print(rag_answer("简单的KV cache 怎么实现？"))