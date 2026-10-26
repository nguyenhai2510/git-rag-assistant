
import csv
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.rag_pipeline import ask_rag

DATASET = ROOT / "evaluation" / "test_questions.json"
OUTPUT = ROOT / "evaluation" / "generation_results.csv"

TOP_K = 4

COLUMNS = [
    "test_id",
    "category",
    "in_scope",
    "question",
    "expected_answer",
    "actual_answer",
    "retrieved_sources",
    "response_time",
    "status",
    "correctness",
    "faithfulness",
    "out_of_scope_pass",
    "notes",
]


def load_existing_results():
    if not OUTPUT.exists():
        return {}

    with OUTPUT.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        return {
            row["test_id"]: row
            for row in csv.DictReader(file)
        }


def save_results(results):
    with OUTPUT.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=COLUMNS
        )
        writer.writeheader()

        for test_id in sorted(results):
            writer.writerow(results[test_id])


def main():
    with DATASET.open(
        "r", encoding="utf-8"
    ) as file:
        tests = json.load(file)

    results = load_existing_results()

    print("===== GENERATION EVALUATION =====")
    print(f"Total tests: {len(tests)}")

    for test in tests:
        test_id = test["id"]

        # Skip previously successful cases.
        if (
            test_id in results
            and results[test_id]["status"] == "success"
        ):
            print(f"[SKIP] {test_id}")
            continue

        print(f"\n[RUN] {test_id}")

        start = time.perf_counter()

        try:
            result = ask_rag(
                question=test["question"],
                top_k=TOP_K,
            )

            elapsed = time.perf_counter() - start

            sources = [
                source["url"]
                for source in result["sources"]
            ]

            results[test_id] = {
                "test_id": test_id,
                "category": test["category"],
                "in_scope": test["in_scope"],
                "question": test["question"],
                "expected_answer": test["expected_answer"],
                "actual_answer": result["answer"],
                "retrieved_sources": json.dumps(
                    sources, ensure_ascii=False
                ),
                "response_time": round(elapsed, 3),
                "status": "success",
                "correctness": "",
                "faithfulness": "",
                "out_of_scope_pass": "",
                "notes": "",
            }

            print(f"[OK] {test_id}: {elapsed:.2f}s")

        except Exception as error:
            elapsed = time.perf_counter() - start

            results[test_id] = {
                "test_id": test_id,
                "category": test["category"],
                "in_scope": test["in_scope"],
                "question": test["question"],
                "expected_answer": test["expected_answer"],
                "actual_answer": "",
                "retrieved_sources": "",
                "response_time": round(elapsed, 3),
                "status": "error",
                "correctness": "",
                "faithfulness": "",
                "out_of_scope_pass": "",
                "notes": str(error)[:300],
            }

            print(f"[ERROR] {test_id}: {error}")

        # Save after every test.
        save_results(results)

        # Small interval between requests.
        time.sleep(6)

    success = sum(
        row["status"] == "success"
        for row in results.values()
    )

    print("\n===== SUMMARY =====")
    print(f"Successful: {success}/{len(tests)}")
    print(f"Saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
