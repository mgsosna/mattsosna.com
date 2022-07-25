---
layout: post
title: AWS Essentials for Data Science - 2. Storage
title-clean: AWS Essentials for Data Science<div class="a2">2. Storage</div>
author: matt_sosna
---

Do you have a store your music, videos, and personal files in a garage full of hard drives? My bet is... no. Unless you've avoided [iCloud](https://www.apple.com/icloud/), [Dropbox](https://www.dropbox.com/), and [Google Drive](https://www.google.com/drive/) the last fifteen years $-$ and if you have, props to you! $-$ then you're likely using storage. You can recover your texts if you lose your phone; you can share files with links instead of massive email attachments; you can organize and search your photos by who's in them.

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

But what happens when you want to add someone to your project? It doesn't make sense to take turns using your laptop. You could copy the data to their laptop, but what if there's more data than can fit on your teammate's computer? Once the work starts, syncing changes across datasets is a headache waiting to happen. It's also a lot of trust to hand over all the data right away $-$ what if this new person leaves, taking everything with them to share with competitors or malicious actors?

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/single_source.png" alt="Sharing data in the cloud">

Cloud storage is designed to address these issues. As with Dropbox or Google Drive, you can simply send data through a link: "click _here_ to access the database." This data can be made read-only, with fine-tuned access rules $-$ if your teammate turns out to be a spy from the competition, you can instantly turn those URLs into error messages the next time they try to fetch the data.<sup>[[1]](#1-why-cloud-storage)</sup>

We can use [**SDKs** (software development kits)](https://www.ibm.com/cloud/blog/sdk-vs-api) to access the data straight from our code, which is critical for scaling any application beyond a tiny handful of users. And as long as your internet connection is reliable, you should be able to access the data at any time $-$ AWS, for example, guarantees an uptime of [99.9%](https://aws.amazon.com/s3/sla/), [99.99%](https://aws.amazon.com/dynamodb/sla/), or [99.999%](https://aws.amazon.com/blogs/publicsector/achieving-five-nines-cloud-justice-public-safety/) depending on your application.<sup>[[2]](#2-why-cloud-storage)</sup>

### What am I storing?
So we see that it's useful to store data in the cloud so it's secure, accessible by code, and highly-available. But "data" is a broad term $-$ is it raw videos and text transcripts? A user profile and activity logs? Python and R scripts? Grainy screenshots of Excel?

We _could_ throw all our files into a big Dropbox folder, with photos mixing with config files and CSVs. As long as you know the name of the file containing the data you want, Dropbox will fetch the file when requested. But unless the file contains strictly the data you requested, you'll need to then search through the file to extract the relevant data.

This issue $-$ not knowing exactly where a piece of data is $-$ is where a big Dropbox folder fails us as the amount of data grows. Because we often need to _search_ for data that matches some criteria, **_the way we organize our data_ determines whether our applications can support 100 users or 100 million.** And as we'll see, the optimal way to access a particular type of data will strongly depend on how it's _formatted_.

This format, i.e., _structured_, _semi-structured_, or _unstructured_, refers to how the data is organized within the file. **Structured** data is the tabular set of rows and columns you're likely familiar with: typically, each row is a sample and each column is a [feature](https://www.datarobot.com/wiki/feature/) of that sample. The tables in a relational database consist of structured data, which we can quickly search if the tables are [_indexed_](https://www.codecademy.com/article/sql-indexes) by a column that partitions the data well.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/storage_types.png">

**Semi-structured** data includes [JSON](https://www.w3schools.com/js/js_json_intro.asp), [XML](https://www.w3.org/standards/xml/core), [HTML](https://en.wikipedia.org/wiki/HTML), and large graphs, where the data usually doesn't fit nicely into columns and rows. This format is ideal for hierarchical data, where a field may have subfields, many containing subfields of their own. **There is no limit on the number of layers, but there _is_ a required structure.** An HTML page, for example, can have many `<div>` sections nested within one another, each with unique CSS formatting.

Finally, **unstructured** data is raw and unformatted, impossible to split into the rows and columns of structured data, or even the nested fields of semi-structured data, without further processing. One example of unstructured data that can't $-$ or shouldn't $-$ be broken up is **binary large objects** (**[BLOB](https://en.wikipedia.org/wiki/Binary_large_object)s**). You usually want to load an entire image at once, for example, so you shouldn't store half the pixels in one file and half in another. Similarly, [executable programs](https://en.wikipedia.org/wiki/Executable) (e.g., compiled C++ scripts) are entities that you'll always want to fetch all at once.

### Avoiding getting hacked when using an SDK
Now that we have an idea on the types of data we can store in the cloud, we can start experimenting with AWS services optimized for each type. To really show the strength of the cloud, we'll use the AWS Python SDK to integrate these services into our code. To use the Python SDK, we simply install the `boto3` library. In Terminal or Command Prompt, we can simply type the following:

{% include header-bash.html %}
```bash
pip install boto3
```

But before we run any scripts, there's one thing we need to do to avoid getting obliterated by a hacker. **It is crucial that we store our AWS credentials in a secure location in our code.**

AWS servers receive dozens or hundreds of queries per second. If a server receives a request to download a file from your S3 bucket, how does the server know whether to block or allow the action? To ensure this request is coming from you $-$ or a machine acting on your behalf $-$ **we [_sign_ our API requests](https://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html) with our AWS access key ID and secret access key.** These keys are used to [encrypt our message content](https://www.okta.com/identity-101/hmac/) and [generate a hash](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) to prove the message AWS receives is the same one we sent.

So in essence, any requests AWS receives that were signed with your access keys will be treated like they came from you. So it's important to ensure that you're the only one performing these requests!

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/access_keys.png">

`boto3` requires us to pass in our access key ID and secret access key when we instantiate a client object. We can technically do this by defining our access keys as variables and then passing them in, like this:

{% include header-python.html %}
```python
import boto3

# DON'T DO THIS!!
access_key = 'abc123'
secret_key = 'xyz456'

client = boto3.client(access_key, secret_key, region_name='us-east-1')
```

But this is a huge security vulnerability, as **anyone who reads this code can impersonate you!** And if you accidentally push this file to a version control system like Git, removing lines 4-5 and pushing a new version won't be enough $-$ anyone can scroll through the history of the file to find your keys.

Rather than hard-coding the values in Python, MacOS and Linux users can store these [**secrets**](https://secrethub.io/blog/what-is-secrets-management/) in a `.bash_profile.rc` file. ([See here](https://saralgyaan.com/posts/set-passwords-and-secret-keys-in-environment-variables-maclinuxwindows-python-quicktip/) for Windows.) This file contains aliases for filepaths (so Terminal knows you mean `/opt/homebrew/bin/python` when you type `python`, for example), as well as database passwords or other sensitive information. This file is located in your root directory and is hidden $-$ to find it, you need to type `⌘` + `.` to see it.

In this file, we can set our AWS access keys. (Note the lack of spaces around the equals signs.)

{% include header-bash.html %}
```bash
export AWS_ACCESS_KEY_ID=abc123
export AWS_SECRET_ACCESS_KEY=xyz456
```

Once we do this, we can access our variables through Python's `os` module. By accessing the values from `os.environ`, they're never visible to anyone reading the code.<sup>[[3]](#3-avoiding-getting-hacked-when-using-an-sdk)</sup>

{% include header-python.html %}
```python
import os

access_key = os.environ['AWS_ACCESS_KEY_ID']
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
```

With that, we're now ready to start using AWS.

<img src="{{ site.baseurl }}/images/data_engineering/aws/storage/s3_landing.png">

## S3: Simple Storage Service
**S3**, or **Simple Storage Service**, is the closest analogue to Dropbox or Google Drive. Think of S3 as a "catch-all" for your files. Simply create a **bucket** (i.e., distinct directory) and upload [_any_ number of files of _any_ type](https://docs.amazonaws.cn/en_us/AmazonS3/latest/userguide/upload-objects.html) $-$ text, CSVs, executables, Python pickle files, images, videos, zipped folders, etc. Define the access rules at the file, folder,<sup>[[4]](#4-s3-simple-storage-service)</sup> or bucket level with just a few clicks.

The downside to this simplicity is that S3 only contains data _about_ the files, not what's inside them. So you're out of luck if you forget your Facebook password and can't search your text files for the phrase `my Facebook password is`. If we need to search the data _within_ our files, we're better off storing that data in a database.<sup>[[5]](#5-s3-simple-storage-service)</sup>

But even with a database, S3 is still ideal for storing the _raw data_ that generated those data. S3 can serve as a backup for logs, raw sensor data for your IoT application, text files from user interviews, and more. And some file types, such as images or trained machine learning models, are best kept in S3, with the database simply storing the path to the object.

### Using S3
So let's actually create a bucket. Don't worry about getting charged by AWS for storing data $-$ we'll stay well within the boundaries of the [Free Tier](https://aws.amazon.com/free/) and delete everything once we're done. We'll create a bucket, then upload and download files. We'll use the console, AWS CLI, and Python SDK to perform each of these steps, though note that we can do all steps from any one of the tools.

#### Create a bucket
Let's start with the console to create a bucket. We first [log into our AWS account](https://aws.amazon.com) (preferably with an [IAM role]({{  site.baseurl  }}/AWS-Intro/#iam-identity-and-access-management)) and navigate to S3. Then we just click the "Create bucket" button:

<img src="{{ site.baseurl }}/images/data_engineering/aws/storage/create_bucket.png">

When we create a bucket, we need to give it a name that's globally distinct across all AWS buckets. Here we create one called `matt-sosnas-test-bucket`.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/name_bucket.png">

Our bucket can have customized access rules, but let's just keep it at disabled public access for now. Once we select that, our bucket is ready.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/bucket_created.png">

#### Upload files
Let's now switch to the AWS CLI. In Terminal or Command Prompt, we can see our new bucket with the following command. (You may need to authenticate following the steps [here]({{  site.baseurl }}/AWS-Intro/#cli-command-line-interface)).

{% include header-bash.html %}
```bash
aws s3 ls
# 2022-07-04 22:42:25 matt-sosnas-test-bucket
```

We can now create a file and upload it to our bucket. To keep things simple, we'll just create a file straight from the command line by piping a string into a file with `echo` and `>`. We'll then upload the file with `aws s3 cp <source> <destination>`.

{% include header-bash.html %}
```bash
# Create file
echo 'Hello there, this is a test file!' > test.txt

# Verify contents
cat test.txt
# Hello there, this is a test file!

# Upload to S3
aws s3 cp test.txt s3://matt-sosnas-test-bucket/test.txt
# upload: .\test.txt to s3://matt-sosnas-test-bucket/test.txt
```

We can now view our file with `aws s3 ls <bucket_name>`.

{% include header-bash.html %}
```bash
aws s3 ls s3://matt-sosnas-test-bucket
# 2022-07-18 00:31:54   27 test.txt
```

If the S3 file path contains a folder, AWS will automatically create a folder for us. Let's create a Python file this time, `test.py`, and upload it into a `python/` directory in our bucket. Because `s3://matt-sosnas-test-bucket/python/test.py` contains a `python/` directory, S3 will create one for us.

{% include header-bash.html %}
```bash
echo 'print("This is a different test file")' > test.py

aws s3 cp test.py s3://matt-sosnas-test-bucket/python/test.py
# upload: .\test.py to s3://matt-sosnas-test-bucket/python/test.py
```

Now when we view the contents with `aws s3 ls`, we see the `python/` folder next to `test.txt` in the root directory. If we add `/python/` to the end of our bucket name in the command, we then see the contents of the folder.

{% include header-bash.html %}
```bash
aws s3 ls s3://matt-sosnas-test-bucket
#                      PRE python/
# 2022-07-18 00:31:54   27 test.txt

aws s3 ls s3://matt-sosnas-test-bucket/python/
# 2022-07-18 00:42:39   39 test.py
```

Finally, we can upload multiple files by specifying the `--recursive`, `--exclude`, and `--include` flags. Below, we create two CSVs, `file1.csv` and `file2.csv`, first creating the header and then appending two rows each. We then use the AWS CLI to upload all files in our current directory (`.`) that match the `file*` pattern into the `csv/` folder in our bucket. Finally, we list the contents of the `csv/` folder.

{% include header-bash.html %}
```bash
# Create file1.csv
echo "name,age" > file1.csv
echo "abe,31" >> file1.csv
echo "bea,5" >> file1.csv

# Create file2.csv
echo "name,age" > file2.csv
echo "cory,50" >> file2.csv
echo "dana,100" >> file2.csv

aws s3 cp . s3://matt-sosnas-test-bucket/csv/ --recursive --exclude "*" --include "file*"
# upload: .\file1.csv to s3://matt-sosnas-test-bucket/csv/file1.csv
# upload: .\file2.csv to s3://matt-sosnas-test-bucket/csv/file2.csv

aws s3 ls matts-sosnas-test-bucket/csv/
# 2022-07-19 01:05:22    23 file1.csv
# 2022-07-19 01:05:22    25 file2.csv
```

#### Download files
Uploading files is great, but at some point we'll want to download them. Let's use our third tool, the Python SDK `boto3`, to demonstrate downloading files. This step is more involved than the one-line AWS CLI commands, but we'll go through it line by line below.

{% include header-python.html %}
```python
import boto3
from io import StringIO
import os
import pandas as pd

# Establish a connection
client = boto3.client(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name='us-east-1',
    service_name='s3'
)

# Get the file
obj = client.get_object(
    Bucket="matt-sosnas-test-bucket",
    Key='csvs/file1.csv'
)

# Convert the file to a dataframe
body = obj['Body'].read()
string = StringIO(body.decode('utf-8'))
df = pd.read_csv(string)
#    name  age
# 0  abe    31
# 1  bea     5
```

We first import `boto3`, `io.StringIO`, `os`, and `pandas`. `boto3` contains code for interacting with AWS, `io` is a library for working with [stream data](https://en.wikipedia.org/wiki/Stream_(computing)), `os.environ` stores our AWS credentials, and `pandas` will convert our CSV to a dataframe.

On lines 7-12 we instantiate a `boto3` client that allows us to make requests to AWS. We perform such a request to get the `csvs/file1.csv` file from `matt-sosnas-test-bucket` on lines 15-18. This object is packed with metadata, so we extract the byte string on line 21, decode it to a CSV string on line 22, and finally parse the string to a dataframe on line 23.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/rds.png">

## RDS: Relational Database Service
Throwing all our data into a bucket, even with file types arranged by folder, only gets us so far. As our data grows, we need a more scalable way to find, join, filter, and perform calculations on our data. A **relational database** is one way to store and organize our data more optimally. (See [this post]({{  site.baseurl  }}/SQL_vs_NoSQL) for a primer on databases.)

We _could_ rent an EC2 instance (i.e., virtual server) in the cloud and install a MySQL or PostgreSQL database ourselves. But this is [barely better than hosting a database on a server in our garage](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html) $-$ while AWS would handle server maintenance, we would still be responsible for scaling, availability, backups, and software and operating system updates. For slightly added cost, we can use a service like [**Amazon RDS**](https://aws.amazon.com/rds/) to have AWS manage everything except our actual data.

So let's create a database in RDS. We'll sign into the AWS console, navigate to RDS, and click `Create database`. Let's create a MySQL database with the `Standard create` option.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/mysql_configure_1.png">

Make sure to specify that you want to use the Free Tier!

<img src="{{  site.baseurl  }}/images/data_engineering/aws/storage/mysql_configure_2.png">

While we'll tear down our database at the end of this post, we can also uncheck "Enable storage autoscaling" under the "Storage" header. Finally, we'll want to make our database public for our demo. It won't be truly open to the world, don't worry $-$ we'll specify that only our IP address is allowed to access the database. (For a professional application, though, you'll want to [configure a VPC](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html).)

Everything else in the configuration can stay the same. When we hit `Create database`, we're taken back to the RDS landing page. We'll see that our database is being created $-$ this step can take a while, up to 20 minutes.

Once the database is created, we can connect to it from any MySQL client, such as the command line or [MySQL Workbench])(https://www.mysql.com/products/workbench/).



We start by [defining a DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SettingUp.html#CHAP_SettingUp.Requirements), which will provide an address called an _endpoint_ for us to access our database.
* Need to set up security group rules. Default AWS VPC likely fine.
* Configure IAM policy to allow access to RDS

DB instance = isolated database environment. Can host multiple databases. A DB engine = the specific relational database software, e.g., MySQL, PostgreSQL, Oracle, etc.





## DynamoDB
DynamoDB is for non-relational databases.



[This website](https://aws-certified-cloud-practitioner.fandom.com/wiki/3.3_Identify_the_core_AWS_services) looks super helpful.
[This whitepaper](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/aws-overview.pdf) looks awesome.

## Cleaning up
Let's delete our stuff to avoid incurring charges.

## Other services
### Cloudwatch
Logs.

### Glue, Athena
These combine with S3 to let you treat a bucket (or directory within one) as a big table that you can query with SQL.

There are services that build off these.

[AWS infrastructure explained](https://aws.plainenglish.io/aws-infrastructure-explained-b0f4fb7b6829)

### Redshift
Data warehouse. A data warehouse is a https://www.talend.com/resources/what-is-data-warehouse/.

## Conclusions
This post walked us through three AWS services for storing data in the cloud: S3, RDS, and DynamoDB.

## Footnotes
#### 1. [Why cloud storage?](#why-cloud-storage)
While we can revoke a user's access to cloud data, there's of course always the concern that the user made a local copy. There's no real good answer to this $-$ we can't make that downloaded data self-destruct once the person leaves your team. For files from S3, there's likely little hope, but at least for data from databases, it's impractical or impossible to download everything. At companies like Meta, data access is carefully monitored, from access to tables with sensitive data to any time data is downloaded.

#### 2. [Why cloud storage?](#why-cloud-storage)
99.999% uptime is a hard number to wrap your head around. Per year, ["five 9s"](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/s-99.999-or-higher-scenario-with-a-recovery-time-under-1-minute.html) means AWS guarantees it will be unavailable less than 5 minutes and 15 seconds.

#### 3. [Avoiding getting hacked when using an SDK](#avoiding-getting-hacked-when-using-an-sdk)
We can use a similar process for data that isn't as sensitive, such as constants or filepaths.

{% include header-python.html %}
```python
# config.py
SAMPLE_SIZE = 100
EXEMPTED_USER_IDS = [123, 456]
```

By storing the values in a config file, we can keep our main workflow clean:

{% include header-python.html %}
```python
# sampler.py
import .config as config

class Sampler:
    def __init__(self):
        self.sample_size = config.SAMPLE_SIZE
        self.exempted_user_ids = config.EXEMPTED_USER_IDS
    ...
```

If config.py stores data we don't want others to see, we can add it to our `.gitignore` file and Git won't try to version control it. Below, Git won't track files with `.ipynb`, `.pyc`, or `config.py` in their name.

```
.ipynb
.pyc
config.py
```

#### 4. [S3: Simple Storage Service](#s3-simple-storage-service)
A pedantic note: "folders" in S3 [don't _really_ exist](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html). They're more like human-friendly ways to organize your data.

#### 5. [S3: Simple Storage Service](#s3-simple-storage-service)
You _can_ treat an S3 bucket like a database by storing CSVs or JSONs in a standardized format, indexing the bucket with [AWS Glue](https://aws.amazon.com/glue/) and then querying the indexes with [AWS Athena](https://aws.amazon.com/athena/). But there are some serious caveats to this $-$ at a former job, I accidentally uploaded a CSV in the wrong format and made the entire bucket impossible to search. With hundreds of files, I had no idea where the error was. In my opinion, you're better off using a database with strict write rules that will immediately flag (and block) data in the wrong format.
