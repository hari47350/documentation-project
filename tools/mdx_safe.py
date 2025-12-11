#!/usr/bin/env python3
"""
tools/mdx_safe.py

Goal:
- Make any generated Markdown MDX-safe for Docusaurus.
- Avoid MDX/acorn errors from:
  * raw `import` / `export` / `from ... import ...` lines
  * `<2025>` / `<2` / random `<...>` being treated like JSX
  * weird lines causing "Unexpected character `2`" / `\` before name

How it works (high level):
1. Keeps YAML front matter (`--- ... ---`) untouched.
2. Walks the rest of the file line by line.
3. Detects "code-looking" lines (Python/JS/PowerShell/CLI) OUTSIDE fences and
   groups them into fenced code blocks:

      ```python title="storage/mongo_client.py"
      <code lines>
      ```

   Title is guessed from the nearest heading like
   "4. storage/mongo_client.py (DB connection & index ensures)".
4. For normal text lines (not in fences):
   - strips HTML-ish tags like <a id="...">, <p>, <div> etc.
   - fixes `<2` → `2`, `<Something` → `Something`
5. Ensures any accidental odd number of ``` fences is closed.

Usage:
  - One file:
      python tools/mdx_safe.py docs/modules/module1/teamA/week1.md
  - All docs under a directory:
      python tools/mdx_safe.py docs/modules
"""

import sys
import re
from pathlib import Path
from typing import List

# prefixes that mean "this is a runnable command"
CLI_PREFIXES = (
    "python ",
    "pip ",
    "npm ",
    "node ",
    "./",
    ".\\",
    "powershell ",
    "pwsh ",
    "mongodump",
    "mongo ",
    "set-executionpolicy",
)


def is_codey_line(line: str) -> bool:
    """
    Heuristic: decide if a line looks like *real* code or a runnable command.

    We only use this OUTSIDE existing ``` fences.
    """
    s = line.rstrip("\n")
    stripped = s.lstrip()

    # blank line by itself is not "code start"
    if not stripped:
        return False

    # ---- 0) Numeric "step" lists like `11. How to run:`  (NOT code) ----
    if re.match(r"\d+[\.)]\s", stripped):
        return False

    # ---- 1) Headings / bullet lists / quotes (NOT code) ----
    # treat headings that start with "##" as docs headings
    if stripped.startswith(("##", "-", "*", ">")):
        return False

    # NOTE: lines starting with single "#" we allow as code comments
    # so they can stay inside PowerShell / Python snippets.

    # ---- 2) runnable commands (YES code snippet) ----
    low = stripped.lower()
    if low.startswith(CLI_PREFIXES):
        return True

    # ---- 3) Explicit language keywords at the start ----
    if re.match(
        r"\s*(import|from|class|def|for|while|try|except|finally|with|switch|public|private|protected|using)\b",
        stripped,
    ):
        return True

    # ---- 4) Indented lines are often code (inside blocks) ----
    if line.startswith(("    ", "\t")):
        return True

    # ---- 5) Lines that look like assignments / function calls / dicts ----
    if any(tok in stripped for tok in (" = ", "==", "!=", "()", "[]", "{}", ".find(", ".insert_", ".update_", "return ", "await ")):
        return True

    # ---- 6) Lines ending with ":" used as control-flow ----
    if stripped.endswith(":") and any(
        kw in stripped for kw in ("for ", "if ", "while ", "try", "except", "case ")
    ):
        return True

    # OTHERWISE: treat as normal documentation text
    return False


def guess_title_from_heading(heading_text: str, fallback: str) -> str:
    """
    From a heading like:
      '4. storage/mongo_client.py (DB connection & index ensures)'
    try to return 'storage/mongo_client.py'.

    If no filename is present, return a cleaned heading or fallback.
    """
    text = heading_text.strip()

    # Try to find a filename with extension inside the heading
    m = re.search(r"([\w./-]+\.(py|js|ts|java|sh|ps1|md))", text)
    if m:
        return m.group(1)

    # Otherwise, use text before '(' if present
    main = text.split("(", 1)[0].strip()
    if main:
        return main

    return fallback


def transform_body_lines(lines: List[str], filename: str) -> List[str]:
    """
    Transform the body (after front matter) into MDX-safe markdown.

    - Keeps existing ``` or ~~~ fenced blocks intact.
    - Outside those, wraps codey runs into ``` blocks.
    - For normal text, strip HTML tags and fix `<2` style constructs.
    - Tracks nearest heading text to use as snippet title.
    """
    new_lines: List[str] = []

    in_fence = False
    snippet_counter = 0
    i = 0
    n = len(lines)

    base_title = filename.rsplit(".", 1)[0]
    current_title = base_title

    while i < n:
        line = lines[i]
        stripped = line.lstrip()

        # Detect entering/exiting explicit code fences
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            new_lines.append(line)
            i += 1
            continue

        # Inside fence: leave content untouched
        if in_fence:
            new_lines.append(line)
            i += 1
            continue

        # Track headings to guess better snippet titles
        heading_match = re.match(r"\s*#{1,6}\s+(.*)", line)
        if heading_match:
            heading_text = heading_match.group(1)
            current_title = guess_title_from_heading(heading_text, base_title)
            new_lines.append(line)
            i += 1
            continue

        # Outside fence: detect a run of code-looking lines
        if is_codey_line(line):
            snippet_counter += 1

            # Language guess (simple)
            low = stripped.lower()
            if low.startswith(("set-executionpolicy", "powershell", "pwsh", "$")):
                lang = "powershell"
            elif low.startswith(("npm ", "node ", "bash ", "./")):
                lang = "bash"
            elif any(tok in line for tok in ("def ", "import ", "from ")):
                lang = "python"
            else:
                lang = "text"

            title = current_title or base_title
            new_lines.append(f"```{lang} title=\"{title}\"")

            # consume consecutive codey lines + comments (# ...) + blank lines
            while i < n:
                cur = lines[i]
                cur_strip = cur.lstrip()
                if (
                    is_codey_line(cur)
                    or not cur_strip  # blank
                    or cur_strip.startswith("#")  # code comments
                ):
                    new_lines.append(cur)
                    i += 1
                else:
                    break

            new_lines.append("```")
            continue

        # ---- Normal text line ----
        safe = line

        # 1) Remove HTML-like tags: <a ...>, </a>, <p>, <div class="...">, etc.
        safe = re.sub(
            r"</?([A-Za-z][A-Za-z0-9:_-]*)(\s[^>]*)?>",
            "",
            safe,
        )

        # 2) Deal with `<2` or `<2025` → remove `<`, keep the number/word
        safe = re.sub(r"<(\d)", r"\1", safe)

        # 3) For `<Something` where it's not a real HTML tag, drop `<`
        safe = re.sub(r"<([A-Za-z])", r"\1", safe)

        new_lines.append(safe)
        i += 1

    # Safety: ensure fences are balanced
    fence_count = sum(
        1 for l in new_lines
        if l.lstrip().startswith("```") or l.lstrip().startswith("~~~")
    )
    if fence_count % 2 == 1:
        new_lines.append("```")

    return new_lines


def mdx_safe_file(path: Path) -> bool:
    """
    Make a single .md file MDX-safe.
    Returns True if file was changed.
    """
    original_lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    if not original_lines:
        return False

    new_lines: List[str] = []

    i = 0
    n = len(original_lines)

    # 1) Keep YAML front matter (`---` .. `---`) intact if present
    if original_lines[0].strip() == "---":
        new_lines.append(original_lines[0])
        i = 1
        while i < n:
            new_lines.append(original_lines[i])
            if original_lines[i].strip() == "---":
                i += 1
                break
            i += 1

    # 2) Transform the rest safely
    body = original_lines[i:]
    transformed_body = transform_body_lines(body, filename=path.name)
    new_lines.extend(transformed_body)

    new_text = "\n".join(new_lines)
    orig_text = "\n".join(original_lines)

    if new_text != orig_text:
        path.write_text(new_text, encoding="utf-8")
        print(f"[OK] MDX-safe rewrite: {path}")
        return True
    else:
        print(f"[SKIP] Already MDX-safe: {path}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/mdx_safe.py <file.md | directory>")
        sys.exit(2)

    target = Path(sys.argv[1])

    if target.is_file():
        if target.suffix.lower() != ".md":
            print("Not a .md file, skipping:", target)
            return
        mdx_safe_file(target)
        return

    if target.is_dir():
        changed = 0
        for p in target.rglob("*.md"):
            if mdx_safe_file(p):
                changed += 1
        print("Done. Total MD files changed:", changed)
        return

    print("Path not found:", target)
    sys.exit(3)


if __name__ == "__main__":
    main()