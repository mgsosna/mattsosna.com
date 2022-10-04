---
layout: post
title: AWS Essentials for Data Science - 3. Compute
title-clean: AWS Essentials for Data Science<div class="a2">3. Compute</div>
author: matt_sosna
tags: aws python
---

If you ever have software you want to share with others -- like an [AI-powered cat picture generator](https://affinelayer.com/pixsrv/) or [viral LinkedIn post generator](https://viralpostgenerator.com) -- you'll want to store this data on a cloud server. Cloud servers don't turn off when you close your laptop, you don't need to worry about malicious users stealing your private data, and you can rent a much stronger machine than your laptop.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/edges2cats.png">
<span style="font-size: 12px"><i>Screenshot from Christopher Hesse's amazing [Image-to-Image Demo](https://affinelayer.com/pixsrv/)</i></span>

But what sort of services are out there? How can we use them? In the final post in [our AWS series]({{  site.baseurl  }}/AWS-Intro), we'll cover several **Amazon Web Services** that let us leverage cloud servers in different ways to run calculations. We'll start with the fundamental cloud building block, EC2, before moving on to serverless computing with Lambda.


## Table of contents
* [Background](#background)
* [EC2](#ec2)
* [Lambda](#lambda)

## Background
In the early 2000s, the holiday season was a yearly pain point for the e-commerce industry. Q4 can account for [32% of online retailers' yearly revenue](https://www.forbes.com/sites/shelleykohan/2022/01/12/record-sales-for-online-holiday-shopping-hitting-over-204-billion/?sh=a8ec2f36bb56), which means a lot of users spending a lot more time on your website.

How can you handle this extra load? One option is to buy more computers. And there are indeed [stories of early Amazon engineers](https://open.spotify.com/episode/14LmWeOMRZysw2i2vYSOuw?si=ce630660e3b44461) shopping for the most powerful servers they could find, hoping it would handle the spike in requests to the online retailer. But when the holiday buzz ends, that extra compute might end up sitting around unused.

Ideally, you'd be able to _scale up_ when you need the compute, then _scale down_ when you don't need the computers. This **elasticity** is a central goal of cloud computing -- use only what you need, when you need it. 



* EC2, ECS



<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/ec2_landing.png" alt="AWS EC2 landing page">

## EC2
Let's start with the fundamental building block of AWS: the virtual server. Virtual servers are partitions of physical servers in data centers, distinct chunks of compute you can reserve to do essentially _anything_ involving a computer. Whether they're running simulations for a weather forecast, fetching data from a database, or sending the HTML for your app's fancy webpage, virtual servers are the engines powering the cloud.

At AWS, these engines are called **EC2** instances. EC2 stands for "Elastic Compute Cloud" and was Amazon's first cloud offering, back in 2006. EC2 instances are modular and configurable, meaning you can easily add or remove instances that are as small or large as you need. You can choose the amount of resources your server has (i.e. CPU, memory)<sup>[[1]](#1-ec2)</sup>, and then you can configure the operating system and applications on your instance.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/ec2_intro.png">

The first thing you do when you launch an instance is select the [Amazon Machine Image](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html). This is like a Docker image that specifies the basic configurations of your instance: the operating system, application server, and applications required for your server to run. The basic AMI comes with a Linux kernel optimized for EC2, [the system and service manager systemd](https://en.wikipedia.org/wiki/Systemd), [the GCC compiler](https://en.wikipedia.org/wiki/GNU_Compiler_Collection), and other very low-level software.

We'll create a key pair. From the [AWS website](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html):
> AWS uses public-key cryptography to secure the login information for your instance. A Linux instance has no password; you use a key pair to log in to your instance securely. You specify the name of the key pair when you launch your instance, then provide the private key when you log in using SSH.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/ec2_setup1.png" alt="Setting up AWS EC2">


## Lambda
Lambda is _serverless_ computing. This is a bit of a confusing term because there _is_ a server involved... you just don't have to worry about the configurations. With an EC2 instance, you need to choose how much CPU and RAM you want the instance to have. Your instance will be there when you submit your requests, run your app, etc. But it'll still be quietly running in the background when you're not using it. This is often what you want $-$ you don't know when someone will make a request to your database, so you want the server to be ready at any time to serve that request. (Or for larger websites, there may never be a time where users _aren't_ making requests to your database. Think Amazon or Google displaying search results.)

But sometimes you don't want an instance to be running constantly in the background. You may have a tiny operation you want to run, like saving a log to S3, any time a user clicks on something. Or you want to write to a database or kick off a data processing pipeline whenever a file is uploaded to S3. For this, a lambda is the way to go.

## Footnotes
#### 1. [EC2](#ec2)
It's tempting to say that you choose what _hardware_ you want your virtual server to have when you're deciding the amount of memory and CPU your instance will have, but this is likely provisioned via software as well.
