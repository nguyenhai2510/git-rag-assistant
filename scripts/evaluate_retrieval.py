
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.vector_store import search_documents

DATASET = ROOT / "evaluation" / "test_questions.json"
OUTPUT = ROOT / "evaluation" / "retrieval_results.csv"

TOP_K = 4


def main():
    with DATASET.open("r", encoding="utf-8") as file:
        tests = json.load(file)

    rows = []

    print("===== RETRIEVAL EVALUATION =====")

    for test in tests:
        if not test["in_scope"]:
            continue

        question = test["question"]

        results = search_documents(
            query=question,
            top_k=TOP_K,
        )

        print(
            f"{test['id']} | "
            f"Retrieved: {len(results)} chunks"
        )

        for rank, item in enumerate(results, start=1):
            rows.append({
                "test_id": test["id"],
                "question": question,
                "expected_answer": test["expected_answer"],
                "rank": rank,
                "document": item["title"],
                "source": item["source"],
                "cosine_distance": round(
                    item["distance"], 4
                ),
                "retrieved_context": item["content"],
                "relevant": "",
            })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "test_id",
        "question",
        "expected_answer",
        "rank",
        "document",
        "source",
        "cosine_distance",
        "retrieved_context",
        "relevant",
    ]

    with OUTPUT.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=columns,
        )
        writer.writeheader()
        writer.writerows(rows)

    print("\n===== COMPLETE =====")
    print(f"In-scope questions: {sum(t['in_scope'] for t in tests)}")
    print(f"Retrieved rows: {len(rows)}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
