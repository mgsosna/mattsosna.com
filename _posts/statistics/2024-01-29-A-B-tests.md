---
layout: post
title: Navigating Big Decisions with Experiments
author: matt_sosna
tags: statistics
---

The average adult makes [**35,000 decisions**](https://hbr.org/2023/12/a-simple-way-to-make-better-decisions) per day. The stakes are low for most of these -- choosing the "wrong" lunch or outfit doesn't really matter. (Usually!) But some of these decisions can be momentous, especially in business, where the wrong move can cost time, money, or even the future of your company.

Imagine you're running an e-commerce startup and just launched a "Products You Might Like" feature. Your engineers invested significant resources building a solid recommender system, but customer engagement is unfortunately far lower than you expected. Your company is burning through cash, so you need to get these recommendations right. The engineers are eager to start making tweaks, **but what if changing the algorithm actually _worsens_ engagement?** (More existentially, what if the added revenue from a PYML service never outweighs the cost of running it?) In this high-pressure moment, how do you decide between staying the course or pivoting?

<img src="{{  site.baseurl  }}/images/statistics/a-b/choice.jpg">
<span style="font-size: 12px"><i>Photo by <a href="https://unsplash.com/@burst">Burst</a> on <a href="https://unsplash.com">Unsplash</a></i></span>

These questions ultimately revolve around **_how we navigate uncertainty when making decisions_**. We often don't have enough information to identify the best path to take, so unless we're ok with outright guessing, we need some way to efficiently and effectively gather information about our options.

Our botched launch -- and further failed iterations -- could have been avoided through **experimentation**, of which **A/B testing** is the gold standard. In this post, we'll cover experimentation and why it's important, how to set up A/B tests and interpret the results, and how to understand and avoid classic caveats and traps.

## Background
### How are decisions made?
First, how did we get into this situation where we blindly launched a product with an assumption that it would increase purchases? Before we cover A/B testing, it's worth thinking more broadly about how people decide to launch products in general. A/B testing is at the end of a long ladder of sophistication, but that doesn't mean it's by default the best option.

1. Don't ask anyone
2. Ask someone
3. Ask a few people
4. Experiment

#### Level 1: Just make the change
Self-explanatory. Just do it. I'll include asking around your company and getting alignment internally before launching, since unless you're a 1-person startup you're going to need to convince someone else what you're doing.

<center>
<img src="{{  site.baseurl  }}/images/statistics/a-b/change-1.png" height="60%" width="60%">
</center>

One option is to just make the change outright. If you're confident it's an improvement, then just do it. But that's risky: what if the change makes it worse? What if something breaks? What if it leads to a huge drop in user engagement? You like the new version, but will your customers?

#### Level 2: Ask a few customers
Another option is to pay some users to look at the new version and tell you. This [focus group](https://www.shopify.com/blog/what-is-a-focus-group) is useful, since you can get detailed info on the proposed changes. But it's a lot of work -- you need to carefully select participants to make sure they're representative of your app's audience, curate their feedback carefully to avoid biasing them, etc. Cost might not be a big deal but it still costs something to hire these participants. And it takes time to get your group together, get their feedback and process it. And you might end up with a lot of qualitative feedback rather than quantitative metric changes.

<center>
<img src="{{  site.baseurl  }}/images/statistics/a-b/change-2.png" height="60%" width="60%">
</center>

#### Level 3: Split traffic to each version
So what if there was some way to test changes in real time? What if the change is so small that a focus group doesn't even make sense? Or it's something a user might not really notice, like a backend change: a latency reduction of a few milliseconds when rendering an image, for example?

## Experiments
What is an experiment? What does it mean?

<img src="{{  site.baseurl  }}/images/statistics/a-b/experiments.jpg" loading="lazy" alt="A row of plants in Erlenmeyer flasks">
<span style="font-size: 12px"><i>Photo by <a href="https://unsplash.com/@chuttersnap">Chuttersnap</a> on <a href="https://unsplash.com">Unsplash</a></i></span>

<img src="{{  site.baseurl  }}/images/statistics/a-b/risk_mitigation_ladder.png" loading="lazy" alt="A ladder of increasing confidence in making a decision">
<span style="font-size: 12px"><i>Image from <a href="https://confidence.spotify.com/blog/smaller-sample-experiments?mrt">Experiments with Smaller Samples</a> by Mårten Schultzberg</i></span>



[Experiments with Smaller Samples](https://confidence.spotify.com/blog/smaller-sample-experiments?mrt):



### Designing the experiment
### 1. What are the target metrics?
What are we actually trying to change? How will we quantify the effectiveness of treatment vs. control? There are actually lots of metrics you'll want to test for: the success ones you care about (like user engagement). But then you'll want to have **guardrails** around metrics you don't want to regress, like long-term retention, how long it takes Feed to load, user appeals, etc.

It's important to identify these ahead of time for a few reasons. If you know the data you care about ahead of time, it's a lot easier to collect that data. (You might not even be able to collect it ad hoc if you don't have good automated data infra anyway.) It also helps keep you honest rather than fishing around for significance. If you didn't know the answer, what would you care about? Based on the high-level business needs, how do you define success in general? Rather than trying to move a project-specific metric that isn't ultimately that meaningful.


Some concepts:
* **Online** vs. **offline** testing.

What's the actual test:
* [Permutation tests](https://en.wikipedia.org/wiki/Permutation_test) are non-parametric: they don't assume the data are normally distributed. Generally safer than something like a t-test.
  * Null hypothesis is that all samples come from same distribution.
  * Measure difference in means from popA and popB, then lump all the data together and randomly allocate samples to "A" and "B" and measure difference in means. Then see where your true difference falls on the distribution of differences.
* Stratified sampling: if there are factors (e.g., demographics) that could affect the outcome, should sample in a way that these groups are equally represented across treatments. (But otherwise should have random assignment.)
* Sample size must be large enough to have statistical power. Also make sure to run it long enough to handle weekly variation, etc.
* Adjust for multiple comparisons (e.g., ANOVA, Bonferroni correction)
* Think effect size: does small but significant really matter?

Need to cover confidence intervals, which [don't make sense with permutation tests](https://stats.stackexchange.com/questions/2220/how-do-we-create-a-confidence-interval-for-the-parameter-of-a-permutation-test) since there isn't an interval around a test statistic. (Would be like a CI on a p-value.)
* CI is point estimate +/- (SE * critical value (like 1.96 for 95%))
  * It's like "in the treatment we had 500 users and their distribution of CLR is X. Look at variation in the CLR, calculate SE, etc."
    * What if the sample size is enormous? Do CIs become meaningless?


$$
CI = \bar{x} \pm z\frac{s}{\sqrt{n}}
$$
* $\bar{x}$ is the sample mean, or point estimate.
* $z$ is the critical value, or the score used for a particular confidence level (e.g., 1.96 for 95% confidence)
* $s$ is the sample standard deviation
* $n$ is the sample size.

Note that $s$ is divided by the _square root_ of $n$, which means that we can still have meaningful interval ranges even when the sample size is large.


**A/B test Definition**
* Way to quantify differences in some metric between two versions and say whether the differences are statistically significant.
* Split traffic in two. Doesn't need to be 50-50.
  * What's important is the minimum number of people we need to run an A/B test on to be able to detect differences. If you have a massive volume, you could even do something like 1% vs. 99%. Can also do this in terms of a rollout by country/user segment rather than globally.

**Notes**
* Businesses think they know their customers, but they can often have unexpected behavior. Customers themselves might not even know that they're subconsciously behaving a certain way.
* A/B tests are a way to guide decision-making for product launches. Evaluate some success metric on a subset of users.

**Designing the experiment**
* Simplest version: control A, treatment B.
* Should declare the metric before you begin!
  * Conversion rate, newsletter opens, ad clicks
* How long to run the test?
  * Need to determine the sample size.
    * Type II error (power), significance level, minimum detectable effect

$$N = \frac{16\sigma^2}{\delta^2}$$

### Running the experiment
* Should just change one thing at a time when comparing so you can isolate the cause of the difference.
* As a sanity check, you can also set up an A/A test where there are actually no differences between groups. This lets you test the testing infra itself, e.g., how users are randomly allocated between groups.

Examples:
* Frontend: layout of a page (e.g., image on left/right, button is blue vs. red)
* Backend: ML algorithm serving ads, how stories are ranked in Feed, etc.


You might think of it as the color of a button on the frontend.

<center>
<img src="{{  site.baseurl  }}/images/statistics/a-b/a_vs_b.png" height="80%" width="80%">
</center>

But it could also be _how_ that frontend is generated: a different retrieval system for user data, for example. An A/B test here is particularly important, since users' opinions might not be reliable. (And users might not even be directly affected. Important metric but not the only one - could use proxies.)



How can we tell if a change is good? Are things the _same_ or _different_?
* And by how much? Is it worth actually changing things?
* Confidence intervals

<center>
<img src="{{  site.baseurl  }}/images/statistics/a-b/metric_shifts.png" height="50%" width="50%">
</center>

### Demo

Technically, a true permutation test requires generating the distribution of _every permutation_ of samples allocated to subset A vs. subset B. But unless our datasets are tiny, this is prohibitively expensive: the time cost [grows as a function of $O(n!)$]({{  site.baseurl  }}/CSDS-Intro#big-o-notation). Instead, we can approximate the distribution by permuting the data some `n_iter` of times, where `n_iter` is decently large.

{% include header-python.html %}
```python
import numpy as np

def permutation_test(
    pop_a: np.ndarray,
    pop_b: np.ndarray,
    n_iter: int = 1000
) -> float:
    """
    Returns the p-value of the difference in means
    between pop_a and pop_b.
    """
    true_diff = np.mean(pop_a) - np.mean(pop_b)
    combined = np.concatenate([pop_a, pop_b])
    diffs = _generate_diff_dist(combined, n_iter)

    return min(
        np.mean(true_diff <= diffs),
        np.mean(true_diff >= diffs)
    )

def _generate_diff_dist(
    combined: np.ndarray,
    n_iter: int
) -> list:
    """
    Generates list of differences
    """
    diffs = []

    for _ in range(n_iter):
        np.random.shuffle(combined)
        sim_pop_a, sim_pop_b = np.split(combined, 2)
        sim_diff = np.mean(sim_pop_a) - np.mean(sim_pop_b)
        diffs.append(sim_diff)

    return diffs
```

Now if we run an actual test.

{% include header-python.html %}
```python
pop_a = np.random.normal(0, 1, 1000)
pop_b = np.random.normal(0.1, 1, 1000)

permutation_test(pop_a, pop_b, 10000)
# 0.0019
```

We can also do this for distributions that aren't Gaussian. The distribution of differences actually ends up being normal, too. Though the amount of data we require to tell whether the samples come from the same population may increase quite a bit.

{% include header-python.html %}
```python
pop_a = np.random.beta(10, 1, 1000)
pop_b = np.random.beta(10.1, 1, 1000)
permutation_test(pop_a, pop_b, 10000)
# 0.453
```

We can generate a distribution of differences and see where our true difference falls on this distribution. The proportion of the distribution that is equal to or more extreme than our true difference can be interpreted as a p-value.

## Footnotes
#### 1. [Intro](#)
An even more existential question is whether the benefits of a "Products You Might Like" service will ever outweigh the costs of running it.
