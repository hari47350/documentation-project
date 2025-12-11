---
id: week4
title: Week 04 — Teama
sidebar_label: Week 04
---

# SmartIDH3 Integration Test Runbook

__Purpose:__ Test end\-to\-end integration: ingest documents into MongoDB → Chroma → backup binary to AWS S3 → create pointer in MongoDB → verify backup/restore\.

## __Prerequisites__

1. __Python Environment__
	- Python 3\.10\+ installed
	- Virtual environment activated:
	- & C:/Users/admin/smartidh3/\.venv/Scripts/Activate\.ps1
2. __Dependencies__

- pip install pymongo chromadb boto3

1. __MongoDB__
	- Running on localhost:27017
	- Database: test\_integration
	- Collection: test\_collection
2. __Chroma__
	- Chroma client installed
3. __AWS S3__
	- AWS account with access key and secret key
	- Environment variables set \(replace with your keys\):
	- \[Environment\]::SetEnvironmentVariable\("AWS\_ACCESS\_KEY\_ID", "your\_access\_key>", "User"\)  
\[Environment\]::SetEnvironmentVariable\("AWS\_SECRET\_ACCESS\_KEY", "your\_secret\_key>", "User"\)  
\[Environment\]::SetEnvironmentVariable\("AWS\_DEFAULT\_REGION", "us\-east\-1", "User"\)

## __Steps to Run__

1. Navigate to the integration test directory:

- cd C:\\Users\\admin\\smartidh3\\integration\_test\_setup

1. Run the smoke test:

- python smoke\_test\.py

## __Expected Output__

Inserted new document into MongoDB / Document already exists in MongoDB  
MongoDB test passed: \[\.\.\.\]  
Chroma test passed: \{\.\.\.\}  
Created S3 bucket: test\-backup\-xxxxxx  
✅ Uploaded 'test\_binary\.pdf' to S3 bucket 'test\-backup\-xxxxxx'  
Inserted pointer document into MongoDB  
Backup & restore verified ✅  
Cleanup completed ✅  \(if cleanup enabled\)  
Integration test completed successfully ✅

## __Verification__

1. __MongoDB__
	- Original document \(id=1\)  

	- Pointer document \(id=binary\_1\) with S3 URI
2. __Chroma__
	- Collection test\_collection contains document Test Document 1
3. __AWS S3__
	- Navigate to S3 console → bucket test\-backup\-xxxxxx
	- Ensure test\_binary\.pdf exists
	- Optional: download and compare with local file

## __Cleanup / Reset__

- Optional, already in script \(comment out if you want to retain data\):
	- Delete S3 object & bucket  

	- Remove pointer from MongoDB  

	- Reset Chroma collection

## __Notes__

- Script is idempotent: can safely run multiple times  

- Each run creates a __unique S3 bucket__ to prevent conflicts  

- Environment variables should __not__ be committed to source control  

- Designed for __dev/test stack__ verification
