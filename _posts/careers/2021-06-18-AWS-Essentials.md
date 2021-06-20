---
layout: post
title: AWS Essentials for Data Science
author: matt_sosna
---


Cloud computing is an important aspect of data science work. Basically, don't be limited by the power of your computer; use powerful servers in the cloud. These servers can store your data, process things, etc.

AWS is market leader, so we'll focus on them. But all of these services are available from the other major players in the cloud market, Google Cloud Platform and Microsoft Azure. This post will therefore cover more of the concepts than stuff specific to AWS.



### Table of contents
* [**Storage**](#storage)
  - [S3 (Simple Storage Service)](#s3)
  - [RDS (Relational Database Service)](#rds)
  - [DynamoDB](#dynamodb)
* [**Compute**](#compute)
  - [EC2](#ec2)
  - [Lambda](#lambda)

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

### Compute
#### EC2

#### Lambda

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
