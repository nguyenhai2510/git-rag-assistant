
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.document_loader import load_documents
from src.chunking import split_documents
from src.vector_store import index_chunks


def main():
    print("===== GIT RAG INDEXING =====")

    documents = load_documents()
    print(f"Documents: {len(documents)}")

    if not documents:
        raise RuntimeError("No Markdown documents found.")

    chunks = split_documents(documents)
    print(f"Chunks: {len(chunks)}")

    if not chunks:
        raise RuntimeError("No chunks generated.")

    total = index_chunks(chunks)

    print("\n===== INDEXING COMPLETE =====")
    print(f"Chunks stored: {total}")


if __name__ == "__main__":
    main()
