---
id: week2
title: Week 02 — Team -B
sidebar_label: Week 02
---

SmartIDH3 week \-3 Documentation

# &lt;a id="project-structure"&gt;&lt;/a&gt;1\. Project Structure

\. Project Structure  smartidh3/ │ 
├─ backend/ 
│  
├─ routes/
 │ 
 │ 
  ├─ auth\.py              \# FastAPI router for authentication 
  
  │ 
```text title="week2.md snippet 1"
       │  ├─ documents\.py          \# FastAPI router for document management │  ├─ services/ │  │  ├─ chroma\_service\.py     \# ChromaTenantService class │  ├─ utils/ │  │  ├─ \_\_init\_\_\.py           \# Package initializer │  │  ├─ jwt\_utils\.py           \# JWT create/verify functions │  ├─ seed\_demo\.py             \# Seed demo tenants and users │ ├─ tests/ │  ├─ test\_auth\.py             \# Tests for authentication │  ├─ test\_chroma\_service\.py    \# Tests for ChromaTenantService │  ├─ test\_demo\_tenant\.py      \# Tests for demo tenant isolation │  ├─ test\_seed\_demo\.py        \# Tests for seed\_demo\.py  |── \.venv/ ├── requirements\.txt └── README\.md
```

# &lt;a id="seed-script-seed_demo.py"&gt;&lt;/a&gt;2\. Seed Script \(seed\_demo\.py\)

""" Seed demo tenants and users into MongoDB\. Ensures idempotent insertion using upsert\. """

```python title="fdc4b4fd3f19449399b23447badb8064"
from pymongo import MongoClient
```

```python
\# Database Connection client = MongoClient\("mongodb://admin:StrongPassword123\!@localhost:27017"\) db = client\["multitenant"\]  \# Seed Tenants tenants = \[
```

```text title="week2.md"
```text title="fdc4b4fd3f19449399b23447badb8064"
```python
\{"\_id": "tenant\_acme", "name": "Acme Inc"\},
\{"\_id": "tenant\_beta", "name": "Beta Corp"\}
```
```
``` title="week2.md (snippet 1)"

\]

```text title="fdc4b4fd3f19449399b23447badb8064"
for tenant in tenants:
    db\["tenants"\]\.update\_one\(\{"\_id": tenant\["\_id"\]\}, \{"$set": tenant\}, upsert=True\)
```

```python
\# Seed Users users = \[
```

```text title="week2.md"
```text title="fdc4b4fd3f19449399b23447badb8064"
```python
\{"email": "alice@acme\.com", "password": "1234", "tenant\_id": "tenant\_acme"\},
\{"email": "bob@beta\.com", "password": "1234", "tenant\_id": "tenant\_beta"\}
```
```
``` title="week2.md (snippet 2)"

\]

```text title="fdc4b4fd3f19449399b23447badb8064"
for user in users:
    db\["users"\]\.update\_one\(\{"email": user\["email"\]\}, \{"$set": user\}, upsert=True\)
```

```python
print\("Demo tenants/users seeded successfully\."\)
```

# &lt;a id="test-script-teststest_seed_demo.py"&gt;&lt;/a&gt;3\. Test Script \(tests/test\_seed\_demo\.py\)

```python title="week2.md"
```python title="fdc4b4fd3f19449399b23447badb8064"
```python title="week2.md snippet 2"
&lt;!-- SANITIZED IMPORT/EXPORT: import pytest -->
&lt;!-- SANITIZED IMPORT/EXPORT: import backend\.seed\_demo as seed\_demo -->
```
```
``` title="week2.md (snippet 3)"

@pytest\.fixture

```python title="week2.md"
```python title="fdc4b4fd3f19449399b23447badb8064"
```python
def fake\_mongo\(monkeypatch\):
```
"""Mock MongoDB client and collections used in seed\_demo\."""
```
``` title="week2.md (snippet 4)"

```python title="week2.md"
```python title="fdc4b4fd3f19449399b23447badb8064"
```python
class FakeCollection:
    def \_\_init\_\_\(self\):
        self\.data = \{\}
    def update\_one\(self, filter\_query, update\_query, upsert=False\):
        key = filter\_query\.get\("\_id"\) or filter\_query\.get\("email"\)
        self\.data\[key\] = update\_query\["$set"\]
```
```
``` title="week2.md (snippet 5)"

```python title="week2.md"
```python title="fdc4b4fd3f19449399b23447badb8064"
```python
class FakeDB:
    def \_\_init\_\_\(self\):
        self\.collections = \{"tenants": FakeCollection\(\), "users": FakeCollection\(\)\}
    def \_\_getitem\_\_\(self, name\):
```
```text title="week2.md snippet 3"
        return self\.collections\[name\]
```
```
``` title="week2.md (snippet 6)"

```text title="week2.md"
```text title="fdc4b4fd3f19449399b23447badb8064"
```python
fake\_db = FakeDB\(\)
monkeypatch\.setattr\(seed\_demo, "db", fake\_db\)
```
return fake\_db
```
``` title="week2.md (snippet 7)"

```powershell title="week2.md"
```python title="fdc4b4fd3f19449399b23447badb8064"
```python
def test\_seed\_demo\_inserts\_correct\_data\(fake\_mongo\):
```
"""Ensure tenants and users are inserted correctly\."""
```python
for tenant in seed\_demo\.tenants:
    fake\_mongo\["tenants"\]\.update\_one\(\{"\_id": tenant\["\_id"\]\}, \{"$set": tenant\}, upsert=True\)
for user in seed\_demo\.users:
    fake\_mongo\["users"\]\.update\_one\(\{"email": user\["email"\]\}, \{"$set": user\}, upsert=True\)
```
```
``` title="week2.md (snippet 8)"

```text title="week2.md"
```text title="fdc4b4fd3f19449399b23447badb8064"
```python
tenants = fake\_mongo\["tenants"\]\.data
users = fake\_mongo\["users"\]\.data
```
```
``` title="week2.md (snippet 9)"

```text title="week2.md"
```text title="fdc4b4fd3f19449399b23447badb8064"
```python
assert len\(tenants\) == 2
```
assert "tenant\_acme" in tenants
assert "tenant\_beta" in tenants
```
``` title="week2.md (snippet 10)"

```text title="week2.md"
```text title="fdc4b4fd3f19449399b23447badb8064"
```python
assert len\(users\) == 2
assert users\["alice@acme\.com"\]\["tenant\_id"\] == "tenant\_acme"
assert users\["bob@beta\.com"\]\["tenant\_id"\] == "tenant\_beta"
```
```
``` title="week2.md (snippet 11)"

```powershell title="week2.md"
```python title="fdc4b4fd3f19449399b23447badb8064"
```python
def test\_seed\_demo\_idempotency\(fake\_mongo\):
```
"""Ensure running the seeder twice does not duplicate entries\."""
```python
for \_ in range\(2\):
    for tenant in seed\_demo\.tenants:
        fake\_mongo\["tenants"\]\.update\_one\(\{"\_id": tenant\["\_id"\]\}, \{"$set": tenant\}, upsert=True\)
    for user in seed\_demo\.users:
        fake\_mongo\["users"\]\.update\_one\(\{"email": user\["email"\]\}, \{"$set": user\}, upsert=True\)
```
```
``` title="week2.md (snippet 12)"

```text title="week2.md"
```text title="fdc4b4fd3f19449399b23447badb8064"
```python
assert len\(fake\_mongo\["tenants"\]\.data\) == 2
assert len\(fake\_mongo\["users"\]\.data\) == 2
```
```
``` title="week2.md (snippet 13)"

# &lt;a id="running-tests"&gt;&lt;/a&gt;4\. Running Tests

```python
\# Activate virtual environment \.venv\\Scripts\\activate  \# Set PYTHONPATH $env:PYTHONPATH="C:\\Users\\admin\\smartidh3"  \# Run tests
```

```text title="week2.md"
```text title="fdc4b4fd3f19449399b23447badb8064"
```python
python \-m pytest tests/test\_seed\_demo\.py \-v
```
```
```

```text title="week2.md snippet 4"
Expected output:  tests/test\_seed\_demo\.py::test\_seed\_demo\_inserts\_correct\_data PASSED tests/test\_seed\_demo\.py::test\_seed\_demo\_idempotency PASSED
```

# &lt;a id="best-practices"&gt;&lt;/a&gt;5\. Best Practices

- Keep seed scripts __idempotent__ using upsert=True\. - Use __monkeypatch or mocks__ to isolate database dependencies in tests\. - Include __docstrings__ for clarity\. - Separate __demo data__ from production data\. - Optionally, add __logging__ to track seeding\.

# &lt;a id="seeder-flow-diagram-optional"&gt;&lt;/a&gt;6\. Seeder Flow Diagram \(Optional\)

```text title="week2.md snippet 5"
__Seeder Flow:__ 1\. Connect to MongoDB\. 2\. Iterate tenants and users\. 3\. Upsert each document\. 4\. Print completion message\.  __Test Flow:__ 1\. Monkeypatch db with FakeDB\. 2\. Run seed logic\. 3\. Assert data is inserted correctly\. 4\. Assert idempotency\.  __Document Complete__
```