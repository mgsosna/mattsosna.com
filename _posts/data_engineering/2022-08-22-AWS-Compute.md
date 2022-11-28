---
layout: post
title: AWS Essentials for Data Science - 3. Compute
title-clean: AWS Essentials for Data Science<div class="a2">3. Compute</div>
author: matt_sosna
tags: aws python
---

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/edges2cats.png">
<span style="font-size: 12px"><i>Screenshot from Christopher Hesse's amazing [Image-to-Image Demo](https://affinelayer.com/pixsrv/)</i></span>

So you've built a cool app and want to show it off to the world. Maybe it's an AI that generates [cat pictures from scribbles](https://affinelayer.com/pixsrv/), a [viral LinkedIn post generator](https://viralpostgenerator.com), or an [English to RegEx translator](https://www.autoregex.xyz/). You want a user to just click a link and immediately start interacting with your app, rather than needing to download and run it on their computer.

This "immediate interactivity" is going to require a **server**, which takes user requests (e.g., cat scribbles) and _serves_ responses (e.g., AI-generated cat images). You _could_ use your personal laptop, but it'll stop serving requests when it goes to sleep or turns off. A sophisticated hacker could also steal your private data, and your hard drive might melt if your app gets popular and your computer tries serving too many requests!

Unless you like hacked, melted laptops, you'll probably want to rent a server from the cloud. While you do sacrifice some control by not having access to the physical machine, you'll abstract away a lot of configuration and maintenance you likely don't want to deal with anyway. And if you're willing to pay a bit more, you can easily rent a machine -- or several -- that are significantly stronger than your laptop. So how do we get started?

We previously covered a [high-level overview]({{  site.baseurl  }}/AWS-Intro) of the cloud, as well as a tutorial on [storing data]({{  site.baseurl  }}/AWS-Storage). But what about the _engines_ of the cloud? In this final post, we'll cover two compute-focused **Amazon Web Services**. We'll start with the fundamental cloud building block, **EC2**, before moving on to server-less computing with **Lambda**.

## Table of contents
* [Background](#background)
* [EC2: Elastic Cloud Compute](#ec2-elastic-cloud-compute)
* [Lambda](#lambda)

## Background
The holiday season is a recurring chaotic time for retailers. Q4 accounts for **a staggering 33-39%** of [Macy's](https://ycharts.com/companies/M/revenues) and [Kohl's](https://ycharts.com/companies/KSS/revenues) yearly revenues, for example, and even with Prime Day in the summer, [Amazon's](https://ycharts.com/companies/AMZN/revenues) Q4 is still around 31%. Much of this holiday rush [takes place online](https://www.cbre.com/insights/articles/omnichannel-what-is-the-share-of-e-commerce-in-overall-retail-sales), translating to _a lot of users_ spending _a lot more time_ on your website.

This extra load is often much more than your servers -- configured for normal traffic the rest of the year -- can handle. You need to do something: the last thing you want is for your site to be down, [millions of dollars of sales slipping by](https://www.independent.co.uk/news/business/amazon-down-internet-outage-sales-b1861737.html) as frustrated shoppers switch to another website.<sup>[[1]](#1-background)</sup>

One way to handle the additional load is to buy more computers. And there are indeed [stories of early Amazon engineers](https://open.spotify.com/episode/14LmWeOMRZysw2i2vYSOuw?si=ce630660e3b44461) preparing for the holidays by buying the most powerful servers they could find, hoping they'd handle the spike in requests! But when the holiday buzz ended, that extra compute would end up sitting around unused until the next holiday season.<sup>[[2]](#2-background)</sup>

Ideally, you'd be able to _scale up_ when you need the compute, then _scale down_ when you don't need the extra power. This **elasticity** is a central goal of cloud computing -- use only what you need, when you need it. And being able to **quickly** get up and running, without needing to buy and set up the hardware, was another key need.

Amazon Web Services set out to address needs like these in the fledgling internet. We've [already covered]({{  site.baseurl  }}/AWS-Storage) one of their core early offerings: Amazon Simple Storage Service (S3), a catch-all Dropbox analogue for storing data. But Amazon's _very first_ offering was a compute service: Elastic Cloud Compute.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/ec2_landing.png" alt="AWS EC2 landing page">

## EC2: Elastic Cloud Compute
Amazon's first offering, EC2, is the fundamental building block of the cloud: the virtual server. Virtual servers are [logical partitions](https://en.wikipedia.org/wiki/Logical_partition) of physical servers sitting in data centers. They're like miniature computers we can reserve _inside_ a bigger computer. Whether they're running simulations for a weather forecast, fetching data from a database, or sending the HTML for your app's fancy webpage, virtual servers are the engines powering the cloud.

At AWS, these engines are called **EC2** instances. EC2 stands for "Elastic Compute Cloud" and was Amazon's first public cloud offering, in 2006. EC2 instances are modular and configurable, meaning you can easily add or remove instances that meet your specific needs. You can specify both the hardware (e.g., the compute, memory, GPU, etc.)<sup>[[3]](#3-ec2)</sup> and software (e.g., its operating system and programs).

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/ec2_intro.png">

### Set up
#### AMI
The first thing you do when you launch an instance is select the [Amazon Machine Image](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html). This is like a Docker image that specifies the basic configurations of your instance: the operating system, application server, and applications required for your server to run. Another way to think of this is like a Python class: a reusable template.

The basic AMI comes with a Linux kernel optimized for EC2, [the system and service manager systemd](https://en.wikipedia.org/wiki/Systemd), [the GCC compiler](https://en.wikipedia.org/wiki/GNU_Compiler_Collection), and other very low-level software. We could create our own, e.g., if we had strong opinions about optimizing for our custom use case. But this is an intro to AWS tutorial, so let's just choose the default Amazon Linux 2 AMI.

<img src="{{ site.baseurl  }}/images/data_engineering/aws/compute/ec2_ami.png" alt="EC2 Amazon Machine Images">

#### Instance Type
Next up is **Instance Type.** This is where we can choose the hardware for our server. We won't want to deviate from the `t2.micro` option, which is covered by the Free Tier. In a production setting, we could decide whether to optimize for compute (e.g., if running a lot of computations), memory (if needing to store a lot of data in cache), GPU (e.g., for gaming), storage (e.g., if reading and writing a lot to disk), or some balance of these.

Once we choose an instance type, we can't go back -- unlike an application or even the operating system, this is the hardware of the machine. We can't yet warp the metal with a few code commands. But anyway, let's choose the `t2.micro` option.

#### Key Pair
Next we'll create a key pair. From the [AWS website](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html):
> AWS uses public-key cryptography to secure the login information for your instance. A Linux instance has no password; you use a key pair to log in to your instance securely. You specify the name of the key pair when you launch your instance, then provide the private key when you log in using SSH.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/ec2_setup1.png" alt="Setting up AWS EC2">

* Pick a region geographically close to where you are
* AMI: the template. Like a class in Python
  * Operating system, software, etc. Can get predefined ones from AWS, or create your own and reuse it later.
* Instance type: how powerful our machine should be
  * e.g., compute-optimized (processing power), memory-optimized (if storing a lot of in-memory cache), GPU-optimized (e.g., gaming), storage-optimized, general-purpose
  * These are fixed because they're hardware.
* Additional configuration: can set your availability zone within your geographic region, but most likely you don't have a preference.
  * The kind of network, purchasing options, IP addresses for security group, stopping behavior, etc.
  * Bootstrap shell scripts: code that's run before the instance is officially online. Useful if setting up the instance for someone else
  * For storage: we can do ephemeral (free), which disappears when we release the instance. But we can also go for Amazon Elastic Block Storage (EBS), or S3
* For Security Group, we can just set IP as 0.0.0.0/0. Open to the world.
  * Then need to create a key pair, which will let us SSH into the instance
    * Public key that AWS stores, and private one that we store
* SSH: Secure Shell. Works for Unix. Need Putty for Windows but we'll connect to Linux server
  * SSH is a network protocol that provides [a secure way to access a computer](https://www.techtarget.com/searchsecurity/definition/Secure-Shell) over an unsecured network (like the internet). Strong password and public key authentication, encrypted data communications between two computers.
  * Most basic use of SSH is to connect to a remote host for a terminal session. In other words: controlling a remote server from the command line. Once we've SSH'd into the server, it'll be as if our computer is that machine.
* Tags = useful if you have a lot of EC2 instances. e.g., for a big company, the team that is using this instance.

We'll see a public DNS and a public IP. That IP is how we'll access it. We can also check our EC2 instance's inbound rules and confirm that port 22 is open.

```bash
ssh ec2-user@xx.xxx.xxx.xxx
```

* It'll say the authenticity of the host can't be guaranteed. Do we want to continue? Yes.
* Then it'll say that we can't connect: permission denied. That's because we need to pass in our key. (The `.pem` file.)

```bash
ssh -i matt_ec2_key.pem ec2-user@xx.xxx.xxx.xxx
```

* It'll say Warning: unprotected private key file. Permission 0644 is too open
  * This permission is what's on the file when you first download it.
* To fix this, we'll need to `chmod` the file.

```bash
chmod 0400 matt_ec2_key.pem
ssh -i matt_ec2_key.pem ec2-user@xx.xxx.xxx.xxx
```

Now we're in the machine.

```bash
whoami
# ec2-user
```

```bash
exit
```



## Lambda
Lambda is _server-less_ computing. This is a bit of a confusing term because there _is_ a server involved... you just don't have to worry about the configurations. With an EC2 instance, you need to choose how much CPU and RAM you want the instance to have. Your instance will be there when you submit your requests, run your app, etc. But it'll still be quietly running in the background when you're not using it. This is often what you want $-$ you don't know when someone will make a request to your database, so you want the server to be ready at any time to serve that request. (Or for larger websites, there may never be a time where users _aren't_ making requests to your database. Think Amazon or Google displaying search results.)

But sometimes you don't want an instance to be running constantly in the background. You may have a tiny operation you want to run, like saving a log to S3, any time a user clicks on something. Or you want to write to a database or kick off a data processing pipeline whenever a file is uploaded to S3. For this, a lambda is the way to go.

## Footnotes
#### 1. [Background](#background)
In researching for this post, I found plenty of interesting statistics about the cost of websites that are clunky or down. Some of the more interesting ones:
* Taobao's Singles Day 20-minute crash in 2021 could have cost [several billion dollars](https://queue-it.com/blog/singles-day-statistics/) in sales.
* A webpage that loads within two seconds has an average bounce rate of 9%. That number [jumps to 38%](https://www.pingdom.com/blog/page-load-time-really-affect-bounce-rate/) when the webpage takes five seconds to load.




#### 2. [Background](#background)
For hyper-growth early Amazon, the extra compute purchased during the holiday season would eventually just serve the normal business needs as the company grew. But for most companies, this extra compute wouldn't be helpful to have most of the year.

#### 3. [EC2: Elastic Cloud Compute](#ec2-elastic-cloud-compute)
It's tempting to say that you choose what _hardware_ you want your virtual server to have when you're deciding the amount of memory and CPU your instance will have, but this is likely provisioned via software as well.
