---
layout: post
title: How to enter data science - <br>2. Master the analytics
author: matt_sosna
summary: The technical skills needed to succeed in data science
image: ""
---
In [the last post]({{ site.baseurl }}/DS-transition-1), we defined the key elements of data science as 1) deriving insights from data and 2) communicating those insights to others. Despite the huge diversity in how these elements are expressed in actual data scientist roles, **there is a core skill set** that will serve you well no matter where you go. The remaining posts in this series will define and explore these skills in detail.

The next three posts will cover the _<u>technical</u>_ skills needed to be successful as a data scientist: the statistics (this post), the [programming]({{  site.baseurl  }}/DS-transition-3) and [the engineering]({{  site.baseurl  }}/DS-transition-4). The [final post]({{  site.baseurl  }}/DS-transition-5) will cover the _<u>business</u>_, _<u>personal</u>_, and _<u>interpersonal</u>_ skills needed to succeed. Consider the distinction here as **knowing _how_ to do it** (technical) versus **knowing _what_ to do and _why_** (business, personal, and interpersonal). Let's get started!

---
**How to enter data science:**
1. [The target]({{  site.baseurl  }}/DS-transition-1)
2. **The statistics**
3. [The programming]({{  site.baseurl  }}/DS-transition-3)
4. [The engineering]({{  site.baseurl  }}/DS-transition-4)
5. [The people]({{  site.baseurl  }}/DS-transition-5)

---

## Becoming one with the machine
Data science is a broad field that is still iterating towards a solid distinction from data analytics, data engineering, and software engineering, so it's hard to create a definitive skill set that's applicable for all data scientist roles. Someone working all day with building statistical models out of spreadsheets, for example, is going to need a different set of skills than someone improving autonomous vehicles!

But consider this learning checklist as a set of fundamental skills that will get you started for your role, no matter where you go. We'll cover the **Inferential Statistics** and **Programming** sections in this post; in [the next post]({{  site.baseurl  }}/DS-transition-3), we'll cover **Software Engineering.**

* **Inferential Statistics**
- [ ] [Sampling and bias](#sampling-and-bias)
- [ ] [Model fundamentals](#model-fundamentals)
- [ ] [Linear regression](#linear-regression)
- [ ] [Logistic regression](#logistic-regression) <br><br>
* **Programming**
- [ ] [Dataframes](#dataframes) and [arrays](#arrays)
- [ ] [Visualizations](#visualizations)
- [ ] [Descriptive statistics](#descriptive-statistics)
- [ ] [Working with dates](#working-with-dates)
- [ ] [Machine learning](#machine-learning) <br><br>
* **Software engineering**
- [ ] [SQL]({{  site.baseurl  }}/DS-transition-3/#sql)
- [ ] [Interacting with APIs]({{  site.baseurl  }}/DS-transition-3/#interacting-with-apis)
- [ ] [Version control]({{  site.baseurl  }}/DS-transition-3/#version-control)
- [ ] Object-oriented programming (i.e. classes, module imports)
- [ ] Virtual environments
- [ ] Writing tests
- [ ] Servers and deployment <br><br>
{: style='list-style-type: none'}

## Inferential Statistics
Inferential statistics is the discipline of drawing inferences about a _**population**_ from a _**sample.**_ We rarely have data on every single individual, decision, or atom in whatever process we're examining. Rather than throw in the towel on understanding anything around us, we can turn to statistics for tools that translate data on *our sample* into inferences on *the entire population*. Inferential statistics is used all the time to make sense of the world, from [weather forecasts](https://thisisstatistics.org/beyond-barometers-how-statisticians-help-to-predict-the-weather/) to [opinion polls](https://www.math.arizona.edu/~jwatkins/505d/Lesson_12.pdf) and [medical research](https://emj.bmj.com/content/17/5/357), and **thinking carefully about how to generalize from our data to the broader world is a critical skill for data science.** We'll start with some fundamentals of statistics before diving deep into programming.

### Wait, do I actually need to learn stats?
In the era of big data and machine learning, it's tempting to shrug off learning any stats. When the average laptop is [*2 million times* more powerful](https://www.realclearscience.com/articles/2019/07/02/your_mobile_phone_vs_apollo_11s_guidance_computer_111026.html) than the computer that got us to the moon<sup>[[1]](#footnotes)</sup>, it's easier than ever to throw a dataset into a deep learning algorithm, get a coffee while it crunches the numbers, and then come back to some model that always delivers world-shattering insights. Right? Well... not quite.<sup>[[2]](#footnotes)</sup>

The following quote usually refers to the *quality of data* going into an analysis or prediction, but I think it's an apt summary for why we need to care about stats as well.

> "Garbage in, garbage out."

**A model is a simplified representation of reality.** If that representation is flawed, the picture it paints can very easily be nonsensical or misleading. The reason people dedicate their lives to researching statistics is that **condensing reality down to models is incredibly challenging, yet necessary.**

It's usually impossible or impractical to process every detail before making a decision; our brains, for example, constantly use [processing short-cuts](https://jamesclear.com/schemas) to interpret the world faster. The question isn't how to make a model that isn't flawed; it's how to ensure the flaws don't affect the conclusions. As statistician George Box ([allegedly](https://en.wikipedia.org/wiki/All_models_are_wrong)) said:

> "All models are wrong, but some are useful."

The difference between a model that's *wrong but useful* versus one that's *just wrong* is often hidden in the details. **Unlike in programming, hitting "run" on a half-baked model *will* output a result that qualitatively looks identical to a highly-polished, accurate model.** But whether the model represents *the reality we actually live in* requires a trained eye.  

### Ok, so how much stats do I actually need?
Data science roles vary tremendously in the depth of statistical knowledge expected, so the following concepts should serve as a *starting point*. If your role involves lots of data analysis, I think the more statistical knowledge the better, as you'll want as many tools as you can get for parsing *signals* from *noise* in your data.

Especially if your analyses inform major decisions like public policy or the direction your company takes, you'll want to account for nuances like [random effects](https://www.theanalysisfactor.com/understanding-random-effects-in-mixed-models/), [regression discontinuities](https://en.wikipedia.org/wiki/Regression_discontinuity_design), [nonparametric](http://mlss.tuebingen.mpg.de/2015/slides/ghahramani/gp-neural-nets15.pdf) or [Bayesian](http://www.scholarpedia.org/article/Bayesian_statistics) alternatives to [frequentism](https://en.wikipedia.org/wiki/Frequentist_inference), and more. Similarly, if you're in a field where you actually *do* have access to all the data in a process, such as analyzing [Internet of Things (IoT)](https://www.zdnet.com/article/what-is-the-internet-of-things-everything-you-need-to-know-about-the-iot-right-now/) sensor data, then you'll want to dive deep on [time series analysis](https://www.statisticssolutions.com/time-series-analysis/) and [anomaly detection](https://www.anodot.com/blog/what-is-anomaly-detection/).

Regardless, the fundamentals here are likely enough to cover the stats you'll need for jobs on most of the [analytics-engineering spectrum]({{  site.baseurl  }}/DS-transition-1#the-scalpel-versus-the-shovel).

### Sampling and bias
<img align="right" src="https://i.imgur.com/JbXsczj.png" height="40%" width="40%">
One of the key concepts to understand is that when you collect data, you are **sampling** from a **population.** (Except, of course, in a case like IoT mentioned above.) Because we're condensing a large, diverse body down into a relatively small sample, we need to make sure the sample actually looks like a microcosm of the broader population.

In the graphic on the right, for example, our sample isn't really representative of the population $-$ several colors aren't present at all! We can't run an analysis on this sample and then generalize to the population; **we can only generalize to red, orange, yellow, and green.** No matter how perfectly we model our sample data, our model's scope is trapped. If we try to comment on the broader population, we'll find that our seemingly accurate model suddenly makes embarrassingly inaccurate predictions.

A recent example of this is the 2020 U.S. election forecasts. After President Trump's surprise 2016 victory that [defied the vast majority of public opinion polls](https://www.voanews.com/usa/us-politics/election-experts-puzzled-over-surprise-trump-victory), pollsters spent years tweaking their models, fixing blindspots in preparation for a 2020 redemption. Yet, as states started releasing results on November 3, we found ourselves yet again watching [polls underestimate the number of Trump voters](https://www.scientificamerican.com/article/why-polls-were-mostly-wrong/).

David Shor, the former head of political data science at [Civis Analytics](https://www.civisanalytics.com/), believes the predictions were so off because [**their underlying samples are not representative of American voters.**](https://www.vox.com/policy-and-politics/2020/11/10/21551766/election-polls-results-wrong-david-shor) In short, the people who respond to polls tend to score high on social trust, which the [General Social Survey](https://gssdataexplorer.norc.org/variables/441/vshow) indicates represents only 30% of Americans. Until 2016, this group used to vote comparably to low-trust voters who didn't pick up the phone for pollsters $-$ now, low-trust voters tend to vote more conservatively and are hence underrepresented in the sample.

If we're aware of these discrepancies, we can try to implement fixes such as [differentially weighting classes in the sample](https://www.researchgate.net/post/How-can-I-deal-with-uneven-sample-sizes-in-my-study). But the best remedy is to make sure the sample [is truly representative of the broader population](https://www.healthknowledge.org.uk/public-health-textbook/research-methods/1a-epidemiology/methods-of-sampling-population).

### Model fundamentals
Let's say we're confident our sample is representative of the broader population. Once we've built a model, two fundamental components to understand are **coefficients** and **residuals.**

#### Coefficients
Let's say we have a linear model that looks like this:

$$y = \beta_0 + \beta_1x_1 + \beta_2x_2$$

In plain English, this means $y$ is equal to:
* Our intercept $\beta_0$...
* ...plus $\beta_1$ times $x_1$...
* ...plus $\beta_2$ times $x_2$.



#### Residuals
<img src="{{  site.baseurl  }}/images/careers/residual.png" align='right' height='60%' width='60%'>
In a classical statistical model, as well as when evaluating a machine learning model accuracy, we can compare the model's predictions to the actual values. In other words, given the inputs to the model, what did it think the output would be, versus what the output actually was? The **residual** is the distance between the predicted vs. actual values.

The graphic on the right shows this well. The linear model's predictions are the red line. The distance between the predictions and the actual values are the residuals. The goal is to build a model that minimizes the residuals.





### Linear regression
Let's try this: $A$.

You should be able to explain the following equation again and again:

$$ h(x) = \sum_{j=1}^{n}\beta_jx_j $$

**Linear regression** is one of the most common statistical model you'll encounter in industry, and you need to understand its ins and outs. Make sure you have a solid understanding of what **residuals** are, **least squared error**, and $$R^2$$.

### Logistic regression
The below equation for logistic regression might not come up as frequently, but you should understand it and be able to explain it, as well.

$$ P(y) = \frac{1}{1+e^{-h(x)}} $$

For least squares:
$$ y = \sum_{i=1}^{m}(h(x_i)-y_i)^2 $$



## Concluding thoughts


## Footnotes
1. [[Wait, do I actually need to learn stats?]](#wait-do-i-actually-need-to-learn-stats) The [Apollo Guidance Computer](https://www.realclearscience.com/articles/2019/07/02/your_mobile_phone_vs_apollo_11s_guidance_computer_111026.html) had 4.096 KB of RAM. An average laptop in 2020 has 8 GB, which is 1.95 million times more powerful. If we use a [memory-optimized AWS EC2 instance](https://aws.amazon.com/ec2/instance-types), we have access to upwards of _**1.57 billion**_ times more compute than the Apollo mission. And all to identify pictures of cats...

2. [[Wait, do I actually need to learn stats?]](#wait-do-i-actually-need-to-learn-stats) Rather than removing the need for statistics, big data *exacerbates* common statistical risks. I've linked some further reading below.
* American Statistical Association: [Statistics and Big Data](http://higherlogicdownload.s3.amazonaws.com/AMSTAT/UploadedImages/49ecf7cf-cb26-4c1b-8380-3dea3b7d8a9d/BigDataOnePager.pdf)
* National Science Review: [Challenges of Big Data Analysis](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4236847/)
