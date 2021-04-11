---
layout: post
title: 3 levels of technical abstraction when sharing your code
author: matt_sosna
---

![]({{ site.baseurl }}/images/projects/sharing/sharing_services.png)

I've been programming now for eight years, and it wasn't until *just months ago* that I was able to answer a question I've had this whole time: **"How do I share my project with someone?"**

When I say "project," I'm not talking about a single R script or a handful of bash commands $-$ even 22-year old me could figure out copy and paste! I mean a project that has _**several files**_, perhaps in _**multiple languages**_, with _**external dependencies**_. Do I just throw it all into a zip folder? How do I deal with new versions of languages and packages that aren't backwards-compatible? What if the person I'm sharing with doesn't know how to code at all?

The right way to share your code depends on how you want your recipient to interact with it. This post will cover three levels of abstraction when sharing your project: [**GitHub**](https://guides.github.com/introduction/flow/), [**Docker**](https://docs.docker.com/get-started/overview/), and [**Heroku**](https://www.heroku.com/what). We'll start with the lowest amount of hand-holding and end with completely abstracting away all code.

### Level 1: GitHub
_**What your recipient needs to do:** ensure their computer has the appropriate languages and packages, in the correct versions, that work for their operating system; actually know what code to execute to launch your app._

[GitHub](https://guides.github.com/activities/hello-world/) is the industry standard for hosting your code, tracking changes to it, and sharing it with others. By sending someone a URL to your repository, they can view your code, see the history of changes, save the code to their computer, and submit changes to you for approval.

Sharing code via GitHub is the least abstract of our three options $-$ **your recipient gets the raw code itself.** While this is great for getting another pair of eyes on the inner workings of your project, a GitHub repo by itself is actually pretty bare-bones for *using* your code. Without detailed instructions, your recipient may have no idea what your code is supposed to do or how to actually run it!

For example, take a look at [the GitHub repo for Python](https://github.com/python/cpython) (yes, *the* Python). Just looking at the files and folders, do you have any idea what commands to type to install Python? (Thankfully, their README has detailed instructions!)

![]({{ site.baseurl }}/images/projects/sharing/cpython_repo.png)

Aside from instructions on how to launch the project, it's also critical to list the *external dependencies* (e.g. Python libraries) and their versions. Even though you're sharing the raw code when you send someone a GitHub repo, your project *likely still won't work* on their computer if your code references libraries your recipient doesn't have installed.

That's why **it's critical to provide instructions for how to recreate the environment on your computer.** In fact, Python-based projects almost invariably start with the user creating a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) and installing the libraries provided in a `requirements.txt` file.

But even detailed instructions and a `requirements.txt` file may fall short if your project involves multiple languages and a database. This sample repo for a [vote tallying app](https://github.com/dockersamples/example-voting-app), for example, involves Python, [Node.js](https://nodejs.org/en/about/), [Redis](https://aws.amazon.com/redis/), [Postgres](https://www.postgresql.org/), and [.NET](https://dotnet.microsoft.com/learn/dotnet/what-is-dotnet). If you're willing to hide some of the code to make it easier to download your app, it may be worth moving to the next level of abstraction: Docker.

### Level 2: Docker
_**What your recipient needs to do:** have Docker installed, pull the relevant images, and run a [Docker Compose](https://docs.docker.com/compose/)._

[Docker](https://docs.docker.com/get-started/overview/) is a containerization service. A **container** is an isolated software environment, where its libraries, programs, *and even operating system* are independent from the rest of your computer. Think of a Docker container as a miniature computer inside your computer<sup>[[1]](#1-level-2-docker)</sup>.

When your project involves multiple services, each with its own dependencies, it's worth considering Docker. With Docker, you can download publicly-available software "snapshots," or **images**, from which you can create containers. If your app only runs on Python2, rather than go through the headache of convincing your recipient to downgrade their Python from v3 to v2, *just have them download the Python2.7 Docker image.*

As of April 2021, there are *over 5.8 million images* on Docker Hub that you can download for free. And there's no cost to experimentation: any images you download are quietly hidden from your computer's global environment until you call on them to create a container.

<img src = "{{ site.baseurl }}/images/projects/sharing/dockerhub.png" loading="lazy">

Even better, though, you can *create your own* images.


reate an **image** of a service like a Python Flask app, a snapshot of a computer environment where your app works, and then *share that image* with someone else. For an app with multiple components, you'd simply create images for each component, then write instructions for pulling them together with a [Docker Compose](https://docs.docker.com/compose/) file.



Here's what the code looks like for creating a Docker image for a simple Flask app:

{% include header-dockerfile.html %}
```dockerfile
# Use the Ubuntu OS Docker image
FROM ubuntu

# Update the Ubuntu packages
RUN apt-get update

# Install Python3, pip, and Flask
RUN apt-get install -y python3 python3-pip
RUN python3 -m pip install flask

# Copy the local app.py file to the Docker image directory
COPY app.py /opt/app.py

# Expose port 80 from the Docker container to the host
EXPOSE 80

# Run this code on starting the container
ENTRYPOINT python3 /opt/app.py
```

And here's what a Docker Compose file looks like for bundling that image with another one you create for a Postgres database. Notice how we're passing in environmental variables and specifying ports in this configuration file.

{% include header-yaml.html %}
```yaml
version: "3"
services:
  db:
    image: postgres:9.4
    environment:
    	POSTGRES_USER: "postgres"
    	POSTGRES_PASSWORD: "postgres"

  flask:
    image: my-flask-app
    ports:
      - 5000:80
```





### Level 3: Heroku
_**What your recipient needs to do:** click on a URL._





## Conclusions
These things aren't exclusive! In fact, I recommend sharing all of them with your user: the GitHub repo for in-the-weeds code, the Dockerfile for a quick execution on your machine, and Heroku if you just want to see the final product.


Commonality in Docker & Heroku: needing to know Flask. Honestly, learning Flask was a gamechanger for me.


## Docker
Technical requirements of user: medium
* They don't necessarily need to install all the components. But they at least need to have Docker on their computer, and then they have to pull the image and run a container. Probably easier with the right instructions
  - I guess Docker Compose would help here...

## Footnotes
#### 1. [Level 2: Docker](#level-2-docker)
Any time you talk about Docker, you probably need the obligatory disambiguation from [virtual machines](https://www.vmware.com/topics/glossary/content/virtual-machine). While a Docker container is isolated from the rest of your computer (and other Docker containers unless you explicitly link them), containers *do* share host resources such as RAM and CPU, as well as use the same host [kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)). If you don't specify limits, a container can happily suck up CPU and slow down all containers around it.

A virtual machine, on the other hand, has its own RAM and CPU and is *truly* isolated. Docker containers are a lot "lighter" than virtual machines in that they don't require an independent operating system and resources.

When you run a Docker container with a Linux operating system on your Windows or Mac computer, Docker actually runs the container [on a Linux virtual machine](https://www.docker.com/blog/docker-for-mac-windows-beta/).
