from pathlib import Path

p = Path("docs/modules/module1/teamA/week1.md")
text = p.read_text(encoding="utf-8")

count = text.count("```")
print("Backtick fences found:", count)

if count % 2 == 1:
    print("Odd number of fences -> appending closing ``` at end of file")
    text = text.rstrip() + "\n\n```\n"
    p.write_text(text, encoding="utf-8")
    print("Fixed.")
else:
    print("Fences already balanced, nothing to do.")