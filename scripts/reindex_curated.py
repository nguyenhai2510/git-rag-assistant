
from pathlib import Path
import sys

import chromadb

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.document_loader import load_documents
from src.chunking import split_documents
from src.embeddings import embed_documents

DB_PATH = ROOT / "storage" / "chroma_db"
COLLECTION_NAME = "git_documentation_curated"


def main():
    print("===== CURATED KNOWLEDGE BASE INDEXING =====")

    documents = load_documents()
    print(f"Documents: {len(documents)}")

    if len(documents) != 15:
        raise RuntimeError(
            f"Expected 15 documents, found {len(documents)}"
        )

    chunks = split_documents(documents)
    print(f"Chunks: {len(chunks)}")

    if not chunks:
        raise RuntimeError("No chunks generated")

    # Generate embeddings before modifying the DB.
    print("Generating embeddings...")

    texts = [chunk["content"] for chunk in chunks]
    vectors = embed_documents(texts)

    DB_PATH.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    # Use a separate collection, preserving the old one.
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # Clear existing curated records for a clean re-index.
    existing = collection.get(include=[])

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    print("Saving curated embeddings...")

    batch_size = 100

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        batch_vectors = vectors[start:start + batch_size]

        collection.upsert(
            ids=[chunk["id"] for chunk in batch],
            documents=[
                chunk["content"] for chunk in batch
            ],
            embeddings=batch_vectors,
            metadatas=[
                {
                    "source": chunk["source"],
                    "title": chunk["title"],
                    "chunk_index": chunk["chunk_index"],
                }
                for chunk in batch
            ],
        )

    print("\n===== INDEXING COMPLETE =====")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Chunks stored: {collection.count()}")


if __name__ == "__main__":
    main()
