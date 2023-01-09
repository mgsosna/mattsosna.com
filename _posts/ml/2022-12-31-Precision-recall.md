---
layout: post
title: A deep dive on precision and recall
author: matt_sosna
tags: machine-learning statistics
---

<img src="{{  site.baseurl  }}/images/ml/precision_recall/base_pop.png" alt="Population under a magnifying glass">

Imagine we're in charge of fighting misinformation on YouTube. With [**_2.5 billion_ monthly active users**](https://www.businessofapps.com/data/youtube-statistics/), the stakes are high: falsehoods like Covid miracle cures, election fraud conspiracies, or climate change denial have [serious global consequences](https://www.cnn.com/2023/01/08/americas/brazil-bolsonaro-supporters-breach-congress/index.html). We feel the pressure of ensuring that the world can trust the data it gets from the site. But this is a colossal task: users upload [**over 500 hours of video every minute**](https://www.statista.com/statistics/259477/hours-of-video-uploaded-to-youtube-every-minute/), or **1.8 million hours per day.** How can we consistently identify abuse in a never-ending flood of information?

Misinformation is complex and context-dependent. Did someone make a factually incorrect claim but say it was just their opinion? Was this claim a quote from a politician? Is the claim actually meant to be a joke, or sarcastic? Or is a false claim intentionally being made to mislead viewers? To parse this nuance, we _could_ have trained reviewers watch every video and follow some set of guidelines that define all misinformation.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/manual_review.png" height="60%" width="60%">
</center>

**But this approach doesn't scale well.** To stay atop the torrent of videos, we would need _30,000 reviewers_ working nonstop to catch all misinformation. (Make that _100,000_ if reviewers only work 8-hour shifts and have a lunch break.) 100,000 is an unrealistic number, even for a company as large as Google.<sup>[[1]](#1-intro)</sup> But even if we could get 100,000 reviewers, good luck training them to be consistent, as well as have perfect, up-to-date knowledge of all misleading claims and which violate YouTube's content policies.

Human review is necessary. But 100,000 reviewers isn't going to work. So we need some way to cut down that flood of videos to just borderline cases, ones where we _do_ need a human to review. Is there some way to remove 90%, or 99%, or 99.999% of videos from the review queue, so the videos that are left are actually worth looking at?

Given how strong OCR, NLP, and AI content understanding in general is these days, our second approach is to **train a model (or several dozen) to _predict_ whether content is bad.** Using a model has the tremendous advantage that it is thousands or even millions of times faster than a human at labeling whether content is abusive.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/scaled_review.png" height="60%" width="60%">
</center>

The major caveat, though, is that the model classification is a _prediction._ We still need a human to review.<sup>[[2]](#2-intro)</sup> But we can structure our automated classification systems to avoid anything that isn't that likely to be bad.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/misinfo_flow.png" height="70%" width="70%">
</center>




use [trained reviewers partnered with third-party fact-checkers](https://www.facebook.com/formedia/blog/third-party-fact-checking-how-it-works) to determine whether a video's claims match debunked hoaxes.


## Definitions
Two of the most important metrics of any machine learning system in production include **precision** and **recall**.

It helps to view a confusion matrix.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/confusion_matrix.png" alt="Confusion matrix" height="50%" width="50%">
</center>

## Other things
How do we quantify the _change_ in precision or recall? Let's say that we have our Baseline and Treatment. We're evaluating whether it's worth changing.

To quantify the change in recall, we could do something like:

$$\LARGE \frac{N_{new} - N_{old}}{N_{old}} $$

Where $N_{old}$ is the number of abusive videos caught with the old method and $N_{new}$ with the new.

## Code


## Footnotes
#### 1. [Intro](#)
Google only has [150,000 employees](https://www.macrotrends.net/stocks/charts/GOOG/alphabet/number-of-employees), to put the infeasibility of hiring 100,000 reviewers in perspective.

#### 2. [Intro](#intro)
The major point in this paragraph is that models generate predictions, which have inherent uncertainty relative to human review. But a whole separate, more uncomfortable issue is that human review has uncertainty, too! Even experts disagree with one another, and reviewers themselves can be inconsistent.
