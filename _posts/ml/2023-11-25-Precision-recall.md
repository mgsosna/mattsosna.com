---
layout: post
title: A business lens on precision and recall
author: matt_sosna
tags: machine-learning statistics
---

<img src="{{  site.baseurl  }}/images/ml/precision_recall/base_pop2.png" alt="Population under a magnifying glass">

_Disclaimer: the examples in this post are for illustrative purposes and are not commentary on any specific content policy at any specific company. All views expressed in this article are mine and do not reflect my employer._

Why is there _any_ spam on social media? Aside from spammers, literally no one enjoys clickbait scams or phishing attempts. We have _decades_ of training data to feed machine learning classifiers. So why does spam on every major tech platform feel inevitable? After all these years, why do bot farms still exist?

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/feed.png" height="75%" width="75%">
</center>

The answer, in short, is that it is _really_ hard to fight spam at scale, and exponentially harder to do so without harming genuine users and advertisers. In this post, we'll use **precision** and **recall** as a framework for the spam problem. We'll see that eradicating 100% of spam is impractical and actually undesirable, and that there is some "equilibrium" spam prevalence based on finance, regulations, and user sentiment.

## Our app
Imagine you're launching a competitor to TikTok and Instagram. (Forget that they have [**1.1 billion**](https://www.demandsage.com/tiktok-user-statistics/) and [**2 billion**](https://www.statista.com/statistics/272014/global-social-networks-ranked-by-number-of-users/) monthly active users, respectively; you're feeling ambitious!) Your key differentiator in this tight market is that you guarantee users will have only the highest quality of videos: absolutely no "get rich quick" schemes, blatant reposts of existing content, URLs that infect your computer with malware, etc.

### Attempt 1: Human Review
To achieve this quality guarantee, you've hired a staggering 1,000 reviewers to audit every upload before it's allowed on the platform. **Some things just need a human touch**, you argue: video spam is too complex and context-dependent to rely on automated logic. A video that urges you to click on a URL could be a malicious phishing attempt or a fundraiser for Alzheimer's research, for example -- the stakes are too high to automate a decision like that.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/manual_review.png" height="60%" width="60%">
</center>

The app launches. To your delight, your "integrity first" message resonates with users and they join in droves. You quickly reach millions of users uploading 50,000 hours of video per day.

In other words, each reviewer now has _50 hours of video to review per day_. They try watching at 6x speed to get through all the videos, but they make mistakes: users start complaining both that **their videos are being incorrectly blocked _and_ that spam is making it onto the platform.** You quickly hire more reviewers, but as your app grows and the firehose of uploads only gets bigger, you realize you'll bankrupt the company long before you can hire enough eyes.<sup>[[1]](#1-attempt-1-human-review)</sup> You need a different strategy.

### Attempt 2: Machine Learning
You can't replace a human's intuition, but maybe you can get close with machine learning. Given the tremendous advances in [computer vision](https://www.ibm.com/topics/computer-vision) and [natural language processing](https://www.ibm.com/topics/natural-language-processing) over the past decade, you can extract **features** from the videos: the pixel similarity to existing videos, keywords from the audio, whether the video appears to have been [generated with AI](https://www.techtarget.com/searchenterpriseai/definition/generative-AI), etc. You can then see how these features relate to whether a video is spam.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/numbers.png" height="85%" width="85%">
</center>

Determining the relationship between features and spam labels is best left to an algorithm.<sup>[[2]](#2-attempt-2-machine-learning)</sup> The feature space is simply too large for a human to understand: features interact non-linearly, have complex dependencies, are useful in some contexts but useless in others, and so on. So you use machine learning to **train a classifier that _predicts_ whether a video is spam.** Your model takes in a video and outputs the probability that the video is spam.<sup>[[3]](#3-attempt-2-machine-learning)</sup>

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/scaled_review.png" height="60%" width="60%">
</center>

When you first run your classifier on videos you know are spam and benign, you hope to see something like below: two distributions neatly separable by their probability of being spam. In this ideal state, there is a spam probability threshold below which all videos are benign and above which all videos are spam, and you can use that threshold to perfectly categorize new videos.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/spam_dist1.png" height="90%" width="90%">
</center>

But what you actually see is that **the probability distributions overlap.** Yes, the vast majority of benign videos have a low probability and the vast majority of spam videos have a high probability. But **there's an uncomfortable "intermediate" spam probability where it's impossible to tell if a video is spam or benign.**

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/spam_dist2.png" height="90%" width="90%">
</center>

If you zoom in on where the distributions overlap, it looks something like this. Nowhere can you draw a line that perfectly separates benign videos from spam. If you set the threshold too high, then spam makes it onto the platform. If you set the threshold too low, then benign videos are incorrectly blocked.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/boundary.png" height="95%" width="95%">
</center>

**So how do you choose a "least-bad" threshold?** To answer this question, we need to understand **precision** and **recall**, two metrics that provide a framework for navigating the tradeoffs of any classification system. We'll then revisit your app with our new understanding and see if there's a way to optimally classify spam.

## Evaluation Framework
### Model Creation
Let's start with a quick overview of how machine learning classifiers are created and evaluated, using our spam classifier as an example. The first step when training a model is to split our data into _train_ and _test_ sets. An algorithm then parses the training data to learn the relationship between features and labels (spam or benign). The result is a model that can take in any vector of features and return a probability of the positive label (whether a video is spam). This probability is then binarized -- usually at 0.5 -- to say whether the model classifies the input as a positive (spam) or negative (benign) label.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/training1.png" alt="Training a machine learning classifier">
</center>

Our model is a best effort at understanding the data it was given. But while understanding the data _we have_ is useful, the real goal is to be able to predict the labels for data _we haven't seen before_, like incoming uploaded videos.<sup>[[4]](#4-evaluation-framework)</sup> We measure our model's ability to do so with the _test_ data: feature-label pairs that weren't used to train the model. We feed in the features from our test data, see what the model predicts, and compare those predictions to the actual labels. (This is why we don't train the model on all available data: we need some holdout labeled data to assess the model's performance.)

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/training2.png" alt="Training a machine learning classifier" height="55%" width="55%">
</center>

There are four components to measuring our model's ability to classify new data, based on the four possible outcomes of a prediction:
* **True Positive:** the model correctly identifies spam.
* **False Positive:** the model predicts spam, but the video is benign.
* **False Negative:** the model predicts benign, but the video is spam.
* **True Negative:** the model correctly identifies a benign video.

We can arrange these possibilities in a **confusion matrix.** The columns of the matrix are the _predicted_ spam and benign labels, and the rows are the _actual_ spam and benign labels.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/cm2.png" alt="Confusion matrix" height="55%" width="55%">
</center>

**A solid performance on the test set ensures that our model is able to accurately generalize to new data.** But how do we explicitly quantify performance?

### Metric 1: Accuracy
Our first approach may be to maximize **accuracy:** our model's ability to detect true positives (TP) and true negatives (TN). Accuracy, in other words, is **_the proportion of labels that our model correctly predicted_**. A model with perfect accuracy would have zero false positives (FP) or false negatives (FN).

$$Accuracy = \frac{TP+TN}{TP+FP+FN+TN}$$

Accuracy is an intuitive metric to start with. But if our [labels are imbalanced](https://developers.google.com/machine-learning/data-prep/construct/sampling-splitting/imbalanced-data), our model may struggle to learn how to predict the less frequent labels or even converge on a nonsensical approach. Imagine that because spam videos are relatively rare, our training data has 99.9% benign labels and 0.1% spam labels. **A model that always predicts that a video is benign will be 99.9% accurate.** That's not good at all -- we're missing all the videos we want to catch!

Because of nuances like this, we should never solely rely on accuracy when judging a model. Other metrics will help us get a more holistic picture.

### Metric 2: Recall
If it's important for us to catch all the bad videos, we'll want to use a metric like **recall.** Recall is _of all the positive labels, how many did we catch?_ In other words:

$$Recall = \frac{TP}{TP+FN}$$

We can think of this as the top row of the confusion matrix.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/cm_recall.png" alt="Recall columns of confusion matrix" height="50%" width="50%">
</center>

### Metric 3: Precision
Recall is valuable, but it's also easy to "game": a model that always predicts that a video is abusive will have perfect recall. But we won't get much value out of this model, since we'll also be labeling benign videos as abusive.

Another metric we can get from a confusion matrix, then, is **precision.** Precision is _when our model thinks something is abusive, how often is it <u>actually</u> abusive?_ In other words:

$$Precision = \frac{TP}{TP+FP}$$

We can think of this as the left column of the confusion matrix.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/cm_precision.png" alt="Precision columns of confusion matrix" height="50%" width="50%">
</center>


### Optimizing for a metric
There are techniques we can use such as upsampling the minority class or [ranking the raw probabilities outputted from the classifier](https://stats.stackexchange.com/questions/122409/why-downsample). But optimizing the training of our model on another metric may be more useful for our task.



Specifically, we need a framework for the following:
1. Determining how to convert a classifier's predicted _probability that a video is spam into an _"is abusive"_ or _"is benign"_ label.
2. Comparing the performance of one model to another.


## Demo

{% include header-python.html %}
```python
import numpy as np
import pandas as pd

is_spam = np.concatenate(
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
        'is_spam': is_spam,
        'feature_1': feature_1,
    }
)
```


We'll want to calculate the AUC: area under the curve. We'll look at the false positive rate (FPR) vs. the true positive rate (TPR). This lets us know that for a given threshold, what is our ratio of true positives to false positives?

The perfect model would have an AUC of 1: there are never any false positives. The model's outputted probabilities are perfectly 0 or 1, and they perfectly divide the true and false labels.

In reality, no model is perfect. We'll have predicted probabilities of 0.3, or 0.49, for videos that look a _little_ sketchy. We'll have some probabilities of 0.55, or 0.6, for videos that look pretty sketchy but our model isn't 100% sure about. Depending on where we set our binarization threshold, we'll either count those videos as predicted spam, or not.



## Other things
How do we quantify the _change_ in precision or recall? Let's say that we have our Baseline and Treatment. We're evaluating whether it's worth changing.

To quantify the change in recall, we could do something like:

$$\LARGE \frac{N_{new} - N_{old}}{N_{old}} $$

Where $N_{old}$ is the number of abusive videos caught with the old method and $N_{new}$ with the new.





## Back to our app
### Attempt 3: Machine Learning + Human Review
Are we out of luck? No. What if we combine ML and human review?


<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/boundary2.png" height="95%" width="95%">
</center>


If we run that 500 hours/minute firehose of videos through our classifier, we'd get some distribution of spam probabilities ($P(spam)$). We could then set some probability threshold above which we send the video to a human to review.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/spam_flow.png" height="70%" width="70%">
</center>

Depending on where we set this threshold, we can cut down 90%, or 99%, or 99.999%, or any percent of videos to review. Awesome -- so we set our threshold to exclude 99.9999999% of videos, hire one reviewer to handle the remaining 1 minute per day, and congratulate ourselves for solving a tough problem.

But... that doesn't quite work. Unless our classifier is perfect (which it never is), **we're definitely missing a lot of bad content by setting our threshold so high.** Even if our model _is_ really accurate and we can automatically delete any video the model predicts is abusive, we'd still want _some_ people to review its decisions: we may not uncover biases or blind spots in our model if we never audit its outputs.

On the other hand, though, if we set our threshold for manual review too low, we'll start digging into the bulk of the green distribution above: the benign videos. The number of reviewers we'll need to hire will quickly skyrocket, and they'll spend much of their time reviewing benign videos.

**So how do we choose a "least-bad" threshold? What are the tradeoffs we face when picking a number that determines whether a video is sent to review or not? And how do we compare the performance of multiple potential models?**

To answer these questions, we need to understand **precision** and **recall**, two metrics that are provide a framework for navigating the tradeoffs of systems involving machine learning classifiers.


## Equilibria
From a financial standpoint, there is some "optimal" amount of bad stuff on a platform, given the cost of manual review, engineering development, etc. to identify and delete that bad content and the long-term benefit of users staying on the platform. To push a company beyond that point would require regulation (so there are significant financial penalties), an internal acceptance of operating sub-optimally (but with a higher ethical standard, for example) or to have users lower the threshold at which they would leave a platform.

Regulations, user sentiment.



## Footnotes
#### 1. [Attempt 1: Human Review](#attempt-1-human-review)
To illustrate how impractical 100% human review is, consider YouTube. Users upload [**over 500 hours of video every minute**](https://www.statista.com/statistics/259477/hours-of-video-uploaded-to-youtube-every-minute/), or **1.8 million hours per day.** Reviewing this number of videos manually would require _75,000 reviewers_ watching videos 24/7, or _240,000_ if reviewers only work 8-hour shifts and have a lunch break. Add 1,000 to handle _re-reviewing_ videos whose creators [claim were incorrectly deleted](https://www.tspa.org/curriculum/ts-fundamentals/content-moderation-and-operations/user-appeals/). We're left with **241,000 reviewers**, or [160% the number of Google employees](https://www.macrotrends.net/stocks/charts/GOOG/alphabet/number-of-employees). That's not going to work.

#### 2. [Attempt 2: Machine Learning](#attempt-2-machine-learning)
Note that machine learning isn't the only option for fighting spam. There _is_ a solid use case for hand-crafted deterministic rules for subsets of spam. Something like "how often should a user be allowed to post a video?" probably doesn't need a dedicated ML classifier and could be inferred from a distribution of the number of times users post in a day, for example.

#### 3. [Attempt 2: Machine Learning](#attempt-2-machine-learning)
I write "model" here but our spam classifier can actually be an [ensemble](https://en.wikipedia.org/wiki/Ensemble_learning) of models, each trained on different subsets of spam. This is how [Facebook's News Feed](https://about.fb.com/news/2021/01/how-does-news-feed-predict-what-you-want-to-see/) works, for example. There are a set of component models that target small chunks of a problem, like whether a user will like a piece of content, or start following the page that posted the content, etc. These models can be incredibly complex, but they ultimately output a probability that the action will occur. Then you can simply attach weights to each of the probabilities, sum them, and rank by these scores. This is one way to navigate the tradeoff of high accuracy and low explainability of complex models (like what, exactly, leads to a person deciding to react with a heart emoji on a post) while having explainability in the overall ranking of an item in the feed.

#### 4. [Evaluation framework](#evaluation-framework)
Modeling just the existing data can be useful, too, but this falls more in the realm of business intelligence or data analytics. The goal there is to understand our data, the relationships between features, etc. but there is not necessarily a _predictive_ component of trying to understand future data.
