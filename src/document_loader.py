from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data' / 'curated'


def load_documents():
    documents = []
    for path in sorted(DATA_DIR.glob('*.md')):
        content = path.read_text(encoding='utf-8').strip()
        if not content:
            continue
        match = re.search(r'^Source:\s*(https?://\S+)', content, re.MULTILINE)
        if not match:
            raise ValueError(f'Missing Source URL: {path.name}')
        first_line = content.splitlines()[0]
        title = first_line.removeprefix('#').strip()
        documents.append({
            'id': path.stem,
            'content': content,
            'source': match.group(1),
            'title': title,
        })
    return documents
