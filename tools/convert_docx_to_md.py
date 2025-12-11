#!/usr/bin/env python3
# tools/convert_docx_to_md.py
import sys
from pathlib import Path
import mammoth

# Usage:
# python tools/convert_docx_to_md.py input.docx output.md

if len(sys.argv) < 3:
    print("Usage: python tools/convert_docx_to_md.py in.docx out.md")
    sys.exit(2)

in_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])

if not in_path.exists():
    print("ERROR: input file not found:", in_path)
    sys.exit(3)

with in_path.open("rb") as f:
    # convert to markdown (mammoth supports markdown conversion)
    result = mammoth.convert_to_markdown(f)
    md = result.value

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(md, encoding="utf-8")
print("Converted", in_path, "->", out_path)
# # so MDX tries to parse your raw code as JavaScript expressions and explodes.

# # Let’s fix this **once** in the converter, so:

# # - every upload (DOCX or PDF)
# # - for every team / week / module

# # automatically becomes clean markdown with **OpenAI-style snippet cards**.

# # ---

# # ## STEP 1 – Replace your DOCX converter with a “snippet-aware” one

# # Create/replace the file:

# # > `tools/convert_docx_to_md.py`

# # with **this full code**:

# # ```python
# # tools/convert_docx_to_md.py
# """
# Usage:
#     python tools/convert_docx_to_md.py input.docx output.md

# Converts a DOCX to markdown AND:
#   - detects code-like lines
#   - groups them into fenced code blocks:
#         ```python title="file-stem"
#         ...
#         ```
#   - sanitizes things that break MDX (<script>, <iframe>, "<2", etc.)
# """

# import sys
# import re
# from pathlib import Path
# import mammoth


# def detect_language(text: str) -> str:
#     """Very simple language guesser for snippet fencing."""
#     t = text.lower()
#     if "import " in t or "def " in t or "print(" in t or "from " in t:
#         return "python"
#     if "console.log" in t or "function(" in t or "=> {" in t:
#         return "javascript"
#     if "public class" in t or "static void main" in t:
#         return "java"
#     if "select " in t and " from " in t:
#         return "sql"
#     if "curl " in t or t.strip().startswith(("GET ", "POST ", "PUT ", "DELETE ")):
#         return "bash"
#     return "text"


# def is_code_line(line: str) -> bool:
#     """Heuristic: decide if a single line looks like code."""
#     stripped = line.rstrip("\n")
#     if not stripped:
#         return False

#     # Indentation is a strong signal for code
#     if stripped.startswith(("    ", "\t")):
#         return True

#     # Typical keywords / patterns
#     if re.match(
#         r'^\s*(import |from .* import |def |class |if |for |while |try:|except|#include|public |private |var |let |const )',
#         stripped,
#     ):
#         return True

#     # Lines that look like shell commands (curl, npm, python, etc.)
#     if re.match(r'^\s*(curl |python |pip |npm |node |uvicorn )', stripped):
#         return True

#     # Contains braces / semicolons / => which often appear in code
#     if any(ch in stripped for ch in ("{", "}", ";", "=>")):
#         return True

#     return False


# def main():
#     if len(sys.argv) != 3:
#         print("Usage: python tools/convert_docx_to_md.py input.docx output.md")
#         sys.exit(1)

#     in_path = Path(sys.argv[1])
#     out_path = Path(sys.argv[2])

#     if not in_path.exists():
#         print("ERROR: input DOCX does not exist:", in_path)
#         sys.exit(1)

#     # 1) DOCX → raw markdown
#     with in_path.open("rb") as docx_file:
#         result = mammoth.convert_to_markdown(docx_file)
#         raw_md = result.value  # plain markdown text

#     lines = raw_md.splitlines()

#     md_chunks = []
#     normal_buf = []
#     code_buf = []
#     in_code = False

#     def flush_normal():
#         nonlocal normal_buf
#         if not normal_buf:
#             return
#         # keep headings as-is, but join plain paragraphs
#         paragraph = []
#         for l in normal_buf:
#             if l.lstrip().startswith("#"):
#                 if paragraph:
#                     md_chunks.append(" ".join(paragraph).strip())
#                     paragraph = []
#                 md_chunks.append(l)
#             else:
#                 paragraph.append(l.strip())
#         if paragraph:
#             md_chunks.append(" ".join(paragraph).strip())
#         normal_buf = []

#     def flush_code():
#         nonlocal code_buf
#         if not code_buf:
#             return
#         code_text = "\n".join(code_buf)
#         lang = detect_language(code_text)
#         block = f"```{lang} title=\"{in_path.stem}\"\n{code_text}\n```"
#         md_chunks.append(block)
#         code_buf = []

#     # 2) Walk lines and classify as normal vs code
#     for line in lines:
#         if is_code_line(line):
#             if not in_code:
#                 flush_normal()
#                 in_code = True
#             code_buf.append(line.rstrip())
#         else:
#             if in_code:
#                 flush_code()
#                 in_code = False
#             normal_buf.append(line)

#     # Flush leftovers
#     if in_code:
#         flush_code()
#     else:
#         flush_normal()

#     md = "\n\n".join(chunk for chunk in md_chunks if chunk.strip())

#     # 3) Sanitize things that MDX hates
#     #    - <script>, <iframe>, <2, etc.
#     md = re.sub(r'(?i)<(?=\s*script)', '&lt;', md)
#     md = re.sub(r'(?i)<(?=\s*iframe)', '&lt;', md)
#     md = re.sub(r'<(?=\d)', '&lt;', md)

#     out_path.parent.mkdir(parents=True, exist_ok=True)
#     out_path.write_text(md, encoding="utf-8")
#     print("Converted DOCX →", out_path)


# if __name__ == "__main__":
#     main()
