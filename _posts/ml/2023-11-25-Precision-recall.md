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
Imagine we're launching a competitor to TikTok and Instagram. (Forget that they have [**1.1 billion**](https://www.demandsage.com/tiktok-user-statistics/) and [**2 billion**](https://www.statista.com/statistics/272014/global-social-networks-ranked-by-number-of-users/) monthly active users, respectively; we're feeling ambitious!) Our key differentiator in this tight market is that we guarantee users will have only the highest quality of videos: absolutely no "get rich quick" schemes, blatant reposts of existing content, URLs that infect your computer with malware, etc.

### Attempt 1: Human Review
To achieve this quality guarantee, we've hired a staggering 1,000 reviewers to audit every upload before it's allowed on the platform. **Some things just need a human touch**, we argue: video spam is too complex and context-dependent to rely on automated logic. A video that urges users to click on a URL could be a malicious phishing attempt or a benign fundraiser for Alzheimer's research, for example -- the stakes are too high to automate a decision like that.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/manual_review.png" height="60%" width="60%">
</center>

The app launches. To our delight, our "integrity first" message resonates with users and they join in droves. We quickly reach millions of users uploading 50,000 hours of video per day.

In other words, each reviewer now has _50 hours of video to review per day_. They try watching at 6x speed to get through all the videos, but they make mistakes: users start complaining both that **their benign videos are being blocked _and_ that spam is making it onto the platform.** We quickly hire more reviewers, but as our app grows and the firehose of uploads only gets bigger, we realize we'll bankrupt the company long before we can hire enough eyes.<sup>[[1]](#1-attempt-1-human-review)</sup> We need a different strategy.

### Attempt 2: Machine Learning
We can't replace a human's intuition, but maybe we can get close with machine learning. Given the tremendous advances in [computer vision](https://www.ibm.com/topics/computer-vision) and [natural language processing](https://www.ibm.com/topics/natural-language-processing) over the past decade, we can extract **features** from the videos: the pixel similarity to existing videos, keywords from the audio, whether the video appears to have been [generated with AI](https://www.techtarget.com/searchenterpriseai/definition/generative-AI), etc. We can then see how these features relate to whether a video is spam.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/numbers.png" height="85%" width="85%">
</center>

Determining the relationship between features and spam labels is best left to an algorithm.<sup>[[2]](#2-attempt-2-machine-learning)</sup> The feature space is simply too large for a human to understand: features interact non-linearly, have complex dependencies, are useful in some contexts but useless in others, and so on. So we use machine learning to **train a classifier that _predicts_ whether a video is spam.** Our model takes in a video and outputs the probability that the video is spam.<sup>[[3]](#3-attempt-2-machine-learning)</sup>

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/scaled_review.png" height="60%" width="60%">
</center>

When we first run our classifier on videos we know are spam and benign, we hope to see something like below: two distributions neatly separable by their probability of being spam. In this ideal state, there is a spam probability threshold below which _all videos are benign_ and above which _all videos are spam_, and we can use that threshold to perfectly categorize new videos.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/spam_dist1.png" height="90%" width="90%">
</center>

But what we actually see is that **the probability distributions overlap.** Yes, the vast majority of benign videos have a low probability and the vast majority of spam videos have a high probability. But **there's an uncomfortable "intermediate" spam probability where it's impossible to tell if a video is spam or benign.**

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/spam_dist2.png" height="90%" width="90%">
</center>

If we zoom in on where the distributions overlap, it looks something like this. Nowhere can we draw a line that perfectly separates benign videos from spam. If we set the threshold too high, then spam makes it onto the platform. If we set the threshold too low, then benign videos are incorrectly blocked.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/boundary.png" height="95%" width="95%">
</center>

**So how do we choose a "least-bad" threshold?** To answer this question, we need to understand **precision** and **recall**, two metrics that provide a framework for navigating the tradeoffs of any classification system. We'll then revisit our app with our new understanding and see if there's a way to optimally classify spam.

## Evaluation Framework
### Model Creation
Let's start with a quick overview of how machine learning classifiers are created and evaluated, using our spam classifier as an example. The first step when training our model is to split our data into **_train_** and **_test_** sets. An algorithm then parses the training data to learn the relationship between features and labels (spam or benign). The result is a model that can take in the features of a video and return the probability it is spam.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/training1.png" alt="Training a machine learning classifier">
</center>

Probabilities are great, but we need some way to convert numbers like 0.17 or 0.55 into a decision on whether a video is spam or not. So we binarize the outputted probabilities -- by default at 0.5 -- into _spam_ or _benign_ classifications. For an arbitrary feature in our model, the model's probability curve (black line) and classifications (yellow and green regions) might look like this.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/classify1.png" height="75%" width="75%">
</center>

Our model is a best effort at understanding the data it was given. But while understanding the data _we have_ is useful, the real goal is to be able to predict the labels for data _we haven't seen before_, like incoming uploaded videos.<sup>[[4]](#4-evaluation-framework)</sup> We measure our model's ability to do so with the _test_ data: feature-label pairs that weren't used to train the model. We feed in the features from our test data, see what the model predicts, and compare those predictions to the actual labels. (This is why we don't train the model on all available data: we need some holdout labels to audit the model's predictions.)

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/training2.png" alt="Training a machine learning classifier" height="55%" width="55%">
</center>

There are four components to measuring our model's ability to classify new data, based on the four possible outcomes of a prediction:
* **True Positive:** the model correctly identifies spam.
* **False Positive:** the model predicts spam, but the video is benign.
* **False Negative:** the model predicts benign, but the video is spam.
* **True Negative:** the model correctly identifies a benign video.

We can arrange these outcomes in a **confusion matrix.** The columns of the matrix are the _predicted_ spam and benign labels, and the rows are the _actual_ spam and benign labels.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/cm2.png" alt="Confusion matrix" height="55%" width="55%">
</center>

We said earlier that our model's spam probabilities are binarized at 0.5 into _spam_ and _benign_ classifications. But 0.5 isn't always the best threshold, especially if the data is imbalanced. We could set our threshold to any value between 0 and 1 to better partition our classifications.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/classify2.png">
</center>

**These thresholds will generate different confusion matrices, reflecting differing ability of each model to accurately generalize to new data.** So how we choose a threshold? To answer this, we'll need to review a few metrics.

### Metric 1: Accuracy
Our first strategy for finding a metric that produces the best model may be to maximize **accuracy:** our model's ability to detect true positives (TP) and true negatives (TN). Accuracy, in other words, is **_the proportion of labels that our model correctly predicted_**. A model with perfect accuracy would have zero false positives (FP) or false negatives (FN).

$$Accuracy = \frac{TP+TN}{TP+FP+FN+TN}$$

Accuracy is an intuitive metric to start with, but it can hide some blindspots in our model. If [one label is far more frequent than the other](https://developers.google.com/machine-learning/data-prep/construct/sampling-splitting/imbalanced-data), for example, our model may struggle to predict the less frequent labels or even converge on a nonsensical rule! If our training data was just a random sample of uploaded videos, for example, we may end up with 99.9% benign videos and 0.1% spam. **A model that always predicts that a video is benign would be 99.9% accurate.** That's not good at all -- we'd miss all the videos we want to catch!

Even with balanced data, we should never rely solely on accuracy when judging a model. Let's look at other metrics that can give us a more holistic picture.

### Metric 2: Recall
If it's important for our model to flag all positive labels, we'll want a metric like **recall**. Recall is **_the proportion of <u>positive</u> labels our model correctly predicted._** In other words:

$$Recall = \frac{TP}{TP+FN}$$

We can think of this as the top row of the confusion matrix. Recall is the number of true positives divided by the total number of _positive labels_: labels our model caught (true positives) and missed (false negatives). A model with 100% recall is one that correctly classified all positive labels in the test set.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/cm_recall.png" alt="Recall columns of confusion matrix" height="50%" width="50%">
</center>

That 99.9% accurate "always predict benign" model would have _zero_ recall, a glaring red flag indicating the model should be immediately thrown out. Ideally, our model is sensitive enough to catch all spam labels in the test set. But to ensure this sensitivity doesn't come at the expense of mis-labeling benign videos, we need to look at one more metric: precision.

### Metric 3: Precision
When our model classifies a video as spam, how often is it _actually_ spam? This is the core idea behind **precision**, or **_the proportion of predicted positive labels that are true positives_**. As an equation, precision takes the following form:

$$Precision = \frac{TP}{TP+FP}$$

We can think of this as the left column of the confusion matrix. Precision is the number of true positives divided by the total number of _predictions_: those that were correct (true positives) and incorrect (false positives).

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/cm_precision.png" alt="Precision columns of confusion matrix" height="50%" width="50%">
</center>

Precision is a crucial metric for understanding how confident we should be when our model predicts that a video is spam. When a high-precision model predicts that a video is spam, the video is likely spam; if the model has low precision, who knows if it's actually spam unless we look at it ourselves.

It may therefore be tempting to just optimize for precision, maximizing our confidence in the model's predictions. **But the more we prioritize precision, the more _conservative_ our model will be with labeling videos as spam**, meaning we'll inevitably miss some spam videos that should have been caught.

To illustrate this, let's look at that diagram of the overlap of benign and spam distributions again. We can binarize our spam probabilities at two thresholds: A or B.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/boundary1.png" height="85%" width="85%">
</center>

Every video to the right of threshold B is spam, so a classifier that binarizes at that spam probability will have 100% precision. That's impressive, but that threshold misses the two spam videos to the left. Those videos would be incorrectly classified benign (false negatives) because our model isn't confident enough that they're spam. Meanwhile, a model whose cutoff is threshold A would catch those spam videos, but it would also mis-label the three benign videos to the right (false positives), resulting in lower precision.  

### Striking a balance
This tradeoff gets at the inherent tension between precision and recall: **when we increase our classification threshold, we _increase precision_ but _decrease recall_.** We can redraw our figure to highlight this tradeoff.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/boundary2.png" height="90%" width="90%">
</center>

Another way to visualize this is to plot precision and recall as a function of the classification threshold. Using a [classifier I trained on some sample data](#code), we can see how precision increases as we increase our threshold but recall steadily decreases. The higher our threshold, the more accurate our model's predictions become, but also the more spam videos we miss.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/precision_vs_recall.png" height="80%" width="80%">
</center>

So how do we strike a balance? Ultimately, **we must ask whether we're more comfortable with false positives or false negatives, and by how much**. Is it worse if some users are incorrectly blocked from uploading videos or if they encounter scams on the platform? Is it worth blocking 100 benign videos to prevent 1 spam video? 1000 benign videos?

Our app's main selling point was that users would never see spam videos. To achieve 100% recall with our classifier, we'd have to settle for around 45% precision -- an embarrassingly imprecise model that would result in thousands of benign videos being blocked daily. If we were comfortable with only catching 90% of spam, we could perhaps get up to 60% precision, but we'd still be blocking far too many videos as well as allowing spam through.

### Comparing models
We go back to the drawing board, digging deep into the data to find better features associated with spam. We identify some promising trends and retrain our classifier. When we visualize the precision and recall versus classification threshold for our old and new models, we see something like the plot below; the solid lines are the old model and the dashed lines are the new.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/precision_vs_recall2.png" height="80%" width="80%">
</center>

That's looking a lot better! For most thresholds, the new model is a huge improvement in both precision and recall, making our tradeoff discussions more palatable. The highest precision we can now get while maintaining 100% recall is roughly 60%. At 90% recall, we have 85% precision.

We can summarize our improvement in model fit across all thresholds with **AUC-ROC**, or the **Area Under the ROC** (Receiver Operator Characteristic). An ROC curve is a plot of the true positive rate (recall) versus the false positive rate (how often benign videos are flagged as spam). The area under this curve is 1 if our model can perfectly separate benign and spam videos across all thresholds, 0.5 if it is no better than randomly guessing (the gray dashed line below), and somewhere in between otherwise. This one number provides a quick way to show the overall improvement in our new model (with an AUC of 0.96) compared to the old one (AUC of 0.84).

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/auc2.png" height="80%" width="80%">
</center>

So by any metric, we can celebrate our improved ability to fight spam with our new classifier. But we're left looking uncomfortably at our commitment to absolutely zero spam videos on our app. To achieve 100% recall, do we really need to settle for 60% precision, barely better than a coin flip, when classifying videos uploaded to our app? Do we need to go back to model development, or is there anything else we can do?

## Spam Prevalence Equilibria
### Attempt 3: Machine Learning + Human Review
If we continue thinking solely in terms of machine learning, we're going to spend a lot of effort chasing diminishing returns. Yes, we can find better features, algorithms, and hyperparameters to improve model fit. But if we take a step back, we can see that **our classifier is really only one part of a _funnel_ for identifying spam**, and that we'll be far more successful investing in _the funnel as a whole_ rather than just the machine learning portion.

If we revisit our overlapping spam distribution figure from before, we can define three regions of spam probabilities: confidently benign, confidently spam, and "not sure." We spent much of this post explaining precision and recall as a way to navigate the region of uncertainty in terms of our classifier threshold. But we can take this a step further by bringing back our human reviewers.

<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/spam_dist3.png">
</center>


What if we rely on our classifier for these videos where it's very confident? Then for the videos it's not sure about, we pull in our human reviewers.




(change figure so it's like the ends get enforced automatically, and the middle is sent out to review.)


<center>
<img src="{{  site.baseurl  }}/images/ml/precision_recall/spam_flow.png" height="70%" width="70%">
</center>

Depending on where we set this threshold, we can cut down 90%, or 99%, or 99.999%, or any percent of videos to review. Awesome -- so we set our threshold to exclude 99.9999999% of videos, hire one reviewer to handle the remaining 1 minute per day, and congratulate ourselves for solving a tough problem.

But... that doesn't quite work. Unless our classifier is perfect (which it never is), **we're definitely missing a lot of bad content by setting our threshold so high.** Even if our model _is_ really accurate and we can automatically delete any video the model predicts is abusive, we'd still want _some_ people to review its decisions: we may not uncover biases or blind spots in our model if we never audit its outputs.

On the other hand, though, if we set our threshold for manual review too low, we'll start digging into the bulk of the green distribution above: the benign videos. The number of reviewers we'll need to hire will quickly skyrocket, and they'll spend much of their time reviewing benign videos.

**So how do we choose a "least-bad" threshold? What are the tradeoffs we face when picking a number that determines whether a video is sent to review or not? And how do we compare the performance of multiple potential models?**

To answer these questions, we need to understand **precision** and **recall**, two metrics that are provide a framework for navigating the tradeoffs of systems involving machine learning classifiers.


Finally, we can use a high-recall classifier for proxy labels of spam if we wanted to get estimates of how prevalent spam was on our platform.


From a financial standpoint, there is some "optimal" amount of bad stuff on a platform, given the cost of manual review, engineering development, etc. to identify and delete that bad content and the long-term benefit of users staying on the platform. To push a company beyond that point would require regulation (so there are significant financial penalties), an internal acceptance of operating sub-optimally (but with a higher ethical standard, for example) or to have users lower the threshold at which they would leave a platform.

Regulations, user sentiment.

Precision is a useful metric when there's a high cost of false positives. Relying on a low-precision classifier that predicts [whether someone is likely to commit a crime](https://www.brennancenter.org/our-work/research-reports/predictive-policing-explained), for example, would lead to innocent people being arrested.

If our data is heavily imbalanced, we can perform techniques like [upsampling the minority class](https://developers.google.com/machine-learning/data-prep/construct/sampling-splitting/imbalanced-data).

## Conclusions
Thanks for reading.<br>
Matt

## Code
Here is the code for generating the data and classifier, as well as plotting the precision vs. recall graph.

{% include header-python.html %}
```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import train_test_split

# Generate labels
is_spam = np.concatenate(
    [
        np.random.choice([0, 1], p=[0.9, 0.1], size=200),
        np.random.choice([0, 1], p=[0.8, 0.2], size=200),
        np.random.choice([0, 1], p=[0.6, 0.4], size=200),
        np.random.choice([0, 1], p=[0.4, 0.6], size=200),
        np.random.choice([0, 1], p=[0.1, 0.9], size=200),
    ]
)

# Generate features
feature_1 = [np.random.normal(0, 1.5, 1) if x == 0 else np.random.normal(3, 1.5, 1) for x in is_spam]
feature_2 = [np.random.normal(0, 2.5, 1) if x == 0 else np.random.normal(3, 2.5, 1) for x in is_spam]

df = pd.DataFrame(
    {
        'is_spam': is_spam,
        'feature_1': feature_1,
        'feature_2': feature_2,
    }
)

############################################################
# Train classifier
X = df[['feature_1', 'feature_2']]
y = df['is_spam']

X_train, X_test, y_train, y_test = train_test_split(X, y)

mod = LogisticRegression()
mod.fit(X_train, y_train)

############################################################
# Generate predictions
preds = mod.predict_proba(X_test)[:,1]
precision, recall, thresholds = precision_recall_curve(y_test, preds)

df = pd.DataFrame(
    {
        'precision': precision[:-1],
        'recall': recall[:-1],
        'threshold': thresholds,
    }
)

############################################################
# Plot precision/recall vs. threshold
plt.plot(df['threshold'], df['precision'], label='Precision', color='C0')
plt.plot(df['threshold'], df['recall'], label='Recall', color='goldenrod')
plt.xlabel("Classification threshold", fontsize=14)
plt.ylabel("Precision or Recall", fontsize=14)
plt.legend(fontsize=12, framealpha=1)
plt.grid()
plt.savefig("precision_vs_recall.png", dpi=400, bbox_inches='tight')
plt.show()
```


## Footnotes
#### 1. [Attempt 1: Human Review](#attempt-1-human-review)
To illustrate how impractical 100% human review is, consider YouTube. Users upload [**over 500 hours of video every minute**](https://www.statista.com/statistics/259477/hours-of-video-uploaded-to-youtube-every-minute/), or **1.8 million hours per day.** Reviewing this number of videos manually would require _75,000 reviewers_ watching videos 24/7, or _240,000_ if reviewers only work 8-hour shifts and have a lunch break. Add 1,000 to handle _re-reviewing_ videos whose creators [claim were incorrectly deleted](https://www.tspa.org/curriculum/ts-fundamentals/content-moderation-and-operations/user-appeals/). We're left with **241,000 reviewers**, or [160% the number of Google employees](https://www.macrotrends.net/stocks/charts/GOOG/alphabet/number-of-employees). That's not going to work.

#### 2. [Attempt 2: Machine Learning](#attempt-2-machine-learning)
Note that machine learning isn't the only option for fighting spam. There _is_ a solid use case for hand-crafted deterministic rules for subsets of spam. Something like "how often should a user be allowed to post a video?" probably doesn't need a dedicated ML classifier and could be inferred from a distribution of the number of times users post in a day, for example.

#### 3. [Attempt 2: Machine Learning](#attempt-2-machine-learning)
I write "model" here but our spam classifier can actually be an [ensemble](https://en.wikipedia.org/wiki/Ensemble_learning) of models, each trained on different subsets of spam. This is how [Facebook's News Feed](https://about.fb.com/news/2021/01/how-does-news-feed-predict-what-you-want-to-see/) works, for example. There are a set of component models that target small chunks of a problem, like whether a user will like a piece of content, or start following the page that posted the content, etc. These models can be incredibly complex, but they ultimately output a probability that the action will occur. Then you can simply attach weights to each of the probabilities, sum them, and rank by these scores. This is one way to navigate the tradeoff of high accuracy and low explainability of complex models (like what, exactly, leads to a person deciding to react with a heart emoji on a post) while having explainability in the overall ranking of an item in the feed.

#### 4. [Evaluation framework](#evaluation-framework)
Modeling just the existing data can be useful, too, but this falls more in the realm of business intelligence or data analytics. The goal there is to understand our data, the relationships between features, etc. but there is not necessarily a _predictive_ component of trying to understand future data.
