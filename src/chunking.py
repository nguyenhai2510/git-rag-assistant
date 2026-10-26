
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120,
        separators=["\n## ", "\n\n", "\n", " ", ""],
    )

    chunks = []

    for document in documents:
        parts = splitter.split_text(document["content"])

        for index, part in enumerate(parts):
            chunks.append({
                "id": f"{document['id']}-{index:04d}",
                "content": part,
                "source": document["source"],
                "title": document["title"],
                "chunk_index": index,
            })

    return chunks
