---
id: week4
title: Week 04 — Teama
sidebar_label: Week 04
---

SmartIDH3 Multi\-Tenant Seeder Documentation

# 1\. Project Structure

smartidh3/  
│  
├── backend/  
│   ├── routes/  
│   │   ├── auth\.py  
│   │   └── documents\.py  
│   ├── utils/  
│   │   ├── \_\_init\_\_\.py  
│   │   └── jwt\_utils\.py  
│   └── seed\_demo\.py  
├── tests/  
│   ├── test\_auth\.py  
│   ├── test\_chroma\_service\.py  
│   ├── test\_demo\_tenant\.py  
│   └── test\_seed\_demo\.py  
├── \.venv/  
├── requirements\.txt  
└── README\.md

```text title="week4.md snippet 1"
<a id="seed-script-seed_demo.py"></a># 2\. Seed Script \(seed\_demo\.py\)

```
"""  
Seed demo tenants and users into MongoDB\.  
Ensures idempotent insertion using upsert\.  
"""  
  
```python title="week4.md snippet 2"
from pymongo import MongoClient  
  
```
\# Database Connection  
```text title="week4.md snippet 3"
client = MongoClient\("mongodb://admin:StrongPassword123\!@localhost:27017"\)  
```
```text title="1\. Project Structure"
db = client\["multitenant"\]  
  
```
\# Seed Tenants  
```text title="1\. Project Structure"
tenants = \[  
```
```text title="week4.md snippet 4"
    \{"\_id": "tenant\_acme", "name": "Acme Inc"\},  
    \{"\_id": "tenant\_beta", "name": "Beta Corp"\}  
```
\]  
```text title="week4.md snippet 5"
for tenant in tenants:  
    db\["tenants"\]\.update\_one\(\{"\_id": tenant\["\_id"\]\}, \{"$set": tenant\}, upsert=True\)  
  
```
\# Seed Users  
```text title="1\. Project Structure"
users = \[  
```
```text title="week4.md snippet 6"
    \{"email": "alice@acme\.com", "password": "1234", "tenant\_id": "tenant\_acme"\},  
    \{"email": "bob@beta\.com", "password": "1234", "tenant\_id": "tenant\_beta"\}  
```
\]  
```text title="week4.md snippet 7"
for user in users:  
    db\["users"\]\.update\_one\(\{"email": user\["email"\]\}, \{"$set": user\}, upsert=True\)  
  
print\("Demo tenants/users seeded successfully\."\)

<a id="test-script-teststest_seed_demo.py"></a># 3\. Test Script \(tests/test\_seed\_demo\.py\)

import pytest  
import backend\.seed\_demo as seed\_demo  
  
```
@pytest\.fixture  
```python title="week4.md snippet 8"
def fake\_mongo\(monkeypatch\):  
    """Mock MongoDB client and collections used in seed\_demo\."""  
  
    class FakeCollection:  
        def \_\_init\_\_\(self\):  
            self\.data = \{\}  
        def update\_one\(self, filter\_query, update\_query, upsert=False\):  
            key = filter\_query\.get\("\_id"\) or filter\_query\.get\("email"\)  
            self\.data\[key\] = update\_query\["$set"\]  
  
    class FakeDB:  
        def \_\_init\_\_\(self\):  
            self\.collections = \{"tenants": FakeCollection\(\), "users": FakeCollection\(\)\}  
        def \_\_getitem\_\_\(self, name\):  
            return self\.collections\[name\]  
  
    fake\_db = FakeDB\(\)  
    monkeypatch\.setattr\(seed\_demo, "db", fake\_db\)  
    return fake\_db  
  
  
def test\_seed\_demo\_inserts\_correct\_data\(fake\_mongo\):  
    """Ensure tenants and users are inserted correctly\."""  
    for tenant in seed\_demo\.tenants:  
        fake\_mongo\["tenants"\]\.update\_one\(\{"\_id": tenant\["\_id"\]\}, \{"$set": tenant\}, upsert=True\)  
    for user in seed\_demo\.users:  
        fake\_mongo\["users"\]\.update\_one\(\{"email": user\["email"\]\}, \{"$set": user\}, upsert=True\)  
  
    tenants = fake\_mongo\["tenants"\]\.data  
    users = fake\_mongo\["users"\]\.data  
  
    assert len\(tenants\) == 2  
    assert "tenant\_acme" in tenants  
    assert "tenant\_beta" in tenants  
  
    assert len\(users\) == 2  
    assert users\["alice@acme\.com"\]\["tenant\_id"\] == "tenant\_acme"  
    assert users\["bob@beta\.com"\]\["tenant\_id"\] == "tenant\_beta"  
  
  
def test\_seed\_demo\_idempotency\(fake\_mongo\):  
    """Ensure running the seeder twice does not duplicate entries\."""  
    for \_ in range\(2\):  
        for tenant in seed\_demo\.tenants:  
            fake\_mongo\["tenants"\]\.update\_one\(\{"\_id": tenant\["\_id"\]\}, \{"$set": tenant\}, upsert=True\)  
        for user in seed\_demo\.users:  
            fake\_mongo\["users"\]\.update\_one\(\{"email": user\["email"\]\}, \{"$set": user\}, upsert=True\)  
  
    assert len\(fake\_mongo\["tenants"\]\.data\) == 2  
    assert len\(fake\_mongo\["users"\]\.data\) == 2

```
# 4\. Running Tests

\# Activate virtual environment  
\.venv\\Scripts\\activate  
  
\# Set PYTHONPATH  
```text title="week4.md snippet 9"
$env:PYTHONPATH="C:\\Users\\admin\\smartidh3"  
  
```
\# Run tests  
```text title="4\. Running Tests"
python \-m pytest tests/test\_seed\_demo\.py \-v

```
```text title="week4.md snippet 10"
Expected output:

tests/test\_seed\_demo\.py::test\_seed\_demo\_inserts\_correct\_data PASSED  
 tests/test\_seed\_demo\.py::test\_seed\_demo\_idempotency PASSED

```
# 5\. Best Practices

- Keep seed scripts __idempotent__ using upsert=True\.
- Use __monkeypatch or mocks__ to isolate database dependencies in tests\.
- Include __docstrings__ for clarity\.
- Separate __demo data__ from production data\.
- Optionally, add __logging__ to track seeding\.

```text title="week4.md snippet 11"
<a id="seeder-flow-diagram-optional"></a># 6\. Seeder Flow Diagram \(Optional\)

__Seeder Flow:__ 1\. Connect to MongoDB\. 2\. Iterate tenants and users\. 3\. Upsert each document\. 4\. Print completion message\.

__Test Flow:__ 1\. Monkeypatch db with FakeDB\. 2\. Run seed logic\. 3\. Assert data is inserted correctly\. 4\. Assert idempotency\.

```
__Document Complete__