---
layout: post
title: Fish schools as ensemble learning algorithms
author: matt_sosna
---
<img src="{{  site.baseurl  }}/images/theory/coll_beh/koi_shoal.jpg" alt="Fish school">
<span style="font-size: 12px"><i>Photo by <a href="https://unsplash.com/@jwimmerli">jean wimmerlin</a> on <a href="https://unsplash.com">Unsplash</a></i></span>

**Animal groups are greater than the sum of their parts.** The individual termite wanders cluelessly while the colony builds a sturdy and [well-ventilated mound](http://www.bbc.com/earth/story/20151210-why-termites-build-such-enormous-skyscrapers). The lone stork loses its way while [the flock successfully migrates](https://flightforsurvival.org/white-stork/). Across the spectrum of cognitive complexity, we regularly see the emergence of behaviors at the group level that the members alone aren't capable of. How is this possible?

I spent my Ph.D. puzzling over how golden shiner fish $-$ a generally hopeless and not very intelligent creature $-$ form schools capable of elegantly evading predators. I read dozens of articles and textbooks, conducted experiments, analyzed data, and worked with theorists to try to make sense of how when it comes to animal groups, $1 + 1 = 3$, not $2$.

All the knowledge I gained seemed destined to become a pile of dusty facts in some corner of my brain when I [left academia to enter data science]({{  site.baseurl  }}/Academia-to-DS). But as I started my data science education, I was surprised to see a curious parallel between _**decision-making in the fish I'd studied**_, and _**decision-making in [ensemble learning](http://www.scholarpedia.org/article/Ensemble_learning) algorithms**_.

This post will show you how ensembles of weak learners $-$ whether they're fish or decision trees $-$ can together form an accurate information processor.

### The machine
Let's first cover the machine learning side, since you're probably more familiar with algorithms than animals! **Ensemble learning methods use a _set_ of models to generate a prediction,** rather than one single model. The idea is that the errors in the models' predictions cancel out, leading to more accurate predictions overall.

In the schematic below, our ensemble is the set of gray boxes, each of which is a model. To generate a predicted value for the input, the input is sent into each model, which generates a prediction. These individual predictions are then collapsed into one _aggregate_ prediction by either averaging (for regression) or taking the majority vote (for classification).

<img src="{{ site.baseurl }}/images/theory/coll_beh/ensemble.png">

One popular ensemble method is a [**random forest**](https://en.wikipedia.org/wiki/Random_forest), a model that consists of dozens or hundreds of [decision trees](https://en.wikipedia.org/wiki/Decision_tree). While there are [plenty of ways](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) to configure how the forest is assembled, the general process is that each tree is independently trained on [bootstrapped](https://machinelearningmastery.com/a-gentle-introduction-to-the-bootstrap-method/) observations and random subsets of the features. (If we used the same data for each tree, we'd create the same tree each time!)

The result is a collection of models, **each with a _slightly different understanding_ of the training data.** This variation is crucial. Individual decision trees easily become [overfit](https://www.investopedia.com/terms/o/overfitting.asp) to their training data, meaning they fail to generalize well to new data. But because the ensemble consists of many trees, these errors tend to cancel one another out, leading to a more accurate model overall.

### The theory
The enhanced accuracy of a random forest can be summarized as the [wisdom of the crowds](https://en.wikipedia.org/wiki/Wisdom_of_the_crowd). The concept dates back to 1906 at a livestock fair in Plymouth, MA, which held a competition to guess the weight of an ox. Nearly 800 farmers gave their best estimates. Statistician [Sir Francis Galton](https://en.wikipedia.org/wiki/Francis_Galton) later examined the guesses and observed that while individual estimates varied widely, the _mean_ of the estimates was more accurate than any individual guess. Galton went on to formalize his theory in his famous [_Vox Populi_ paper](https://www.all-about-psychology.com/the-wisdom-of-crowds.html).

<img src="{{  site.baseurl  }}/images/theory/coll_beh/ox.jpg" loading="lazy">
<span style="font-size: 12px"><i>Photo by <a href="https://www.pexels.com/@pixabay">Pixabay</a> from <a href="https://www.pexels.com/photo/brown-bull-on-green-glass-field-under-grey-and-blue-cloudy-sky-139399/">Pexels</a></i></span>

There are two key requirements for the wisdom of the crowds to work. The first is that **individuals must _vary in their information_.** If everyone has the same information, the group's decision isn't going to be any more accurate than an individual's. This can even lead to _less_ accurate decisions in general as group members become overly confident in their [echo chamber](https://en.wikipedia.org/wiki/Echo_chamber_(media)).<sup>[[1]](#1-the-theory)</sup>

The second requirement is that **individual estimates must be _independent_.** If those 800 farmers deliberated with their neighbors before voting, the number of unique perspectives would drop to a few hundred, maybe even only a few dozen, as people's opinions began influencing each other. The opinions of loud personalities would weigh more than those of the quiet; rare information would be discarded in favor of common knowledge.

A random forest isn't too different from the farmers at that fair. Throughout their lives, each farmer was "trained" on mapping various features of an ox $-$ the size of its horns, the height at the shoulder $-$ to a weight. At the fair, each farmer took a new datapoint and independently cast an estimate. Galton then finished the analogy by aggregating their responses into a final prediction.

### The fish
The story gets more interesting for our shiners. A random forest isn't quite the right algorithm to describe schools of fish for one major reason: the information a fish has about its environment is strongly correlated with its neighbors.

Consider the image below of a school of 150 golden shiners. The field of view of each shiner has been approximated using a ray-casting algorithm, and only the rays that actually leave the group are colored white.

<img src="{{  site.baseurl  }}/images/theory/coll_beh/school_FOV.png" loading="lazy">
<span style="font-size: 12px"><i>Image from the <a href="https://www.pnas.org/content/pnas/suppl/2015/03/24/1420068112.DCSupplemental/pnas.1420068112.sapp.pdf">supplementary info</a> for <a href="https://www.pnas.org/content/pnas/early/2015/03/24/1420068112.full.pdf?with-ds=yes">Rosenthal et al. 2015</a>.</i></span>

The first thing that jumps out is that the inside of the school is a dead zone of information about the outside world $-$ these fish only see other fish. And even for the shiners that _do_ see the outside, individuals near one another are receiving essentially the same information about their surroundings.

Yet, even though individuals' information is [spatially autocorrelated](https://rspatial.org/raster/analysis/3-spauto.html), which [prevents the wisdom of the crowds from occurring](http://thekaolab.com/inc/papers/Kao_ProcB_2014.pdf), schools of shiners are able to elegantly avoid attacking predators like in the video below.

In short, individual estimates about what behavior to perform

So how can a group like this make more informed decisions when most fish can't see the outside and those that can see mostly the same thing?


One important consideration is that these are independent estimates. This makes it more like bagging, rather than boosting. Bagging: actually independent, more like wisdom of crowd. Boosting: individual models learn from failures of previous model. Bagging more accurate, boosting might actually be more like the fish in nature.



One additional parallel. We typically think of artificial neural networks as modeled off of biological neural networks. But the entire school can also be thought of as a neural network.




### Collective decision-making
How are groups smarter than individuals? The short answer is that it varies wildly by species and context $-$ the mechanisms leading to a locusts swarm finding food are different than [small human groups solving a cognitive task](https://www.einsteinmed.org/uploadedFiles/diversity/collective-intelligence-science.pdf). But there are also many surprising commonalities.

* Information cascades in bird flocks, [fish schools](https://www.pnas.org/content/pnas/112/15/4690.full.pdf), human crowds.
* https://icts.res.in/sites/default/files/Couzin_2009_Cognition.pdf



This seemingly innocent question has dozens of answers that vary by species and context $-$ a locust swarm



Individuals within groups have limited personal information and only local information about the group - positions, orientations, movement.



The short answer is that it's complicated! The slightly longer answer is that shiners have evolved mechanisms of translating noisy *social cues* into decisions more accurate than they could reach themselves.


Can think of it as fish have different experiences.

Fish schools, and animal groups in general, aren't comprised of completely independent estimators: there can be significant [spatial and temporal autocorrelation](http://thekaolab.com/inc/papers/kao2014.pdf).


### Fish
For fish species that live in large groups, staying close to others is often not a choice $-$ it's a matter of life or death. The surrounding environment is too unpredictable and too dangerous to go alone. I can try to find food by myself, or detect a predator early and hide, but it's easier when you're in a group. Then let's say the predator actually _does_ arrive - if you're the only one around, he can target you, but if you're in a big group, your risk is diluted by the presence of everyone around you.





### RF
**Note: the trees in a forest are uncorrelated.** That isn't the case in nature; fish close to one another in the school have highly correlated social information. But especially in fission-fusion species, they likely differ in their personal experience, their knowledge about the environment or how to interpret cues.

Hard to rule out other explanations for why fish schools are smarter than individuals: https://core.ac.uk/download/pdf/82291278.pdf


## Conclusions

## Footnotes
#### 1. [The theory](#the-theory)
If you _never_ encounter a different worldview online, or you only ever see it framed as belonging to an idiot, then you're likely in an echo chamber. A lot of this is inevitable as [social networks tend to self-segregate](https://www.pnas.org/content/118/7/e2022761118), meaning it's on you to seek out the diverse viewpoints necessary for a more objective worldview.
