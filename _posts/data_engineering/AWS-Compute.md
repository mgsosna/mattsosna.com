---
layout: post
title: AWS Essentials for Data Science - 3. Compute
title-clean: AWS Essentials for Data Science<div class="a2">3. Compute</div>
author: matt_sosna
---

In the [first post]({{  site.baseurl  }}/AWS-Intro) we covered an introduction to AWS. In the [second post]({{  site.baseurl  }}/AWS-Storage) we covered storing data in the cloud. This post will cover the other big use case for the cloud: compute.

But these benefits extend into the professional realm, too. If you ever have data or code that you want to share with others $-$ like an [AI-powered cat picture generator](https://affinelayer.com/pixsrv/) or the [daily number of occupied hotel rooms in Brussels](https://datastore.brussels/web/data/dataset/f03544a1-a01c-4374-b19d-e93697f1ac73)$-$ you'll want to store this data on a cloud server. Cloud servers don't turn off when you close your laptop, and you don't have to worry if some of those queries are fetching your private data when they visit your laptop.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/edges2cats.png">
<span style="font-size: 12px"><i>Screenshot from Christopher Hesse's amazing [Image-to-Image Demo](https://affinelayer.com/pixsrv/)</i></span>


## Table of contents
* [**Compute**](#compute)
  - [EC2](#ec2)
  - [Lambda](#lambda)
  - [API Gateway](#api-gateways)

## Compute
### EC2
Let's start with the fundamental building block of AWS: the virtual server. Virtual servers are partitions of physical servers in data centers, distinct chunks of compute power you can reserve to do essentially _anything_ involving a computer. Whether they're running simulations for a climate forecast, fetching data from a database, or sending the HTML for your app's fancy webpage, virtual servers are the engines powering the cloud.

At AWS, these engines are called **EC2** instances. EC2 stands for "Elastic Compute Cloud" and was Amazon's first cloud offering, back in 2006. EC2 instances are modular and configurable, meaning you can easily add or remove instances that are as small or large as you need. You can choose the amount of resources your server has (i.e. CPU, memory) <sup>[[1]](#1-ec2)</sup>, and then you can configure the operating system and applications on your instance.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/ec2_intro.png">

The first thing you do when you launch an instance is select the [Amazon Machine Image](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html). This is like a Docker image that specifies the basic configurations of your instance: the operating system, application server, and applications required for your server to run. The basic AMI comes with a Linux kernel optimized for EC2, [the system and service manager systemd](https://en.wikipedia.org/wiki/Systemd), [the GCC compiler](https://en.wikipedia.org/wiki/GNU_Compiler_Collection), and other very low-level software.

We'll create a key pair. From the [AWS website](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html):
> AWS uses public-key cryptography to secure the login information for your instance. A Linux instance has no password; you use a key pair to log in to your instance securely. You specify the name of the key pair when you launch your instance, then provide the private key when you log in using SSH.


#### Lambda
Lambda is _serverless_ computing. This is a bit of a confusing term because there _is_ a server involved... you just don't have to worry about the configurations. With an EC2 instance, you need to choose how much CPU and RAM you want the instance to have. Your instance will be there when you submit your requests, run your app, etc. But it'll still be quietly running in the background when you're not using it. This is often what you want $-$ you don't know when someone will make a request to your database, so you want the server to be ready at any time to serve that request. (Or for larger websites, there may never be a time where users _aren't_ making requests to your database. Think Amazon or Google displaying search results.)

But sometimes you don't want an instance to be running constantly in the background. You may have a tiny operation you want to run, like saving a log to S3, any time a user clicks on something. Or you want to write to a database or kick off a data processing pipeline whenever a file is uploaded to S3. For this, a lambda is the way to go.

## Footnotes
#### 1. [EC2](#ec2)
It's tempting to say that you choose what _hardware_ you want your virtual server to have when you're deciding the amount of memory and CPU your instance will have, but this is likely provisioned via software as well.
