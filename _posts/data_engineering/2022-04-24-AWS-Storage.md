---
layout: post
title: AWS Essentials for Data Science - 2. Storage
title-clean: AWS Essentials for Data Science<div class="a2">2. Storage</div>
author: matt_sosna
---

Unless you've avoided [iCloud](https://www.apple.com/icloud/), [Dropbox](https://www.dropbox.com/), and [Google Drive](https://www.google.com/drive/) the last fifteen years $-$ and if you have, props to you! $-$ then you're likely familiar with cloud storage. You can recover your texts if you lose your phone; you can share files with links instead of massive email attachments; you can organize and search your photos by who's in them.

But these benefits extend into the professional realm, too. If you ever start a company that shares data $-$ like, say, thousands of 4K movies and shows for a low monthly fee (😛) $-$ you'll want to store this data on a cloud server. Cloud servers don't turn off when you close your laptop, and you don't have to worry about nefarious users fetching your private data when they visit your laptop.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/hulu.jpeg">
<span style="font-size: 12px"><i>Photo by [Tech Daily](https://unsplash.com/@techdailyca) on [Unsplash](https://unsplash.com)</i></span>

So how can we set up cloud storage? What's the right type of storage for our data? And how can we interact with cloud storage directly from code, rather than needing to click around in a UI?

This post will answer these questions. We'll set up our software environment before showing how to efficiently store [blobs](https://en.wikipedia.org/wiki/Binary_large_object), tabular data, and JSONs in **Amazon Web Services (AWS)**. (For an intro to the cloud industry in general, check out the [last post]({{  site.baseurl  }}/AWS-Intro).) Stay tuned for a follow-up post on _compute_, the other major offering of the cloud.

## Table of contents
* [Background](#background)
  * [Why cloud storage?](#why-cloud-storage)
  * [What am I storing?](#what-am-i-storing)
  * [Avoiding getting hacked when using an SDK](#avoiding-getting-hacked-when-using-an-sdk)
* [S3 (Simple Storage Service)](#s3-simple-storage-service)
* [RDS (Relational Database Service)](#rds)
* [DynamoDB](#dynamodb)

## Background
### Why cloud storage?
When you work alone on a small project, you probably don't think too hard about data storage. Maybe you have a few CSVs in the same folder as your Jupyter Notebook or R scripts. Hopefully everything's backed up to a hard drive.

But what happens when you want to add someone to your project? It doesn't make sense to take turns using your laptop. You could copy the data to their laptop, but what if there's more data than can fit on your teammate's computer? It's also a lot of trust to hand over all the data right away $-$ what if this new person leaves, taking everything with them to share with competitors or malicious actors?

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/single_source.png" alt="Sharing data in the cloud">

Cloud storage is designed to address these issues. As with Dropbox or Google Drive, you can simply send data through a link: "click _here_ to access the database." This data can be made read-only, with fine-tuned access rules $-$ if your teammate turns out to be a spy from the competition, you can instantly turn those links you shared into error messages the next time they try to fetch the data.<sup>[[1]](#1-why-cloud-storage)</sup>

We can use [**SDKs** (software development kits)](https://www.ibm.com/cloud/blog/sdk-vs-api) to access the data straight from our code, which is critical for scaling any application beyond a tiny handful of users.

And as long as your internet connection is reliable, you should be able to access the data at any time $-$ AWS, for example, guarantees an uptime of [99.9%](https://aws.amazon.com/s3/sla/), [99.99%](https://aws.amazon.com/dynamodb/sla/), or [99.999%](https://aws.amazon.com/blogs/publicsector/achieving-five-nines-cloud-justice-public-safety/) depending on your application. (For justice and public safety customers, for example, AWS guarantees it will be unavailable fewer than 315 seconds per year.)

### What am I storing?
So we see that it's useful to store data in the cloud so it's secure, accessible by code, and highly-available. But "data" is a broad term $-$ is it raw videos and text transcripts? Is it a user profile and activity logs? Is it Python and R scripts? Is it all screenshots of Excel?

We _could_ throw all our files into a big Dropbox folder, with photos mixing with config files and CSVs. As long as you know the name of the file containing the data you want, Dropbox will fetch the file when requested. This works ok $-$ unless the file contains only the data you want, you'll need to then search through the file to extract the relevant data. But the real issue is when you _don't_ know exactly what you're looking for.

Because we often need to _search_ for data that matches some criteria, **_the way we organize our data_ will determine whether our applications can support 100 users or 100 million as our data grows.** And as we'll see, the optimal way to access a particular type of data will strongly depend on how it's _formatted_.

This format, i.e., _structured_, _semi-structured_, or _unstructured_, refers to how the data is organized within the file. **Structured** data is the tabular set of rows and columns you're likely familiar with: typically, each row is a sample and each column is a [feature](https://www.datarobot.com/wiki/feature/) of that sample. The tables in a relational database consist of structured data, which we can quickly search if the tables are [_indexed_](https://www.codecademy.com/article/sql-indexes) by a column that partitions the data well.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/storage_types.png">

**Semi-structured** data includes [JSON](https://www.w3schools.com/js/js_json_intro.asp), [XML](https://www.w3.org/standards/xml/core), [HTML](https://en.wikipedia.org/wiki/HTML), and large graphs, where the data usually doesn't fit nicely into columns and rows. This format is ideal for hierarchical data, where a field may have subfields, many containing subfields of their own. **There is no limit on the number of layers, but there _is_ a required structure.** An HTML page, for example, can have many `<div>` sections nested within one another, each with unique CSS formatting.

Finally, **unstructured** data is raw and unformatted, impossible to split into the rows and columns of structured data, or even the nested fields of semi-structured data, without further processing. One example of unstructured data is **binary large objects**, or **[BLOB](https://en.wikipedia.org/wiki/Binary_large_object)s**. BLOBs are large chunks of data that can't be easily broken up, or shouldn't. You usually want to load an entire image at once, for example, so you shouldn't store half the pixels in one file and half in another. Similarly, [executable programs](https://en.wikipedia.org/wiki/Executable) (i.e., compiled code) are large entities that you'll always want to fetch all at once.

### Avoiding getting hacked when using an SDK
Now that we have an idea on the types of data we can store in the cloud, we can start experimenting with AWS services optimized for each type. To really show the strength of the cloud, we'll use the AWS Python SDK to integrate these services into our code.

But before we run any scripts, there's one crucial thing we need to do to avoid getting obliterated by a hacker. **It is crucial that we store our AWS credentials in a secure location in our code.**

Any interaction with an AWS server requires _authentication_. If a server receives a request to download a file from your S3 bucket, how does the server know whether to allow or block the action? The server can't send back a verification message like "Please type the name of the account owner" $-$ the whole point of calling AWS through code is that we're making requests through a computer acting _on behalf_ of us.

To ensure the action is allowed, the server will compare a _fingerprint_ from the requester against the fingerprint




When we interact with AWS, we need to identify ourselves to Amazon's servers, showing that we're allowed to perform the actions we're requesting. We do this with our access key and secret access key. In the last post, we set these variables in the Terminal when using the AWS CLI. In Python, we'll need to do something slightly different.


What you _shouldn't_ do is store your AWS credentials in the code that you're running $-$ _especially_ if that code is version controlled with a service like Git! Accidentally pushing that code will create a version that will last forever.

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


## S3: Simple Storage Service
<img src="{{ site.baseurl }}/images/data_engineering/aws/storage/s3_landing.png">

S3 is **Simple Storage Service.** Think of it like Dropbox or Google Drive, a "catch-all" place for files in the cloud. Upload your text files, CSVs, R scripts, Python pickle files, images, videos, zipped programs, etc. by clicking and dragging in the UI or using the AWS CLI.

It's hard to beat the ease of using S3. Simply create a **bucket** (i.e., distinct directory) and start uploading files. We can organize data into folders <sup>[[1]](#1-s3)</sup> and easily load in the data from a script.

The downside to this simplicity is that S3 only contains data _about_ the files, not what's inside them. So you're out of luck if you forget your Facebook password and can't search your text files for the phrase `my Facebook password is`. If we need to search the data _within_ our files, we're better off storing that data in a database.<sup>[[2]](#2-s3)</sup>. But even with a database, S3 is still ideal for storing the _raw data_ that generated those data, such as the logs, raw sensor data for your IoT application, text files from user interviews, etc., as a backup.

### Using S3
So let's actually create a bucket. We can do this from the console like this:

<img src="{{ site.baseurl }}/images/data_engineering/aws/storage/create_bucket.png">

When we create a bucket, we need to give it a name. This needs to globally distinct across all AWS buckets.


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


## RDS: Relational Database Service
RDS is Relational Database Service. This is like a SQL database hosted in the cloud (on top of an EC2 instance). For NoSQL, you're looking at DynamoDB.

## DynamoDB
DynamoDB is for non-relational databases.

## Redshift
Data warehouse. A data warehouse is a https://www.talend.com/resources/what-is-data-warehouse/.


[This website](https://aws-certified-cloud-practitioner.fandom.com/wiki/3.3_Identify_the_core_AWS_services) looks super helpful.
[This whitepaper](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/aws-overview.pdf) looks awesome.


## Other services
### Cloudwatch
Logs.

### Glue, Athena
These combine with S3 to let you treat a bucket (or directory within one) as a big table that you can query with SQL.

There are services that build off these.

[AWS infrastructure explained](https://aws.plainenglish.io/aws-infrastructure-explained-b0f4fb7b6829)


## Footnotes
#### 1. [Why cloud storage?](#why-cloud-storage)
While we can revoke a user's access to cloud data, there's of course always the concern that the user made a local copy. There's no real good answer to this $-$ we can't make that downloaded data self-destruct once the person leaves your team. For files from S3, there's likely little hope, but at least for data from databases, it's impractical or impossible to download everything. At companies like Meta, data access is carefully monitored, from access to tables with sensitive data to any time data is downloaded.

#### 2. [S3: Simple Storage Service](#s3-simple-storage-service)
"Folders" in S3 don't _really_ exist. They're more like human-friendly ways to organize your data.

#### 3. [S3: Simple Storage Service](#s3-simple-storage-service)
There _are_ services like Glue that let you index your buckets and search them as if they were a database with Athena, but there are some serious caveats to this, and you're still far better off writing to a database in my experience!
