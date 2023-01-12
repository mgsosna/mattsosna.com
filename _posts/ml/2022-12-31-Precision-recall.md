---
layout: post
title: A deep dive on precision and recall
author: matt_sosna
tags: machine-learning statistics
---

<img src="{{  site.baseurl  }}/images/ml/precision_recall/base_pop.png" alt="Population under a magnifying glass">

Imagine we're in charge of fighting misinformation on YouTube. With [**_2.5 billion_ monthly active users**](https://www.businessofapps.com/data/youtube-statistics/), the stakes are high: falsehoods like Covid miracle cures, election fraud conspiracies, or climate change denial have [serious global consequences](https://www.cnn.com/2023/01/08/americas/brazil-bolsonaro-supporters-breach-congress/index.html). We feel the pressure of ensuring that the world can trust the data it gets from the site. But this is a colossal task: users upload [**over 500 hours of video every minute**](https://www.statista.com/statistics/259477/hours-of-video-uploaded-to-youtube-every-minute/), or **1.8 million hours per day.** How can we consistently identify abuse in a never-ending flood of information?

Misinformation is complex and context-dependent. Did someone make a factually incorrect claim but say it was just their opinion? Is the claim a quote from a politician? Is the post sarcastic? Or is a false claim intentionally being made to mislead viewers? To parse this nuance, we _could_ set some rules, train a bunch of people, and have them watch every video and label the violating ones.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/manual_review.png" height="60%" width="60%">
</center>

**But this approach doesn't scale well.** To stay atop the torrent of videos, we would need _30,000 reviewers_ working nonstop to catch all misinformation. Actually, make that _100,000_ if reviewers only work 8-hour shifts and have a lunch break. Add 1,000 to handle _re-review_ of videos that we take down but users [appeal](https://www.tspa.org/curriculum/ts-fundamentals/content-moderation-and-operations/user-appeals/). We're left with 101,000 reviewers, an unrealistic number even for a company as large as Google.<sup>[[1]](#1-intro)</sup>

We need some way to reduce the amount of content that requires a human reviewer. Given the tremendous advances in [computer vision](https://www.ibm.com/topics/computer-vision) and [natural language processing](https://www.ibm.com/topics/natural-language-processing) over the past decade, **what if we train a classifier (or several dozen) to _predict_ whether content is bad?** Our classifier will output some probability that a video is information. We can set some threshold on this probability, then only send videos that are likely to be misinformation out for manual review.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/misinfo_flow.png" height="70%" width="70%">
</center>

Depending on where we set this threshold, we can cut down 90%, or 99%, or 99.999%, or any percent of videos to review. Congrats! We set our threshold to require a video to be 99.9999999% likely to be misinformation, hire 1 reviewer, and call it a day.

But... that doesn't quite work. Unless our model is perfect (which it never is), we're probably missing a lot of bad content by setting our threshold so high. But if we set our threshold too low, we might get so many videos that we need to hire more reviewers than we can afford. **So how do we choose a threshold? What are the tradeoffs we face when picking a number that determines whether a video is sent to review or not?**

To answer these questions, we need to understand **precision** and **recall**, two metrics that are provide a framework for navigating the tradeoffs of systems involving machine learning classifiers.

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
