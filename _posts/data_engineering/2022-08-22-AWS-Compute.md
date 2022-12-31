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

This "immediate interactivity" is going to require a **server**, which takes user requests (e.g., cat scribbles) and _serves_ responses (e.g., AI-generated cat images). You _could_ use your personal laptop, but it'll stop serving requests when it goes to sleep or turns off, and a sophisticated hacker could probably steal your private data. The cherry on top is that your hard drive might melt if your computer tries serving too many requests at once!

Unless you like hacked, melted laptops, you'll probably want to [rent a server from the cloud]({{  site.baseurl  }}/AWS-Intro). While you do sacrifice some control by not having access to the physical machine, you'll abstract away a lot of configuration and maintenance you likely don't want to deal with anyway. And if you're willing to pay a bit more, you can easily rent a machine -- or several -- that are significantly stronger than your laptop. So how do we get started?

We previously covered a [high-level overview]({{  site.baseurl  }}/AWS-Intro) of the cloud, as well as a tutorial on [storing data]({{  site.baseurl  }}/AWS-Storage). But what about the _engines_ of the cloud? In this final post, we'll cover two compute-focused **Amazon Web Services**. We'll start with the fundamental cloud building block, **EC2**, before moving on to server-less computing with **Lambda**.

## Table of contents
* [**Background**](#background)
* [**EC2: Elastic Compute Cloud**](#ec2-elastic-compute-cloud)
  * [Set up](#set-up)
  * [Connecting to our instance](#connecting-to-our-instance)
  * [Beyond the basics](#beyond-the-basics)
* [**Lambda**](#lambda)
  * [When is EC2 not the right choice?](#when-is-ec2-not-the-right-choice)
  * [What is Lambda?](#what-is-lambda)
  * [Creating a function](#creating-a-function)
  * [Triggering via API Gateway](#triggering-via-api-gateway)

## Background
The holiday season is a recurring chaotic time for retailers. Q4 accounts for **a staggering 33-39%** of [Macy's](https://ycharts.com/companies/M/revenues) and [Kohl's](https://ycharts.com/companies/KSS/revenues) yearly revenues, for example, and even with Prime Day in the summer, [Amazon's](https://ycharts.com/companies/AMZN/revenues) Q4 is still around 31%. Much of this holiday rush [takes place online](https://www.cbre.com/insights/articles/omnichannel-what-is-the-share-of-e-commerce-in-overall-retail-sales), translating to _a lot more users_ spending _a lot more time_ on stores' websites.

Put yourself in the shoes of an Amazon infrastructure engineer in October 2005, a few years after the [dot-com bubble](https://en.wikipedia.org/wiki/Dot-com_bubble), but before the cloud industry really started. You know you have to do _something_ to handle the tsunami of traffic on the horizon: the last thing you want is for the site to be down, [millions of dollars of sales slipping by](https://www.independent.co.uk/news/business/amazon-down-internet-outage-sales-b1861737.html) as frustrated shoppers switch to another website.<sup>[[1]](#1-background)</sup>

One way to handle the additional load is to _buy more computers_. (There are indeed [stories of early Amazon engineers](https://open.spotify.com/episode/14LmWeOMRZysw2i2vYSOuw?si=ce630660e3b44461) preparing for the holidays by buying the most powerful servers they could find and crossing their fingers!) These extra servers should indeed handle the spike in traffic. But when the holiday buzz ends, that extra compute will end up sitting around unused until the next holiday season.<sup>[[2]](#2-background)</sup>

The alternative would be to _rent_ compute somehow. Ideally, resources would **elastically** and **automatically** increase and decrease to your immediate needs, rather than needing to guess ahead of time. You'd abstract away the physical hardware, instead just dipping into a "pool" of resources.

Amazon Web Services was born out of needs like these in the fledgling internet: dynamically accessing the compute resources you need, when you need them. We've [already covered]({{  site.baseurl  }}/AWS-Storage) one of their fundamental _storage_ offerings: Amazon Simple Storage Service (S3), a catch-all Dropbox analogue for storing data. But let's now turn to Amazon's fundamental _compute_ offering: **Elastic Compute Cloud.**

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/ec2_landing.png" alt="AWS EC2 landing page">

## EC2: Elastic Compute Cloud
We can use **Amazon EC2** to access the fundamental building block of the cloud: the **virtual server**. Data centers are filled with servers, which are [logically partitioned](https://en.wikipedia.org/wiki/Logical_partition) into virtual servers, allowing multiple people to simultaneously and independently use the hardware.

One server could be simultaneously running simulations for a weather forecast, fetching data from multiple databases, sending the HTML for a dozen webpages, and more. Importantly, this physical server would be abstracted away from its users beyond the configurations of their virtual servers, letting them focus on their applications.

At AWS, virtual servers are called **EC2 instances**. Released in 2006, EC2 was [one of Amazon's first cloud services](https://aws.amazon.com/blogs/aws/aws-blog-the-first-five-years/) and has grown to be a [central component of the tech stacks](https://aws.amazon.com/ec2/customers/) of Netflix, Pinterest, Lyft, and many others. EC2 instances are modular and configurable, allowing users to optimize for compute, memory, GPU, storage, or a combination depending on their needs. A GPU-optimized instance could be used for training machine learning models, for example, while a storage-optimized instance could host a database.

Let's now create an EC2 instance to take a closer look. We [log into our AWS account](https://aws.amazon.com/login), then navigate to EC2 from the menu of services. We should see something like the image below. Let's click on the `Launch instance` button and begin.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/ec2_setup1.png" alt="Setting up AWS EC2">

### Set up
#### AMI: Amazon Machine Image
The first thing we'll do when launching an EC2 instance is select the [**Amazon Machine Image**](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html). An AMI specifies the basic software configuration our instance: the operating system, [application server](https://www.gartner.com/en/information-technology/glossary/application-server), and applications required for your server to run. AMIs are like [Docker images](https://www.tutorialspoint.com/docker/docker_images.htm): **reusable templates** that let us create the exact environment we want each time.

The default AMI comes with a Linux kernel optimized for EC2, [the system and service manager _systemd_](https://en.wikipedia.org/wiki/Systemd), [the GCC compiler](https://en.wikipedia.org/wiki/GNU_Compiler_Collection), and other very low-level software. We could create our own AMI if we had strong opinions about how to optimize for our use case. But this is an intro tutorial, so let's just choose the default Amazon Linux 2 AMI.

<img src="{{ site.baseurl  }}/images/data_engineering/aws/compute/ec2_ami.png" alt="EC2 Amazon Machine Images">

#### Instance Type
Next up is **Instance Type**, where we choose the hardware for our server. We won't want to deviate from the `t2.micro` option, which is covered by the Free Tier. In a production setting, we could decide to optimize for **CPU** (for running a [wide range of system operations simultaneously](https://www.weka.io/learn/hpc/cpu-vs-gpu)), **GPU** (for machine learning or graphics processing), **storage** (for slow reads and writes of persistent data), **memory** (for [fast reads and writes of volatile data](https://www.backblaze.com/blog/whats-diff-ram-vs-storage/)), or some combination.

We can't change the instance type once we launch our instance, so make sure you don't accidentally click [the one that charges $31.21 per hour](https://www.todayilearnedcloud.com/Amazon-EC2-How-Much-Does-The-Most-Expensive-Instance-Cost/)! Triple-checking that we've selected `t2.micro`, we can continue to the next step.

#### Key Pair
We'll now create a key pair. [AWS uses public-key cryptography](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html) to secure the login information for EC2 instances. Rather than a password, we'll use the key pair to remotely log into our instance via [SSH](https://www.techtarget.com/searchsecurity/definition/Secure-Shell).

We'll click on `Create a new key pair`. We then give it a name and stick with the RSA and .pem defaults. (Select PuTTY if you're using Windows.)

<center>
<img src="{{ site.baseurl  }}/images/data_engineering/aws/compute/key-pair.jpg" alt="Amazon EC2 key pair" height="70%" width="70%">
</center>

Once we click `Create key pair`, Amazon will save a public part of our key, and our computer will download the private key. Make sure you don't lose this .pem (or .ppk) file, as we'll use it to identify ourselves when remotely accessing the EC2 instance.

#### Network settings
We now set the rules for how to access our EC2 instance via the internet. For this demo, let's just click `Select existing security group`, then our default VPC ([virtual private cloud](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)). If you followed along in the previous [AWS Storage post]({{  site.baseurl  }}/AWS-Storage), you'll have already tinkered with the inbound and outbound access rules for this VPC.

#### Configure storage
We'll leave our storage config at the default values, which are well within the Free Tier limits. Any data we write to our instance will be deleted once our demo is over; if we cared about persisting this data, we could click `Add new volume` to reserve an [Amazon Elastic Block Storage (EBS)](https://aws.amazon.com/ebs/) volume and save our data there. But let's stick with the root volume for now.

#### Advanced details
We'll skip this section for our demo. But this is where we can specify configurations like using on-demand [spot instances](https://aws.amazon.com/ec2/spot/), shutdown and [hibernate](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Hibernate.html) behavior, whether we want detailed [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) logs, and more.

### Connecting to our instance
Our instance will be available within a few minutes after we hit `Create`. On the EC2 home page, we can then click on `Instances` and see something like the image below.

<center>
<img src="{{ site.baseurl  }}/images/data_engineering/aws/compute/ec2-instances.png" alt="Amazon EC2 instance info">
</center>

Let's now connect to our instance. We'll use [**SSH**](https://www.techtarget.com/searchsecurity/definition/Secure-Shell), a network protocol that enables secure communication over an unsecured network (like the internet). Once we've SSH'd into our instance, we will be able to control the machine as if we were in a Terminal on our laptop.

The first thing to do is **modify the instance's security group to allow inbound traffic.** On our instance page, we'll click on the `Security` tab at the bottom, then the link for the instance's security group.

<center>
<img src="{{ site.baseurl  }}/images/data_engineering/aws/compute/ec2-security-groups.png" alt="Amazon EC2 security groups">
</center>

On the Security Group page, click `Edit inbound rules`, then `Add rule`. Select **SSH** for `Type`, then **My IP** for `Source`. Finally, click `Save rules`.

So let's try connecting to our instance now. The command is `ssh` followed by the Public IPv4 DNS, available on the Instance page. You can also go to `Connect` > `SSH client` to get the address.

{% include header-bash.html %}
```bash
ssh ec2-user@xx.xx.xx.xxx
# ec2-user@ec2-xx-xx-xx-xxx.compute-1.amazonaws.com:
# Permission denied (publickey,gssapi-keyex,gssapi-with-mic).
```

We get a Permission denied error because we haven't passed in our private key. Let's change directories to the one with our key and try again.

{% include header-bash.html %}
```bash
cd path/to/your/key
ssh -i matt-test.pem ec2-user@ec2-xx-xx-xx-xxx.compute-1.amazonaws.com
# The authenticity of host 'ec2-xx-xx-xx-xxx.compute-1.amazonaws.com
# (xx.xx.xx.xxx)' can't be established.
# ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
# This key is not known by any other names
# Are you sure you want to continue connecting (yes/no/[fingerprint])?
# yes
```

So far so good, but then we get another error:

{% include header-bash.html %}
```bash
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Permissions 0644 for 'matt-test.pem' are too open.
# It is required that your private key files are NOT accessible by others.
# This private key will be ignored.
# Load key "matt-test.pem": bad permissions
# ec2-user@ec2-xx-xx-xx-xxx.compute-1.amazonaws.com:
# Permission denied (publickey,gssapi-keyex,gssapi-with-mic).
```

The error is that our private key has [permission code 644](https://chmodcommand.com/chmod-0644/), which means that anyone can read the file. This is the [default access level](https://www.namecheap.com/support/knowledgebase/article.aspx/400/205/file-permissions/) for new files, but AWS considers this too insecure: anyone with your key could impersonate you.

So we'll need to modify the file privacy to make it more secure. To do so, we use [**chmod**](https://en.wikipedia.org/wiki/Chmod) to change the read and write permissions of the file. Specifically, we'll change the file so that **the only valid action is a read by the owner (us).** Even if someone copied our private key to another computer, or a different user on our network somehow found the key, the file wouldn't open because that person isn't the owner. As an additional precaution, we remove our write access as well.

The `chmod` code for [this permission level is 400](https://chmodcommand.com/chmod-400/): owner can only read (`4`), security group can't read/write/execute (`0`), and others can't read/write/execute (`0`). Let's therefore run this command in the Terminal:

{% include header-bash.html %}
```bash
chmod 400 matt-test.pem
```

Now when we try to connect, we succeed:

{% include header-bash.html %}
```bash
ssh -i matt-test.pem ec2-user@ec2-xx-xx-xx-xxx.compute-1.amazonaws.com
# The authenticity of host 'ec2-xx-xx-xx-xxx.compute-1.amazonaws.com
# (xx.xx.xx.xxx)' can't be established.
# ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
# This key is not known by any other names
# Are you sure you want to continue connecting (yes/no/[fingerprint])?
# yes

#        __|  __|_  )
#        _|  (     /   Amazon Linux 2 AMI
#       ___|\___|___|
```

We're in! To the left of our cursor we should see something like `[ec2-user@ip-xx-xx-xx-xxx ~]$`, where we previously just saw `$`. Let's now run some quick commands to explore the instance.

{% include header-bash.html %}
```bash
ls
# (nothing)

whoami
# ec2-user

python3 --version
# Python 3.7.15
```

Python already comes installed, which is convenient! Let's download a [sample Python file](https://raw.githubusercontent.com/mgsosna/code_samples/master/calculate_mean.py) from GitHub and run some basic calculations on our EC2 instance. We'll use `curl` to download the file from the URL, then pass in some arguments to `calculate_mean.py` to get their average value.

{% include header-bash.html %}
```bash
# Download file
curl -O https://raw.githubusercontent.com/mgsosna/code_samples/master/calculate_mean.py

# Run it
python3 calculate_mean.py 1 -5 0 33   # 7.25
python3 calculate_mean.py 0 1e5 -1e5  # 0.0
```

Let's now train a random forest classifier on some generated data. We'll download `numpy`, `pandas`, and `scikit-learn`, open Python, generate the data, then create the model.

Let's first download the necessary libraries.

{% include header-bash.html %}
```bash
python3 -m pip install numpy pandas scikit-learn
# Defaulting to user installation because normal site-packages is not writeable
# Collecting numpy
#   Downloading numpy-1.21.6-cp37-cp37m-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (15.7 MB)
#      |████████████████████████████████| 15.7 MB 25.1 MB/s
# Installing collected packages: numpy
# Successfully installed numpy-1.21.6
# Defaulting to user installation because normal site-packages is not writeable
# Collecting pandas
#   Downloading pandas-1.3.5-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (11.3 MB)
#      |████████████████████████████████| 11.3 MB 23.8 MB/s
# Requirement already satisfied: numpy>=1.17.3; platform_machine != "aarch64" and platform_machine != "arm64" and python_version < "3.10" in ./.local/lib/python3.7/site-packages (from pandas) (1.21.6)
# Collecting pytz>=2017.3
#   Downloading pytz-2022.7-py2.py3-none-any.whl (499 kB)
#      |████████████████████████████████| 499 kB 29.1 MB/s
# Collecting python-dateutil>=2.7.3
#   Downloading python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
#      |████████████████████████████████| 247 kB 32.8 MB/s
# Collecting six>=1.5
#   Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
# Installing collected packages: pytz, six, python-dateutil, pandas
# Successfully installed pandas-1.3.5 python-dateutil-2.8.2 pytz-2022.7 six-1.16.0
# Defaulting to user installation because normal site-packages is not writeable
# Collecting scikit-learn
#   Downloading scikit_learn-1.0.2-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (24.8 MB)
#      |████████████████████████████████| 24.8 MB 19.7 MB/s
# Requirement already satisfied: numpy>=1.14.6 in ./.local/lib/python3.7/site-packages (from scikit-learn) (1.21.6)
# Collecting scipy>=1.1.0
#   Downloading scipy-1.7.3-cp37-cp37m-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (38.1 MB)
#      |████████████████████████████████| 38.1 MB 41.1 MB/s
# Collecting threadpoolctl>=2.0.0
#   Downloading threadpoolctl-3.1.0-py3-none-any.whl (14 kB)
# Collecting joblib>=0.11
#   Downloading joblib-1.2.0-py3-none-any.whl (297 kB)
#      |████████████████████████████████| 297 kB 34.3 MB/s
# Installing collected packages: scipy, threadpoolctl, joblib, scikit-learn
# Successfully installed joblib-1.2.0 scikit-learn-1.0.2 scipy-1.7.3 threadpoolctl-3.1.0
```

We can now run Python, generate our data, train the model, and generate some predictions. We'll use `np.random.normal` for the features and `np.random.choice` for the labels.

{% include header-bash.html %}
```bash
python3
# Python 3.7.15 (default, Oct 31 2022, 22:44:31)
# [GCC 7.3.1 20180712 (Red Hat 7.3.1-15)] on linux
# Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy as np
>>> import pandas as pd
>>> from sklearn.ensemble import RandomForestClassifier
>>>
>>> x1 = np.random.normal(0, 1, 5000)
>>> x2 = np.random.normal(0, 1, 5000)
>>> x3 = np.random.normal(0, 1, 5000)
>>> y = np.random.choice([0, 1], 5000)
>>>
>>> df = pd.DataFrame({'x1': x1, 'x2': x2, 'x3': x3, 'y': y})
>>> X = df[['x1', 'x2', 'x3']]
>>> y = df['y']
>>>
>>> rf = RandomForestClassifier(n_estimators=100)
>>> rf.fit(X, y)
# RandomForestClassifier()
>>> rf.predict(X[:10])
# array([0, 1, 0, 0, 1, 1, 1, 0, 0, 1])
```

Tada! You've (technically) trained a machine learning model in the cloud. Since we've hit the pinnacle of EC2 use cases (😜), let's sever our SSH connection and terminate our instance.

{% include header-bash.html %}
```bash
exit
# logout
# Connection to ec2-xx-xx-xx-xxx.compute-1.amazonaws.com closed.
```

Now on our Instance page on the EC2 page, we can click on `Instance state` > `Terminate instance`. Note that we'll lose our Python libraries and the `calculate_mean.py` file, since the instance's data will be wiped as it's made available for someone else to use. If we want to hold onto the instance a little longer, we can click `Stop instance` instead.

### Beyond the basics
So we just created an EC2 instance, downloaded files from the internet, and ran some Python code. While this is awesome, we haven't experienced anything that we couldn't run on our own laptop, which is likely more powerful than a `t2.micro` server. **So what value are we really getting from EC2?**

The first thing to note is that **there are a wide range of EC2 options beyond the Free Tier.** If we wanted to run simulations for a research paper, we could simply select an EC2 instance with more CPU or GPU than our laptop. This would get the job done more quickly, especially if we don't have a decent computer or can't dedicate all of its resources to the simulations. (It would also prevent damaging your own laptop, which I accidentally did in college with a horribly inefficient R script!)

But more importantly, we need to remember that **EC2 instances are just _building blocks_.** For our research simulations, it may be more efficient to rent two or three instances and parallelize the calculations. If we're using an EC2 instance to host a Flask API for our website, when traffic grows we can simply duplicate the instance and add a load balancer to distribute traffic. Better yet, [we can automatically scale](https://aws.amazon.com/ec2/autoscaling/) the number of instances up and down to meet demand, letting us focus more on our actual application. Q4, while still a demanding time for retailers, has become so much more manageable with cloud computing.

All this abstraction is a tremendous step forward from the internet of the early 2000's. And yet... sometimes even a virtual server isn't flexible or scalable enough for our use case. In that case, we may want a "server-less" option like **Amazon Lambda.**

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/lambda-intro.png" alt="Amazon Lambda homepage">

## Lambda
### When is EC2 _not_ the right choice?
EC2 is fantastic for giving us all the flexibility we want to fine-tune our instance. We choose the hardware, the machine image, and many other options. (The [EC2 set up](#set-up) section in this post was dozens of lines long!)

But this puts the responsibility on _us_ to make sure we're configuring our instances properly. It may be straightforward if you're just running simulations, but what about a full-scale application with a database, caching layer, frontend, etc.? Scaling a complex service here can involve many moving pieces, even with some automated help.

One other issue is that **our instance is only accessible while it's running.** If we have some code that we want to execute infrequently, do we really want to keep an instance running? If this code is computationally heavy, we may need an instance that's just sitting around, costing us money but not really being used.



### What is Lambda?
In 2014, Amazon released **Lambda**, pushing the abstraction of the cloud to a new level. Lambda is _server-less_ computing. This is a bit misleading because there _is_ a server involved... it just becomes a black box abstracted away from you.

Lambda runs code in response to _events_ and automatically manages the underlying compute resources for you.

With an EC2 instance, you need to choose how much CPU and RAM you want the instance to have. Your instance will be there when you submit your requests, run your app, etc. But it'll still be quietly running in the background when you're not using it. This is often what you want $-$ you don't know when someone will make a request to your database, so you want the server to be ready at any time to serve that request. (Or for larger websites, there may never be a time where users _aren't_ making requests to your database. Think Amazon or Google displaying search results.)

But sometimes you don't want an instance to be running constantly in the background. You may have a tiny operation you want to run, like saving a log to S3, any time a user clicks on something. Or you want to write to a database or kick off a data processing pipeline whenever a file is uploaded to S3. For this, a lambda is the way to go.

So in Lambda, you just focus on the code. You upload it to create a lambda function. Get an ARN, which you can then reference from anywhere.
* Great for small one-off scripts.
* Have an API Gateway in front of Lambda, so any time you invoke a REST API on the API Gateway, the endpoint will point to a Lambda function.

Because abstracted away, a lot less configurability. Basically can just specify the amount of memory on the machine(s).

Downside:
* If Lambda is inactive, there's a brief warmup period. Subsequent calls will be fine. Not an issue with EC2, since it's always on.

### Creating a function
Let's set up a Lambda function that returns the mean of a set of numbers.

In the AWS Console, we start by navigating to the Lambda homepage. We then click the big orange `Create function` button. We'll stick with the "Author from scratch" option, then give our function a name (`calculate_mean`) and select the Python 3.9 runtime. Then we scroll down and click `Create function`.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/lambda-setup.png" alt="AWS Lambda setup">

We're then taken to the Lambda function page. Scrolling down to the `Code` tab, we see a basic template provided for our function:

{% include header-python.html %}
```python
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

And in the `Test` tab, we see a simple JSON input we can use to test our function.

```javascript
{
  "key1": "value1",
  "key2": "value2",
  "key3": "value3"
}
```

We'll want to change both of these for our "calculate mean" function. Let's start by changing the test input to an array of numbers, like below. Make sure to give your test a name (e.g., `my_array`) and hit `Save`. You should see a green banner at the top that says, _"The test event **my_array** was successfully saved."_

```javascript
{
  "nums": [1, 2, 3, 4, 5]
}
```

Now let's go back to the Lambda function and change it to the code below. Specifically, we remove the `json` import, extract the `nums` field from `event`, and change the return `body` field to calculate the mean. In a production setting, we'd want to add error handling for empty arrays, arrays with non-numbers, etc., but this is fine for now.

{% include header-python.html %}
```python
def lambda_handler(event, context):

  nums = event['nums']

  return {
    'statusCode': 200,
    'body': sum(nums)/len(nums)
  }
```

Save your function (⌘ + `s`, or `File` > `Save`), then click `Deploy`. You should see a green banner that says, _"Successfully updated the function **calculate_mean**."_ Now hit `Test`, which should generate some logs like below. The import thing is that the response `body` field should be the mean of the array of numbers in your test file (for us 3, the mean 1 to 5).

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/lambda-test.png" alt="Testing an AWS Lambda function">

Let's try this now from the **AWS CLI**. (If you haven't downloaded the CLI, you can follow [these steps]({{  site.baseurl  }}/AWS-Intro/#cli-command-line-interface).) Open a Terminal window, create an input JSON file, and send the file to your Lambda function. Lambda will return the response as a file, `output.json` here, which we can then view.

{% include header-bash.html %}
```bash
# Create input file
echo '{"nums": [1, 2, 3]}' > input.json

# Invoke Lambda function
aws lambda invoke \
--function-name calculate_mean \
--payload file://input.json \
--cli-binary-format raw-in-base64-out \
output.json

# {
#     "StatusCode": 200,
#     "ExecutedVersion": "$LATEST"
# }

# View the output
cat output.json
# {"statusCode": 200, "body": 2.0}
```

### Triggering via API Gateway
Congrats, we have a Lambda function! But we can only really interact with this function in the Lambda console and on our personal computer. What we really want is **to be able to _trigger_ this function from anywhere**. So back in the browser, let's scroll to the top of the `calculate_mean` function page, where we can see the triggers (and destinations) for our function.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/lambda-trigger.png" alt="Triggering an AWS Lambda function">

When we click on the `Add trigger` button, we're taken to a drop-down menu with an astonishing number of services, from [Alexa](https://aws.amazon.com/alexaforbusiness/), [AWS IoT](https://aws.amazon.com/iot/), and [DynamoDB](https://aws.amazon.com/dynamodb/), to non-AWS services like [Auth0](https://auth0.com/), [Datadog](https://www.datadoghq.com/), and [Shopify](https://www.shopify.com/).

Let's choose **[API Gateway](https://aws.amazon.com/api-gateway/)** to create an HTTP endpoint for our function. This will let us invoke our Lambda function from any code that can send an HTTP request. We'll select `Create a new API`, `HTTP API` for API type, and `Open` for Security. Then click `Add`.

<img src="{{  site.baseurl  }}/images/data_engineering/aws/compute/api-gateway.png" alt="AWS API Gateway setup">

We should now see API Gateway as a trigger for our `calculate_mean` function. We can click on the link, `calculate_mean-API`, to be taken to its API Gateway page. On the left, we can then navigate to `Develop` > `Integrations` and attach our Lambda function to the gateway.


We'll specify the array of numbers as a string parameter in the URL, like `calculate_mean?nums=1,2,3`. To access the values, we'll need to modify our function to pull out the numbers. We'll add a try-except block, where we first try pulling the `nums` param

{% include header-python.html %}
```python
def lambda_handler(event, context):

    # For GET requests
    try:
        nums = event["queryStringParameters"]["nums"]
        nums = nums.split(",")
        nums = [int(x) for x in nums]
    except:
        nums = event["nums"]

    return {
        'statusCode': 200,
        'body': sum(nums) / len(nums)
    }
```



## Conclusions



## Footnotes
#### 1. [Background](#background)
In researching for this post, I found plenty of interesting statistics about how expensive it can be for a popular website to be unresponsive or unavailable. Some of the more interesting stats:
* [Taobao](https://en.wikipedia.org/wiki/Taobao), a Chinese online shopping platform, had a 20-minute crash during Singles' Day in 2021 that may have cost [**several billion dollars**](https://queue-it.com/blog/singles-day-statistics/) in sales.
* A webpage that loads within two seconds has an average [bounce rate](https://en.wikipedia.org/wiki/Bounce_rate) of 9%. That number [**jumps to 38%**](https://www.pingdom.com/blog/page-load-time-really-affect-bounce-rate/) when the webpage takes five seconds to load.

#### 2. [Background](#background)
For hyper-growth early Amazon, the extra compute purchased during the holiday season would eventually just serve the normal business needs as the company grew. But for most companies, this extra compute would be a hindrance most of the year.

As a side note, there's a common narrative that AWS spun out of Amazon trying to utilize all this "extra compute" sitting around Q1-Q3. They had all these unused servers, so why not just let customers use them? My [favorite rebuttal](https://open.spotify.com/episode/14LmWeOMRZysw2i2vYSOuw?si=ce630660e3b44461&nd=1) of this narrative is that when Q4 came up the following year, Amazon obviously couldn't just terminate all those customers to take back their servers! Amazon would be stuck needing to buy a bunch more servers again.
