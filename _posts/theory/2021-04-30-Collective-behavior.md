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
Let's first cover the machine learning side, since you're probably more familiar with algorithms than animals! **Ensemble learning methods use a _set_ of models to generate a prediction,** rather than one single model.

In the schematic below, our ensemble is the set of gray boxes, each of which is a model. To generate a predicted value for the input, the input is sent into each model, which generates a prediction. These individual predictions are then collapsed into one _aggregate_ prediction by either averaging (for regression) or taking the majority vote (for classification).

<img src="{{ site.baseurl }}/images/theory/coll_beh/ensemble.png">

One popular example of an ensemble method is a [**random forest**](https://en.wikipedia.org/wiki/Random_forest). A random forest consists of dozens or hundreds of [decision trees](https://en.wikipedia.org/wiki/Decision_tree). While there are [plenty of ways](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) to configure how the forest is assembled, the general process is that each tree is independently trained on [bootstrapped](https://machinelearningmastery.com/a-gentle-introduction-to-the-bootstrap-method/) replicates of the data and random subsets of the features. (If we used the same data for each tree, we'd create the same tree each time!)

The result is a collection of models, each with a _slightly different understanding_ of the training data. This variation is crucial. Individual decision trees easily become [overfit](https://www.investopedia.com/terms/o/overfitting.asp) to their training data, meaning they fail to generalize well to new data. But because the ensemble consists of many trees, these errors tend to cancel one another out, leading to a more accurate model overall.

### The beast
The strength of ensemble methods


There's one more nuance to mention: boosted vs. bagged

### Collective decision-making
How are groups smarter than individuals? The short answer is that it varies wildly by species and context $-$ the mechanisms leading to a locusts swarm finding food are different than [small human groups solving a cognitive task](https://www.einsteinmed.org/uploadedFiles/diversity/collective-intelligence-science.pdf). But there are also many surprising commonalities.

* Information cascades in bird flocks, [fish schools](https://www.pnas.org/content/pnas/112/15/4690.full.pdf), human crowds.
* https://icts.res.in/sites/default/files/Couzin_2009_Cognition.pdf



This seemingly innocent question has dozens of answers that vary by species and context $-$ a locust swarm



Individuals within groups have limited personal information and only local information about the group - positions, orientations, movement.



The short answer is that it's complicated! The slightly longer answer is that shiners have evolved mechanisms of translating noisy *social cues* into decisions more accurate than they could reach themselves.
Maybe should start with the model, which people will be more familiar with

Can think of it as fish have different experiences.

There _are_ some important differences to point out, however. Ensemble methods rely on each estimator submitting _independent_ guesses. The "many-wrongs" idea here is that the inaccuracies of the guesses average out, resulting in a more accurate guess than any individual. But this only holds if the models aren't aware of one another.

Fish schools, and animal groups in general, aren't comprised of completely independent estimators: there can be significant [spatial and temporal autocorrelation](http://thekaolab.com/inc/papers/kao2014.pdf).


### Fish
For fish species that live in large groups, staying close to others is often not a choice $-$ it's a matter of life or death. The surrounding environment is too unpredictable and too dangerous to go alone. I can try to find food by myself, or detect a predator early and hide, but it's easier when you're in a group. Then let's say the predator actually _does_ arrive - if you're the only one around, he can target you, but if you're in a big group, your risk is diluted by the presence of everyone around you.


Wisdom of the crowds
* Started by statistician [Sir Francis Galton](https://en.wikipedia.org/wiki/Francis_Galton) in 1907. Competition at a livestock fair to estimate weight of ox. Nearly 800 farmers guessed, and there was considerable variation. The mean of the guesses turned out to be more accurate than any individual guess.


### RF
**Note: the trees in a forest are uncorrelated.** That isn't the case in nature; fish close to one another in the school have highly correlated social information. But especially in fission-fusion species, they likely differ in their personal experience, their knowledge about the environment or how to interpret cues.

Spatial and temporal correlation: http://thekaolab.com/inc/papers/kao2014.pdf

Hard to rule out other explanations for why fish schools are smarter than individuals: https://core.ac.uk/download/pdf/82291278.pdf

Bagging vs. boosting. Bagging: actually independent, more like wisdom of crowd. Boosting: individual models learn from failures of previous model. Bagging more accurate, boosting might actually be more like the fish in nature.

## Conclusions
