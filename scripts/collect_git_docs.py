
from pathlib import Path
from datetime import datetime, timezone
import json
import re
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

COMMANDS = [
    "git-init",
    "git-clone",
    "git-add",
    "git-commit",
    "git-status",
    "git-branch",
    "git-switch",
    "git-merge",
    "git-fetch",
    "git-pull",
    "git-reset",
    "git-revert",
]

GITHUB_RAW = (
    "https://raw.githubusercontent.com/git/git/"
    "master/Documentation"
)

OFFICIAL_DOCS = "https://git-scm.com/docs"


def download_document(command):
    url = f"{GITHUB_RAW}/{command}.adoc"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    content = response.text

    if len(content.strip()) < 300:
        raise ValueError("Document is unexpectedly short")

    return url, content


def normalize_document(content):
    """
    Lightweight AsciiDoc to Markdown normalization.
    This is not a complete AsciiDoc converter.
    """
    lines = content.splitlines()
    result = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Convert common AsciiDoc headings.
        if i + 1 < len(lines):
            underline = lines[i + 1].strip()
            title = line.strip()

            if title and len(underline) >= 3:
                if re.fullmatch(r"=+", underline):
                    result.append(f"# {title}")
                    i += 2
                    continue

                if re.fullmatch(r"-+", underline):
                    result.append(f"## {title}")
                    i += 2
                    continue

                if re.fullmatch(r"~+", underline):
                    result.append(f"### {title}")
                    i += 2
                    continue

        # Omit unresolved AsciiDoc includes.
        if line.strip().startswith("include::"):
            i += 1
            continue

        # Omit standalone AsciiDoc block directives.
        if line.strip() in ("[synopsis]", "[verse]"):
            i += 1
            continue

        # Convert references to other Git commands.
        line = re.sub(
            r"linkgit:([a-zA-Z0-9-]+)\[\d+\]",
            r"`\1`",
            line,
        )

        result.append(line)
        i += 1

    text = "\n".join(result)

    # Avoid excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def main():
    results = []

    print("===== GIT DOCUMENT COLLECTION =====")

    for command in COMMANDS:
        print(f"\n[DOWNLOAD] {command}")

        try:
            source_url, content = download_document(
                command
            )

            # Save original AsciiDoc.
            raw_path = RAW_DIR / f"{command}.adoc"
            raw_path.write_text(
                content,
                encoding="utf-8",
            )

            normalized = normalize_document(content)

            reference_url = (
                f"{OFFICIAL_DOCS}/{command}"
            )

            collected_at = datetime.now(
                timezone.utc
            ).isoformat()

            # Markdown metadata header.
            header = (
                f"# {command}\n\n"
                f"Source: {reference_url}\n\n"
                f"Original: {source_url}\n\n"
                "---\n\n"
            )

            output_path = (
                PROCESSED_DIR / f"{command}.md"
            )

            output_path.write_text(
                header + normalized,
                encoding="utf-8",
            )

            results.append({
                "command": command,
                "source": reference_url,
                "original": source_url,
                "collected_at": collected_at,
                "file": output_path.name,
                "characters": len(normalized),
                "status": "success",
            })

            print(
                f"[OK] {output_path.name} "
                f"({len(normalized)} characters)"
            )

        except Exception as error:
            results.append({
                "command": command,
                "status": "failed",
                "error": str(error),
            })

            print(f"[ERROR] {command}: {error}")

    manifest_path = (
        PROCESSED_DIR / "manifest.json"
    )

    manifest_path.write_text(
        json.dumps(
            results,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    success_count = sum(
        item["status"] == "success"
        for item in results
    )

    print("\n===== SUMMARY =====")
    print(f"Total: {len(COMMANDS)}")
    print(f"Success: {success_count}")
    print(f"Failed: {len(COMMANDS) - success_count}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
