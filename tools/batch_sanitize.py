#!/usr/bin/env python3
# tools/batch_sanitize.py
from pathlib import Path
import subprocess
import sys

TOOLS = Path(__file__).resolve().parent
DOCS = Path.cwd() / "docs"  # run from repo root

sanitizer = TOOLS / "sanitize_and_wrap.py"
if not sanitizer.exists():
    print("Sanitizer not found:", sanitizer)
    sys.exit(1)

md_files = list(DOCS.rglob("*.md"))
print("Found", len(md_files), "markdown files. Processing...")

for md in md_files:
    print("->", md)
    subprocess.run(["python", str(sanitizer), str(md), md.name])
    # #!/usr/bin/env python3
# """
# tools/batch_sanitize.py
# Run the sanitizer over all markdown files in docs/modules (or a single file).
# Usage:
#   python tools/batch_sanitize.py
#   python tools/batch_sanitize.py path/to/specific.md
# """
# import subprocess
# import sys
# from pathlib import Path

# ROOT = Path(__file__).resolve().parent.parent
# TOOLS = ROOT / "tools"
# DOCS_ROOT = ROOT / "docs" / "modules"
# SANITIZER = TOOLS / "sanitize_and_wrap.py"

# if not SANITIZER.exists():
#     print("sanitize_and_wrap.py not found in tools/. Place it there first.")
#     sys.exit(1)

# def run_on_file(md_path):
#     print("Sanitizing:", md_path)
#     try:
#         subprocess.run(
#             ["python", str(SANITIZER), str(md_path), md_path.name],
#             check=True,
#         )
#     except subprocess.CalledProcessError as e:
#         print("Sanitizer failed for", md_path, ":", e)

# if __name__ == "__main__":
#     if len(sys.argv) >= 2:
#         p = Path(sys.argv[1])
#         if p.exists():
#             run_on_file(p)
#         else:
#             print("File not found:", p)
#             sys.exit(2)
#     else:
#         # walk all md files under docs/modules
#         for md in DOCS_ROOT.rglob("*.md"):
#             run_on_file(md)
#         print("Done.")