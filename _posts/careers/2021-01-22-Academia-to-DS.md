---
layout: post
title: Transitioning to data science from academia
author: matt_sosna
summary: Academics have many valuable skills to succeed in data science, but some need to be cultivated. This post outlines the soft and hard skills needed for success.
image: "images/complexity_spectrum2.png"
---
**"I could always do data science if academia doesn't work out."** It's a recurring thought many graduate students and postdocs experience, especially if their work involves hearty servings of [programming]({{  site.baseurl  }}/DS-transition-3) and [statistics]({{  site.baseurl  }}/DS-transition-2), the core elements of data science. Academics *do* have many qualities that make them attractive candidates for data science positions, but there are *also* large holes in their skills that will prevent them from being hired straight off the bat.

This post will outline the skills needed to make the leap from the ivory tower to industry. We'll go light on the technical details or business acumen; for a deep dive on those skills, check out my five-part [how to enter data science series]({{  site.baseurl  }}/DS-transition-1). Especially if you're just starting to consider data science as a career, I highly recommend thinking about where your ideal role falls on the [analytics-engineering spectrum]({{  site.baseurl  }}/DS-transition-1/#the-scalpel-versus-the-shovel), which will help you identify which skills to prioritize learning.

## Table of contents
* [**What are we working with?**](#what-are-we-working-with)
  - [Where academics excel](#where-academics-excel)
  - [Where academics struggle](#where-academics-struggle)
* [**Tips for the transition**](#tips-for-the-transition)

## What are we working with?
### Where academics excel
Successful research is incredibly challenging. Making it through a Ph.D. (and beyond) requires significant mental and emotional growth. If you're surviving the challenges of independent research, then you undoubtedly have:
1. The ability to distill interesting questions from large amounts of information
2. The analytical chops to answer those questions
3. Extreme attention to detail
4. Strong planning and organization
5. Serious mental fortitude to push through (and learn from) failure

Many of the skills you gain in graduate school align nicely with what makes for a strong data scientist. In both cases, you need to think critically about what questions to ask, how to get data, and how to extract meaningful insights from that data. Both professions need to communicate and coordinate with stakeholders of varying backgrounds. Finally, both are expected to continually learn, and to innovate solutions when none already exist.

It's hard to overstate how valuable these skills are. **Many senior- or director-level data science positions *require* a Ph.D.** because of the rigor academic research brings to identifying ways to solve tough problems. Below are a few senior roles I found with five minutes of searching on Google, along with their expected education level. Maybe these requirements will loosen over the years as the field matures, but for now, having a Ph.D. is a *major* asset for your career progression as a data scientist.

![]({{  site.baseurl  }}/images/careers/Academia/lead_ds_roles.png)

### Where academics struggle
The attractive jobs above, however, **assume that you *unlearn* much of the mentality from grad school.** While the *skills* you gain in academia are incredibly valuable for data science, the *priorities* are often actually a detriment. Here's where I think academics often struggle when switching to roles outside academia.

1. **The speed-accuracy tradeoff.** Academia prioritizes precision to the tenth decimal place. The point of research, after all, is to *uncover the truth* no matter how long it takes. But 100% accuracy just isn't realistic for many companies, given their limited resources. "Good enough" can be a tough concept to swallow, and your workflow will likely need to shift to maximizing accuracy *as fast as possible* under limited time.

2. **Implementing the results of an analysis.** Unless you're in a data science role that's effectively still academia (e.g. [Mathematica](https://www.mathematica.org/), [Brookings](https://www.brookings.edu/)), it's not enough to just *generate knowledge.* You need to then convince stakeholders to adopt your results, which calls on an entirely separate set of [business skills]({{  site.baseurl  }}/DS-transition-5). If you work for a tech company, incorporating your results will also call for another entirely separate set of [software engineering skills]({{  site.baseurl  }}/DS-transition-4). These skills gaps can sneak up on you, and they're painfully visible $-$ the difference between a mediocre and stellar predictive model requires a trained eye, but anyone can see that your model isn't available to users weeks after you said it'd be.

3. **Focusing on team above self.** When you leave academia, you transition from maximizing *your personal* output, to maximizing *your team's* output. Yes, in academia you invest significant effort into the success of your collaborators and students. But your name is still front and center on any paper, poster, or seminar your coauthors produce. Outside of academia, you become a lot more anonymous. It can feel disheartening to have your name detached from your work, your contributions invisible to anyone outside your company. (And likely invisible to many within, too!) Similarly, it can be challenging to transition from the fierce independence of academic work to working on *literally the same codebase* with coworkers and needing to abide by [programming best practices]({{  site.baseurl  }}/DS-transition-4/#object-oriented-programming) and [product management](https://www.atlassian.com/agile/product-management), not just what worked for you in grad school.

These issues take time to overcome. Maybe you can easily turn off the "100% accuracy" mentality, but it'll take more than a few afternoons to pick up software engineering skills like [Git]({{  site.baseurl  }}/DS-transition-4/#version-control), [SQL]({{  site.baseurl  }}/DS-transition-4/#sql), and [working with APIs]({{  site.baseurl  }}/DS-transition-4/#interacting-with-apis). And while you're applying for jobs, it can be disorienting to have the impressive credential of a Ph.D. while simultaneously be outcompeted by fresh computer science or boot camp graduates. This next section will focus on how to smooth the transition into a new role.

## Tips for the transition
### The mentality
Regardless of where you're aiming on the [analytics-engineering spectrum]({{  site.baseurl  }}/DS-transition-1/#the-scalpel-versus-the-shovel), **there's a shift in how you view yourself as a coder** that's required for you to succeed in industry:

> **What you might be thinking:** <br>"I can code anything I want." <br><br>
> **What industry wants:** <br>"I can code anything someone asks me."

Especially in open-ended Ph.D. programs in the U.S., you have the flexibility to choose the research questions you pursue, as well as how you go about answering those questions. This makes it easy to gravitate towards questions and methods you're comfortable with and get _really good_ at a narrow set of skills. In a way, that's what a Ph.D. is all about: you choose a very precise question to answer, and you work until you know more about this sliver of knowledge than anyone else in the world.

**You don't have the luxury of a narrow skill set when you're a data scientist,** *especially* if you're at a smaller company. There's a term called ["full-stack"](https://www.w3schools.com/whatis/whatis_fullstack.asp) in software engineering $-$ it refers to programmers who can code professionally in both the [front-end and back-end environments](https://en.wikipedia.org/wiki/Front_end_and_back_end), which require entirely different languages, perspectives, and skill sets. Data science is like being a full-stack analyst: you need to be comfortable rotating between extracting insights from data and then building the infrastructure to communicate those insights (like pipelines and dashboards).

During your Ph.D., you're likely to have developed expert-level skills in extracting *certain types* of insights from data. Maybe you worked heavily with time series data, for example. Unless you want to only analyze time series data in your next role, you will need to get comfortable working with any type of data.

Check out Kaggle. Work on practice problems. Kind of like being an athlete.

During my Ph.D., I found it incredibly easy to stay in the areas of R and statistics that I already knew well. I didn't want to get out of my comfort zone, because it would require me to face the scary concept that I _didn't_ actually have that wide a grasp on stats and coding. Especially with a Ph.D., there are a lot of expectations on how much you're "supposed to" know or how smart you're supposed to be. But you need to remember that the Ph.D. is a very deep, narrow knowledge set, versus the broad knowledge needed for being a versatile data scientist.

### Applications
* Cutting publications from the CV is painful.
* Having a portfolio is important. It's easy to say "I know Python," but can you demonstrate that? Pick a few projects and then have fun building something.  

## Conclusions
Finally, you don't have to do this alone. There are several coding boot camps aimed specifically at Ph.Ds looking to enter industry, such as the [Insight Fellowship](https://insightfellows.com/data-science) and [Data Incubator](https://www.thedataincubator.com/fellowship.html). While you likely have the discipline to teach yourself the skills you need, it can be challenging to *identify* what these skills exactly are, and it's *far* more time-efficient to have professionals teach you.
