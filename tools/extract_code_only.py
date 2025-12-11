#!/usr/bin/env python3
import re
from pathlib import Path


CODE_BLOCK_RE = re.compile(
    r"```([\w+-]*)\s*\n(.*?)\n```",
    re.DOTALL
)


def extract_code_sections(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")

    sections = CODE_BLOCK_RE.findall(text)
    if not sections:
        return (
            "---\n"
            "title: Uploaded Document\n"
            "sidebar_label: Document\n"
            "---\n\n"
            "_No code found in this upload._"
        )

    out = [
        "---\n"
        "title: Code Extracted\n"
        "sidebar_label: Code\n"
        "---\n"
        "# Extracted Code\n"
    ]

    for idx, (lang, code) in enumerate(sections, start=1):
        lang = lang or "text"
        out.append(f"```{lang} title=\"Code Block {idx}\"\n{code.strip()}\n```")

    return "\n\n".join(out) + "\n"