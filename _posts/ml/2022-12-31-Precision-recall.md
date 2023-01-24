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

**But this approach doesn't scale well.** To stay atop the torrent of videos, we would need _30,000 reviewers_ working nonstop to catch all misinformation. Actually, make that _100,000_ if reviewers only work 8-hour shifts and have a lunch break. Add 1,000 to handle _re-reviewing_ taken-down videos that users [appeal](https://www.tspa.org/curriculum/ts-fundamentals/content-moderation-and-operations/user-appeals/). We're left with 101,000 reviewers, an unrealistic number even for a company as large as Google.<sup>[[1]](#1-intro)</sup>

We need some way to reduce the amount of content that requires manual review. Given the tremendous advances in [computer vision](https://www.ibm.com/topics/computer-vision) and [natural language processing](https://www.ibm.com/topics/natural-language-processing) over the past decade, **what if we train a classifier (or several dozen) to _predict_ whether content is bad?** Our model(s) will output the probability that a video is misinformation, and we can set some threshold above which we send over the video to review.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/misinfo_flow.png" height="70%" width="70%">
</center>

Depending on where we set this threshold, we can cut down 90%, or 99%, or 99.999%, or any percent of videos to review. Awesome -- so we set our threshold to exclude 99.9999999% of videos, hire one reviewer to handle the remaining 1 minute per day, and congratulate ourselves for solving a tough problem.

But... that doesn't quite work. Unless our classifier is perfect (which it never is), **we're definitely missing a lot of bad content by setting our threshold so high.** Even if our model _is_ really accurate and we can automatically un-publish anything the model predicts to be violating, we'd still want _some_ people to review its decisions: we may not uncover biases or blind spots in our model if we never audit its outputs.

On the other hand, though, if we set our threshold for manual review too low, we'll start digging into the bulk of the green distribution above: the benign videos. The number of reviewers we'll need to hire will quickly skyrocket, and they'll spend much of their time reviewing benign videos.

**So how do we choose a threshold? What are the tradeoffs we face when picking a number that determines whether a video is sent to review or not? And how do we compare the performance of multiple potential models?**

To answer these questions, we need to understand **precision** and **recall**, two metrics that are provide a framework for navigating the tradeoffs of systems involving machine learning classifiers.

## Definitions
One core challenge we face is deciding how to convert a classifier's predicted _probability that a video is misinformation_ into an "is abusive" or "is benign" label. The default threshold in most software is 50%: if a video is more likely to be abusive than benign, we could just call it abusive. But this default is likely not great if the distribution of our classifier looks like the one above.

A similar problem is comparing models. Let's say we build a new classifier that uses a different algorithm than our current approach. How can we tell if it's better?

We need a framework for evaluating model performance. The typical way we evaluate the performance of machine learning models is by splitting our data into _training_ and _test_ sets. The model is trained on the training data, then asked to predict the labels of the test data. At whatever threshold we set, our model will either predict that a video 1) _is_ or 2) _is not_ misinfo. Meanwhile, in the real world, this video either 1) _is_ or 2) _is not_ misinfo. This leads us with four possibilities:
* **True Positive:** the model correctly identifies misinfo.
* **False Positive:** the model predicts misinfo, but the video is benign.
* **False Negative:** the model predicts benign, but the video is misinfo
* **True Negative:** the model correctly identifies a benign video.

We can arrange these possibilities in a **confusion matrix.** The columns of the matrix are the _predicted_ abuse and benign labels, and the rows are the _actual_ abuse and benign labels.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/confusion_matrix.png" alt="Confusion matrix" height="50%" width="50%">
</center>

Our first impression is that we want to maximize **accuracy:** our model's ability to detect true positives and true negatives. A model with perfect accuracy would perfectly predict the test set's labels and never have any false positives or false negatives.

$$\frac{TP+TN}{TP+FP+FN+TN}$$

Accuracy often works fine as a metric. But if our labels are imbalanced, it's easy for a model to learn a cheap way to "game" the system. Imagine that because abusive videos are (thankfully) rare, our training data has 99.9% benign labels and 0.1% abusive labels. A model that always predicts that a video is benign will be 99.9% accurate. That's not good at all -- we're missing all the videos we want to catch!

If it's important for us to catch all the bad videos, we'll want to use a metric like **recall.** Recall is _of all the positive labels, how many did we <u>actually</u> catch?_ In other words:

$$\frac{TP}{TP+FN}$$

We can think of this as the top row of the confusion matrix.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/cm_recall.png" alt="Recall columns of confusion matrix" height="50%" width="50%">
</center>

Recall is valuable, but it's also easy to "game": a model that always predicts that a video is abusive will have perfect recall. But we won't get much value out of this model, since we'll also be labeling benign videos as abusive.

Another metric we can get from a confusion matrix, then, is **precision.** Precision is _when our model thinks something is abusive, how often is it <u>actually</u> abusive?_ In other words:

$$\frac{TP}{TP+FP}$$

We can think of this as the left column of the confusion matrix.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/cm_precision.png" alt="Precision columns of confusion matrix" height="50%" width="50%">
</center>


## Demo

{% include header-python.html %}
```python
import numpy as np
import pandas as pd

is_misinfo = np.concatenate(
    [
        np.random.choice([0, 1], p=[0.8, 0.2], size=250),
        np.random.choice([0, 1], p=[0.6, 0.4], size=250),
        np.random.choice([0, 1], p=[0.4, 0.6], size=250),
        np.random.choice([0, 1], p=[0.2, 0.8], size=250),
    ]
)

feature_1 = range(1000) + np.random.normal(0, 1, 1000)

df = pd.DataFrame(
    {
        'is_misinfo': is_misinfo,
        'feature_1': feature_1,
    }
)
```


We'll want to calculate the AUC: area under the curve. We'll look at the false positive rate (FPR) vs. the true positive rate (TPR). This lets us know that for a given threshold, what is our ratio of true positives to false positives?

The perfect model would have an AUC of 1: there are never any false positives. The model's outputted probabilities are perfectly 0 or 1, and they perfectly divide the true and false labels.

In reality, no model is perfect. We'll have predicted probabilities of 0.3, or 0.49, for videos that look a _little_ sketchy. We'll have some probabilities of 0.55, or 0.6, for videos that look pretty sketchy but our model isn't 100% sure about. Depending on where we set our binarization threshold, we'll either count those videos as predicted misinformation, or not.



## Other things
How do we quantify the _change_ in precision or recall? Let's say that we have our Baseline and Treatment. We're evaluating whether it's worth changing.

To quantify the change in recall, we could do something like:

$$\LARGE \frac{N_{new} - N_{old}}{N_{old}} $$

Where $N_{old}$ is the number of abusive videos caught with the old method and $N_{new}$ with the new.

## Taking it to the next level
I briefly mentioned that we may want _multiple_ classifiers for a task as complex as catching misinformation. One approach we could take is that if we have a _set number_ of videos that we want to review per day (rather than a set probability threshold, which as we've shown can be much harder to determine), we could try flipping this classification problem into a regression one.

[Facebook's News Feed](https://about.fb.com/news/2021/01/how-does-news-feed-predict-what-you-want-to-see/) works like this. There are a set of component models that target small chunks of a problem, like whether a user will like a piece of content, or start following the page that posted the content, etc. These models can be incredibly complex, but they ultimately output a probability that the action will occur. Then you can simply attach weights to each of the probabilities, sum them, and rank by these scores.  




## Footnotes
#### 1. [Intro](#)
Google only has [150,000 employees](https://www.macrotrends.net/stocks/charts/GOOG/alphabet/number-of-employees), to put the infeasibility of hiring 100,000 reviewers in perspective.
