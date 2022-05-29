---
layout: post
title: AWS Essentials for Data Science - 2. Storage
title-clean: AWS Essentials for Data Science<div class="a2">2. Storage</div>
author: matt_sosna
---

Unless you've avoided [iCloud](https://www.apple.com/icloud/), [Dropbox](https://www.dropbox.com/), and [Google Drive](https://www.google.com/drive/) the last fifteen years $-$ and if you have, props to you! $-$ then you're likely familiar with cloud storage. You can recover your texts if you lose your phone; you can share files with links instead of massive email attachments; you can organize and search your photos by who's in them.

But these benefits extend into the professional realm, too. If you ever have data or code that you want to share with others $-$ like an [AI-powered cat picture generator](https://affinelayer.com/pixsrv/) or the [daily number of occupied hotel rooms in Brussels](https://datastore.brussels/web/data/dataset/f03544a1-a01c-4374-b19d-e93697f1ac73)$-$ you'll want to store this data on a cloud server. Cloud servers don't turn off when you close your laptop, and you don't have to worry if some of those queries are fetching your private data when they visit your laptop.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/edges2cats.png">
<span style="font-size: 12px"><i>Screenshot from Christopher Hesse's amazing [Image-to-Image Demo](https://affinelayer.com/pixsrv/)</i></span>


So how can we set up cloud storage? And how can we leverage [SDKs](https://www.ibm.com/cloud/blog/sdk-vs-api) to integrate our cloud storage into our code?

In the [last post]({{  site.baseurl  }}/AWS-Intro), we introduced cloud computing as an industry, as well as Amazon Web Services (AWS). In this post, we'll cover **storage**, one of the two main offerings of the cloud. (The other being compute, which we'll cover in the next post.) We'll set up our software environment before showing how to efficiently store [blobs](https://en.wikipedia.org/wiki/Binary_large_object), tabular data, and JSONs.

## Table of contents
* [Background](#background)
  * [Why cloud storage?](#why-cloud-storage)
  * [Storing AWS credentials](#storing-aws-credentials)
  * [Types of data](#types-of-data)
* [S3 (Simple Storage Service)](#s3-simple-storage-service)
* [RDS (Relational Database Service)](#rds)
* [DynamoDB](#dynamodb)

## Background
### Why cloud storage?
When you're working by yourself on a relatively small project, you probably don't think too hard about data access and storage. Maybe the CSVs are in the same folder as your Jupyter Notebook or R scripts, or if you're fancy they're backed up to a hard drive.

But what happens when you want to share that data with someone, or have multiple people access it at the same time? It doesn't make sense to keep the data on your laptop and then take turns using your data. Maybe you decide to copy the data to each person's laptop. But if the files are large, this can take a while. And what if someone unknowingly modifies their copy of the data, meaning their analyses don't sync up with yours? Without a single source of truth, it can be really hard to debug the issue. And finally, what happens if someone leaves the project? They can just take their copy of the data with them, sharing it with competitors or malicious actors.

Cloud storage is meant to address these issues. You're likely already familiar with Dropbox or Google Drive $-$ these services have become ubiquitous because it's now unthinkable to try sending data through an email or handing it over on a USB stick. Upload a file to Dropbox, send your friend a link to the file, and you're done.

But cloud storage can go beyond this $-$ AWS and others provide [SDKs](https://www.ibm.com/cloud/blog/sdk-vs-api), or **software development kits** that allow you to interact with the cloud through code. So instead of needing to click and drag a file from Google Drive onto your Desktop, then load it into Python, you can pull it straight into Python with the `boto3` library.

In this post we'll show you how to leverage S3, RDS, and DynamoDB.

AWS guarantees ["five nines"](https://aws.amazon.com/blogs/publicsector/achieving-five-nines-cloud-justice-public-safety/), or 99.999% availability for justice and public safety customers, for example. (That means AWS guarantees it will be unavailable less than five minutes and 15 seconds per year.)

### Storing AWS credentials
Before we get started, we need to store our credentials in a secure location. What you _shouldn't_ do is store your AWS credentials in the code that you're running $-$ _especially_ if that code is version controlled with a service like Git! Accidentally pushing that code will create a version that will last forever.

{% include header-python.html %}
```python
# DON'T do this
access_key = 'abc123'
secret_key = 'xyz456'

# the rest of your code
```

This is a huge security vulnerabilty, as **anyone with these values can make calls to your AWS services as if they were you.** Rather, we should store these in a local file that we _don't_ version control.

For MacOS and Linux users, we can store these secrets in a `.bash_profile.rc` file. ([See here](https://saralgyaan.com/posts/set-passwords-and-secret-keys-in-environment-variables-maclinuxwindows-python-quicktip/) for Windows.) In this file, we can set our variables. (Note the lack of spaces around the equals signs.)

{% include header-bash.html %}
```bash
export AWS_ACCESS_KEY_ID=abc123
export AWS_SECRET_ACCESS_KEY=xyz456
```

Once we do this, we can access our variables through Python's `os` module.

{% include header-python.html %}
```python
import os

access_key = os.environ['AWS_ACCESS_KEY_ID']
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
```

### Types of data
So we see that it's useful to store data in the cloud so it's easily accessible to the right people, hard to access for everyone else, resilient and robust, etc.

But "data" is a broad term $-$ is it raw videos or text transcripts? Is it a user profile? Is it code? Is it tabular data? The _structure_ of the data (unstructured, semi-structured, and structured) will determine what the right storage solution is.

The amount of data we have can grow very quickly, and we want to be able to access it quickly.

But there are certain files that are hard to neatly store in a database. **Binary large objects**, or **[BLOB](https://en.wikipedia.org/wiki/Binary_large_object)s** for short, are large collections of binary data that can't be easily broken up, or shouldn't. Think of an image $-$ you don't really want half the pixels in one file and half in another, when you'll always be fetching the entire image any time you want to access it. Similarly, audio, video, or [executable programs](https://en.wikipedia.org/wiki/Executable) are large entities that you almost always to fetch all at once.

## S3: Simple Storage Service
<img src="{{ site.baseurl }}/images/data_engineering/aws/storage/s3_landing.png">

S3 is **Simple Storage Service.** Think of it like Dropbox or Google Drive, a "catch-all" place for files in the cloud. Upload your text files, CSVs, R scripts, Python pickle files, images, videos, zipped programs, etc. by clicking and dragging in the UI or using the AWS CLI.

It's hard to beat the ease of using S3. Simply create a **bucket** (like a distinct directory) and start uploading files. We can organize data into folders <sup>[[1]](#1-s3)</sup> and easily load in the data from a script.

The downside to this simplicity is that S3 only contains data _about_ the files, not what's inside them. So you're out of luck if you forget your Facebook password and can't search your text files for the phrase `my Facebook password is`. If we need to search the data _within_ our files, we're better off storing that data in a database.<sup>[[2]](#2-s3)</sup>. But even with a database, S3 is still ideal for storing the _raw data_ that generated those data, such as the logs, raw sensor data for your IoT application, text files from user interviews, etc., as a backup.

### Using S3
So let's actually create a bucket. We can do this from the console like this:

<img src="{{ site.baseurl }}/images/data_engineering/aws/storage/create_bucket.png">

**ACL:** Access Control List

{% include header-bash.html %}
```bash
aws s3 mb s3://my-bucket
```

We can list files like this:

{% include header-bash.html %}
```bash
$ aws s3 ls
# s3://my-bucket
# s3://my-other-bucket

aws s3 ls s3://my-bucket
# folder1/file.py
# folder2/file2.py

aws s3 ls s3://my-bucket/folder1/
# file.py
```


### Pulling data
(I wonder if we can get this in fewer lines.)

{% include header-python.html %}
```python
import os
import json
import boto3
import pandas as pd
from io import StringIO

# Get credentials
access_key = os.environ['AWS_ACCESS_KEY_ID'],
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']

# Establish a connection
client = boto3.client(aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      region_name='us-east-1')

# Get the file
obj = client.get_object(Bucket="my_company", Key='datasets/data.json')

# Convert the file to a dataframe
body = obj['Body'].read()
string = body.decode(encoding='utf-8')
df = pd.DataFrame(json.load(StringIO(string)))
```



## RDS
RDS is Relational Database Service. This is like a SQL database hosted in the cloud (on top of an EC2 instance). For NoSQL, you're looking at DynamoDB.

## Redshift
Data warehouse. A data warehouse is a https://www.talend.com/resources/what-is-data-warehouse/.


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


## Footnotes
#### 1. [S3: Simple Storage Service](#s3-simple-storage-service)
"Folders" in S3 don't _really_ exist. They're more like human-friendly ways to organize your data.

#### 2. [S3: Simple Storage Service](#s3-simple-storage-service)
There _are_ services like Glue that let you index your buckets and search them as if they were a database with Athena, but there are some serious caveats to this, and you're still far better off writing to a database in my experience!
