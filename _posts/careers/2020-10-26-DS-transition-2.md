---
layout: post
title: How to enter data science - <br>2. The statistics
author: matt_sosna
summary: The analytical skills needed to succeed in data science
image: "images/careers/two_models.png"
---
In [the last post]({{ site.baseurl }}/DS-transition-1), we defined the key elements of data science as 1) deriving insights from data and 2) communicating those insights to others. Despite the huge diversity in how these elements are expressed in actual data scientist roles, **there is a core skill set** that will serve you well no matter where you go. The remaining posts in this series will define and explore these skills in detail.

The next three posts will cover the _<u>technical</u>_ skills needed to be successful as a data scientist: the statistics (this post), [the programming]({{  site.baseurl  }}/DS-transition-3) and [the engineering]({{  site.baseurl  }}/DS-transition-4). The [final post]({{  site.baseurl  }}/DS-transition-5) will cover the _<u>business</u>_, _<u>personal</u>_, and _<u>interpersonal</u>_ skills needed to succeed. Consider the distinction here as **knowing _how_ to do it** (technical) versus **knowing _what_ to do and _why_** (business, personal, and interpersonal). Let's get started!

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

But consider this learning checklist as a set of fundamental skills that will get you started for your role, no matter where you go. We'll cover the **Inferential Statistics** section in this post, **Programming** in the [next]({{  site.baseurl  }}/DS-transition-3/), and **Software Engineering** in the [fourth]({{  site.baseurl  }}/DS-transition-4/).

* **Inferential Statistics**
- [ ] [Experimental design](#experimental-design)
- [ ] [Predictive modeling](#predictive-modeling)
- [ ] [Comparisons between groups](#comparisons-between-groups)
- [ ] [Measures of statistical significance](#measures-of-statistical-significance)
- [ ] [Model evaluation](#model-evaluation) <br><br>
* **Programming**
- [ ] [Dataframes]({{  site.baseurl  }}/DS-transition-3/#dataframes) and [arrays](#arrays)
- [ ] [Visualizations]({{  site.baseurl  }}/DS-transition-3/#visualizations)
- [ ] [Descriptive statistics]({{  site.baseurl  }}/DS-transition-3/#descriptive-statistics)
- [ ] [Working with dates]({{  site.baseurl  }}/DS-transition-3/#working-with-dates)
- [ ] [Machine learning]({{  site.baseurl  }}/DS-transition-3/#machine-learning) <br><br>
* **Software engineering**
- [ ] [SQL]({{  site.baseurl  }}/DS-transition-4/#sql)
- [ ] [Interacting with APIs]({{  site.baseurl  }}/DS-transition-4/#interacting-with-apis)
- [ ] [Version control]({{  site.baseurl  }}/DS-transition-4/#version-control)
- [ ] Object-oriented programming (i.e. classes, module imports)
- [ ] Virtual environments
- [ ] Writing tests
- [ ] Servers and deployment <br><br>
{: style='list-style-type: none'}

## Intro to Stats
Inferential statistics is the discipline of drawing inferences about a _**population**_ from a _**sample.**_ We rarely have data on every single individual, decision, or atom in whatever process we're examining. Rather than throw in the towel on understanding anything around us, we can turn to statistics for tools that translate data on *our sample* into inferences on *the entire population*. Inferential statistics is used all the time to make sense of the world, from [weather forecasts](https://thisisstatistics.org/beyond-barometers-how-statisticians-help-to-predict-the-weather/) to [opinion polls](https://www.math.arizona.edu/~jwatkins/505d/Lesson_12.pdf) and [medical research](https://emj.bmj.com/content/17/5/357). **Thinking carefully about how to generalize from our data to the broader world is a critical skill for data science,** so we'll want to make sure we have a solid grasp of stats.

### Wait, do I actually need to learn stats?
In the era of big data and machine learning, it's tempting to shrug off learning any stats. When the average laptop is [*2 million times* more powerful](https://www.realclearscience.com/articles/2019/07/02/your_mobile_phone_vs_apollo_11s_guidance_computer_111026.html) than the computer that got us to the moon<sup>[[1]](#1-wait-do-i-actually-need-to-learn-stats)</sup>, it's easier than ever to throw a dataset into a deep learning algorithm, get a coffee while it crunches the numbers, and then come back to some model that always delivers world-shattering insights. Right? Well... not quite.<sup>[[2]](#2-wait-do-i-actually-need-to-learn-stats)</sup>

As data scientists, **a core part of our job is to generate models that help us understand the past and predict the future.** Despite the importance of getting models right, it's easy to create models with serious flaws. It's then *uncomfortably* easy to make confident recommendations to stakeholders based on these flawed models. The following quote usually refers to the *quality of data* going into an analysis or prediction, but I think it's an apt summary for why we need to care about stats as well.

> "Garbage in, garbage out."

**A model is a simplified representation of reality.** If that representation is flawed, the picture it paints can very easily be nonsensical or misleading. The reason people dedicate their lives to researching statistics is that **condensing reality down to models is incredibly challenging, yet necessary.**

<img src="{{  site.baseurl  }}/images/careers/clothes_model.png" align="right" height="40%" width="40%" style="padding-left: 30px" alt="A positive relationship between how cold it is outside and how many layers of clothes I should wear."> It's usually impossible or impractical to process every detail before making a decision; our brains, for example, constantly use [processing short-cuts](https://jamesclear.com/schemas) to interpret the world faster. You don't need to memorize what clothes to wear for every possible temperature outside; you know that, in general, as the temperature goes down, you put on more layers. This mental model isn't perfect $-$ sometimes it's windy or humid, and a different number of layers feels more comfortable $-$ but it's a great rule of thumb.

When we build a model, **the question isn't how to make a model that isn't flawed; it's how to ensure the flaws don't affect the conclusions.** The fact that wind or humidity sometimes alters the best number of layers doesn't change the fact that "the colder it is, the more clothes I should put on" is a good model. As statistician George Box ([allegedly](https://en.wikipedia.org/wiki/All_models_are_wrong)) said:

> "All models are wrong, but some are useful."

The difference between a model that's *wrong but useful* versus one that's *just wrong* is often hidden in the details. **Unlike in programming, hitting "run" on a half-baked model *will* output a result that qualitatively looks identical to a highly-polished, accurate model.** But whether the model represents *the reality we actually live in* requires a trained eye.  

### Ok, so how much stats do I actually need?
It's hard not to write an entire textbook when it comes to important stats concepts for data science. It's also hard to identify which concepts are most relevant for data scientists, given the tremendous variation in depth of statistical knowledge expected. You'll need far more than intro stats if you're expected to inform major decisions like public policy or the direction your company takes<sup>[[3]](#3-ok-so-how-much-stats-do-i-actually-need)</sup>, but basic stats may be more than enough if your role is deep in the engineering side of data science.

Similarly, if you're in a field where you actually *do* have access to all the data in a process, such as analyzing [Internet of Things (IoT)](https://www.zdnet.com/article/what-is-the-internet-of-things-everything-you-need-to-know-about-the-iot-right-now/) sensor data or applying [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing) to legal documents, then you'll want a deep dive on additional stats skills, like [time series analysis](https://www.statisticssolutions.com/time-series-analysis/), [clustering](https://en.wikipedia.org/wiki/Cluster_analysis), and [anomaly detection](https://www.anodot.com/blog/what-is-anomaly-detection/).

Consider the following concepts, then, as a *starting point* that you can then build off and tailor to your specific role. I'm assuming you have some basic familiarity with modeling but maybe haven't had a deep dive into the nuances of coefficients and residuals. (If you're a newcomer to stats, check out an upcoming "Model fundamentals" series of posts with lots of content from earlier drafts of this post!)

Here are the stats essentials I think any data scientist should feel comfortable explaining to both technical and non-technical audiences:

* **Experimental design:** sampling and bias, control groups
* **Predictive modeling:** regression, classification
* **Comparisons between groups:** t-tests, ANOVA
* **Measures of statistical significance:** p-values, effect sizes, confidence intervals
* **Model evaluation:** coefficients, residuals, AIC, correlation vs. causation, overfitting vs. underfitting

We'll go through each of these in the rest of the post. Let's get started!

## Experimental design
Broadly, experimental design refers to how we structure our *data collection* process. Do we poll our friends on Facebook, random passersby at the mall, or random phone numbers? Does every patient get the drug, or do we give some a placebo? **Think of the quality of any analysis we run as a funnel starting from the quality of the data we collect.** If we have solid data, we can ask more interesting questions and discover more meaningful insights. If we have shoddy data, there'll always be that shadow of doubt for whether the results can truly be trusted. So let's make sure we can identify how to get good data.

### Sampling and bias
<img align="right" src="https://i.imgur.com/JbXsczj.png" height="40%" width="40%">
One of the key concepts to understand is that when you collect data, you are **sampling** from a **population.** (Except, as I mentioned, in fields like [IoT](https://en.wikipedia.org/wiki/Internet_of_things).) Because we're condensing a large, diverse body down into a relatively small sample, we need to make sure the sample actually looks like a microcosm of the broader population.

In the graphic on the right, for example, our sample isn't really representative of the population $-$ several colors aren't present at all! We can't run an analysis on this sample and then generalize to the population; **we can only generalize to red, orange, yellow, and green.** No matter how perfectly we model our sample data, our model's scope is trapped. If we try to comment on the broader population, we'll find that our seemingly accurate model suddenly makes embarrassingly inaccurate predictions.

A recent example of this sample-population discrepancy is the 2020 U.S. election forecasts. After President Trump's surprise 2016 victory that [defied the vast majority of public opinion polls](https://www.voanews.com/usa/us-politics/election-experts-puzzled-over-surprise-trump-victory), pollsters spent years tweaking their models, fixing blindspots in preparation for a 2020 redemption. Yet, as states started releasing results on November 3, we found ourselves yet again watching [polls underestimate the number of Trump voters](https://www.scientificamerican.com/article/why-polls-were-mostly-wrong/).

David Shor, the former head of political data science at [Civis Analytics](https://www.civisanalytics.com/), believes the predictions were so off because [**their underlying samples are not representative of American voters.**](https://www.vox.com/policy-and-politics/2020/11/10/21551766/election-polls-results-wrong-david-shor) In short, the people who respond to polls tend to score high on social trust, which the [General Social Survey](https://gssdataexplorer.norc.org/variables/441/vshow) indicates represents only 30% of Americans. Until 2016, this group used to vote comparably to low-trust voters who didn't pick up the phone for pollsters $-$ now, low-trust voters tend to vote more conservatively and are hence underrepresented in the sample.

If we're aware of these discrepancies, we can try to implement fixes such as [differentially weighting classes in the sample](https://www.researchgate.net/post/How-can-I-deal-with-uneven-sample-sizes-in-my-study). But the best remedy is to make sure the sample [is truly representative of the broader population](https://www.healthknowledge.org.uk/public-health-textbook/research-methods/1a-epidemiology/methods-of-sampling-population). Note: this is often easier said than done!

### Control groups

When you remove the effect of the control, it lets you isolate what the true effect was. You're controlling for variation not due to the variable of interest.


## Predictive modeling

### Model fundamentals
Let's say we take all these considerations to heart and are confident our sample is representative of the broader population. Now what? Since it's easy to build a model that actually isn't informative at all, let's start with a foundation for what models and their components are. We'll first take a high-level view of two of the main types of models $-$ **regression** and **classification** $-$ before diving into **coefficients** and **residuals**, as well as **linear and logistic regression.** These concepts will help us understand what a model is, how to quantify trends in our data, and how to evaluate model accuracy.

### Regression
As a recap, a model is a simplified representation of reality, like *"The colder it is, the more clothes I should put on"* or *"Students are more likely to pass an exam if they study a lot and sleep well."* <sup>[[5]](#footnotes)</sup> A model takes in inputs, such as temperature, and returns an output, such as the number of clothes to wear.

The type of model we'll want to build will depend on whether we want to predict a _**continuous**_ or _**discrete**_ outcome. A continuous value is a number with a decimal, like 0.555 mL, $13.81, or 99.9%. A discrete value is a distinct category, like "big," "red," or "cat." ("Big red cat" could also be a category!)

We use regression models to predict continuous outcomes and classification models to predict discrete outcomes. A typical regression model could answer the question *"What is a student's score on an exam, given factors like how much they studied?"* A classification model, meanwhile, would answer *"Does a student pass the exam, given factors like how much they studied?"* The regression model predicts the student's specific score, while the classification model predicts whether they belong to the "passed" or "failed" categories.

Here's a simple **linear regression model** that predicts a student's exam score based off 1) the number of hours the student studied and 2) the number of hours of sleep the night before:

$$y = \beta_0 + \beta_1x_1 + \beta_2x_2$$

In plain English, this equation is saying that $y$ (exam score) is equal to:
* The student's score if they studied zero hours and got zero sleep (the intercept, $\beta_0$)
* ...plus the "study multiplier" ($\beta_1$) times the hours studied ($x_1$)
* ...plus the "sleep multiplier" ($\beta_2$) times the hours slept ($x_2$)

No matter where you work, it's hard to escape the simplicity and convenience of a good linear regression model. Linear regressions are extremely fast to compute and they're easy to explain: the [coefficients](#coefficients) give a clear explanation of how each variable affects the output<sup>[[6]](#footnotes)</sup>, and you just add all the $\beta_jx_j$ together to get your output. Make sure you have your "30-second spiel" ready for regression, since you'll likely be explaining these models repeatedly to various stakeholders.

Once you're comfortable, it'd be good to brush up on more advanced topics, like feature [scaling](https://en.wikipedia.org/wiki/Feature_scaling), [interactions](https://christophm.github.io/interpretable-ml-book/interaction.html), and [collinearity](https://medium.com/future-vision/collinearity-what-it-means-why-its-bad-and-how-does-it-affect-other-models-94e1db984168), as well as [model regularization](https://medium.com/@zxr.nju/the-classical-linear-regression-model-is-good-why-do-we-need-regularization-c89dba10c8eb) and [how coefficients are calculated]({{  site.baseurl  }}/LR-grad-desc).

### Classification
Our model above predicted an exam score based on the hours a student studied and slept. A **logistic regression model** (which is actually classification despite having "regression" in the name) with the same predictors looks like this:

$$ P(y) = \frac{1}{1+e^{-h(x)}}$$

where $$h(x) = \beta_0 + \beta_1x_1 + \beta_2x_2 $$.

In plain English, this means $P(y)$ (the probability of passing the exam) is equal to:
* 1 divided by...
* 1 plus...
* the mathematical constant $e$ raised to the negative of some value $h(x)$
  - <span style="font-size: 13px">(And that value looks a lot like a linear regression output!)</span>

#### Making sense of that equation
While the equation may look intimidating, it looks a *lot* simpler if you set $h(x)$ to the extremes. Let's say $h(x)$ is *extremely negative.* That would mean $-h(x)$ would be positive, which would make $1 + e^{-h(x)}$ *huge*. For example, if $e^{-h(x)}$ is 10000000, we see $P(y)$ is nearly zero.

$$ P(y) = \frac{1}{1+10000000} = 0.0000001$$

On the other extreme, if $h(x)$ is *extremely positive*, then $-h(x)$ becomes *tiny*, meaning we're essentially dividing 1 by 1. When $e^{-h(x)}$ is 0.00000001, we see $P(y)$ is pretty much 1.

$$ P(y) = \frac{1}{1+0.00000001} = 0.99999999$$

This is the major distinction from linear regression: **logistic regression outputs are constrained to between 0 and 1.** We interpret logistic regression outputs as **the probability of event $y$ occurring, given our predictors.** We can work with these outputted probabilities directly, or we can binarize them into 0s and 1s. In our student model, this would mean predicting whether the student passed (1) or failed (0) the exam. We typically use $P(y)$ = 0.5 as the probability cutoff.

One last thing before we move on. What happens when $h(x)$ equals zero? Any real number raised to the zeroth power equals 1, so $e^{-h(x)}$ becomes 1.

$$ P(y) = \frac{1}{1+1} = 0.5 $$

When $h(x)$ equals zero, $P(y)$ equals 0.5. If we're using 0.5 as the probability cutoff, that means **we'll predict the student passed if $h(x)$ is positive. If $h(x)$ is negative, we'll predict the student failed.** Interesting...

#### Making sense of $h(x)$
<img src="{{  site.baseurl  }}/images/careers/decision_boundary.png" height="55%" width="55%" align="right">
So what's up with $h(x)$? In short, when $h(x)$ = 0, we get **a line that best separates our data into classes.** Training a logistic regression model is all about identifying *where to put this line* to best separate the classes in the data.

In the figure on the right<sup>[[7]](#footnotes)</sup>, we've plotted some fake training data of students who passed vs. failed the exam. The blue line is the model's **decision boundary**, where it determined the best separation of the "passed" vs. "failed" classes falls, based on $x_1$ and $x_2$. It's not perfect $-$ there are some "passed" students on the left and "failed" students on the right $-$ but this is the best separation the model could come up with. For any new data falling to the left of the decision boundary, our model will predict the student failed. For any new data falling on the right, our model will predict the student passed.  

Once you're comfortable with these topics, it's a small step to move onto logistic regression models for more than two classes, such as [multinomial](https://en.wikipedia.org/wiki/Multinomial_logistic_regression) and [one-vs-rest](https://scikit-learn.org/stable/auto_examples/linear_model/plot_logistic_multinomial.html) classification.

### Coefficients
Let's take another look at the linear regression model that predicts student exam scores.

$$y = \beta_0 + \beta_1x_1 + \beta_2x_2$$

The intercept ($\beta_0$), study multiplier ($\beta_1$), and sleep multiplier ($\beta_2$) are the **coefficients** of our model. These parameters convert our inputs (hours studied and hours slept) to the output (exam score). A coefficient of 10 for $\beta_1$, for example, means that a student's score is expected to increase by 10 for each additional hour they study. An intercept of 30 would mean the student is expected to get a 30 if they don't study or sleep at all.

Model coefficients help us understand the trends in our data, such as whether studying an extra hour versus going to bed would lead to a higher exam score. **But we should always take a careful look at the coefficients before accepting our model.** I always try to mentally validate the *strength* and *direction* of each coefficient when I examine a model, making sure it's about what I'd expect, and taking a closer look if it isn't. A negative sleep coefficient $\beta_2$, for example, would indicate something wrong with our data, since sleep should improve exam scores! (If not, maybe our students or the exam they took are very strange...) Similarly, if our intercept is *above* 100 and the study and sleep coefficients are negative, we likely have too little data or there are outliers hijacking our model. **Make sure to plot your data to confirm the trends are actually what you think they should be.**


TALK ABOUT EFFECT SIZES AND CONFIDENCE INTERVALS

For least squares:
$$ y = \sum_{i=1}^{m}(h(x_i)-y_i)^2 $$


### Residuals
<img src="{{  site.baseurl  }}/images/careers/residual.png" align='right' height='55%' width='55%'>
Once we've built a model, how do we tell if it's any good? One way is to compare *<u>the model's predictions</u>* to *<u>the actual values</u>* in our data. In other words, given some sample inputs, what does the model *think the output is*, versus *what the output actually is*? The **residual** is the distance between the predicted versus actual values.

You can see this illustrated in the graphic on the right. The model's predictions are the red line. The distance between the predictions and the actual values are the residuals. The goal with building a model is to get the predicted and actual values as similar as possible $-$ to *minimize the residuals*, in other words.<sup>[[8]](#footnotes)</sup> A more accurate model will have tend to generate predictions closer to the actual values than an inaccurate one.

Especially for linear models, the residuals should be normally distributed around zero, meaning our predictions are usually pretty good but sometimes a little too high or too low, and rarely way too high or way too low.

![]({{  site.baseurl  }}/images/careers/residuals_good.png)

**It's important to plot your data.** Otherwise you can fit a model but realize it's crap, like this:

![]({{  site.baseurl  }}/images/careers/residuals_bad.png)


You need to do two models, or have a factor.

![]({{  site.baseurl  }}/images/careers/two_models.png)


### $R^2$
Let's try this: $A$.

You should be able to explain the following equation again and again:

$$ h(x) = \sum_{j=1}^{n}\beta_jx_j $$

**Linear regression** is one of the most common statistical model you'll encounter in industry, and you need to understand its ins and outs. Make sure you have a solid understanding of what **residuals** are, **least squared error**, and $$R^2$$.




## Concluding thoughts


## Footnotes
#### 1. [[Wait, do I actually need to learn stats?]](#wait-do-i-actually-need-to-learn-stats)
The [Apollo Guidance Computer](https://www.realclearscience.com/articles/2019/07/02/your_mobile_phone_vs_apollo_11s_guidance_computer_111026.html) had 4.096 KB of RAM. An average laptop in 2020 has 8 GB, which is 1.95 million times more powerful. If we use a [memory-optimized AWS EC2 instance](https://aws.amazon.com/ec2/instance-types), we have access to upwards of _**1.57 billion**_ times more compute than the Apollo mission. And all to identify pictures of cats...

#### 2. [[Wait, do I actually need to learn stats?]](#wait-do-i-actually-need-to-learn-stats)
Rather than removing the need for statistics, big data *exacerbates* common statistical risks. I've linked some further reading below.
* American Statistical Association: [Statistics and Big Data](http://higherlogicdownload.s3.amazonaws.com/AMSTAT/UploadedImages/49ecf7cf-cb26-4c1b-8380-3dea3b7d8a9d/BigDataOnePager.pdf)
* National Science Review: [Challenges of Big Data Analysis](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4236847/)

#### 3. [[Ok, so how much stats do I actually need?]](#ok-so-how-much-stats-do-i-actually-need)
If people come to you for help making crucial decisions from data, you'll want to account for statistical nuances like [random effects](https://www.theanalysisfactor.com/understanding-random-effects-in-mixed-models/), [regression discontinuities](https://en.wikipedia.org/wiki/Regression_discontinuity_design), [nonparametric](http://mlss.tuebingen.mpg.de/2015/slides/ghahramani/gp-neural-nets15.pdf) or [Bayesian](http://www.scholarpedia.org/article/Bayesian_statistics) alternatives to [frequentism](https://en.wikipedia.org/wiki/Frequentist_inference), [bootstrapping](https://en.wikipedia.org/wiki/Bootstrapping_(statistics)) and more.

5. [[The high-level view]](#the-high-level-view) To the best of my knowledge, clustering unlabeled data falls neatly into machine learning rather than classical statistics, so I won't be covering it in this post. But of course, clustering is a crucial skill to have: make sure you understand [k-means clustering](https://en.wikipedia.org/wiki/K-means_clustering) as a starting point, and [Gaussian mixture models](https://scikit-learn.org/stable/modules/mixture.html) if you want to get fancy.

6. [[Regression]](#regression) There *is* one important caveat to mention here regarding the ease of understanding a regression model's coefficients. Yes, they do show the influence each input variable has on the output, **but these coefficients are affected by all other variables in the model.** <br><span style="color:white">......</span>In our "study and sleep" exam model, for example, removing "hours studied" from our model will cause the "sleep" coefficient to skyrocket, since it's now entirely responsible for converting "hours slept" into an exam score. <br><span style="color:white">.....</span>You'll find that variables' coefficients can shrink, explode, or even change sign when you add or remove predictors and rerun the model. Trying to understand *these* changes is where you need a deep understanding of your data.

7. [[Classification]](#classification) Here's the code to generate the decision boundary plot.
    ```python
    import numpy as np
    import pandas as pd
    import statsmodels.formula.api as smf

    # Generate sample data with pos (x1) & neg (x2) slopes
    x1 = np.arange(0, 10, 0.1) + np.random.normal(0, 2, 100)
    x2 = np.arange(0, 10, 0.1) + np.random.normal(0, 2, 100)
    y = np.round(np.arange(0, 1, 0.01) + np.random.normal(0, 0.1, 100))

    # Put into df and fit a model
    df = pd.DataFrame({'x1': x1, 'x2': x2, 'y': y})
    mod = smf.logit('y ~ x1 + x2', data=df).fit()

    # Get decision boundary params
    b0 = mod.params.Intercept
    b1 = mod.params.x1
    b2 = mod.params.x2

    # Calculate the intercept and gradient of the decision boundary
    c = -b0/b2
    m = -b1/b2

    # Generate the decision boundary line
    xmin, xmax = -10, 15
    ymin, ymax = -15, 15

    xd = np.array([xmin, xmax])
    yd = m*xd + c

    # Subset to prep for plotting
    df0 = df[df['y'] == 0]
    df1 = df[df['y'] == 1]

    # Generate the plot
    plt.figure(figsize=(5, 5))
    plt.scatter(df0['x1'], df0['x2'], marker='o', color='orange', s=35)
    plt.scatter(df1['x1'], df1['x2'], marker='x', color='red', s=40)

    plt.plot(xd, yd, 'k', lw=1, ls='--', color='blue')
    plt.xlim(-2.75, 13.25)
    plt.ylim(-3.75, 13)
    plt.xlabel(r'$x_1$', fontweight='bold', fontsize=25)
    plt.ylabel(r'$x_2$', fontweight='bold', fontsize=25)
    plt.tick_params(bottom= False, left=False, labelbottom=False,
                    labelleft=False)
    plt.legend(framealpha=1)
    plt.show()
    ```
    <br>

8. [[Residuals]](#residuals) I talk about minimizing residuals at great length in [this blog post]({{  site.baseurl  }}/LR-grad-desc), where I recreate R's linear regression function by hand. Fun times!
