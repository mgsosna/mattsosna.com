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

## Compute
### EC2
Let's start with the fundamental building block of AWS: the virtual server. Whatever you need to do, from this to that, comes from here.

first cloud service Amazon offered


EC2 is Elastic Compute Cloud. Amazon's first cloud offering in 2006. Basically just a server you can rent on the web. An _instance_ is a virtual server in the AWS cloud. You can choose the amount of resources your server has (i.e. CPU, memory) <sup>[[1]](#1-ec2)</sup>, and then you can configure the operating system and applications on your instance.

The first thing you do when you launch an instance is select the Amazon Machine Image. This is like a Docker image that specifies the basic configurations of your instance: the operating system, application server, and applications required for your server to run. The basic AMI comes with a Linux kernel optimized for EC2, [the system and service manager systemd](https://en.wikipedia.org/wiki/Systemd), [the GCC compiler](https://en.wikipedia.org/wiki/GNU_Compiler_Collection), and other very low-level software.

#### Lambda

## Identity
### IAM
Identity Access Management. Before we go any further, we need to know who you are. By default, no AWS service can access any other service. But an easy way to manage permissions is to have an IAM profile.



### Storage
Need to put your data somewhere. But "data" is a broad term $-$ is it raw videos or text transcripts? Is it a user profile? Is it code? Is it tabular data? The _structure_ of the data (unstructured, semi-structured, and structured) will determine what the right storage solution is.

#### S3
S3 is Simple Storage Service.

#### RDS
RDS is Relational Database Service.

#### Redshift
Data warehouse.



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