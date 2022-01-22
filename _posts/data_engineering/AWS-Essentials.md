---
layout: post
title: AWS Essentials for Data Science
author: matt_sosna
---

Data science requires computers. The stronger your computer, the more computations you can run per second, the larger the datasets you can manipulate at once, and the more data you can store on your machine. This is the case for any programming work (e.g. even just having an app).

But the laptop or desktop you're using right now probably isn't optimized for running calculations all day $-$ it's optimized for providing a good consumer experience. Some resources are dedicated to the graphical interface displayed on your monitor; malware detection is running in the background; weather and news apps are pinging external APIs every few minutes to stay up-to-date.

Cloud computing is an important aspect of data science work. Basically, don't be limited by the power of your computer; use powerful servers in the cloud. These servers can store your data, process things, etc.

Scalable. You're an online retailer getting ready for Black Friday. Your website is going to get a lot more traffic... so much so that the server will have trouble fulfilling HTTP requests (such as sending the HTML for the homepage when a user lands on the site, or updating the database with the availability of each item as orders are placed). It's normally pretty fast, but as the number of users increases on your site, there'll start to be a backlog of requests, causing the website to be slow. Similarly, it can take a while for an item to be marked as out of stock... hopefully before another person adds it to their cart and orders it too!

https://queue-it.com/blog/how-high-online-traffic-can-crash-your-website/



You'd normally have to buy a bunch of servers to handle the surge in traffic your website will get.


Cloud services as an industry


AWS is market leader, so we'll focus on them. But all of these services are available from the other major players in the cloud market, Google Cloud Platform and Microsoft Azure. This post will therefore cover more of the concepts than stuff specific to AWS.



### Table of contents
* [**Storage**](#storage)
  - [S3 (Simple Storage Service)](#s3)
  - [RDS (Relational Database Service)](#rds)
  - [DynamoDB](#dynamodb)
* [**Compute**](#compute)
  - [EC2](#ec2)
  - [Lambda](#lambda)

## Storage
Your computer has a finite amount of data it can store (which is different from memory). But you also want to be able to access this information from other computers. Dropbox's business model is based off this, as well as Google Drive, etc. Unthinkable to go back.

## Compute
### EC2
Let's start with the fundamental building block of AWS: the virtual server. Whatever you need to do, from this to that, comes from here. Whether you have a database you're hosting in the cloud, or an application, etc., you need to have some sort of engine to _service_ the requests. If someone visits your website, a server needs to process the HTTP request and send the HTML back to them. If someone submits a query for your database, some server needs to execute the query to search through the data. This is where EC2 comes in.

Data science work is usually fairly far removed from the nuts and bolts configurations of EC2 instances, but you should know what your Sagemaker notebook $-$ and all of AWS, really $-$ is built on top of.



EC2 is Elastic Compute Cloud. Amazon's first cloud offering in 2006. Basically just a server you can rent on the web. An _instance_ is a virtual server in the AWS cloud. You can choose the amount of resources your server has (i.e. CPU, memory) <sup>[[1]](#1-ec2)</sup>, and then you can configure the operating system and applications on your instance.

The first thing you do when you launch an instance is select the Amazon Machine Image. This is like a Docker image that specifies the basic configurations of your instance: the operating system, application server, and applications required for your server to run. The basic AMI comes with a Linux kernel optimized for EC2, [the system and service manager systemd](https://en.wikipedia.org/wiki/Systemd), [the GCC compiler](https://en.wikipedia.org/wiki/GNU_Compiler_Collection), and other very low-level software.

#### Lambda
Lambda is _serverless_ computing. This is a bit of a confusing term because there _is_ a server involved... you just don't have to worry about the configurations. With an EC2 instance, you need to choose how much CPU and RAM you want the instance to have. Your instance will be there when you submit your requests, run your app, etc. But it'll still be quietly running in the background when you're not using it. This is often what you want $-$ you don't know when someone will make a request to your database, so you want the server to be ready at any time to serve that request. (Or for larger websites, there may never be a time where users _aren't_ making requests to your database. Think Amazon or Google displaying search results.)

But sometimes you don't want an instance to be running constantly in the background. You may have a tiny operation you want to run, like saving a log to S3, any time a user clicks on something. Or you want to write to a database or kick off a data processing pipeline whenever a file is uploaded to S3. For this, a lambda is the way to go.


## Identity
### IAM
Identity Access Management. Before we go any further, we need to know who you are. By default, no AWS service can access any other service. But an easy way to manage permissions is to have an IAM profile.


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

## Footnotes
#### 1. [EC2](#ec2)
It's tempting to say that you choose what _hardware_ you want your virtual server to have when you're deciding the amount of memory and CPU your instance will have, but this is likely provisioned via software as well.
