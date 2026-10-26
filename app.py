
import streamlit as st

from src.rag_pipeline import ask_rag


# ==================================================
# 1. Page Configuration
# ==================================================

st.set_page_config(
    page_title="Git RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# 2. Session State
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "latest_retrieval" not in st.session_state:
    st.session_state.latest_retrieval = []


# ==================================================
# 3. Sidebar
# ==================================================

with st.sidebar:
    st.title("⚙️ Configuration")

    st.markdown("### RAG Settings")

    top_k = st.slider(
        "Number of retrieved chunks (Top-K)",
        min_value=1,
        max_value=8,
        value=4,
        step=1,
        help="Số đoạn tài liệu được đưa vào context.",
    )

    st.divider()

    st.markdown("### Knowledge Base")

    st.info(
        "Dataset: Git Documentation Curated\n\n"
        "Documents: 15\n\n"
        "Indexed chunks: 32\n\n"
        "Embedding: multilingual-e5-small\n\n"
        "LLM: Gemini 3.5 Flash-Lite"
    )

    st.caption(
        "Các số liệu trên phản ánh lần indexing "
        "đã xác nhận, không tự cập nhật."
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.session_state.latest_retrieval = []
        st.rerun()

    st.markdown("---")
    st.caption(
        "Git RAG Assistant | University Project"
    )


# ==================================================
# 4. Header
# ==================================================

st.title("🤖 Git RAG Assistant")

st.markdown(
    """
    **Trợ lý AI tra cứu tài liệu Git ứng dụng
    Retrieval-Augmented Generation (RAG).**

    Đặt câu hỏi bằng tiếng Việt và khám phá
    những tài liệu Git được hệ thống truy xuất.
    """
)

st.divider()


# ==================================================
# 5. Main Layout
# ==================================================

chat_col, insight_col = st.columns(
    [3, 2],
    gap="large",
)


# ==================================================
# 6. Chat Interface
# ==================================================

with chat_col:
    st.subheader("💬 Chatbot")

    chat_container = st.container(
        height=510,
        border=True,
    )

    with chat_container:
        if not st.session_state.messages:
            st.info(
                "Xin chào! Tôi là Git RAG Assistant. "
                "Hãy đặt câu hỏi về Git."
            )

            st.markdown(
                """
                **Ví dụ:**
                - Git fetch khác Git pull thế nào?
                - Làm sao hoàn tác commit nhưng giữ code?
                - Cách xử lý merge conflict?
                """
            )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                if message["role"] == "assistant":
                    sources = message.get(
                        "sources", []
                    )

                    if sources:
                        with st.expander(
                            "📚 Tài liệu được truy xuất"
                        ):
                            for source in sources:
                                st.markdown(
                                    f"- [{source['title']}]"
                                    f"({source['url']})"
                                )

    question = st.chat_input(
        "Nhập câu hỏi về Git..."
    )


# ==================================================
# 7. Process Question
# ==================================================

if question and question.strip():
    question = question.strip()

    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.spinner(
        "Đang tìm tài liệu và tạo câu trả lời..."
    ):
        try:
            result = ask_rag(
                question=question,
                top_k=top_k,
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
                "sources": result["sources"],
            })

            st.session_state.latest_retrieval = (
                result["retrieved_chunks"]
            )

        except Exception:
            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "⚠️ Không thể xử lý câu hỏi. "
                    "Vui lòng kiểm tra kết nối, "
                    "API quota và terminal."
                ),
                "sources": [],
            })

            st.session_state.latest_retrieval = []

            # Avoid exposing API keys or request
            # details in the user interface.
            # Use terminal traceback while developing.
            import traceback
            traceback.print_exc()

    st.rerun()


# ==================================================
# 8. Retrieval Insights
# ==================================================

with insight_col:
    st.subheader("🔎 Retrieval Insights")

    st.caption(
        "Các đoạn văn bản ChromaDB truy xuất "
        "cho câu hỏi gần nhất."
    )

    chunks = st.session_state.latest_retrieval

    if not chunks:
        st.info(
            "Chưa có dữ liệu retrieval. "
            "Hãy đặt một câu hỏi để bắt đầu."
        )

    else:
        st.success(
            f"Retrieved {len(chunks)} chunks"
        )

        for index, chunk in enumerate(
            chunks, start=1
        ):
            distance = chunk["distance"]

            with st.expander(
                f"Top {index} — "
                f"{chunk['title']}",
                expanded=(index == 1),
            ):
                st.metric(
                    "Cosine Distance",
                    f"{distance:.4f}",
                )

                st.caption(
                    "Khoảng cách cosine càng nhỏ "
                    "thường biểu thị độ tương đồng "
                    "vector càng cao."
                )

                st.markdown("**Source:**")
                st.markdown(
                    f"[Open Git Documentation]"
                    f"({chunk['source']})"
                )

                st.markdown("**Retrieved Context:**")

                st.code(
                    chunk["content"],
                    language="markdown",
                )


# ==================================================
# 9. Footer
# ==================================================

st.divider()

st.caption(
    "Powered by Streamlit, ChromaDB, "
    "Sentence Transformers and Gemini API. "
    "Nội dung AI cần được kiểm chứng trước "
    "khi thực thi lệnh Git có rủi ro."
)