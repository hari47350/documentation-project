# Project Docs — Setup & Run

## Prereqs
- Node.js >=18, npm
- Python 3.10+
- pip

## 1) Install Node deps (Docusaurus)
cd project-docs
npm install

## 2) Install Python deps (converters + upload service)
pip install fastapi uvicorn mammoth pdfminer.six

## 3) Start Docusaurus dev server
npm run start
# open http://localhost:3000

Docusaurus watches docs/ — when new MD appears in docs/uploads/ it will show in the sidebar.

## 4) Start upload service (new terminal)
cd project-docs
uvicorn upload_service.upload_api:app --host 0.0.0.0 --port 9000 --reload

## 5) Example upload (curl)
curl -X POST "http://localhost:9000/upload/" -F "week=week-06" -F "team=ingestion" -F "file=@/path/to/Week6.docx"

Response:
{"ok":true,"markdown":"week-06--ingestion--...--Week6.docx.md"}

The converted Markdown will be placed in `docs/uploads/`. Docusaurus dev server auto-refreshes the site.

## Notes
- On Windows, ensure `python` command points to desired interpreter.
- If conversion fails, check Python packages and console logs from upload_service.
## Example: Connecting to MongoDB

Below is an example snippet showing how to connect to MongoDB.

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]

print("Connected:", db.list_collection_names())
```python title="MongoDB Insert Example"
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]

db.users.insert_one({"name": "Hari", "role": "Admin"})
print("Inserted!")
