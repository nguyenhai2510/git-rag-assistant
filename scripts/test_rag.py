
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.rag_pipeline import ask_rag


def main():
    questions = [
        "Làm thế nào để hoàn tác commit gần nhất "
        "nhưng vẫn giữ lại code?",

        "Git fetch khác Git pull như thế nào?",

        "Đã push một commit lỗi, tôi nên dùng "
        "git reset hay git revert?",
    ]

    for index, question in enumerate(questions, start=1):
        print("\n" + "=" * 65)
        print(f"TEST CASE #{index}")
        print("=" * 65)

        print(f"\nQUESTION: {question}")

        result = ask_rag(question, top_k=4)

        print("\n===== RAG ANSWER =====")
        print(result["answer"])

        print("\n===== RETRIEVED SOURCES =====")
        for source in result["sources"]:
            print(f"- {source['title']}")
            print(f"  {source['url']}")

        print("\n===== RETRIEVAL DETAILS =====")
        for rank, chunk in enumerate(
            result["retrieved_chunks"], start=1
        ):
            print(
                f"{rank}. {chunk['title']} "
                f"| distance={chunk['distance']:.4f}"
            )


if __name__ == "__main__":
    main()
