---
id: week15
title: Week 15 — Teama
sidebar_label: Week 15
---

```text title="week15.md snippet 1"
<a id="Xec675c78eb92f49c5e883a3e11e95665726b7db"></a># Week 3 Task Documentation: SmartIDH3 Multi\-Tenant System
```

&amp;lt;a id="project-overview"&amp;gt;&amp;lt;/a&amp;gt;## Project Overview

SmartIDH3 is a multi\-tenant system that provides tenant\-specific data storage, authentication, and document embedding services\. The project leverages FastAPI, MongoDB, Chroma vector database, and JWT authentication\.

&amp;lt;a id="project-structure"&amp;gt;&amp;lt;/a&amp;gt;## 1\. Project Structure

smartidh3/  
│  
├─ backend/  
│  ├─ routes/  
│  │  ├─ auth\.py               \# FastAPI router for authentication  
│  │  ├─ documents\.py          \# FastAPI router for document management  
│  ├─ services/  
│  │  ├─ chroma\_service\.py     \# ChromaTenantService class  
│  ├─ utils/  
│  │  ├─ \_\_init\_\_\.py           \# Package initializer  
│  │  ├─ jwt\_utils\.py           \# JWT create/verify functions  
│  ├─ seed\_demo\.py             \# Seed demo tenants and users  
│  
├─ tests/  
│  ├─ test\_auth\.py             \# Tests for authentication  
│  ├─ test\_chroma\_service\.py    \# Tests for ChromaTenantService  
│  ├─ test\_demo\_tenant\.py      \# Tests for demo tenant isolation  
│  ├─ test\_seed\_demo\.py        \# Tests for seed\_demo\.py

```text title="week15.md snippet 2"
<a id="fastapi-authentication-auth.py"></a>## 2\. FastAPI Authentication: auth\.py
```

- Provides /login endpoint\.
- Uses MongoDB to validate user credentials\.
- Issues JWT containing user\_id and tenant\_id\.

```python
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
from fastapi import APIRouter, HTTPException  
```