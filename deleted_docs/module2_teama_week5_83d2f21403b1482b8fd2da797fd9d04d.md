--- 
id: week5
title: Week 05 — Teama
sidebar_label: Week 05
---

# Week 5 \- SmartIDH3: MongoDB Schema Hardening, Migrations, Backups &amp; Benchmarking

## 1\. Overview

```python
This document contains a comprehensive record of Week 5 work for the SmartIDH3 project\. It covers schema hardening for the parsed\_segments collection, migrations, index tuning, TTLs, backup scripts, stress & benchmark tests, troubleshooting notes \(issues encountered and fixes\), and instructions to run every script with exact file names as present in the repository\.
```

## 2\. Environment &amp; Prerequisites

```python
Required software and environment:
```

```python
\- Python \(3\.10\+ recommended\)
```

```python
\- Virtual environment \(recommended \.venv\)
```

```python
\- MongoDB \(local or remote\) with access and appropriate user/URI
```

```python
\- MongoDB Database Tools \(mongodump\) for backups
```

```text title="week5.md snippet 1"
\- Python dependencies: pymongo
```

  
```python
Setup commands \(example\):
```

```python
python \-m venv \.venv  
```
\.venv\\Scripts\\Activate\.ps1  \# on Windows PowerShell  
pip install pymongo

## 3\. Project files \(exact names \- do not change\)

Below are the important files in the repository\. These names are used exactly in the code and scripts; do not rename them\.

\- storage/mongo\_client\.py

\- storage/migrations/v2\_harden\_parsed\_segments\.py

\- storage/create\_indexes\.py

\- scripts/backup\_mongosh\.ps1

\- tests/stress\_test\_parsed\_segments\.py

\- tests/stress\_benchmark\.py

\- tests/benchmark\_queries\.py

\- tests/benchmark\_post\_migration\.py

\- tests/full\_workflow\.py

\- storage/mongo\_schema\.md

## 4\. storage/mongo\_client\.py \(DB connection &amp; index ensures\)

```python
This file provides the MongoDB client and ensures initial indexes and helper get\_db\(\)\. Keep the file at storage/mongo\_client\.py and import it as 'from storage\.mongo\_client import get\_db'\.
```

```python
Example content \(already present in repo\):
```

```python
from pymongo import MongoClient  
from datetime import datetime, timezone   
```
```python title="week5.md snippet 2"
<!-- SANITIZED IMPORT/EXPORT: import os   -->
```
  
```python
MONGO\_URI = os\.getenv\("MONGO\_URI", "mongodb://localhost:27017/"\)  
client = MongoClient\(MONGO\_URI\)  
```
  
```python
def get\_db\(\):  
```
```text title="week5.md snippet 3"
    return client\["mydb"\]  
```
  
```python
db = get\_db\(\)  
```
  
```python
\# ensure indexes \(examples\)  
db\.raw\_documents\.create\_index\(\[\("tenant\_id", 1\), \("status", 1\), \("uploaded\_at", \-1\)\]\)  
db\.raw\_documents\.create\_index\("sha256", unique=True\)  
```
  
```python
db\.parsed\_segments\.create\_index\(\[\("tenant\_id", 1\), \("doc\_id", 1\), \("page\_number", 1\)\]\)  
db\.parsed\_segments\.create\_index\(\[\("text", "text"\)\]\)  
db\.parsed\_segments\.create\_index\("entities"\)  
db\.parsed\_segments\.create\_index\(\[\("created\_at", 1\)\], expireAfterSeconds=2592000\)  
```
  
```python
db\.extracted\_entities\.create\_index\(\[\("fields\.aadhaar\_number\.value", 1\)\]\)  
db\.extracted\_entities\.create\_index\(\[\("fields\.pan\_number\.value", 1\)\]\)  
db\.extracted\_entities\.create\_index\("document\_type"\)  
db\.extracted\_entities\.create\_index\("tenant\_id"\)  
```
  
```python
db\.users\.create\_index\(\[\("tenant\_id", 1\), \("email", 1\)\], unique=True\)  
```


## 5\. Migrations

```python
Migration scripts apply schema validators and hardened indexes\. The repository contains storage/migrations/v2\_harden\_parsed\_segments\.py\. Run migrations from project root using python \-m storage\.migrations\.v2\_harden\_parsed\_segments \(module syntax\)\.
```

```python
Example migration script \(v2\_harden\_parsed\_segments\.py\):
```

```python
from storage\.mongo\_client import get\_db  
```
  
```python
def apply\_hardened\_indexes\(\):  
    db = get\_db\(\)  
    print\("Applying hardened indexes on parsed\_segments\.\.\."\)  
    db\.parsed\_segments\.create\_index\(\[\("tenant\_id", 1\), \("doc\_id", 1\), \("page\_number", 1\)\], name="tenant\_id\_1\_doc\_id\_1"\)  
    db\.parsed\_segments\.create\_index\(\[\("text", "text"\)\], name="text\_text"\)  
    db\.parsed\_segments\.create\_index\(\[\("entities", 1\)\], name="entities\_1"\)  
    print\("All hardened indexes applied successfully\."\)  
```
  
```python
if \_\_name\_\_ == "\_\_main\_\_":  
    apply\_hardened\_indexes\(\)  
```


## 6\. Backups \(PowerShell\)

```python
Backup script used: scripts/backup\_mongosh\.ps1 \(file name preserved exactly\)\. This script runs mongodump and cleans old backups\.
```

```python
Important: $mongoDumpPath must point to the full path of mongodump\.exe \(including the executable\)\. Example path in your environment:
```

```powershell
$mongoDumpPath = 'C:\\Users\\admin\\Downloads\\mongodb\-database\-tools\-windows\-x86\_64\-100\.13\.0\\mongodb\-database\-tools\-windows\-x86\_64\-100\.13\.0\\bin\\mongodump\.exe'
```

```python
Full backup script \(keep file name scripts/backup\_mongosh\.ps1\):
```

  
```python
\# MongoDB Backup Script \(PowerShell\)  
$mongoUri = "mongodb://localhost:27017/mydb"  
$mongoDumpPath = 'C:\\Users\\admin\\Downloads\\mongodb\-database\-tools\-windows\-x86\_64\-100\.13\.0\\mongodb\-database\-tools\-windows\-x86\_64\-100\.13\.0\\bin\\mongodump\.exe'  
$backupRoot = "C:\\backups"  
$daysToKeep = 90  
```
  
```powershell
$timestamp = Get\-Date \-Format "yyyyMMdd\_HHmmss"  
$backupPath = Join\-Path $backupRoot "mongo\_$timestamp"  
```
New\-Item \-ItemType Directory \-Path $backupPath \-Force | Out\-Null  
  
```python
if \(Test\-Path $mongoDumpPath\) \{  
    & $mongoDumpPath \-\-uri="$mongoUri" \-\-out="$backupPath"  
```
```text title="week5.md snippet 4"
    Write\-Host "Backup completed successfully at: $backupPath"  
```
```python
\} else \{  
```
```text title="week5.md snippet 5"
    Write\-Host "ERROR: mongodump\.exe not found at $mongoDumpPath"  
    exit 1  
```
```python
\}  
```
  
\# Cleanup old backups  
```powershell
$cutoff = \(Get\-Date\)\.AddDays\(\-$daysToKeep\)  
Get\-ChildItem \-Path $backupRoot \-Directory | Where\-Object \{ $\_\.CreationTime \-lt $cutoff \} | ForEach\-Object \{  
```
```text title="week5.md snippet 6"
    Remove\-Item $\_\.FullName \-Recurse \-Force  
```
```python
\}  
```


```python
How to run manually in PowerShell \(example\):
```

Set\-ExecutionPolicy \-Scope Process \-ExecutionPolicy Bypass  
\.\\scripts\\backup\_mongosh\.ps1

```python
Task Scheduler configuration \(Action → Program/script: powershell\.exe, Add arguments: \-ExecutionPolicy Bypass \-File "C:\\Users\\admin\\smartidh3\\scripts\\backup\_mongosh\.ps1", Start in: C:\\Users\\admin\\smartidh3\\scripts\)
```

## 7\. Tests &amp; Benchmarking scripts \(exact file names\)

```python
The tests folder contains the following scripts\. Use module execution from project root \(python \-m tests\.&lt;script>\)\.
```

### 7\.1 tests/stress\_test\_parsed\_segments\.py

```text title="week5.md snippet 7"
Purpose: Bulk insert many parsed\_segments for stress testing\. Make sure storage\.mongo\_client\.get\_db exists\.
```

```python
from datetime import datetime, timezone  
from bson import ObjectId  
from storage\.mongo\_client import get\_db  
```
  
```python
db = get\_db\(\)  
DOC = db\.raw\_documents\.find\_one\(\)  
if not DOC:  
    raise Exception\("No raw document found\. Insert one first\."\)  
DOC\_ID = str\(DOC\['\_id'\]\)  
```
  
```python
NUM\_SEGMENTS = 10000  
for i in range\(NUM\_SEGMENTS\):  
    db\.parsed\_segments\.insert\_one\(\{  
        "tenant\_id": f"t\{i % 5\}",  
```
```text title="week5.md snippet 8"
        "doc\_id": DOC\_ID,  
```
```python
        "page\_number": \(i % 10\) \+ 1,  
        "text": f"Sample text segment \{i\}",  
        "bbox": \{"x": 0, "y": 0, "w": 100, "h": 50\},  
```
```text title="week5.md snippet 9"
        "confidence": 0\.95,  
        "ocr\_engine": "tesseract",  
        "entities": \["sample\_entity"\],  
```
```python
        "created\_at": datetime\.now\(timezone\.utc\)  
    \}\)  
```


### 7\.2 tests/stress\_benchmark\.py

```text title="week5.md snippet 10"
Purpose: Insert missing segments and benchmark query performance across iterations\.
```

```python title="week5.md snippet 11"
<!-- SANITIZED IMPORT/EXPORT: import time   -->
```
```python
from datetime import datetime, timezone  
from storage\.mongo\_client import get\_db  
```
  
```python
db = get\_db\(\)  
DOC = db\.raw\_documents\.find\_one\(\)  
DOC\_ID = str\(DOC\['\_id'\]\)  
TENANT\_ID = "t0"  
```
  
```python
NUM\_SEGMENTS = 10000  
existing\_count = db\.parsed\_segments\.count\_documents\(\{"tenant\_id": TENANT\_ID, "doc\_id": DOC\_ID\}\)  
if existing\_count < NUM\_SEGMENTS:  
    for i in range\(NUM\_SEGMENTS \- existing\_count\):  
        db\.parsed\_segments\.insert\_one\(\{\.\.\.\}\)  \# see exact insertion fields in repo  
```
  
\# Benchmark loop\.\.\.  


### 7\.3 tests/benchmark\_queries\.py

```text title="week5.md snippet 12"
Purpose: Quick benchmark script to measure query time and run explain plan\.
```

```python title="week5.md snippet 13"
<!-- SANITIZED IMPORT/EXPORT: import time   -->
```
```python
from datetime import datetime, timezone  
from storage\.mongo\_client import get\_db  
```
  
```python
db = get\_db\(\)  
DOC = db\.raw\_documents\.find\_one\(\)  
DOC\_ID = str\(DOC\['\_id'\]\)  
TENANT\_ID = "t0"  
query = \{"tenant\_id": TENANT\_ID, "doc\_id": DOC\_ID\}  
```
  
```python
times = \[\]  
for i in range\(10\):  
    start = time\.time\(\)  
    segments = list\(db\.parsed\_segments\.find\(query\)\)  
    elapsed = \(time\.time\(\) \- start\) \* 1000  
    times\.append\(elapsed\)  
print\("Average:", sum\(times\)/len\(times\)\)  
```
  
```python
plan = db\.parsed\_segments\.find\(query\)\.explain\(\)  
print\(plan\["executionStats"\]\["executionTimeMillis"\]\)  
```


### 7\.4 tests/benchmark\_post\_migration\.py

```text title="week5.md snippet 14"
Purpose: Post\-migration single\-run benchmark and sanity check\.
```

\# This file checks a sample segment exists and runs one query \+ explain  
\# It converts doc\_id to string to satisfy schema\.  


### 7\.5 tests/full\_workflow\.py

```text title="week5.md snippet 15"
Purpose: Combine insertion, migration, benchmark, and explain plan into a single flow for end\-to\-end verification\.
```

```text title="week5.md snippet 16"
\# Steps executed:  
\# 1\) Apply migrations/indexes  
\# 2\) Insert missing stress data  
\# 3\) Run benchmark queries and print results  
```


## 8\. storage/mongo\_schema\.md \(documentation\)

This markdown file contains the schema overview, index list, TTL rules, and summarized benchmark results\. Keep this file under storage/mongo\_schema\.md for team review\.

Example content is in the file; ensure it contains index list including tenant\_id\_1\_doc\_id\_1, text text index, and TTL entry\.

## 9\. Troubleshooting &amp; Issues encountered

```python
Below are the common issues encountered during Week 5 and how they were fixed \(record these in the doc for team context\):
```

```python title="week5.md snippet 17"
\- ModuleNotFoundError: No module named 'storage' — Run scripts using module syntax from project root: python \-m tests\.&lt;script> or add project root to PYTHONPATH\.
```

```python
\- Document failed validation — Fix: convert DOC\['\_id'\] \(ObjectId\) to string before inserting into parsed\_segments\. Use DOC\_ID = str\(DOC\['\_id'\]\)\.
```

\- mongodump not found in PowerShell/VS Code — Ensure $mongoDumpPath points to full path including mongodump\.exe; or add tools bin to PATH\.

## 10\. Acceptance Criteria &amp; Benchmark Results

```text title="week5.md snippet 18"
Acceptance: Queries for segments by doc\_id and tenant\_id must be &lt;200ms for sample data\.
```

```python
Representative benchmark results from runs:
```

```python
\- Average query time over multiple runs: ~85 \- 140 ms \(varies by dataset size\)\.
```

```python
\- Example run: Average 139\.42 ms \(one iteration peaked at 250\.98 ms due to local spike\)\.
```

```text title="week5.md snippet 19"
\- Index used consistently: tenant\_id\_1\_doc\_id\_1
```

## 11\. How to run \(step\-by\-step\)

```text title="week5.md snippet 20"
1\. Activate virtual env: \.venv\\Scripts\\Activate\.ps1
```

2\. Ensure MongoDB is running and accessible and MONGO\_URI set if not default\.

```python
3\. Apply migrations \(from project root\):
```

```python
python \-m storage\.migrations\.v2\_harden\_parsed\_segments
```

```python
4\. Run stress insertion: \(from project root\)
```

```python
python \-m tests\.stress\_test\_parsed\_segments
```

```python
5\. Run benchmark:
```

```python
python \-m tests\.stress\_benchmark  
python \-m tests\.benchmark\_queries  
python \-m tests\.benchmark\_post\_migration
```

```python
6\. Run backup manually to verify:
```

```python
\.\\scripts\\backup\_mongosh\.ps1  \# in PowerShell \(ensure execution policy bypass\)
```

## 12\. Next steps &amp; Recommendations

```python
\- Consider bulk insert \(insert\_many\) in stress scripts for speed\.
```

\- Monitor p95 and p99 latencies, not just average\.

\- Configure automated Task Scheduler job for scripts/backup\_mongosh\.ps1 if desired\.

\- Consider sharding/partitioning if dataset grows beyond single\-node IO capacity\.

\- Add CI job to run benchmark script on staging after migrations\.

Generated for SmartIDH3 \- Week 5\. Includes exact file names and instructions as requested\.
