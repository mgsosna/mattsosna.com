---
layout: post
title: AWS Essentials for Data Science - 2. Storage
title-clean: AWS Essentials for Data Science<div class="a2">2. Storage</div>
author: matt_sosna
---

Your computer has a finite amount of data it can store (which is different from memory). But you also want to be able to access this information from other computers. Dropbox's business model is based off this, as well as Google Drive, etc. Unthinkable to go back.

---
**AWS Essentials for Data Science:**
1. Why cloud computing?
2. **Storage**
3. Compute
---

### Table of contents
* [S3 (Simple Storage Service)](#s3)
* [RDS (Relational Database Service)](#rds)
* [DynamoDB](#dynamodb)


### Storage
Need to put your data somewhere. But "data" is a broad term $-$ is it raw videos or text transcripts? Is it a user profile? Is it code? Is it tabular data? The _structure_ of the data (unstructured, semi-structured, and structured) will determine what the right storage solution is.

#### S3
S3 is Simple Storage Service. This is like Dropbox or Google Drive - just the raw data. Even when you have a database, it's probably a good idea to put the raw input data (e.g. text files from user interviews, or the raw sensor data for your IoT application) in S3 as a backup.

#### RDS
RDS is Relational Database Service. This is like a SQL database hosted in the cloud (on top of an EC2 instance). For NoSQL, you're looking at DynamoDB.

#### Redshift
Data warehouse. A data warehouse is a https://www.talend.com/resources/what-is-data-warehouse/.



### Notebooks
#### Sagemaker

[This website](https://aws-certified-cloud-practitioner.fandom.com/wiki/3.3_Identify_the_core_AWS_services) looks super helpful.
[This whitepaper](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/aws-overview.pdf) looks awesome.

### Honorable mentions
#### Sagemaker
I guess we could bring it up. Personally, I've only really used Databricks.

#### Cloudwatch
Logs.

#### Elastic Beanstalk
Deployment, I think...

#### Route 53
DNS management.

#### Glue, Athena
These combine with S3 to let you treat a bucket (or directory within one) as a big table that you can query with SQL.

There are services that build off these.

[AWS infrastructure explained](https://aws.plainenglish.io/aws-infrastructure-explained-b0f4fb7b6829)
