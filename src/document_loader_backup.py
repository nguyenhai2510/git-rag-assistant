
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


def load_documents():
    documents = []

    for path in sorted(DATA_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")

        if not content.strip():
            continue

        documents.append({
            "id": path.stem,
            "content": content,
            "source": f"https://git-scm.com/docs/{path.stem}",
            "title": path.stem,
        })

    return documents
