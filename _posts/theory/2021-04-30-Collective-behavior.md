---
layout: post
title: Fish schools as ensemble learning algorithms
author: matt_sosna
---
<img src="{{  site.baseurl  }}/images/theory/coll_beh/koi_shoal.jpg" alt="Fish school">
<span style="font-size: 12px"><i>Photo by <a href="https://unsplash.com/@jwimmerli">jean wimmerlin</a> on <a href="https://unsplash.com">Unsplash</a></i></span>

**Animal groups are greater than the sum of their parts.** The individual termite wanders cluelessly while the colony builds a sturdy and [well-ventilated mound](http://www.bbc.com/earth/story/20151210-why-termites-build-such-enormous-skyscrapers). The individual stork loses its way while [the flock successfully migrates](https://flightforsurvival.org/white-stork/). Across the spectrum of cognitive complexity, we regularly see the emergence of behaviors at the group level that the individuals aren't capable of. How is this possible?

I spent my Ph.D. puzzling over how golden shiner fish $-$ a generally hopeless and not very intelligent creature $-$ form groups capable of elegantly evading predators. The short answer is that it's complicated! The slightly longer answer is that shiners have evolved mechanisms of translating noisy *social cues* into decisions more accurate than they could reach themselves.

As I neared the end of my Ph.D., I decided to [leave academia and enter data science]({{  site.baseurl  }}/Academia-to-DS). All the knowledge I gained on fish seemed destined to turn into a pile of dusty facts in some corner of my brain, never to be used again. But as I started my data science education, I was surprised to see a curious parallel between how the fish I'd studied make decisions, and how ensemble learning algorithms work. This post will convince you that while individual fish are weak learners, together they form an accurate information processor.

### Fish
For fish species that live in large groups, staying close to others is often not a choice $-$ it's a matter of life or death. The surrounding environment is too unpredictable and too dangerous to go alone. I can try to find food by myself, or detect a predator early and hide, but it's easier when you're in a group. Then let's say the predator actually _does_ arrive - if you're the only one around, he can target you, but if you're in a big group, your risk is diluted by the presence of everyone around you.


Wisdom of the crowds
* Started by statistician [Sir Francis Galton](https://en.wikipedia.org/wiki/Francis_Galton) in 1907. Competition at a livestock fair to estimate weight of ox. Nearly 800 farmers guessed, and there was considerable variation. The mean of the guesses turned out to be more accurate than any individual guess.


### RF
So how does a random forest work? Well in brief, you have a collection of decision trees. Each tree is trained on bootstrapped replicates of the training data, sometimes on a subset of the features.


Note: the trees in a forest are uncorrelated. That isn't the case in nature; fish close to one another in the school have highly correlated social information. But especially in fission-fusion species, they likely differ in their personal experience, their knowledge about the environment or how to interpret cues.

Spatial and temporal correlation: http://thekaolab.com/inc/papers/kao2014.pdf

## Conclusions
Alternate title: "Fish schools use XGBoost to survive"
