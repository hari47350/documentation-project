---
id: week1
title: Week 01 — TeamA
sidebar_label: Week 01
---

```text
# Week 5 - SmartIDH3: MongoDB Schema Hardening, Migrations, Backups & Benchmarking

## Overview
This document contains a comprehensive record of Week 5 work for SmartIDH3 project...

## Environment & Prerequisites
Python 3.10+, MongoDB, pymongo, venv

Setup:
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pymongo

## Project Files (DO NOT RENAME)
storage/mongo_client.py
storage/migrations/v2_harden_parsed_segments.py
scripts/backup_mongosh.ps1
tests/stress_test_parsed_segments.py
tests/stress_benchmark.py
tests/benchmark_queries.py
tests/benchmark_post_migration.py
tests/full_workflow.py
storage/mongo_schema.md

## storage/mongo_client.py
from pymongo import MongoClient
from datetime import datetime, timezone
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

def get_db():
    return client["mydb"]

db = get_db()
db.raw_documents.create_index([("tenant_id", 1), ("status", 1), ("uploaded_at", -1)])
...

## Migration Script
from storage.mongo_client import get_db
def apply_hardened_indexes():
    db = get_db()
    db.parsed_segments.create_index([("tenant_id", 1), ("doc_id", 1), ("page_number", 1)])
...

## Backup Script (PowerShell)
$mongoUri = "mongodb://localhost:27017/mydb"
$mongoDumpPath = "C:\mongodbtools\bin\mongodump.exe"
...

## Stress Test Script
from storage.mongo_client import get_db
db = get_db()
...

## Benchmark Query Script
import time
from storage.mongo_client import get_db
...

## Troubleshooting & Fixes
- Convert ObjectId to string
- Fix mongodump path
...

## Benchmark Results
Avg: 85 - 140ms

## Steps to Run
1) Activate venv
2) Run migration
3) Run stress test
4) Run benchmark scripts
5) Run backup script

## Next Steps
- Measure P95 & P99
- Automated backups
- Bulk inserts
- CI benchmarking

Generated for SmartIDH3 — Week 5
```

## Snippet test

```python title="demo_snippet.py"
def hello():
    print("Hello from snippet!")