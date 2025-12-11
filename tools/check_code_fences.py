# tools/check_code_fences.py
import sys
from pathlib import Path
import re

root = Path("docs/modules")
if not root.exists():
    print("docs/modules not found")
    sys.exit(1)

fence_re = re.compile(r'^```[ \t]*([^\n`]*)\s*$', re.MULTILINE)
for md in sorted(root.rglob("*.md")):
    text = md.read_text(encoding="utf-8")
    matches = list(fence_re.finditer(text))
    if not matches:
        continue
    print(f"\n--- {md} : {len(matches)} fence(s) found ---")
    for i,m in enumerate(matches, start=1):
        info = m.group(1).strip()
        # find the code block body start index and a preview line
        start_pos = m.end()
        # find closing fence
        close = text.find("\n```", start_pos)
        preview = ""
        if close != -1:
            body = text[start_pos:close].lstrip("\n")
            preview = body.splitlines()[0] if body.splitlines() else ""
        else:
            preview = "<no closing fence found>"
        print(f"  [{i}] info='{info or '<none>'}' preview='{preview[:90]}'")