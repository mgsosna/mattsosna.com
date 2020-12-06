---
layout: post
title: Model fundaments p.1
author: matt_sosna
summary:
image:
---

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

<span style='color: red'>More explanation here ^^ </span>


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

## Footnotes
5. [[The high-level view]](#the-high-level-view) To the best of my knowledge, clustering unlabeled data falls neatly into machine learning rather than classical statistics, so I won't be covering it in this post. But of course, clustering is a crucial skill to have: make sure you understand [k-means clustering](https://en.wikipedia.org/wiki/K-means_clustering) as a starting point, and [Gaussian mixture models](https://scikit-learn.org/stable/modules/mixture.html) if you want to get fancy.
