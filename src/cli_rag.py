"""RAG问答 CLI —— 阶段1 综合任务（入口薄壳: 建库逻辑在 capabilities.assembly）

用法:
    python src/cli_rag.py "本项目的四层架构是什么？"
"""
import sys

from capabilities.assembly import TOP_K, get_or_build_store
from capabilities.rag.qa_chain import build_rag_chain


def main() -> None:
    if len(sys.argv) < 2:
        print('用法: python src/cli_rag.py "你的问题"')
        sys.exit(1)

    question = sys.argv[1]
    vs = get_or_build_store()
    chain = build_rag_chain(vs, k=TOP_K)

    print(f"\n[question] {question}")
    answer = chain.invoke(question)
    print("\n=== 回答 ===")
    print(answer)


if __name__ == "__main__":
    main()
