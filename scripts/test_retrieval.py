
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.vector_store import search_documents


def main():
    question = (
        "Làm thế nào để hoàn tác commit gần nhất "
        "nhưng vẫn giữ lại code?"
    )

    print(f"\nQUESTION: {question}\n")

    results = search_documents(
        query=question,
        top_k=4,
    )

    for index, result in enumerate(results, start=1):
        print(f"\n{'=' * 60}")
        print(f"RESULT #{index}")
        print(f"Document: {result['title']}")
        print(f"Source: {result['source']}")
        print(f"Cosine distance: {result['distance']:.4f}")
        print("-" * 60)
        print(result["content"][:900])


if __name__ == "__main__":
    main()
