# tools/fix_mdx.py
import sys
from pathlib import Path
import re
from datetime import datetime

def fix_file(p: Path):
    text = p.read_text(encoding="utf-8")

    changed = False

    # 1) Comment top-level import/export lines
    new_text = re.sub(r'(?m)^\s*(import\s.+|export\s.+)\s*$',
                      r'<!-- SANITIZED: \1 -->', text)
    if new_text != text:
        changed = True
        text = new_text

    # 2) Escape "<" followed by a digit (e.g. "<2" => "&lt;2")
    new_text = re.sub(r'<(?=\d)', '&lt;', text)
    if new_text != text:
        changed = True
        text = new_text

    # 3) Escape raw <script or <iframe (case-insensitive)
    new_text = re.sub(r'(?i)<(?=\s*script\b)', '&lt;', text)
    new_text = re.sub(r'(?i)<(?=\s*iframe\b)', '&lt;', new_text)
    if new_text != text:
        changed = True
        text = new_text

    # 4) Replace any stray unescaped JSX-like "<Component-2" that starts with non-letter
    # (best-effort): turn "<2" already handled; also ensure tags starting with digit are escaped
    new_text = re.sub(r'<(?=[^A-Za-z/$`{])', '&lt;', text)
    if new_text != text:
        changed = True
        text = new_text

    # 5) Ensure fenced code blocks are closed: if odd number of ``` then append closing fence
    fence_count = len(re.findall(r'(?m)^```', text))
    if fence_count % 2 == 1:
        changed = True
        text = text + "\n\n```\n"

    # 6) Backup and write
    if changed:
        backup = p.with_suffix(p.suffix + f".bak.{datetime.now().strftime('%Y%m%d%H%M%S')}")
        p.rename(backup)
        p.write_text(text, encoding="utf-8")
        print(f"[FIXED] {p}  (backup -> {backup.name})")
    else:
        print(f"[SKIP] No changes for {p}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/fix_mdx.py path/to/file.md  OR  path/to/dir")
        sys.exit(1)

    target = Path(sys.argv[1])
    if target.is_file():
        fix_file(target)
    elif target.is_dir():
        for p in sorted(target.rglob("*.md")):
            fix_file(p)
    else:
        print("Path not found:", target)
        sys.exit(2)

if __name__ == "__main__":
    main()