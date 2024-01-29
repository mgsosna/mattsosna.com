---
layout: post
title: A/B Testing
author: matt_sosna
tags: statistics
---

**A/B test Definition**
* Way to quantify differences in some metric between two versions and say whether the differences are statistically significant.
* Split traffic in two. Doesn't need to be 50-50.
  * But what is the minimum number of people we need to run an A/B test on to be able to detect differences?

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



**Running the experiment**
* Should just change one thing at a time when comparing so you can isolate the cause of the difference.
* As a sanity check, you can also set up an A/A test where there are actually no differences between groups. This lets you test the testing infra itself, e.g., how users are randomly allocated between groups.

Examples:
* Frontend: layout of a page (e.g., image on left/right, button is blue vs. red)
* Backend: ML algorithm serving ads, how stories are ranked in Feed, etc.


Questions:
* Is it always a comparison of discrete groups? It'd be something else if I had a continuous variable I guess.
