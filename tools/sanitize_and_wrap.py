#!/usr/bin/env python3
"""
tools/sanitize_and_wrap.py

GOAL:
- Make converted Markdown safe for Docusaurus MDX
- Make code blocks show as nice "snippets" (with title) using Prism + your CSS
- Avoid MDX JSX / ESM parse errors from:
    * raw `import` / `export` lines OUTSIDE code fences
    * text like `<2025-01-01>` or `<2>` which MDX thinks is JSX/HTML

USAGE (single file):
    python tools/sanitize_and_wrap.py path/to/file.md "label for snippet titles"

USAGE (whole folder tree):
    python tools/sanitize_and_wrap.py docs/modules

In upload_service/upload_api.py you already call:
    run_sanitizer(out_md, f"{team_slug} {week_id}")
so every upload is sanitized automatically.
"""

import sys
from pathlib import Path
import re
from typing import Tuple


# --------------------------------------------------------
# 1) Add title="..." to fenced code blocks
# --------------------------------------------------------

def add_title_to_fence(info_str: str, title: str, snippet_index: int) -> str:
    """
    Given an info string (like 'python' or 'python linenos="1"'),
    return an updated info string that includes title="...".
    If title already present, return info_str unchanged.
    """
    if "title=" in info_str:
        return info_str  # already has a title

    safe_title = title.replace('"', '\\"')
    full_title = f"{safe_title} (snippet {snippet_index})"
    info_str = info_str.strip()

    if info_str == "":
        return f'title="{full_title}"'
    else:
        return f'{info_str} title="{full_title}"'


def inject_titles_into_fences(md_text: str, original_label: str) -> Tuple[str, int]:
    """
    Search md_text for fenced code blocks and add title attributes where missing.
    Returns new_text, count_of_modified_fences.
    We only touch the opening ``` line; contents remain unchanged.
    """
    pattern = re.compile(
        r'(^```[ \t]*([^\n`]*)\n)(.*?)(\n```)',
        re.MULTILINE | re.DOTALL,
    )

    snippet_count = 0
    modified = 0

    def repl(match):
        nonlocal snippet_count, modified
        opening_line = match.group(1)
        info = match.group(2)
        code_body = match.group(3)
        closing = match.group(4)

        snippet_count += 1
        if "title=" in info:
            return match.group(0)

        new_info = add_title_to_fence(info, original_label, snippet_count)
        new_opening = "```" + ((" " + new_info) if new_info else "") + "\n"
        modified += 1
        return new_opening + code_body + closing

    new_text = pattern.sub(repl, md_text)
    return new_text, modified


# --------------------------------------------------------
# 2) MDX safety pass (OUTSIDE code fences)
# --------------------------------------------------------

def sanitize_body_for_mdx(md_text: str) -> str:
    """
    Line-based pass:
    - Track fenced code blocks with ``` lines.
    - INSIDE fences: keep everything 100% as-is (code must not be touched).
    - OUTSIDE fences:
        * indent lines starting with 'import ' or 'export ' so MDX
          sees them as code, not real ESM.
        * escape ALL `<` and `>` (except ones already &lt; / &gt;)
          so MDX doesn't treat them as JSX/HTML.
    """
    lines = md_text.splitlines()
    out_lines = []
    in_fence = False

    fence_re = re.compile(r'^```')
    import_re = re.compile(r'^(import|export)\b')
    lt_re = re.compile(r'(?<!&lt;)<')
    gt_re = re.compile(r'(?<!&gt;)>')

    for line in lines:
        stripped = line.lstrip()

        # Toggle fence mode
        if fence_re.match(stripped):
            in_fence = not in_fence
            out_lines.append(line)
            continue

        if in_fence:
            # Never touch code
            out_lines.append(line)
            continue

        # ---------- OUTSIDE fences only ----------

        # 1) ESM: indent import/export to make them code, not MDX ESM
        if import_re.match(stripped):
            new_line = "    " + stripped
        else:
            new_line = line

        # 2) Escape all < and > so MDX doesn't think they are JSX/HTML tags
        new_line = lt_re.sub('&lt;', new_line)
        new_line = gt_re.sub('&gt;', new_line)

        out_lines.append(new_line)

    return "\n".join(out_lines)


# --------------------------------------------------------
# 3) Front-matter handling
# --------------------------------------------------------

def split_front_matter(text: str) -> Tuple[str, str]:
    """
    If text starts with:

        ---
        ...
        ---

    Return (front_matter_with_delimiters, body)
    Else: ("", text)
    """
    if not text.lstrip().startswith("---"):
        return "", text

    if not text.startswith("---"):
        # Some BOM or leading spaces: don't try to be clever
        return "", text

    parts = text.split("\n")
    if len(parts) < 3:
        return "", text

    end_index = None
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            end_index = i
            break

    if end_index is None:
        return "", text

    fm_lines = parts[: end_index + 1]
    body_lines = parts[end_index + 1 :]
    fm_text = "\n".join(fm_lines)
    body_text = "\n".join(body_lines)
    return fm_text, body_text


def sanitize_markdown_file(md_path: Path, label: str) -> int:
    """
    Sanitize a single .md file:
    - split front matter
    - MDX-sanitize body (imports, <2>, <2025-01-01>, etc.)
    - inject snippet titles into fenced code blocks
    - write back
    Returns: number of code fences where title was added.
    """
    original_text = md_path.read_text(encoding="utf-8")

    front_matter, body = split_front_matter(original_text)

    # Step 1: make body MDX-safe
    safe_body = sanitize_body_for_mdx(body)

    # Step 2: inject titles into fenced code blocks
    final_body, changed = inject_titles_into_fences(safe_body, label)

    new_text = (front_matter + "\n" + final_body) if front_matter else final_body

    md_path.write_text(new_text, encoding="utf-8")
    return changed


# --------------------------------------------------------
# 4) CLI entrypoint
# --------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  python tools/sanitize_and_wrap.py path/to/file.md \"label\"\n"
            "  python tools/sanitize_and_wrap.py path/to/dir"
        )
        sys.exit(2)

    target = Path(sys.argv[1])

    # Mode 1: directory (bulk)
    if target.is_dir():
        base = target
        total_changed = 0
        for p in base.rglob("*.md"):
            # Derive label from relative path
            try:
                rel = p.relative_to(base)
                label = str(rel).replace("\\", "/")
            except ValueError:
                label = p.name

            changed = sanitize_markdown_file(p, label)
            if changed > 0:
                print(f"[OK] {p} -> {changed} fences updated")
                total_changed += changed
            else:
                print(f"[SKIP] {p} (no fences or already titled)")
        print("Done. Total fences modified:", total_changed)
        return