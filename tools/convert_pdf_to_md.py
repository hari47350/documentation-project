
# So Docusaurus renders it exactly like OpenAI’s snippet cards (with your existing CSS + Prism).

# ---

# ## ✅ 1. New `tools/convert_pdf_to_md.py`

# Create (or replace) this file:

# `tools/convert_pdf_to_md.py`

# ```python
# tools/convert_pdf_to_md.py
"""
Usage:
    python tools/convert_pdf_to_md.py input.pdf output.md

This script:
  - extracts text from a PDF using pdfminer.six
  - detects code-like blocks
  - wraps them in fenced code blocks:
        ```python title="file-stem"
        ...
        ```
"""

import sys
import re
from pathlib import Path
from pdfminer.high_level import extract_text


def detect_language(text: str) -> str:
    """Very simple language guesser for snippet fencing."""
    t = text.lower()
    if "import " in t or "def " in t or "print(" in t or "from " in t:
        return "python"
    if "console.log" in t or "function(" in t or "=> {" in t:
        return "javascript"
    if "public class" in t or "static void main" in t:
        return "java"
    if "select " in t and " from " in t:
        return "sql"
    return "text"


def is_code_line(line: str) -> bool:
    """Heuristic: decide if a single line looks like code."""
    stripped = line.rstrip("\n")
    if not stripped:
        return False

    # 1) indented lines usually indicate code
    if stripped.startswith(("    ", "\t")):
        return True

    # 2) Starts with typical keywords
    if re.match(
        r'^\s*(import |from .* import |def |class |if |for |while |try:|except|#include|public |private |var |let |const )',
        stripped,
    ):
        return True

    # 3) Contains braces or semicolons that look code-ish
    if any(ch in stripped for ch in ("{", "}", ";", "=>")):
        return True

    return False


def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/convert_pdf_to_md.py input.pdf output.md")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not in_path.exists():
        print("ERROR: Input PDF does not exist:", in_path)
        sys.exit(1)

    # 1) Extract raw text from PDF
    raw_text = extract_text(str(in_path))
    lines = raw_text.splitlines()

    md_chunks = []
    normal_buf = []
    code_buf = []
    in_code = False

    def flush_normal():
        nonlocal normal_buf
        if normal_buf:
            # Join adjacent lines into one paragraph
            para = " ".join(l.strip() for l in normal_buf if l.strip())
            if para:
                md_chunks.append(para)
            normal_buf = []

    def flush_code():
        nonlocal code_buf
        if code_buf:
            code_text = "\n".join(code_buf)
            lang = detect_language(code_text)
            block = f"```{lang} title=\"{in_path.stem}\"\n{code_text}\n```"
            md_chunks.append(block)
            code_buf = []

    # 2) Walk through all lines, grouping normal text vs code
    for line in lines:
        if is_code_line(line):
            if not in_code:
                flush_normal()
                in_code = True
            code_buf.append(line.rstrip())
        else:
            if in_code:
                flush_code()
                in_code = False
            normal_buf.append(line)

    # flush whatever is left
    if in_code:
        flush_code()
    else:
        flush_normal()

    md = "\n\n".join(chunk for chunk in md_chunks if chunk.strip())

    # 3) Escape things that break MDX (like <script>, <iframe>, <2, etc.)
    md = re.sub(r'(?i)<(?=\s*script)', '&lt;', md)
    md = re.sub(r'(?i)<(?=\s*iframe)', '&lt;', md)
    md = re.sub(r'<(?=\d)', '&lt;', md)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print("Converted PDF →", out_path)


if __name__ == "__main__":
    main()
