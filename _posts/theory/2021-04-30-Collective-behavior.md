---
layout: post
title: Fish schools as ensemble learning algorithms
author: matt_sosna
---
<img src="{{  site.baseurl  }}/images/theory/coll_beh/koi_shoal.jpg" alt="Fish school">
<span style="font-size: 12px"><i>Photo by <a href="https://unsplash.com/@jwimmerli">jean wimmerlin</a> on <a href="https://unsplash.com">Unsplash</a></i></span>

Animal groups are greater than the sum of their parts. It's flocks of birds that migrate, colonies of bees that build and maintain hives, and schools of fish that elegantly evade predators. Individual birds, bees, or fish are often clueless on what to do, but somehow the aggregate is capable. How does this happen?

I spent my Ph.D. puzzling over how *simple local interactions* can give rise to *complex group-level behaviors* not possible at the individual level, specifically how the information transmission networks in fish schools enable them to avoid predators.

But at the end of my Ph.D., I decided to [leave academia and enter data science]({{  site.baseurl  }}/Academia-to-DS)...

The short answer is that it's incredibly complicated! But there is one simple mechanism that caught my attention again when I left academia and started working in data science. I saw a curious parallel between the wisdom of the crowds (i.e. many-wrongs hypothesis) and the accuracy of ensemble methods.

In short, this post will show how fish are trees. Specifically, weak learners in a random forest. Let's get started!

### Fish
For fish species that live in large groups, staying close to others is often not a choice $-$ it's a matter of life or death. The surrounding environment is too unpredictable and too dangerous to go alone. I can try to find food by myself, or detect a predator early and hide, but it's easier when you're in a group. Then let's say the predator actually _does_ arrive - if you're the only one around, he can target you, but if you're in a big group, your risk is diluted by the presence of everyone around you.


## RF
So how does a random forest work? Well in brief, you have a collection of decision trees. Each tree is trained on bootstrapped replicates of the training data, sometimes on a subset of the features.

## Conclusions
Alternate title: "Fish schools use XGBoost to survive"
