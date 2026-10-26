
from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "storage" / "chroma_db"

COLLECTION_NAME = "git_documentation_curated"


def get_collection():
    DB_PATH.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def index_chunks(chunks, batch_size=100):
    collection = get_collection()

    from src.embeddings import embed_documents

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        texts = [chunk["content"] for chunk in batch]
        vectors = embed_documents(texts)

        collection.upsert(
            ids=[chunk["id"] for chunk in batch],
            documents=texts,
            embeddings=vectors,
            metadatas=[
                {
                    "source": chunk["source"],
                    "title": chunk["title"],
                    "chunk_index": chunk["chunk_index"],
                }
                for chunk in batch
            ],
        )

    return collection.count()


def search_documents(query, top_k=4):
    from src.embeddings import embed_query

    collection = get_collection()

    if collection.count() == 0:
        raise RuntimeError(
            "Vector database is empty. Run ingestion first."
        )

    query_vector = embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    for content, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        matches.append({
            "content": content,
            "source": metadata["source"],
            "title": metadata["title"],
            "distance": distance,
        })

    return matches
