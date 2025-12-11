---
id: week2
title: Week 02 — Teama
sidebar_label: Week 02
---

# <a id="X827cc48092b775e7f0c4964b0fcd0167b9f581e"></a>Week 1: MongoDB Setup and CRUD Verification

## <a id="project-smartidh3"></a>Project: smartidh3

### <a id="tasks"></a>Tasks

Learning & Focus  Deliverables  Acceptance Criteria  Est\. hrs/week  Dependencies  Design MongoDB schema \(raw\_documents, parsed\_segments, users/tenants\)\. NoSQL modeling, transactions, indexes  storage/mongo\_schema\.md, storage/mongo\_client\.py

```javascript title="week2.md"
```text title="bc00dc005ac04b74874a1a30204738b0"
Mongo container \+ client connection tested; basic CRUD example works
```
```

36  Docker, MongoDB 8\.x, mongosh 2\.5\.x

## <a id="step-by-step-commands-setup"></a>Step\-by\-Step Commands & Setup

### <a id="create-necessary-directories"></a>1️⃣ Create necessary directories

mkdir C:\\Users\\admin\\smartidh3\\data\\db \-Force mkdir C:\\Users\\admin\\smartidh3\\log \-Force

### <a id="mongodb-configuration-file-mongod.cfg"></a>2️⃣ MongoDB Configuration File \(mongod\.cfg\)

systemLog: destination: file path: C:/Users/admin/smartidh3/log/mongod\.log logAppend: true  storage: dbPath: C:/Users/admin/smartidh3/data/db  net: bindIp: 127\.0\.0\.1 port: 27017  security: authorization: enabled

### <a id="start-mongodb-with-config"></a>3️⃣ Start MongoDB with Config

& "C:\\Program Files\\MongoDB\\Server\\8\.0\\bin\\mongod\.exe" \-\-config "C:/Users/admin/smartidh3/mongod\.cfg"

### <a id="create-admin-user"></a>4️⃣ Create Admin User

& "C:\\Users\\admin\\Downloads\\mongosh\-2\.5\.8\-win32\-x64\\mongosh\-2\.5\.8\-win32\-x64\\bin\\mongosh\.exe"  use admin

```text title="week2.md"
```text title="bc00dc005ac04b74874a1a30204738b0"
db\.createUser\(\{
```
```

user: "admin", pwd: "StrongPassword123\!",

```text title="week2.md"
```text title="bc00dc005ac04b74874a1a30204738b0"
  roles: \[ \{ role: "root", db: "admin" \} \]
\}\)
```
```

### <a id="verify-authentication"></a>5️⃣ Verify Authentication

& "C:\\Users\\admin\\Downloads\\mongosh\-2\.5\.8\-win32\-x64\\mongosh\.exe" \-u admin \-p StrongPassword123\! \-\-authenticationDatabase admin

```text title="week2.md"
```text title="bc00dc005ac04b74874a1a30204738b0"
db\.runCommand\(\{ connectionStatus: 1 \}\)
```
```

To verify that your admin user exists and has the correct roles, run:  db\.getUsers\(\)

### <a id="create-database-and-collections"></a>6️⃣ Create Database and Collections

use smartidh3 db\.createCollection\("raw\_documents"\) db\.createCollection\("parsed\_segments"\) db\.createCollection\("users"	\)

### <a id="create-indexes"></a>7️⃣ Create Indexes

```text title="week2.md"
```text title="bc00dc005ac04b74874a1a30204738b0"
db\.raw\_documents\.createIndex\(\{ tenantId: 1 \}\)
db\.parsed\_segments\.createIndex\(\{ documentId: 1, sequence: 1 \}\)
db\.users\.createIndex\(\{ tenantId: 1, email: 1 \}, \{ unique: true \}\)
```
```

### <a id="insert-sample-data-crud"></a>8️⃣ Insert Sample Data \(CRUD\)

// Insert a user

```text title="week2.md"
```text title="bc00dc005ac04b74874a1a30204738b0"
db\.users\.insertOne\(\{ tenantId: 1, email: "user@example\.com", name: "Alice" \}\)
```
```

// Insert raw document and get ObjectId

```javascript title="week2.md"
```text title="bc00dc005ac04b74874a1a30204738b0"
const rawDoc = db\.raw\_documents\.insertOne\(\{ tenantId: 1, title: "Doc1", content: "Sample text" \}\)
const docId = rawDoc\.insertedId
```
```

// Insert parsed segment referencing the document

```text title="week2.md"
```text title="bc00dc005ac04b74874a1a30204738b0"
db\.parsed\_segments\.insertOne\(\{ documentId: docId, sequence: 1, text: "Segment 1" \}\)
```
```

```javascript title="week2.md"
```text title="bc00dc005ac04b74874a1a30204738b0"
### <a id="notes"></a>Docker ;
```
```

docker run \-d \-p 27018:27017 \-\-name smartidh3\_mongo\_alt \-v C:/Users/admin/smartidh3/data/db:/data/db mongo:8\.0 –auth  __You can verify it with:__  docker ps

### ✅ Notes

- Run PowerShell commands __outside mongosh__\. Do not type & "path\\to\\mongod\.exe" inside the MongoDB shell\. - Ensure the __log and data directories exist__ before starting MongoDB to avoid errors\. - Use unique emails in users collection to avoid duplicate key errors\.  __Screenshots \(optional placeholders\)__ \- MongoDB running with authentication \- Admin user creation \- CRUD operations success  *End of Week 1 Documentation*