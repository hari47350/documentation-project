#!/usr/bin/env python3
"""
tools/auto_snippet.py

Usage:
  # process a single file
  python tools/auto_snippet.py docs/modules/module1/teamA/week1.md

  # or process a whole tree
  python tools/auto_snippet.py docs/modules

What it does:

- Reads .md files.
- Skips YAML front-matter at the top (between --- lines).
- DOES NOT touch existing ``` fenced code blocks.
- Detects "naked" code lines (like `from x import y`, `python -m ...`, etc.)
  that are NOT already inside ``` and groups them into code fences.

- Wraps them as:

    ```python
    ...
    ```

- Very conservative heuristics: only groups lines that strongly look like code.
"""

import sys
from pathlib import Path
from typing import List, Tuple

CODE_LANG_DEFAULT = "python"   # fallback for code-ish blocks
ROOT = Path.cwd().resolve()    # ✅ use current working directory as root


def is_frontmatter_line(line: str) -> bool:
    return line.strip() == "---"


def detect_language(block_lines: List[str]) -> str:
    """
    Very small heuristic: guess language from contents.
    """
    joined = "\n".join(l.strip() for l in block_lines)

    # powershell
    if joined.startswith("$") or "Write-Host" in joined or "Get-ChildItem" in joined:
        return "powershell"
    # bash / shell
    if joined.startswith("#!") or joined.startswith("sudo ") or "python -m " in joined:
        return "bash"
    # javascript
    if "const " in joined or ("import " in joined and " from " in joined and ";" in joined):
        return "javascript"
    # text-only lists
    if all(l.strip().startswith("- ") for l in block_lines):
        return "text"
    # default
    return CODE_LANG_DEFAULT


def looks_like_code_line(line: str) -> bool:
    """
    Heuristic: decide if a single line "smells like" code.
    """
    s = line.rstrip("\n")
    if not s.strip():
        return False

    stripped = s.lstrip()

    # Already a markdown heading or list or quote → not code
    if stripped.startswith(("#", "-", "*", ">")):
        return False

    # common code-ish indicators
    code_keywords = (
        "from ",
        "import ",
        "def ",
        "class ",
        "for ",
        "while ",
        "if ",
        "try:",
        "except ",
        "@pytest.",
        "@dataclass",
    )
    if any(stripped.startswith(k) for k in code_keywords):
        return True

    # Lines ending with : are often code
    if stripped.endswith(":"):
        return True

    # braces and equals + typical punctuation
    if any(sym in stripped for sym in (" = ", " =\"", ":{", "};", ");", "{", "}")):
        return True

    # looks like a function call
    if "(" in stripped and ")" in stripped and not stripped.startswith("http"):
        return True

    # looks like command line
    if stripped.startswith("python ") or stripped.startswith("pytest ") or stripped.startswith("uvicorn "):
        return True

    # simple assignment style "X = Y"
    if "=" in stripped and not stripped.lower().startswith("id ="):
        return True

    return False


def group_code_blocks(lines: List[str]) -> List[str]:
    """
    Walk through lines (after front-matter) and wrap sequences of 'code-like'
    lines into fenced code blocks.
    - Does not touch existing ``` fences.
    """
    out: List[str] = []
    inside_fence = False
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # Respect existing fences: copy as-is
        if line.strip().startswith("```"):
            out.append(line)
            # toggle fence state
            inside_fence = not inside_fence
            i += 1
            continue

        if inside_fence:
            out.append(line)
            i += 1
            continue

        # We're not inside a fence: try to detect a run of code lines
        if looks_like_code_line(line):
            # collect contiguous code-ish lines, but stop if we hit a blank
            # or a markdown structure like heading/list.
            block: List[str] = [line.rstrip("\n")]
            j = i + 1
            while j < n:
                ln = lines[j]
                if not ln.strip():
                    break
                if ln.strip().startswith(("#", "```", ">")):
                    break
                if not looks_like_code_line(ln):
                    break
                block.append(ln.rstrip("\n"))
                j += 1

            # Only wrap if block has at least 2 lines, or the single
            # line is VERY code-like
            if len(block) >= 2 or looks_like_code_line(block[0]):
                lang = detect_language(block)
                out.append(f"```{lang}\n")
                for b in block:
                    out.append(b + "\n")
                out.append("```\n")
                i = j
                continue
            else:
                out.append(line)
                i += 1
                continue
        else:
            out.append(line)
            i += 1

    return out


def process_one(md_path: Path) -> Tuple[bool, str]:
    """
    Process a single .md file:
      - preserve YAML front-matter (top --- ... ---),
      - auto-wrap code-like line groups into fenced blocks in the body.
    Returns (changed, message).
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    if not lines:
        return False, "empty file"

    out: List[str] = []

    # 1) Handle front-matter, if any
    idx = 0
    n = len(lines)

    if idx < n and is_frontmatter_line(lines[idx]):
        out.append(lines[idx])
        idx += 1
        # copy until second ---
        while idx < n:
            out.append(lines[idx])
            if is_frontmatter_line(lines[idx]):
                idx += 1
                break
            idx += 1

    # now process remainder (body)
    body_lines = lines[idx:]
    new_body = group_code_blocks(body_lines)
    out.extend(new_body)

    new_text = "".join(out)
    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        return True, "updated"
    return False, "no change"


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/auto_snippet.py <file-or-directory>")
        sys.exit(2)

    target = Path(sys.argv[1])
    if not target.exists():
        print("Path not found:", target)
        sys.exit(3)

    if target.is_file() and target.suffix.lower() == ".md":
        files = [target.resolve()]
    else:
        files = [p.resolve() for p in target.rglob("*.md")]

    changed_count = 0
    for p in sorted(files):
        # show path relative to project root
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            rel = p
        changed, msg = process_one(p)
        print(f"[{msg}] {rel}")
        if changed:
            changed_count += 1

    print(f"\nDone. Files changed: {changed_count}")


if __name__ == "__main__":
    main()