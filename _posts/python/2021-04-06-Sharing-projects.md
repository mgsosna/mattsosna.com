---
layout: post
title: 3 levels of technical abstraction when sharing your code
author: matt_sosna
---

![]({{ site.baseurl }}/images/projects/sharing/sharing_services.png)

I've been programming now for eight years, and it wasn't until *just months ago* that I was able to answer a question I've had this whole time: **"How do I share my project with someone?"**

When I say "project," I'm not talking about a single R script or a handful of bash commands $-$ even 22-year old me could figure out copy and paste! I mean a project that has _**several files**_, perhaps in _**multiple languages**_, with _**external package dependencies**_. Do I just throw it all into a zip folder? How do I deal with new versions of languages and packages that aren't backwards-compatible? What if the person I'm sharing with doesn't know how to code at all?

The right answer, of course, depends on how technically savvy your recipient is. This post will cover three levels of abstraction when sharing your project: [**GitHub**](https://guides.github.com/introduction/flow/), [**Docker**](https://docs.docker.com/get-started/overview/), and [**Heroku**](https://www.heroku.com/what). We'll start with the lowest amount of hand-holding and end with completely abstracting away all code.

### Level 1: GitHub
_**What your recipient needs to do:** ensure their computer has the appropriate languages and packages, in the correct versions, that work for their operating system; actually know what code to execute to launch your app._

With GitHub, you basically just `git push` your code to a public repository and send your friend the URL. This is the most "raw" - it's just the code itself. Without a detailed README, there's no instructions for your friend for how to use your code, what commands to run, etc.

Want that feeling of being lost? Open [the GitHub repo for Python](https://github.com/python/cpython) (yes, *the* Python), look at the files, and try to guess what command to type to install Python. (Thankfully, the README has detailed installation instructions!)





### Level 2: Docker
_**What your recipient needs to do:** have Docker installed, pull the relevant image(s), and run a Docker Compose._

A simple email starts falling short if your project has **dependencies.** If that R script requires the `dplyr` package and your colleague doesn't have that installed, the script won't work for them. So now, maybe you add a README text file with some instructions that say "Download `dplyr` before running!"

But then what if the latest version of `dplyr` made some breaking changes? (Think about how many headaches the Python2 -> Python3 conversion caused.)


### Level 3: Heroku
_**What your recipient needs to do:** click on a URL._


How can we make it easy for them?

This is about as far as I got before I hit a wall.


The problem: you have a project that you want to share with someone.
* If it's really simple: you can just email them the `.r` or `.py` script
* If it's a little more complicated: create a zip file with the `.r` script, the CSV, and maybe a little README text file.

This works ok if your project has few dependencies. Let's say that in R you're using the `tidyverse` package, or in Python you're using `pandas`. These dependencies are something on *your computer* that isn't necessarily on *someone else's computer*. (We're not even thinking about whether they have R/Python installed in the first place $-$ if they don't, jump to \#3 below - Heroku.)




Commonality in Docker & Heroku: needing to know Flask. Honestly, learning Flask was a gamechanger for me.

## GitHub
Technical requirements of user: high
* They need to actually install all the stuff. If you're using a DB, they need to install Postgres or MySQL, then start it up, etc.
* If it's more than a little complicated, need lots of documentation

## Docker
Technical requirements of user: medium
* They don't necessarily need to install all the components. But they at least need to have Docker on their computer, and then they have to pull the image and run a container. Probably easier with the right instructions
  - I guess Docker Compose would help here...

## Heroku
Technical requirements of user: none
