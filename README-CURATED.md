# Git RAG — Curated Knowledge Base (15 Markdown files)

## Setup
1. Copy the `data/curated` directory into your project directory `D:\Workspace\project\git-rag-assistant\data\curated`.
2. Replace your existing `src/document_loader.py` with the packaged version (make a backup if edited).
3. Copy `scripts/reindex_curated.py` into `scripts/`.
4. Keep the existing `src/chunking.py`, `src/embeddings.py`, `src/vector_store.py`, `.env`, and `data/raw` unchanged.
5. In an activated `.venv`, run `python scripts/reindex_curated.py`.
6. Then run `python scripts/test_retrieval.py`.

**Important:** the reindex script **deletes only** the existing Chroma collection `git_documentation` before rebuilding it. This removes the 271 earlier chunks from that collection, not your original Markdown or AsciiDoc files. An incomplete indexing failure should be retried by running the same script after resolving the problem.

## Technical notes
- Notes are authored Vietnamese summaries. They are *not* verbatim copies of Git documentation.
- Each Markdown file includes an official Source URL and an extra references section.
- Command examples may depend on Git version, repository state and workflow.
- The existing splitter counts **characters**, not tokens; retrieval needs validation with Vietnamese questions.
- Run a `git status`/`git log` inspection before destructive Git actions.
