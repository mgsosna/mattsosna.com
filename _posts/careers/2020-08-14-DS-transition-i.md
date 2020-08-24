---
layout: post
title: How to enter data science I - identify the target
author: matt_sosna
summary: Data science is a vast field with roles ranging between stats-heavy and engineering-heavy, with a vast range of data sizes and complexity. This post will help identify what sort of role you'd really want.
image: "images/complexity_spectrum2.png"
---

## TODO: need to change this to be less academia-focused
**"I could always do data science if academia doesn't work out."** It's a recurring thought many graduate students and postdocs experience, especially if their work involves hearty servings of coding and statistics, the core elements of data science. Academics *are* highly sought-after for data science positions: if you're surviving the challenges of independent research, then you undoubtedly have the ability to _**distill interesting questions from large amounts of information**_, as well as _**the focus and analytical chops**_ to answer those questions.

But what necessary technical skills are you *not* picking up in your daily academic work? And perhaps more importantly, what *non-technical* skills are required to succeed in industry? This post will outline the hard and soft skills that will make you even more attractive as a candidate when applying to data science positions.

This post is the first in a series.
1. Identify the target
2. [Build up the skillset]({{ site.baseurl }}/DS-transition-ii)


## Table of contents
* [What is a data scientist?](#what-is-a-data-scientist)
  - [The scalpel versus the shovel](#the-scalpel-versus-the-shovel)
  - [How many cores?](#how-many-cores)
* [So what about you?](#so-what-about-you)

## What is a data scientist?
For this post to be helpful, we need to first define what we mean by data scientist. A strict definition is actually pretty elusive: thanks to the [explosion in interest in data science](https://insidebigdata.com/2018/08/19/infographic-data-scientist-shortage/) over the past decade, companies are happy to assign the "data scientist" label in job postings better titled statistician, data analyst, data engineer, machine learning engineer, or even software engineer. The internet abounds with great thought pieces carefully defining data scientist responsibilities<sup>[[1]](#footnotes)</sup>, so I'll keep things high-level for this post.

### The scalpel versus the shovel
Let's start with something I call the "analytics-engineering" spectrum. Note that I've purposely omitted several related occupations<sup>[[2]](#footnotes)</sup> to narrow in on what most differentiates data science from analytics and engineering.

![]({{ site.baseurl }}/images/careers/analytics-engineering.png)

I think of this spectrum as **"the scalpel versus the shovel."** An analyst carefully examines the data to find insights (**_scalpel_**), while the engineer builds infrastructure to store and move data (**_shovel_**). An analyst is hamstrung if they don't have the data they need, and their value is extinguished if the knowledge they produce isn't incorporated into business decisions or the product itself. An engineer enables the movement of data through an organization, though there's usually no expectation for them to draw any insights from that information.

Somewhere between these extremes lies the data scientist. A data scientist is often expected to _**both understand the data <u>and</u> build the infrastructure**_ to distribute insights to the rest of the organization. They may build a statistical model that accurately describes some data, for example, *and then* build a pipeline to populate a customer-facing dashboard with daily predictions from that model. Their product isn't just the knowledge or just the pipeline - it's some combination of both.

Expectations vary widely on where on this spectrum - _**as well as how much of the spectrum!**_ - a data scientist is expected to cover. A mature big-tech company likely has data scientists in specialized roles, for example working solely on writing more efficient deep learning algorithms. A younger company, meanwhile, will expect the data scientist to span most of the spectrum, and maybe even dabble in software engineering.


#### Example job posts
Here is a sample job posting from Yelp. The title is data scientist, and the position lies deep in the **analytics** side of the spectrum.

<img src="{{ site.baseurl }}/images/careers/ds_job1.png" align="center" height="75%" width="75%">

And here is a sample job posting from Tesla. Again the title is data scientist, but this time the position is heavy on the engineering.

<img src="{{ site.baseurl }}/images/careers/ds_job2.png" align="center" height="75%" width="75%">


### How many cores?
Another spectrum we need to briefly mention is the _**amount**_ and _**complexity**_ of data being processed, which determines the methods needed to derive insights. Any analysis in the heatmap below can fall under the umbrella of "data science," though the sophistication of coding ability needed varies from *almost none*, to years of experience with memory management, distributed computing, and linear algebra. Below, **warmer colors indicate greater computational complexity.**

<img src="{{ site.baseurl }}/images/careers/complexity_spectrum.png" height="55%" width="55%" align="left">

As you increase the **size of the dataset (x-axis)**, matrix operations like inverses and transposes in frequentist statistics become computationally heavy compared to the iterative methods of machine learning. Large datasets are also where we need to start thinking about [dividing our task among parallel computer cores](https://www.omnisci.com/technical-glossary/parallel-computing), renting [powerful servers in the cloud](https://en.wikipedia.org/wiki/Cloud_computing), and utilizing parts of the computer [normally reserved for rendering graphics](https://www.boston.co.uk/info/nvidia-kepler/what-is-gpu-computing.aspx). (Hopefully there are data engineers around to help!)

Similarly, as you increase the **complexity of the data (y-axis)**, you quickly increase the number of iterations an algorithm needs, or the number of calculations per iteration. This is where techniques like [deep learning](https://machinelearningmastery.com/what-is-deep-learning/) or [reinforcement learning](https://deepsense.ai/what-is-reinforcement-learning-the-complete-guide/) become necessary: to identify an animal in an image, a neural network has layers upon layers of functions that first identify lines, then layers that take that output and identify circles, then layers for faces, until many calculations later it matches the cat with examples in the data it was trained on. One image down, onto the next!

The red zone may seem appealing because bigger and more complex is always better, right? Well, there are definite drawbacks: for very large datasets, it's easy to find [spurious correlations](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4236847/), and ignoring fundamental stats principles still makes you reach [incorrect conclusions](https://www.kdnuggets.com/2016/07/big-data-trouble-forgot-applied-statistics.html). Meanwhile, for sophisticated methods like deep learning, explaining *how the model came to its conclusion* is [surprisingly difficult](https://hub.packtpub.com/improve-interpretability-machine-learning-systems/) and can lead to lack of faith in the conclusions.

Ultimately, though, you're likely to only use any of these red-zone methods in companies with access to boatloads of data. If there's no need for something complex, you'll likely find yourself forgoing the deep learning packages and instead cranking out linear and logistic regressions.

## So what about you?
The point of the last two sections is to show the vast range in:
1. Expectations on what level of **analytics and engineering** a data scientist will bring to the table
2. The **complexity and size** of datasets that can be addressed with data science methods

Much like how the term "engineer" encompasses such a wide range of occupations the term is almost meaningless without being more specific, "data scientist" is a catch-all phrase for a wide range of work. To figure out where on the data science spectrum you'd like to be, I'd ask yourself a few questions:

1. **How much do I care about statistical nuances like random effects and blocking?**
 - *Not at all, give me the determinism of code* --> + engineering
 - *I care a lot, and p.s. p-values are misleading!* --> + analytics <br><br>
2. **How much do I care about optimizing code to make it more efficient?**
 - *This function is 150 lines long - let's modularize that* --> + engineering
 - *Getting the stats right is more important than writing perfect code* --> + analytics <br><br>
3. **How much do I want to build a pipeline once the analysis is complete?**
 - *Actually, I care more about the pipeline than the analysis* --> + engineering
 - *I'd rather focus on making sure any conclusion I produce is accurate* --> + analytics <br><br>

**I lean towards analytics!**<br>
If you found yourself identifying more with the analytics answers, I'd focus on building **strong R and data visualization**, **good Excel**, and **decent SQL**. A major bonus would be dashboarding skills like [Shiny](https://shiny.rstudio.com/), [Tableau](https://www.tableau.com/), or [D3.js](https://d3js.org/). A crucial part of your job will be **communicating insights to stakeholders**, so you need to have expert-level skills in explaining your analyses and their conclusions. Your best bet for employers will be mature companies with established data pipelines and who have identified the need for dedicated analysts helping inform business decisions. As a next step, I'd highly recommend Cassie Kozyrkov's *Harvard Business Review* article ["What Great Data Analysts Do - And Why Every Organization Needs Them."](https://hbr.org/2018/12/what-great-data-analysts-do-and-why-every-organization-needs-them)

**I lean towards engineering!**<br>
If you found yourself identifying more with the engineering answers, I'd focus on building **strong Python and SQL.** If you want to work on huge datasets, consider adding in **Scala or Java**. If you want to be well-integrated with the software engineers in whatever team you join, be sure to add **JavaScript**. Your code will be your product, so you'll want to read up on [coding best practices](https://www.aversan.com/coding-standards-and-best-practices-2/) and maybe even a textbook or two. Being able to write efficient code in an array of languages will let you tackle a wide range of challenges - ideal for data and software engineering.

**I want it all!**
If you don't fall neatly in the pure analytics vs. pure engineering bucket, that's great! There are plenty of jobs out there with the right level of computational complexity and analytics vs. engineering you're looking for. No matter where on the spectrum you fall, though, I'd focus on leveling up your **Python and SQL**, as well as being able to identify relevant questions for whatever business you pursue. The data scientist that has the business sense to identify the right question to pursue, the analytical strength to find answers to those analyses, and the self-sufficiency to deploy the results of those analyses is considered a [tremendously valuable unicorn](https://hbr.org/2018/11/the-kinds-of-data-scientist).

## Coming up



## Footnotes
1. [[What is a data scientist?]](#what-is-a-data-scientist) Here are a few pieces that I think are particularly insightful.
  - Andrew Zola, *Springboard*: ["Machine Learning Engineer vs. Data Scientist"](https://www.springboard.com/blog/machine-learning-engineer-vs-data-scientist/)
  - Yael Gerten, *Harvard Business Review*: ["The Kinds of Data Scientist"](https://hbr.org/2018/11/the-kinds-of-data-scientist)
  - Cassie Kozyrkov, *Hackernoon*: ["Why businesses fail at machine learning"](https://hackernoon.com/why-businesses-fail-at-machine-learning-fbff41c4d5db) <br><br>

2. [[The scalpel versus the shovel]](#the-scalpel-versus-the-shovel) Machine learning engineers, computational social scientists, statisticians, deep learning researchers, business intelligence analysts... there's [a lot more](https://www.northeastern.edu/graduate/blog/data-science-careers-shaping-our-future/) we could add here, but our spectrum would start becoming two- or three-dimensional. For an alternate take, here are some interesting visuals I spliced together from a piece by [efinancialcareers](https://news.efinancialcareers.com/uk-en/3001517/data-science-careers-finance): <br>
  ![]({{ site.baseurl }}/images/careers/efinance_figure.png)
