
from functools import lru_cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-small"


@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(
        MODEL_NAME,
        device="cpu",
    )


def embed_documents(texts):
    model = get_embedding_model()

    inputs = [f"passage: {text}" for text in texts]

    vectors = model.encode(
        inputs,
        batch_size=16,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True,
    )

    return vectors.tolist()


def embed_query(query):
    model = get_embedding_model()

    vector = model.encode(
        f"query: {query}",
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    return vector.tolist()
