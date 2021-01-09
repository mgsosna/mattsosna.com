---
layout: post
title: How to enter data science - 5. The people
title-clean: How to enter data science <div class="a2">5. The people</div>
author: matt_sosna
summary: The personal and interpersonal skills needed to succeed in data science
image: ""
---

So far, we've covered the technical side to data science: [statistics]({{  site.baseurl  }}/DS-transition-2), [analytics]({{  site.baseurl  }}/DS-transition-3), and [software engineering]({{  site.baseurl  }}/DS-transition-4). But no matter how talented you are at crunching numbers and writing code, your *effectiveness* as a data scientist is limited if you chase questions that don't actually help your company, or you can't get anyone to incorporate the results of your analyses. Similarly, how do you stay motivated and relevant in a field that's constantly evolving?

In this post, we'll outline the _**business**_ and _**personal**_ skills needed to translate your technical skills into impact. We'll first focus on [business skills](#making-sense-of-business-sense) before turning to personal skills.

### Table of contents
* Making sense of business sense
  - Optimizing resource allocation
  - Empowering coworkers
  - Understanding the market
* The `self` parameter

---
**How to enter data science:**
1. [The target]({{  site.baseurl  }}/DS-transition-1)
2. [The statistics]({{  site.baseurl  }}/DS-transition-2)
3. [The programming]({{  site.baseurl  }}/DS-transition-3)
4. [The engineering]({{  site.baseurl  }}/DS-transition-4)
5. **The people**

---

## Making sense of business sense
Data science is full of tempting rabbit holes. Our code works fine, but what if we added a way to automate tuning model [hyperparameters](https://machinelearningmastery.com/difference-between-a-parameter-and-a-hyperparameter/)? Maybe the stakeholders would be more engaged if we built a better way to visualize the [high-dimensional vector space](https://towardsdatascience.com/lets-understand-the-vector-space-model-in-machine-learning-by-modelling-cars-b60a8df6684f) of our NLP model. Nobody asked for it, but what if we built a sleek dashboard for our data quality outputs so you could click buttons instead of needing to write [SQL]({{  site.baseurl  }}/DS-transition-4/#sql)?

The confusing thing is that **while there usually _is_ some business value at the end of the rabbit hole, it's often not worth pursuing.** Sure, a model that is more accurate or easy to understand will probably help your company in some way. But is this the [highest-leverage use of your time](#optimizing-resource-allocation)? Can you understand your coworkers' needs and [communicate how this project will empower them](#empowering-coworkers)? And is this project addressing [an unmet need in your company's market](#understanding-the-market), or is it a "nice to have"? We'll explore these ideas in the rest of this section.

### Optimizing resource allocation
Here's an example of a dilemma you may face as a data scientist. Your company, a shoe retailer, asks you to forecast sales in New York next quarter. After a month, you present what you have so far $-$ an [ARIMA model](https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/) with an [RMSE](https://www.statisticshowto.com/probability-and-statistics/regression-analysis/rmse-root-mean-square-error/) of about 5,000. While this is pretty good, you've identified two additional [exogenous variables](https://towardsdatascience.com/time-series-forecasting-a-getting-started-guide-c435f9fa2216) that you believe can decrease error to 2,000! You end your presentation with a plan of attack for exploring and incorporating these variables.

To your surprise, your boss says no. The model's accuracy is acceptable, they say, and it's not worth the time (and risk) of exploring further. You're given a week to [productize](https://www.datapred.com/blog/productizing-machine-learning-models-what-is-required) your model, after which you'll start on a new project. You're confused and are sure your boss is making a mistake. How is it not worth just two weeks to potentially halve the model error? There's a real cost your company will pay by using less accurate projections!

**To understand your company's perspective, consider its ever-present need to optimally allocate resources.** Yes, a less accurate model means your company is using worse projections, which may result in less accurate decisions. <u><i>However, the cost of this inaccuracy is likely lower than the <a href="https://www.investopedia.com/terms/o/opportunitycost.asp">opportunity cost</a> of you not working on a different business need.</i></u>

In the context of the company's needs, perhaps the effort invested in the model so far represents the *point of maximum yield* in the graph below, or even just the *point of diminishing returns*. In other words, **your company is willing to pay the cost of a worse model if it means avoiding *a larger cost*,** such as [customer churn](https://blog.hubspot.com/service/what-is-customer-churn) due to errors in their orders. To your company, it'd be more valuable to stop your work on forecasting and instead turn you to data quality.

<center>
<img src = "{{  site.baseurl  }}/images/careers/DS-5/diminishing_returns.jpg" height="70%" width="70%">
</center>
<span style="font-size: 12px"><i>Source: [The Peak Performance Center](https://thepeakperformancecenter.com/business/strategic-management/the-law-of-diminishing-returns/law-of-diminishing-returns/)</i></span>

It's easy to get frustrated by being cut short on a project, especially if you've sunk time into it or have finally built up steam. It's important, though, to **separate your feelings about a project from your judgment on whether it's worth pursuing.** Focusing on how you can best benefit your company, rather than just pursuing questions you alone find interesting, will make you a far more effective employee.<sup>[[1]](#1-optimizing-resource-allocation)</sup>

The next sections will cover how to best help your company through [empowering coworkers](#empowering-coworkers) and [understanding the market](#understanding-the-market). A solid understanding here will enable more productive conversations with your boss, product manager, or other internal departments. It will also help build trust in data science initiatives you may bring to the table, as you will be able to better communicate how they will help the company.

### Empowering coworkers
People often don't need a slick machine learning model. Often, process automation is a huge deal.

A user-first approach. Putting aside your thoughts, what do your coworkers need to more effectively do their jobs? Are they bogged down in manually creating reports for customers? Are they spending a lot of time searching through data to find anomalies? Addressing these needs will go much further than implementing the latest cutting-edge machine learning.


#### Understanding coworker needs
Think from their perspective: what do they need to make their jobs easier?


#### Explainability
Being able to clearly and succinctly explain how models work is critical.


### Understanding the market

Don't stress about being an expert in this. But to vastly improve the value you can bring to your company, seek to understand the context your company is in. Look at what competitors' data science teams are doing. What are [best team practices at top companies](https://docs.microsoft.com/en-us/azure/machine-learning/team-data-science-process/overview)?



## The `self` parameter
We'll shift now from talking about business sense to talking about self $-$ how to *consistently deliver.*

There's not much I can say that people like Nir Eyal (Indistractable), James Clear (Atomic Habits), and plenty of others can do much better. But I can share, at least, some productivity tips that I think are applicable to data science.

For it to be impactful, it needs to be relevant. There's a philosophy/lifestyle for successful people in tech: you need to constantly be learning. There's a sort of humility in knowing that the in-demand tools of the day will keep changing. It's like resting on a slowly-moving treadmill... stop moving and you'll gradually slip away.


* Need to constantly be learning and improving
* New technologies and frameworks will come, and you'll need to learn them to stay relevant.


### CI: Continuous Improvement
Data science is constantly evolving. You need to keep learning.

[Julia](https://julialang.org/) in the future.

Armin Ronacher, the creator of Python's [Flask](https://flask.palletsprojects.com/en/1.1.x/) library, has even [moved on to the language Rust](https://www.youtube.com/watch?v=saW18UvYLQg).

* You need to love programming. For most of your day, for most of your days, you're going to be reading and writing code.
* You need to love learning. There is a staggering amount to programming languages and frameworks out there. There's also a huge number of ways to get a job done, ranging from barely getting the job done to being computationally optimized and able to handle any attempt at forcing an error. Like the Red Queen in *Alice and Wonderland*, you can't stay still - you need to always be learning. (Or you'll eventually end up only able to write code in increasingly esoteric situations, like Maryland's recent call for COBOL programmers...)



It's tempting to follow the path of least resistance as a data scientist. It's enjoyable to keep analyzing data, so let's run some more analyses. I like writing tests, so it's easy to justify refactoring an old repo. Maybe we want to read just a few more articles before we can really start on our thing.


In other words, *given the context the company is currently in, what's the best thing to do?*

This varies by industry and over time. Perhaps a competitor has just come out with a product that gives them an advantage, and you need to build a similar product to avoid losing customers.


### The data science vacuum

fall into the "data science vacuum," as I like to think of it. In the vacuum, we can just focus on the analysis and the code.

But the issue with the vacuum is that we lack the **context** for crunching our numbers.

ignore the interpersonal aspect of data science. Our job is to crunch the numbers, to parse the signals from the noise and uncover the truth. The truth should speak for itself

"Storytelling"

But in this post, we'll instead ask **what** tasks to focus on and **why**? What are the questions that actually help a business move forward?

### Table of contents
1. Critical thinking
  - Like with the statistics post, being able to identify the cause of trends. Parsing signals from noise


* Need to focus on what the business needs are
 - e.g. customers feel like they're not getting enough value from your product. So you need to make that value more visible. e.g. Can you quantify the benefits, such as savings, or increased revenue for them, relative to the cost of your product? Can you do this in a way that controls for external factors like seasonality (e.g. more people buy stuff in November/December)?


**Business skills:** knowing _**what**_ to do and _**why**_
**Personal skills:** knowing how to _**consistently deliver**_

Some thoughts:
* [Speed-accuracy tradeoff](https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-79948-3_1247) from neuroscience. **You need to operate with constraints in mind.** You likely don't have the time to deliver a perfect analysis. Diminishing returns.


* **Business**
- [ ] Strong ability to explain technical concepts
- [ ] Focus on how to best deliver business value <br><br>




### Final business thoughts
A word to the wise, though... programming skills are often easier to pick up than domain knowledge. There are dozens of resources out there for learning coding. Not so many for getting hands-on experience with Building Automation Systems, or legal documentation, or whatever. Think about what you would need a professional to teach you vs. what you can learn on your own.

## Personal skills


## Concluding thoughts
This series has covered a lot. We started by talking about [how to navigate the diversity of data science roles]({{  site.baseurl  }}/DS-transition-1) before going into detail on some useful technical skills: [statistics]({{  site.baseurl  }}/DS-transition-2), [analytics]({{  site.baseurl  }}/DS-transition-3), and [software engineering]({{  site.baseurl  }}/DS-transition-4). The last three posts covered **how** to accomplish a task as a data scientist.

## Footnotes
#### 1. [Optimizing resource allocation](#optimizing-resource-allocation)
It may sound like this section is arguing that <u><i>the work you want to do</i></u> and <u><i>what's best for the company</i></u> are two separate and irreconcilable worlds, which isn't necessarily the case. **If you're focused on delivering business value, i.e. doing work that truly drives positive change at your company, then these two worlds will neatly overlap.** The issue is if you want to *only* build machine learning models and [none of the steps *around* the models]({{  site.baseurl  }}/DS-transition-3/#machine-learning), such as cleaning data, building pipelines, and soliciting and incorporating feedback from users. Shifting your goal from doing "cool data science" to doing "*impactful* data science" will help your goals align with your company's.

But you also shouldn't expect your job to completely fulfill you professionally, and definitely not personally. When I wasn't getting as much teaching as I wanted after leaving academia, a former boss introduced me to the [Trilogy coding boot camp](https://www.trilogyed.com/programs/), where I now happily tutor. Indeed, this article by Kabir Sehgal [in the *Harvard Business Review*](https://hbr.org/2017/04/why-you-should-have-at-least-two-careers) argues that everyone should have at least *two* careers (!), as that lets you enjoy different jobs for what they *do* offer.
