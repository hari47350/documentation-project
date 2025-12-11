# tools/sanitize_and_wrap.py
"""
Sanitize a generated markdown file for Docusaurus/MDX and wrap code blocks
as fenced blocks with a title attribute so your OpenAI-style snippet CSS + Prism works.
Usage:
    python tools/sanitize_and_wrap.py <md_path> "<original_filename>"
Example:
    python tools/sanitize_and_wrap.py docs/modules/module1/teamA/week1.md "Week5_Full_Documentation_SmartIDH3.docx"
"""
import sys
from pathlib import Path
import re

def detect_language_snippet(code_snippet: str) -> str:
    """Very small heuristic to choose a language for Prism.
    Returns a prism-language string or '' if unknown.
    """
    s = code_snippet.strip().lower()
    # python
    if re.search(r'^\s*(def |import |from |class |print\(|async |await )', s, re.M):
        return "python"
    if re.search(r'^\s*(#include |int main\(|std::|cout<<)', s, re.M):
        return "cpp"
    if re.search(r'^\s*(public |private |class |System\.out|package )', s, re.M):
        return "java"
    if re.search(r'^\s*(function |const |let |var |=>|console\.log\()', s, re.M):
        return "javascript"
    if re.search(r'^\s*<\?xml|<html|<!doctype html|<div', s, re.M):
        return "html"
    if re.search(r'^\s*{[\s\S]*:\s', s):  # naive JSON object
        return "json"
    if re.search(r'^\s*db\.|find\(|aggregate\(|\$match', s):
        return "mongodb"
    if re.search(r'^\s*SELECT\s', s, re.I):
        return "sql"
    return ""

def add_title_to_fence(fence_open: str, title: str) -> str:
    """Given opening fence like ``` or ```python, return with title attribute."""
    # Normalize fence
    m = re.match(r'^```([\w+-]*)', fence_open)
    lang = m.group(1) if m else ""
    lang_part = lang if lang else ""
    if lang_part:
        return f"```{lang_part} title=\"{title}\""
    else:
        return f"``` title=\"{title}\""

def sanitize_text(text: str) -> str:
    # 1) comment top-level import/export lines (JS/TS) to avoid MDX ESM
    text = re.sub(r'(?m)^\s*(import\s.*|export\s.*)$', r'<!-- SANITIZED: \1 -->', text)

    # 2) escape "<" followed by digit (e.g. "<2") that MDX may parse as JSX
    text = re.sub(r'<(?=\d)', '&lt;', text)

    # 3) escape script/iframe open tags so they don't become HTML elements
    text = re.sub(r'(?i)<\s*script', '&lt;script', text)
    text = re.sub(r'(?i)<\s*/\s*script', '&lt;/script', text)
    text = re.sub(r'(?i)<\s*iframe', '&lt;iframe', text)
    text = re.sub(r'(?i)<\s*/\s*iframe', '&lt;/iframe', text)

    # 4) replace stray raw backticks inside code blocks if necessary handled later
    return text

def wrap_code_blocks(md_path: Path, original_filename: str):
    text = md_path.read_text(encoding='utf-8')

    # sanitize first
    text = sanitize_text(text)

    # Normalize windows CRLF -> LF for stable regex
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # We will support both converted code forms:
    # - triple backtick blocks (``` ... ```)
    # - indented code blocks (4-space) - convert them to fenced
    # - <pre>...</pre> from html-conversion (rare because mammoth->md tries to avoid, but just in case)
    # Strategy:
    # 1) convert <pre>...</pre> to fenced
    # 2) convert indented blocks to fenced
    # 3) ensure all fenced blocks have title attribute (use original_filename)
    # 4) possibly add a language detection for empty fences

    # 1) <pre>...</pre> -> fenced (preserve content)
    def _pre_repl(m):
        inner = m.group(1)
        # trim trailing/leading newline
        inner_clean = inner.strip('\n')
        lang = detect_language_snippet(inner_clean)
        lang_attr = lang if lang else ""
        title = Path(original_filename).name
        if lang_attr:
            return f"\n```{lang_attr} title=\"{title}\"\n{inner_clean}\n```\n"
        else:
            return f"\n``` title=\"{title}\"\n{inner_clean}\n```\n"
    text = re.sub(r'<pre[^>]*>\s*<code[^>]*>([\s\S]*?)</code>\s*</pre>', _pre_repl, text, flags=re.I)
    text = re.sub(r'<pre[^>]*>([\s\S]*?)</pre>', _pre_repl, text, flags=re.I)

    # 2) Convert indented code blocks (lines that start with 4 spaces or a tab)
    lines = text.splitlines()
    out_lines = []
    in_block = False
    block_buf = []
    for line in lines:
        if re.match(r'^( {4}|\t)', line):
            block_buf.append(re.sub(r'^( {4}|\t)', '', line))
            in_block = True
            continue
        else:
            if in_block:
                # flush buffer to fenced block
                code_text = '\n'.join(block_buf).rstrip('\n')
                lang = detect_language_snippet(code_text)
                title = Path(original_filename).name
                if lang:
                    out_lines.append(f"```{lang} title=\"{title}\"")
                else:
                    out_lines.append(f"``` title=\"{title}\"")
                out_lines.append(code_text)
                out_lines.append("```")
                block_buf = []
                in_block = False
            out_lines.append(line)
    if in_block and block_buf:
        code_text = '\n'.join(block_buf).rstrip('\n')
        lang = detect_language_snippet(code_text)
        title = Path(original_filename).name
        if lang:
            out_lines.append(f"```{lang} title=\"{title}\"")
        else:
            out_lines.append(f"``` title=\"{title}\"")
        out_lines.append(code_text)
        out_lines.append("```")

    text = '\n'.join(out_lines)

    # 3) Ensure all fenced blocks have a title attribute and language hint if missing
    # Find opening fences like ``` or ```python or ``` python
    def fence_repl(m):
        fence = m.group(0)  # e.g. ``` or ```python
        code_preview = m.group(1)[:200] if m.group(1) else ""
        # detect language already in fence
        mlang = re.match(r'^```([\w+-]+)?', fence)
        lang = mlang.group(1) if mlang and mlang.group(1) else ""
        title = Path(original_filename).name
        if lang:
            return f"```{lang} title=\"{title}\""
        else:
            # try to detect language from code_preview (best-effort)
            guessed = detect_language_snippet(code_preview)
            if guessed:
                return f"```{guessed} title=\"{title}\""
            else:
                return f"``` title=\"{title}\""

    # This is a bit tricky — to see code after fence we use regex with DOTALL capturing of (.*?) until next ```
    # We'll rewrite all fences by scanning sequentially to avoid wrong multi-line matches.
    parts = []
    idx = 0
    pattern = re.compile(r'```([\w+-]*)(?:\s*title=".*?")?\n', re.MULTILINE)
    for m in pattern.finditer(text):
        start = m.start()
        # append text before fence
        parts.append(text[idx:start])
        # find the closing fence after this match
        open_lang = m.group(1)
        fence_open_end = m.end()
        # find next closing ```
        close_idx = text.find('\n```', fence_open_end)
        if close_idx == -1:
            # fallback: no closing fence, keep the rest as-is and break
            rest = text[start:]
            parts.append(rest)
            idx = len(text)
            break
        # capture code inside
        code_inside = text[fence_open_end:close_idx]
        # build new fence header
        title = Path(original_filename).name
        if open_lang:
            new_header = f"```{open_lang} title=\"{title}\"\n"
        else:
            guessed = detect_language_snippet(code_inside)
            if guessed:
                new_header = f"```{guessed} title=\"{title}\"\n"
            else:
                new_header = f"``` title=\"{title}\"\n"
        parts.append(new_header)
        parts.append(code_inside)
        parts.append("\n```")
        idx = close_idx + 4  # skip past closing fence (```)
    if idx < len(text):
        parts.append(text[idx:])
    new_text = ''.join(parts)

    # final sanitize again
    new_text = sanitize_text(new_text)

    md_path.write_text(new_text, encoding='utf-8')
    print("Sanitized & wrapped:", md_path)

def main():
    if len(sys.argv) < 3:
        print("Usage: python tools/sanitize_and_wrap.py <md_path> <orig_filename>")
        sys.exit(2)
    md_path = Path(sys.argv[1])
    orig_name = sys.argv[2]
    if not md_path.exists():
        print("Error: md file not found:", md_path)
        sys.exit(1)
    wrap_code_blocks(md_path, orig_name)

if __name__ == "__main__":
    main()