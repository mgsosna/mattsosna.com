---
layout: post
title: Transitioning to data science from academia
author: matt_sosna
summary: Academics have many valuable skills to succeed in data science, but some need to be cultivated. This post outlines the soft and hard skills needed for success.
image: "images/complexity_spectrum2.png"
---
**"I could always do data science if academia doesn't work out."** It's a recurring thought many graduate students and postdocs experience, especially if their work involves hearty servings of [programming]({{  site.baseurl  }}/DS-transition-3) and [statistics]({{  site.baseurl  }}/DS-transition-2), the core elements of data science. Academics *do* have many qualities that make them attractive candidates for data science positions, but there are *also* large holes in their skills that can deter them from being hired straight off the bat.

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

3. **Focusing on team above self.** When you leave academia, you transition from maximizing *your personal* output, to maximizing *your team's* output. Yes, in academia you invest significant effort into the success of your collaborators and students. But your name is still front and center on any paper, poster, or seminar your coauthors produce. Outside of academia, you become a lot more anonymous. It can feel disheartening to have your name detached from your work, your contributions invisible to anyone outside your company. (And likely invisible to many within, too!) Similarly, it can be challenging to transition from the fierce independence of academic work to working on *literally the same codebase* with coworkers and needing to abide by [programming best practices]({{  site.baseurl  }}/DS-transition-4/#object-oriented-programming) and [product management](https://www.atlassian.com/agile/product-management), not just what worked for you personally in grad school.

4. **Working on something you don't want to do.** The unbridled freedom in academia, especially for U.S. programs, means you're free to pursue the questions *you* most find interesting. If you can get funding for your idea, there's no one stopping from you from charting your own intellectual path. In industry, meanwhile, your hands are tied firmly to the questions your organization has decided are worth pursuing. You have some say in this, of course, but if your boss puts their foot down on another linear regression, that's what you're doing.

These issues take time to overcome. Maybe you can easily turn off the "100% accuracy" mentality, but it'll take more than a few afternoons to pick up software engineering skills like [Git]({{  site.baseurl  }}/DS-transition-4/#version-control), [SQL]({{  site.baseurl  }}/DS-transition-4/#sql), and [working with APIs]({{  site.baseurl  }}/DS-transition-4/#interacting-with-apis). And while you're applying for jobs, it can be disorienting to have the impressive credential of a Ph.D. while simultaneously be outcompeted by fresh computer science or boot camp graduates. This next section will focus on how to smooth the transition into a new role.

## Tips for the transition
### The mentality
When you enter the job market, it's useful to think of yourself as **<i><u>selling your labor</u></i> to an employer.** What do you have to sell? During your Ph.D., you likely developed expert-level skills in performing *certain kinds of analyses* on *certain kinds of data.* Maybe you're really good at finding patterns in astronomical radio waves, for example. But who's willing to pay for that skill? And even if NASA *is* hiring, how do you feel about continuing the same work you just did for half a decade?

If you love your research, want to continue it, and there are non-academic employers willing to pay for it, then you're in the great position of already being fully qualified for your first role out of academia. Congrats! But for the rest of us, there's a lot of catching up to do to become competitive applicants. Regardless of where you're aiming on the [analytics-engineering spectrum]({{  site.baseurl  }}/DS-transition-1/#the-scalpel-versus-the-shovel), **there's a shift in how you view yourself as a coder** that's required for you to succeed in industry:

> **What you might be thinking:** <br>"I can code anything I want." <br><br>
> **What industry wants:** <br>"I can code anything anyone asks me."

When you have the flexibility to choose the research questions you pursue, as well as how you go about answering those questions, it's easy to gravitate towards questions and methods you're comfortable with. In a way, a Ph.D. is all about getting _really good_ at a narrow set of skills: you choose a very precise question to answer, and you work until you know more about this sliver of knowledge than anyone else in the world.

**You (usually) don't have the luxury of a narrow skill set when you're a data scientist,** *especially* if you're at a smaller company. There's a term called ["full-stack"](https://www.w3schools.com/whatis/whatis_fullstack.asp) in software engineering $-$ it refers to programmers who can code professionally in both the [front-end and back-end environments](https://en.wikipedia.org/wiki/Front_end_and_back_end), which require entirely different languages and perspectives. Data science is like being a full-stack analyst: you need to be comfortable rotating between *extracting insights from data* and then *building the infrastructure to communicate those insights* (such as dashboards and automated scripts).

During my Ph.D., I found it incredibly easy to stay in the areas of R and statistics that I already knew well. **I didn't want to get out of my comfort zone, because it would require me to face the scary concept that I _didn't_ actually have that wide a grasp on stats and coding.** I felt like since I was using R and stats in my thesis, others expected me to be an expert. Taking formal stats or R classes would therefore violate these expectations and expose me as *not* being an expert. Ironically, all this fear did is stop me from actually developing a solid, well-rounded understanding of R and stats. I also doubt anyone truly cared about how much I knew anyway.

Don't make the same mistake I did $-$ embrace not knowing everything, and get started on filling in the knowledge gaps. You need [a wide range of skills]({{  site.baseurl  }}/DS-transition-2) to be an effective data scientist, and those skills need to be maintained and polished. I recommend checking out the datasets and challenges on [Kaggle](https://www.kaggle.com/), [HackerRank](https://www.hackerrank.com/dashboard), and [Reddit](https://www.reddit.com/r/dailyprogrammer/). But most importantly, **create a coding portfolio on GitHub** and work through some projects on your own.

### Applications
Tailor your application to each company you apply to. Always include a cover letter.

* Cutting publications from the CV is painful.
* Having a portfolio is important. It's easy to say "I know Python," but can you demonstrate that? Pick a few projects and then have fun building something.  

## Conclusions
Finally, you don't have to do this alone. There are several coding boot camps aimed specifically at Ph.Ds looking to enter industry, such as the [Insight Fellowship](https://insightfellows.com/data-science) and [Data Incubator](https://www.thedataincubator.com/fellowship.html). While you likely have the discipline to teach yourself the skills you need, it can be challenging to *identify* what these skills exactly are, and it's *far* more time-efficient to have professionals teach you.
