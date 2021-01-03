---
layout: post
title: How to enter data science - <br>5. The people
author: matt_sosna
summary: The personal and interpersonal skills needed to succeed in data science
image: ""
---
No matter how technical skills you have, you're not that effective if you're chasing answers to questions that don't help the business. Similarly, getting people to actually adopt the results of your analyses will require significant interpersonal skills. This post will outline the _**business**_ and _**personal**_ skills needed to be successful as a data scientist.

---
**How to enter data science:**
1. [The target]({{  site.baseurl  }}/DS-transition-1)
2. [The statistics]({{  site.baseurl  }}/DS-transition-2)
3. [The programming]({{  site.baseurl  }}/DS-transition-3)
4. [The engineering]({{  site.baseurl  }}/DS-transition-4)
5. **The people**

---

## Non-machine learning
The last three posts were a deep dive on some technical skills for data science: [statistics]({{  site.baseurl  }}/DS-transition-2), [analytics]({{  site.baseurl  }}/DS-transition-3), and [software engineering]({{  site.baseurl  }}/DS-transition-4). With these under the belt, you should have a solid starting point for many data science roles.

But in this post, we'll instead ask **what** tasks to focus on and **why**? What are the questions that actually help a business move forward?

* Need to focus on what the business needs are
 - e.g. customers feel like they're not getting enough value from your product. So you need to make that value more visible. e.g. Can you quantify the benefits, such as savings, or increased revenue for them, relative to the cost of your product? Can you do this in a way that controls for external factors like seasonality (e.g. more people buy stuff in November/December)?


**Business skills:** knowing _**what**_ to do and _**why**_
**Personal skills:** knowing how to _**consistently deliver**_

## Table of contents
* [**Business sense**](#business-sense)
  - [ ] [Optimizing resource allocation](#optimizing-resource-allocation)
* [**Personal skills**](#personal-skills)


## Business sense
### Optimizing resource allocation
Here's an example of a dilemma you may face as a data scientist. Your company wants to build a model to forecast sales in New York next quarter. After a month, you present what you have so far $-$ an [ARIMA model](https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/) that is around 88% accurate. While this is pretty good, you've identified two additional [exogenous variables](https://towardsdatascience.com/time-series-forecasting-a-getting-started-guide-c435f9fa2216) that you believe can increase accuracy to 95%! You end your presentation with a plan of attack for exploring and incorporating these variables.

To your surprise, your boss says no. 88% is an acceptable accuracy, they say, and it's not worth the time (and risk) of exploring further. You're given a week to productize your model, after which you start on a new project. You're confused and are sure your boss is making a mistake. How is it not worth just two weeks to potentially create a better model? There's a real cost your company will pay by using less accurate projections!

**To understand your company's perspective, consider its ever-present need to optimally allocate resources.** Yes, a less accurate model means your company is making decisions on less accurate projections, which may mean worse sales. <u><i>However, the cost of this inaccuracy is likely lower than the <a href="https://www.investopedia.com/terms/o/opportunitycost.asp">opportunity cost</a> of not working on another business need.</i></u> In other words, your company is willing to pay the cost of a worse model if it means avoiding *a larger cost*, such as [customer churn](https://blog.hubspot.com/service/what-is-customer-churn) due to delays in their online orders. To your company, it's more valuable to stop your work on forecasting and instead turn you to data quality.

From your perspective, you might only be aware of the cost of the model accuracy, and the legitimate business costs of a less accurate model. But one challenge is that **you often don't have the whole picture.**

<center>
<img src = "{{  site.baseurl  }}/images/careers/DS-5/diminishing_returns.jpg" height="75%" width="75%">
</center>
<span style="font-size: 12px"><i>Source: [The Peak Performance Center](https://thepeakperformancecenter.com/business/strategic-management/the-law-of-diminishing-returns/law-of-diminishing-returns/)</i></span>

Some thoughts:
* [Speed-accuracy tradeoff](https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-79948-3_1247) from neuroscience. **You need to operate with constraints in mind.** You likely don't have the time to deliver a perfect analysis. Diminishing returns.


* **Business**
- [ ] Strong ability to explain technical concepts
- [ ] Focus on how to best deliver business value <br><br>


### Explainability
Being able to clearly and succinctly explain how models work is critical.




### Final business thoughts
A word to the wise, though... programming skills are often easier to pick up than domain knowledge. There are dozens of resources out there for learning coding. Not so many for getting hands-on experience with Building Automation Systems, or legal documentation, or whatever. Think about what you would need a professional to teach you vs. what you can learn on your own.

## Personal skills
For it to be impactful, it needs to be relevant. There's a philosophy/lifestyle for successful people in tech: you need to constantly be learning. There's a sort of humility in knowing that the in-demand tools of the day will keep changing. It's like resting on a slowly-moving treadmill... stop moving and you'll gradually slip away.

* You need to love programming. For most of your day, for most of your days, you're going to be reading and writing code.
* You need to love learning. There is a staggering amount to programming languages and frameworks out there. There's also a huge number of ways to get a job done, ranging from barely getting the job done to being computationally optimized and able to handle any attempt at forcing an error. Like the Red Queen in *Alice and Wonderland*, you can't stay still - you need to always be learning. (Or you'll eventually end up only able to write code in increasingly esoteric situations, like Maryland's recent call for COBOL programmers...)

* Need to constantly be learning and improving
* New technologies and frameworks will come, and you'll need to learn them to stay relevant.

## Concluding thoughts
This series has covered a lot. We started by talking about [how to navigate the diversity of data science roles]({{  site.baseurl  }}/DS-transition-1) before going into detail on some useful technical skills: [statistics]({{  site.baseurl  }}/DS-transition-2), [analytics]({{  site.baseurl  }}/DS-transition-3), and [software engineering]({{  site.baseurl  }}/DS-transition-4). The last three posts covered **how** to accomplish a task as a data scientist.

## Footnotes
