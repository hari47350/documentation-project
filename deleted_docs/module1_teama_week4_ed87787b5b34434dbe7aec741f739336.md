---
id: week4
title: Week 04 — Teama
sidebar_label: Week 04
---

# &amp;lt;a id="mongodb-setup-schema-runbook"&amp;gt;&amp;lt;/a&amp;gt;MongoDB Setup &amp;amp; Schema Runbook

## &amp;lt;a id="overview"&amp;gt;&amp;lt;/a&amp;gt;1\. Overview

```text title="week4.md snippet 1"
This document provides step\-by\-step instructions to:
```

- Design MongoDB schema for SmartIDH3 project
- Deploy MongoDB via Docker
- Connect using Python client \(mongo\_client\.py\)
- Verify authentication and CRUD operations
- Ensure other developers can replicate setup

```text title="week4.md snippet 2"
Learning focus: NoSQL modeling, transactions, indexes, multi\-tenant data isolation\.
```

## &amp;lt;a id="mongodb-schema-design"&amp;gt;&amp;lt;/a&amp;gt;2\. MongoDB Schema Design

### &amp;lt;a id="collections-overview"&amp;gt;&amp;lt;/a&amp;gt;2\.1 Collections Overview

Collection

Purpose

users

Store user metadata, role, tenant association

tenants

Track tenant organizations

raw\_documents

Store uploaded file metadata

parsed\_segments

Store structured content extracted from raw documents

### &amp;lt;a id="users-collection"&amp;gt;&amp;lt;/a&amp;gt;2\.2 users Collection

```text title="week4.md snippet 3"
Example document:
```

```text title="week4.md snippet 4"
\{  
  "\_id": ObjectId\(\),  
  "email": "alice@example\.com",  
  "tenant\_id": "tenant01",  
  "name": "Alice Smith",  
  "role": "admin",  
  "created\_at": ISODate\("2025\-09\-25T12:00:00Z"\),  
  "last\_login": ISODate\("2025\-09\-30T09:30:00Z"\)  
\}
```

```text title="week4.md snippet 5"
__Indexes:__
```

```text title="week4.md snippet 6"
db\.users\.createIndex\(\{ email: 1 \}, \{ unique: true \}\);  
db\.users\.createIndex\(\{ tenant\_id: 1 \}\);
```

### &amp;lt;a id="tenants-collection"&amp;gt;&amp;lt;/a&amp;gt;2\.3 tenants Collection

```text title="week4.md snippet 7"
Example document:
```

```text title="week4.md snippet 8"
\{  
  "\_id": "tenant01",  
  "tenant\_name": "Acme Corporation",  
  "created\_at": ISODate\("2025\-09\-25T12:00:00Z"\),  
  "is\_active": true  
\}
```

### &amp;lt;a id="raw_documents-collection"&amp;gt;&amp;lt;/a&amp;gt;2\.4 raw\_documents Collection

```text title="week4.md snippet 9"
Example document:
```

```text title="week4.md snippet 10"
\{  
  "\_id": ObjectId\(\),  
  "tenant\_id": "tenant01",  
  "file\_name": "invoice\_123\.pdf",  
  "content\_type": "application/pdf",  
  "storage\_path": "/s3/invoices/invoice\_123\.pdf",  
  "sha256": "dummyhash123456789",  
  "uploaded\_by": ObjectId\("user\_id\_here"\),  
  "uploaded\_at": ISODate\("2025\-09\-25T12:02:00Z"\),  
  "status": "uploaded"  
\}
```

```text title="week4.md snippet 11"
__Indexes:__
```

```text title="week4.md snippet 12"
db\.raw\_documents\.createIndex\(\{ tenant\_id: 1 \}\);  
db\.raw\_documents\.createIndex\(\{ sha256: 1 \}, \{ unique: true \}\);
```

### &amp;lt;a id="parsed_segments-collection"&amp;gt;&amp;lt;/a&amp;gt;2\.5 parsed\_segments Collection

```text title="week4.md snippet 13"
Example document:
```

```text title="week4.md snippet 14"
\{  
  "\_id": ObjectId\(\),  
  "document\_id": ObjectId\("ref\_to\_raw\_document"\),  
  "segment\_type": "header/footer/body",  
  "content": "Parsed content text here",  
  "created\_at": ISODate\("2025\-09\-25T12:05:00Z"\)  
\}
```

```text title="week4.md snippet 15"
__Indexes:__
```

```text title="week4.md snippet 16"
db\.parsed\_segments\.createIndex\(\{ document\_id: 1 \}\);
```

## &amp;lt;a id="mongodb-docker-setup"&amp;gt;&amp;lt;/a&amp;gt;3\. MongoDB Docker Setup

### &amp;lt;a id="docker-compose.yml"&amp;gt;&amp;lt;/a&amp;gt;3\.1 docker\-compose\.yml

```text title="week4.md snippet 17"
version: '3\.8'  
services:  
  mongodb:  
    image: mongo:8\.0  
    container\_name: mongodb  
    restart: always  
    environment:  
      MONGO\_INITDB\_ROOT\_USERNAME: admin  
      MONGO\_INITDB\_ROOT\_PASSWORD: StrongPassword123\!  
    ports:  
      \- "27017:27017"  
    volumes:  
      \- \./mongo\_data:/data/db
```

### &amp;lt;a id="run-mongodb-container"&amp;gt;&amp;lt;/a&amp;gt;3\.2 Run MongoDB Container

docker compose up \-d

### &amp;lt;a id="verify"&amp;gt;&amp;lt;/a&amp;gt;3\.3 Verify

docker ps

```text title="week4.md snippet 18"
Should show mongo:8\.0 running on port 27017\.
```

## &amp;lt;a id="python-client-configuration"&amp;gt;&amp;lt;/a&amp;gt;4\. Python Client Configuration

### &amp;lt;a id="dependencies"&amp;gt;&amp;lt;/a&amp;gt;4\.1 Dependencies

pip install pymongo python\-dotenv

### &amp;lt;a id="environment-variables-.env"&amp;gt;&amp;lt;/a&amp;gt;4\.2 Environment Variables \(\.env\)

```text title="week4.md snippet 19"
MONGO\_URI=mongodb://admin:StrongPassword123\!@localhost:27017/  
```
MONGO\_DB\_NAME=smartidh3

### &amp;lt;a id="python-client-example"&amp;gt;&amp;lt;/a&amp;gt;4\.3 Python Client Example

```text title="week4.md snippet 20"
storage/mongo\_client\.py:
```

```python title="week4.md snippet 21"
from pymongo import MongoClient  
from datetime import datetime, timezone  
import os  
from dotenv import load\_dotenv  
```
  
```text title="week4.md snippet 22"
load\_dotenv\(\)  
```
  
```text title="week4.md snippet 23"
MONGO\_URI = os\.getenv\("MONGO\_URI"\)  
DB\_NAME = os\.getenv\("MONGO\_DB\_NAME"\)  
```
  
```text title="week4.md snippet 24"
client = MongoClient\(MONGO\_URI\)  
```
db = client\[DB\_NAME\]  
  
\# Insert or update a user  
```text title="week4.md snippet 25"
user\_data = \{  
    "email": "alice2@example\.com",  
    "tenant\_id": "t1",  
    "name": "Alice",  
    "role": "admin",  
    "created\_at": datetime\.now\(timezone\.utc\),  
    "last\_login": None  
\}  
db\.users\.update\_one\(\{"email": user\_data\["email"\]\}, \{"$set": user\_data\}, upsert=True\)  
```
  
\# Insert a raw document  
```text title="week4.md snippet 26"
doc = \{  
    "tenant\_id": "t1",  
    "file\_name": "invoice\_123\.pdf",  
    "content\_type": "application/pdf",  
    "storage\_path": "/s3/invoices/invoice\_123\.pdf",  
    "sha256": "dummyhash123456789",  
    "uploaded\_by": db\.users\.find\_one\(\{"email": "alice2@example\.com"\}\)\["\_id"\],  
    "uploaded\_at": datetime\.now\(timezone\.utc\),  
    "status": "uploaded"  
\}  
db\.raw\_documents\.update\_one\(\{"sha256": doc\["sha256"\]\}, \{"$setOnInsert": doc\}, upsert=True\)  
```
  
\# Insert a parsed segment  
```text title="week4.md snippet 27"
segment = \{  
    "document\_id": db\.raw\_documents\.find\_one\(\{"sha256": "dummyhash123456789"\}\)\["\_id"\],  
    "segment\_type": "body",  
    "content": "Parsed invoice content\.",  
    "created\_at": datetime\.now\(timezone\.utc\)  
\}  
db\.parsed\_segments\.insert\_one\(segment\)  
```
  
```text title="week4.md snippet 28"
print\("✅ MongoDB basic CRUD operations successful\."\)
```

## &amp;lt;a id="authentication-verification"&amp;gt;&amp;lt;/a&amp;gt;5\. Authentication Verification

```text title="week4.md snippet 29"
db\.runCommand\(\{ connectionStatus: 1 \}\)
```

Should show your authenticated admin user\.

## &amp;lt;a id="acceptance-criteria"&amp;gt;&amp;lt;/a&amp;gt;6\. Acceptance Criteria

- MongoDB container up and running
- Authentication verified
- Python client connected successfully
- Basic CRUD operations complete
- Schema and indexes documented