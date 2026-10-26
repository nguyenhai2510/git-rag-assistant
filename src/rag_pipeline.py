
from src.vector_store import search_documents
from src.llm import generate_answer


def ask_rag(question: str, top_k: int = 4):
    question = question.strip()

    if not question:
        raise ValueError("Câu hỏi không được để trống")

    # Step 1: Retrieve relevant documents
    chunks = search_documents(
        query=question,
        top_k=top_k,
    )

    if not chunks:
        return {
            "question": question,
            "answer": "Không tìm thấy tài liệu phù hợp.",
            "sources": [],
            "retrieved_chunks": [],
        }

    # Step 2: Build context for Gemini
    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[DOCUMENT {index}]\n"
            f"Title: {chunk['title']}\n"
            f"Source: {chunk['source']}\n"
            f"Content:\n{chunk['content']}"
        )

    context = "\n\n".join(context_parts)

    # Step 3: Generate grounded answer
    answer = generate_answer(
        question=question,
        context=context,
    )

    # Step 4: Collect retrieved sources
    sources = []
    seen = set()

    for chunk in chunks:
        url = chunk["source"]

        if url not in seen:
            sources.append({
                "title": chunk["title"],
                "url": url,
            })
            seen.add(url)

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": chunks,
    }
