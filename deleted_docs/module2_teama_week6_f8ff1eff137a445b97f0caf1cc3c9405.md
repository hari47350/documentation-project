--- 
id: week6
title: Week 06 — Teama
sidebar_label: Week 06
---

# &lt;a id="mongodb-setup-schema-runbook"&gt;&lt;/a&gt;MongoDB Setup &amp; Schema Runbook

## &lt;a id="overview"&gt;&lt;/a&gt;1\. Overview

```text title="week6.md snippet 1"
This document provides step\-by\-step instructions to:
```

- Design MongoDB schema for SmartIDH3 project
- Deploy MongoDB via Docker
- Connect using Python client \(mongo\_client\.py\)
- Verify authentication and CRUD operations
- Ensure other developers can replicate setup

```text title="week6.md snippet 2"
Learning focus: NoSQL modeling, transactions, indexes, multi\-tenant data isolation\.
```

## &lt;a id="mongodb-schema-design"&gt;&lt;/a&gt;2\. MongoDB Schema Design

### &lt;a id="collections-overview"&gt;&lt;/a&gt;2\.1 Collections Overview

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

### &lt;a id="users-collection"&gt;&lt;/a&gt;2\.2 users Collection

```text title="week6.md snippet 3"
Example document:
```

```text title="week6.md snippet 4"
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

```text title="week6.md snippet 5"
__Indexes:__
```

```text title="week6.md snippet 6"
db\.users\.createIndex\(\{ email: 1 \}, \{ unique: true \}\);  
db\.users\.createIndex\(\{ tenant\_id: 1 \}\);
```

### &lt;a id="tenants-collection"&gt;&lt;/a&gt;2\.3 tenants Collection

```text title="week6.md snippet 7"
Example document:
```

```text title="week6.md snippet 8"
\{  
  "\_id": "tenant01",  
  "tenant\_name": "Acme Corporation",  
  "created\_at": ISODate\("2025\-09\-25T12:00:00Z"\),  
  "is\_active": true  
\}
```

### &lt;a id="raw_documents-collection"&gt;&lt;/a&gt;2\.4 raw\_documents Collection

```text title="week6.md snippet 9"
Example document:
```

```text title="week6.md snippet 10"
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

```text title="week6.md snippet 11"
__Indexes:__
```

```text title="week6.md snippet 12"
db\.raw\_documents\.createIndex\(\{ tenant\_id: 1 \}\);  
db\.raw\_documents\.createIndex\(\{ sha256: 1 \}, \{ unique: true \}\);
```

### &lt;a id="parsed_segments-collection"&gt;&lt;/a&gt;2\.5 parsed\_segments Collection

```text title="week6.md snippet 13"
Example document:
```

```text title="week6.md snippet 14"
\{  
  "\_id": ObjectId\(\),  
  "document\_id": ObjectId\("ref\_to\_raw\_document"\),  
  "segment\_type": "header/footer/body",  
  "content": "Parsed content text here",  
  "created\_at": ISODate\("2025\-09\-25T12:05:00Z"\)  
\}
```

```text title="week6.md snippet 15"
__Indexes:__
```

```text title="week6.md snippet 16"
db\.parsed\_segments\.createIndex\(\{ document\_id: 1 \}\);
```

## &lt;a id="mongodb-docker-setup"&gt;&lt;/a&gt;3\. MongoDB Docker Setup

### &lt;a id="docker-compose.yml"&gt;&lt;/a&gt;3\.1 docker\-compose\.yml

```text title="week6.md snippet 17"
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

### &lt;a id="run-mongodb-container"&gt;&lt;/a&gt;3\.2 Run MongoDB Container

docker compose up \-d

### &lt;a id="verify"&gt;&lt;/a&gt;3\.3 Verify

docker ps

```text title="week6.md snippet 18"
Should show mongo:8\.0 running on port 27017\.
```

## &lt;a id="python-client-configuration"&gt;&lt;/a&gt;4\. Python Client Configuration

### &lt;a id="dependencies"&gt;&lt;/a&gt;4\.1 Dependencies

pip install pymongo python\-dotenv

### &lt;a id="environment-variables-.env"&gt;&lt;/a&gt;4\.2 Environment Variables \(\.env\)

```text title="week6.md snippet 19"
MONGO\_URI=mongodb://admin:StrongPassword123\!@localhost:27017/  
```
MONGO\_DB\_NAME=smartidh3

### &lt;a id="python-client-example"&gt;&lt;/a&gt;4\.3 Python Client Example

```text title="week6.md snippet 20"
storage/mongo\_client\.py:
```

```python
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
from pymongo import MongoClient  
```