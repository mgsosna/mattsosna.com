---
layout: post
title: AWS Essentials for Data Science - 3. Compute
title-clean: AWS Essentials for Data Science<div class="a2">3. Compute</div>
author: matt_sosna
---

---
**AWS Essentials for Data Science:**
1. Why cloud computing?
2. Storage
3. **Compute**
---

## Table of contents
* [**Compute**](#compute)
  - [EC2](#ec2)
  - [Lambda](#lambda)

## Compute
### EC2
Let's start with the fundamental building block of AWS: the virtual server. Whatever you need to do, from this to that, comes from here. Whether you have a database you're hosting in the cloud, or an application, etc., you need to have some sort of engine to _service_ the requests. If someone visits your website, a server needs to process the HTTP request and send the HTML back to them. If someone submits a query for your database, some server needs to execute the query to search through the data. This is where EC2 comes in.

Data science work is usually fairly far removed from the nuts and bolts configurations of EC2 instances, but you should know what your Sagemaker notebook $-$ and all of AWS, really $-$ is built on top of.



EC2 is Elastic Compute Cloud. Amazon's first cloud offering in 2006. Basically just a server you can rent on the web. An _instance_ is a virtual server in the AWS cloud. You can choose the amount of resources your server has (i.e. CPU, memory) <sup>[[1]](#1-ec2)</sup>, and then you can configure the operating system and applications on your instance.

The first thing you do when you launch an instance is select the Amazon Machine Image. This is like a Docker image that specifies the basic configurations of your instance: the operating system, application server, and applications required for your server to run. The basic AMI comes with a Linux kernel optimized for EC2, [the system and service manager systemd](https://en.wikipedia.org/wiki/Systemd), [the GCC compiler](https://en.wikipedia.org/wiki/GNU_Compiler_Collection), and other very low-level software.

#### Lambda
Lambda is _serverless_ computing. This is a bit of a confusing term because there _is_ a server involved... you just don't have to worry about the configurations. With an EC2 instance, you need to choose how much CPU and RAM you want the instance to have. Your instance will be there when you submit your requests, run your app, etc. But it'll still be quietly running in the background when you're not using it. This is often what you want $-$ you don't know when someone will make a request to your database, so you want the server to be ready at any time to serve that request. (Or for larger websites, there may never be a time where users _aren't_ making requests to your database. Think Amazon or Google displaying search results.)

But sometimes you don't want an instance to be running constantly in the background. You may have a tiny operation you want to run, like saving a log to S3, any time a user clicks on something. Or you want to write to a database or kick off a data processing pipeline whenever a file is uploaded to S3. For this, a lambda is the way to go.

## Footnotes
#### 1. [EC2](#ec2)
It's tempting to say that you choose what _hardware_ you want your virtual server to have when you're deciding the amount of memory and CPU your instance will have, but this is likely provisioned via software as well.
