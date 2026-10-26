
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "evaluation" / "retrieval_results.csv"
OUTPUT = ROOT / "evaluation" / "retrieval_metrics.csv"


def main():
    with INPUT.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    grouped = defaultdict(list)

    for row in rows:
        grouped[row["test_id"]].append(row)

    if len(grouped) != 22:
        raise ValueError(
            f"Expected 22 tests, found {len(grouped)}"
        )

    results = []

    for test_id, chunks in sorted(grouped.items()):

        if len(chunks) != 4:
            raise ValueError(
                f"{test_id} has {len(chunks)} chunks, expected 4"
            )

        # Require manual relevance assessment.
        for chunk in chunks:
            if chunk["relevant"] not in ("0", "1"):
                raise ValueError(
                    f"Missing relevance label for "
                    f"{test_id}, rank {chunk['rank']}"
                )

        chunks.sort(key=lambda x: int(x["rank"]))

        hit_at_1 = int(
            chunks[0]["relevant"] == "1"
        )

        hit_at_4 = int(
            any(chunk["relevant"] == "1" for chunk in chunks)
        )

        first_relevant_rank = next(
            (
                int(chunk["rank"])
                for chunk in chunks
                if chunk["relevant"] == "1"
            ),
            None
        )

        reciprocal_rank = (
            1.0 / first_relevant_rank
            if first_relevant_rank
            else 0.0
        )

        results.append({
            "test_id": test_id,
            "hit_at_1": hit_at_1,
            "hit_at_4": hit_at_4,
            "reciprocal_rank": reciprocal_rank,
        })

    total = len(results)

    hit1 = sum(r["hit_at_1"] for r in results) / total
    hit4 = sum(r["hit_at_4"] for r in results) / total
    mrr = sum(r["reciprocal_rank"] for r in results) / total

    with OUTPUT.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "test_id",
                "hit_at_1",
                "hit_at_4",
                "reciprocal_rank",
            ]
        )
        writer.writeheader()
        writer.writerows(results)

    print("===== RETRIEVAL METRICS =====")
    print(f"Evaluated questions: {total}")
    print(f"Hit@1: {hit1:.2%}")
    print(f"Hit@4: {hit4:.2%}")
    print(f"MRR@4: {mrr:.4f}")
    print(f"Saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
