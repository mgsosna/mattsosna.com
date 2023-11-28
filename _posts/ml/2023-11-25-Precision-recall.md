---
layout: post
title: A practical lens on precision and recall
author: matt_sosna
tags: machine-learning statistics
---

<img src="{{  site.baseurl  }}/images/ml/precision_recall/base_pop.png" alt="Population under a magnifying glass">

_Disclaimer: the examples in this post are for illustrative purposes and are not commentary on any specific content policy at any specific company. All views expressed in this article are mine and do not reflect my employer._

Why is there _any_ spam on social media? Aside from spammers, literally no one enjoys clickbait scams or phishing attempts. We have _decades_ of training data to feed machine learning classifiers and deterministic rules. So why does spam on every major tech platform feel inevitable? After all these years, why do bot farms still exist?

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/feed.png" height="75%" width="75%">
</center>

The answer, in short, is that it is _really_ hard to fight spam at scale, and exponentially harder to do so without harming genuine advertisers and users. In this post, we'll use **precision** and **recall** as a framework for the spam problem. We'll see that eradicating 100% of spam is impractical and actually undesirable, and that there is some "equilibrium" spam prevalence based on finance, regulations, and user sentiment.

## The context
Imagine you're launching a competitor to TikTok and Instagram. (Forget that they have [1.1 billion](https://www.demandsage.com/tiktok-user-statistics/) and [2 billion](https://www.statista.com/statistics/272014/global-social-networks-ranked-by-number-of-users/) monthly active users, respectively; you're feeling ambitious!) Your key differentiator in this tight market is that you guarantee users will have only the highest quality of videos: absolutely no "get rich quick" schemes, blatant reposts of existing content, URLs that infect your computer with malware, etc.

To achieve this, you have a small army of reviewers ready to watch each video and confirm it's not spam before it's allowed on the platform. You know how important it is to have manual review because _spam isn't always immediately obvious_: a video that repeatedly urges users to click on a link might actually be a first aid fundraiser after a crisis -- we definitely don't want to block that! Videos that appear to be reposts might just be an ad campaign with tiny variations based on the target demographic. **You need a human touch to parse this nuance,** you argue.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/manual_review.png" height="60%" width="60%">
</center>

The app launches. To your delight, your "integrity first" message resonates with users and they join in droves. But your video reviewers stare in dread at the thousands of hours of video being uploaded per day. There's just no way to get through the firehose of videos... even watching them on 2x speed! Users are also complaining that their uploaded videos are stuck forever in review.

You therefore decide to automate out your human reviewers by **writing a series of well-crafted `if`-`else` statements** that automatically label videos as spam based on data like video length, the words extracted from the audio, the number of URLs in the summary, the pixel similarity to other videos, etc. You push your changes to the upload section in prod and let the floodgates through. Videos are getting uploaded now, everyone's happy!

Well, not for long. Creators are furious as our automation constantly takes down their benign videos, and users are complaining about the deluge of spam on the platform. You update your code to fix the mistakes again and again. But no matter how complex you make your decision trees, they still constantly fail on basic edge cases, like videos tinted red or with no audio.






But the complaints start rolling in as fast as the signups: there's spam everywhere!






But quality assurance at this scale is a colossal task: users upload [**over 500 hours of video every minute**](https://www.statista.com/statistics/259477/hours-of-video-uploaded-to-youtube-every-minute/), or **1.8 million hours per day.** How can we consistently ensure quality in a never-ending flood of information?

Spam isn't always obvious. A video that repeatedly urges users to click on a link might actually be a first aid fundraiser after a crisis -- we definitely don't want to block that! Videos that appear to be reposts might just be an ad campaign with tiny variations based on the target demographic. **To parse this nuance, we decide to hire a bunch of people**, train them on YouTube's [terms of service](https://support.google.com/youtube/answer/2801973?hl=en), and have them manually watch every video and label the spammy ones.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/manual_review.png" height="60%" width="60%">
</center>

**But this approach doesn't scale well.** To stay atop the torrent of videos, we would need _75,000 reviewers_ watching videos 24/7 to audit everything. Actually, make that _240,000_ if reviewers only work 8-hour shifts and have a lunch break. Add 1,000 to handle _re-reviewing_ videos whose creators [claim were incorrectly deleted](https://www.tspa.org/curriculum/ts-fundamentals/content-moderation-and-operations/user-appeals/). We're left with 241,000 reviewers, or [60% more people](https://www.macrotrends.net/stocks/charts/GOOG/alphabet/number-of-employees) than all Google employees. That's not going to work.

We therefore decide to **simply codify our terms of service as a series of well-crafted `if`-`else` statements** that automatically label videos as spam, but no matter how complex we make our decision trees, they still constantly fail on basic edge cases, like videos tinted red or with no audio. Creators are furious as our automation constantly takes down their benign videos, and users are complaining about the deluge of spam on the platform.


The feature space is just too massive for a human to understand: how can we deterministically say a video is spam from data like video length, the words extracted from the audio, the number of URLs in the summary, the pixel similarity to other videos, etc.?


We need some way to reduce the amount of content that requires manual review. Given the tremendous advances in [computer vision](https://www.ibm.com/topics/computer-vision) and [natural language processing](https://www.ibm.com/topics/natural-language-processing) over the past decade, **what if we train a classifier to _predict_ whether content is bad?**


Our fancy model (which is likely an ensemble of classifiers, each tailored to a different type of spam) takes in a video and outputs the probability that the video violates any of YouTube's spam policies.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/scaled_review.png" height="70%" width="70%">
</center>

If we run that 500 hours/minute firehose of videos through our classifier, we'd get some distribution of spam probabilities ($P(spam)$). We could then set some probability threshold above which we send the video to a human to review.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/spam_flow.png" height="70%" width="70%">
</center>

Depending on where we set this threshold, we can cut down 90%, or 99%, or 99.999%, or any percent of videos to review. Awesome -- so we set our threshold to exclude 99.9999999% of videos, hire one reviewer to handle the remaining 1 minute per day, and congratulate ourselves for solving a tough problem.

But... that doesn't quite work. Unless our classifier is perfect (which it never is), **we're definitely missing a lot of bad content by setting our threshold so high.** Even if our model _is_ really accurate and we can automatically delete any video the model predicts is abusive, we'd still want _some_ people to review its decisions: we may not uncover biases or blind spots in our model if we never audit its outputs.

On the other hand, though, if we set our threshold for manual review too low, we'll start digging into the bulk of the green distribution above: the benign videos. The number of reviewers we'll need to hire will quickly skyrocket, and they'll spend much of their time reviewing benign videos.

The unsettling thing to realize is that **_there is actually no perfect threshold at all_**, meaning we either 1) miss spam if we set the threshold too high, or 2) waste reviewer hours by reviewing benign content. Until we have a superhuman [AGI](https://en.wikipedia.org/wiki/Artificial_general_intelligence) that can perfectly discern spam and non-spam videos in all countries and all languages, our model probabilities won't perfectly line up with spam and non-spam. In the simple example below, we can see that while green circles tend to be on the left and yellow triangles on the right, there is no line we can draw that will perfectly separate the circles and triangles.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/boundary.png" height="70%" width="70%">
</center>

**So how do we choose a "least-bad" threshold? What are the tradeoffs we face when picking a number that determines whether a video is sent to review or not? And how do we compare the performance of multiple potential models?**

To answer these questions, we need to understand **precision** and **recall**, two metrics that are provide a framework for navigating the tradeoffs of systems involving machine learning classifiers.

## Evaluation Framework
Let's start with a quick overview of how machine learning models are created and evaluated. Typically, our available data is split into _train_ and _test_ sets. (The test set can be split further to include _validation_ sets, too.) Our model uses an algorithm to learn the relationship between features and labels in our training data.

To ensure our model doesn't _overfit_ to our training data and just memorize every pair of features and labels, we use our _test_ set to evaluate its performance. We feed in the features from our test data, see what the model predicts, and compare those predictions to the actual labels. A solid performance on the test set ensures that our model is able to accurately generalize to data it hasn't seen before.

We've thrown around the word "performance" here, but we'll need to be much more specific to answer the questions from the previous section. Let's zoom in on these specific abuse _probabilities_ that our model outputs.

To compare our model outputs to the real-world labels, we need to convert a model's _probability that a video is abusive_ into a binary "yes, this is spam" or "no, this is benign" label. When we set a threshold (typically 50%), our model will then either predict that a video _is_ or _is not_ abusive. Meanwhile, in the real world, this video either _is_ or _is not_ spam. This leads us with four possibilities:
* **True Positive:** the model correctly identifies spam.
* **False Positive:** the model predicts spam, but the video is benign.
* **False Negative:** the model predicts benign, but the video is spam
* **True Negative:** the model correctly identifies a benign video.

We can arrange these possibilities in a **confusion matrix.** The columns of the matrix are the _predicted_ abuse and benign labels, and the rows are the _actual_ abuse and benign labels.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/confusion_matrix.png" alt="Confusion matrix" height="50%" width="50%">
</center>

Our first impression may be to maximize **accuracy:** our model's ability to detect true positives and true negatives. A model with perfect accuracy would perfectly predict the test set's labels and never have any false positives or false negatives.

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

## Taking it to the next level
I briefly mentioned that we may want _multiple_ classifiers for a task as complex as catching spam. One approach we could take is that if we have a _set number_ of videos that we want to review per day (rather than a set probability threshold, which as we've shown can be much harder to determine), we could try flipping this classification problem into a regression one.

[Facebook's News Feed](https://about.fb.com/news/2021/01/how-does-news-feed-predict-what-you-want-to-see/) works like this. There are a set of component models that target small chunks of a problem, like whether a user will like a piece of content, or start following the page that posted the content, etc. These models can be incredibly complex, but they ultimately output a probability that the action will occur. Then you can simply attach weights to each of the probabilities, sum them, and rank by these scores.  


From a financial standpoint, there is some "optimal" amount of bad stuff on a platform, given the cost of manual review, engineering development, etc. to identify and delete that bad content and the long-term benefit of users staying on the platform. To push a company beyond that point would require regulation (so there are significant financial penalties), an internal acceptance of operating sub-optimally (but with a higher ethical standard, for example) or to have users lower the threshold at which they would leave a platform.



## Footnotes
#### 1. [The context](#the-context)
2.5 billion MAU is a _lot_ of users! The only app with more monthly users is Facebook at [3.03 billion](https://www.statista.com/statistics/272014/global-social-networks-ranked-by-number-of-users/) in Oct 2023.
