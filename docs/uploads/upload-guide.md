---
sidebar_label: Upload New Doc
---

# Upload Documentation

You can upload weekly docs using the form at `http://localhost:9000/form` or use curl.

Example:
```bash
curl -X POST "http://localhost:9000/upload/" \
  -F "month=month-01" \
  -F "team=ingestion" \
  -F "week=week-05" \
  -F "file=@C:\path\to\Week5.docx"
    