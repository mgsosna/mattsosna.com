---
layout: post
title: A deep dive on precision and recall
author: matt_sosna
tags: machine-learning statistics
---

Two of the most important metrics of any machine learning system in production include **precision** and **recall**. 



## Intro

Imagine we are monitoring the amount of misinformation on Twitter. The number of Tweets is staggeringly massive, so much so that it's like a wave of information. We can only tell whether something is misinfo by zooming in on it.

<img src="{{  site.baseurl  }}/images/ml/precision_recall/base_pop.png">

There are two ways we can inspect whether a Tweet is misinformation. The first option is the slow but sure approach: human review. Given how nuanced misinformation is, sometimes you just need a person to do the looking to be 100% sure.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/manual_review.png" height="60%" width="60%">
</center>

But this approach doesn't scale well. It might work for a smaller company, where the population of content, actions, etc. to review is small enough. But at a big scale, this population is like a never-ending tidal wave of information.

The second approach, then, is to train a model to _predict_ whether content is bad. Using a model has the tremendous advantage that it is thousands or even millions of times faster than a human at labeling whether content is abusive.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/scaled_review.png" height="60%" width="60%">
</center>

The major caveat, though, is that the model classification is a _prediction._ We still need a human to review.<sup>[[1]](#1-intro)

## Other things
How do we quantify the _change_ in precision or recall? Let's say that we have our Baseline and Treatment. We're evaluating whether it's worth changing.

To quantify the change in recall, we could do something like:

$$\LARGE \frac{N_{new} - N_{old}}{N_{old}} $$

Where $N$ is the

## Code


## Footnotes
#### 1. [Intro](#intro)
The major point in this paragraph is that models generate predictions, which have inherent uncertainty relative to human review. But a whole separate, more uncomfortable issue is that human review has uncertainty, too! Even experts disagree with one another, and reviewers themselves can be inconsistent.
