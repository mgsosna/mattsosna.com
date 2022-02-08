---
layout: post
title: AWS Essentials for Data Science - 2. Storage
title-clean: AWS Essentials for Data Science<div class="a2">2. Storage</div>
author: matt_sosna
---

In the [intro post]({{  site.baseurl  }}/AWS-Intro), we introduced cloud computing as an industry, as well as Amazon Web Services (AWS). In this post, we'll talk about one of the major advantages of the cloud: **data storage.** We'll cover [blob](https://en.wikipedia.org/wiki/Binary_large_object) storage (S3) and databases.

Your computer has a finite amount of data it can store (which is different from memory). But you also want to be able to access this information from other computers. Dropbox's business model is based off this, as well as Google Drive, etc. Unthinkable to go back.

## Table of contents
* [Why cloud storage?](#why-cloud-storage)
* [Types of data](#types-of-data)
* [S3 (Simple Storage Service)](#s3)
* [RDS (Relational Database Service)](#rds)
* [DynamoDB](#dynamodb)

## Why cloud storage?
When you're working by yourself on a relatively small project, you probably don't think too hard about data access and storage. Maybe the CSVs are in the same folder as your Jupyter Notebook or R scripts, or if you're fancy they're backed up to a hard drive.

But what happens when you want to share that data with someone, or have multiple people access it at the same time? It doesn't make sense to keep the data on your laptop and then take turns using your data. Maybe you decide to copy the data to each person's laptop. But if the files are large, this can take a while. And what if someone unknowingly modifies their copy of the data, meaning their analyses don't sync up with yours? Without a single source of truth, it can be really hard to debug the issue. And finally, what happens if someone leaves the project? They can just take their copy of the data with them, sharing it with competitors or malicious actors.

Cloud storage is meant to address these issues. You're likely already familiar with Dropbox or Google Drive $-$ these services have become ubiquitous because it's now unthinkable to try sending data through an email or handing it over on a USB stick. Upload a file to Dropbox, send your friend a link to the file, and you're done.

But cloud storage can go beyond this $-$ AWS and others provide [SDKs](https://www.ibm.com/cloud/blog/sdk-vs-api), or **software development kits** that allow you to interact with the cloud through code. So instead of needing to click and drag a file from Google Drive onto your Desktop, then load it into Python, you can pull it straight into Python with the `boto3` library.



AWS guarantees ["five nines"](https://aws.amazon.com/blogs/publicsector/achieving-five-nines-cloud-justice-public-safety/), or 99.999% availability for justice and public safety customers, for example. (That means AWS guarantees it will be unavailable less than five minutes and 15 seconds per year.)

## Types of data
So we see that it's useful to store data in the cloud so it's easily accessible to the right people, hard to access for everyone else, resilient and robust, etc.

But "data" is a broad term $-$ is it raw videos or text transcripts? Is it a user profile? Is it code? Is it tabular data? The _structure_ of the data (unstructured, semi-structured, and structured) will determine what the right storage solution is.

The amount of data we have can grow very quickly, and we want to be able to access it quickly.

But there are certain files that are hard to neatly store in a database. **Binary large objects**, or **[BLOB](https://en.wikipedia.org/wiki/Binary_large_object)s** for short, are large collections of binary data that can't be easily broken up, or shouldn't. Think of an image $-$ you don't really want half the pixels in one file and half in another, when you'll always be fetching the entire image any time you want to access it. Similarly, audio, video, or [executable programs](https://en.wikipedia.org/wiki/Executable) are large entities that you almost always to fetch all at once.

### S3
S3 is Simple Storage Service. This is like Dropbox or Google Drive - just the raw data. Even when you have a database, it's probably a good idea to put the raw input data (e.g. text files from user interviews, or the raw sensor data for your IoT application) in S3 as a backup.

Data is stored in **buckets,** which are like distinct folders. We can create a bucket in the UI like this:

<img src="{{ site.baseurl }}/images/data_engineering/aws/storage/create_bucket.png">s




### RDS
RDS is Relational Database Service. This is like a SQL database hosted in the cloud (on top of an EC2 instance). For NoSQL, you're looking at DynamoDB.

### Redshift
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
