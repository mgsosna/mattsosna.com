---
layout: post
title: Fish schools as ensemble learning algorithms
author: matt_sosna
tags: academia machine-learning
---
<img src="{{  site.baseurl  }}/images/theory/coll_beh/koi_shoal.jpg" alt="Fish school">
<span style="font-size: 12px"><i>Photo by <a href="https://unsplash.com/@jwimmerli">jean wimmerlin</a> on <a href="https://unsplash.com">Unsplash</a></i></span>

**Animal groups are greater than the sum of their parts.** The individual termite wanders cluelessly while the colony builds a sturdy and [well-ventilated mound](http://www.bbc.com/earth/story/20151210-why-termites-build-such-enormous-skyscrapers). The lone stork loses its way while [the flock successfully migrates](https://flightforsurvival.org/white-stork/). Across the spectrum of cognitive complexity, we regularly see the emergence of behaviors at the group level that the members alone aren't capable of. How is this possible?

I spent my Ph.D. puzzling over how golden shiner fish $-$ a generally hopeless and not very intelligent creature $-$ form schools capable of elegantly evading predators. I read dozens of articles and textbooks, conducted experiments, analyzed data, and worked with theorists to try to make sense of how when it comes to fish, $1 + 1 = 3$, not $2$.

All the knowledge I gained seemed destined to become a pile of dusty facts in some corner of my brain when I [left academia to enter data science]({{  site.baseurl  }}/Academia-to-DS). But as I started my data science education, I was surprised to see a curious parallel between _**decision-making in the fish I'd studied**_, and _**decision-making in [ensemble learning](http://www.scholarpedia.org/article/Ensemble_learning) algorithms**_.

This post will show you how ensembles of weak learners $-$ whether they're fish or decision trees $-$ can together form an accurate information processor.

### The machine
Let's first cover the machine learning side, since you're probably more familiar with algorithms than animals! **Ensemble learning methods use a _set_ of models to generate a prediction,** rather than one single model. The idea is that the errors in the models' predictions cancel out, leading to more accurate predictions overall.

In the schematic below, our ensemble is the set of gray boxes, each of which is a model. To generate a predicted value for the input, the input is sent into each model, which generates a prediction. These individual predictions are then reduced to one _aggregate_ prediction by either averaging (for regression) or taking the majority vote (for classification).

<img src="{{ site.baseurl }}/images/theory/coll_beh/ensemble.png">

One popular ensemble method is a [**random forest**](https://en.wikipedia.org/wiki/Random_forest), a model that consists of dozens or hundreds of [decision trees](https://en.wikipedia.org/wiki/Decision_tree). While there are [plenty of ways](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) to configure how the forest is assembled, the general process is that each tree is independently trained on [bootstrapped](https://machinelearningmastery.com/a-gentle-introduction-to-the-bootstrap-method/) observations and random subsets of the features. (If we used the same data for each tree, we'd create the same tree each time!)

The result is a collection of models, **each with a _slightly different understanding_ of the training data.** This variation is crucial. Individual decision trees easily become [overfit](https://www.investopedia.com/terms/o/overfitting.asp) to their training data, obsessing over patterns in their sample that aren't necessarily present in the broader world. But because the ensemble consists of many trees, these errors tend to cancel one another out when the aggregate prediction is calculated.

### The theory
The enhanced accuracy of a random forest can be summarized as the [wisdom of the crowds](https://en.wikipedia.org/wiki/Wisdom_of_the_crowd). The concept dates back to 1906 at a livestock fair in Plymouth, MA, which held a competition to guess the weight of an ox. Nearly 800 farmers gave their best estimates. Statistician [Sir Francis Galton](https://en.wikipedia.org/wiki/Francis_Galton) later examined the guesses and observed that while individual estimates varied widely, the _mean_ of the estimates was more accurate than any individual guess. Galton went on to formalize his theory in his famous [_Vox Populi_ paper](https://www.all-about-psychology.com/the-wisdom-of-crowds.html).

<img src="{{  site.baseurl  }}/images/theory/coll_beh/ox.jpg">
<span style="font-size: 12px"><i>Photo by <a href="https://www.pexels.com/@pixabay">Pixabay</a> from <a href="https://www.pexels.com/photo/brown-bull-on-green-glass-field-under-grey-and-blue-cloudy-sky-139399/">Pexels</a></i></span>

There are two key requirements for the wisdom of the crowds to work. The first is that **individuals must _vary in their information_.** If everyone has the same information, the group's decision isn't going to be any more accurate than an individual's. This can even lead to _less_ accurate decisions in general as group members become overly confident in their [echo chamber](https://en.wikipedia.org/wiki/Echo_chamber_(media)).<sup>[[1]](#1-the-theory)</sup>

The second requirement is that **individual estimates must be _independent_.** If those 800 farmers deliberated with their neighbors before voting, the number of unique perspectives would collapse to a few hundred, maybe even only a few dozen, as people's opinions began influencing each other. The opinions of loud personalities would weigh more than those of the quiet; rare information would be discarded in favor of common knowledge.

In a way, those farmers are like a random forest that took decades to train. Throughout their lives, each farmer learned how to map various features of an ox $-$ the size of its horns, the height at the shoulder $-$ to a weight. At the fair, each farmer took a new datapoint and independently cast an estimate. Galton then finished the analogy by aggregating their responses into a final prediction.

### The fish
While the wisdom of the crowds can explain the cattle fair, the story gets more nuanced for our shiners. A random forest isn't quite the right algorithm to describe schools of fish for one major reason: the information a fish has about its environment is strongly correlated with its neighbors.

Consider the image below of a school of 150 golden shiners. The field of view of each shiner has been approximated using a ray-casting algorithm, and only the rays that actually leave the group are colored white.

<img src="{{  site.baseurl  }}/images/theory/coll_beh/school_FOV.png">
<span style="font-size: 12px"><i>Image from the <a href="https://www.pnas.org/content/pnas/suppl/2015/03/24/1420068112.DCSupplemental/pnas.1420068112.sapp.pdf">supplementary info</a> for <a href="https://www.pnas.org/content/pnas/early/2015/03/24/1420068112.full.pdf?with-ds=yes">Rosenthal et al. 2015</a>.</i></span>

The first thing that jumps out is that the inside of the school is a dead zone of information about the outside world $-$ these fish only see _other fish_. The second thing to notice is that even for shiners that _do_ see the outside, individuals near one another are receiving essentially identical information about their surroundings.

How can a group like this possibly make informed decisions about whether to turn left or right, or explore for food or hide from a predator, when there's only a tiny handful of independent datapoints about the outside world? (And then _coordinate_ those dozens of group members without a leader!) Yet somehow shiner schools [efficiently find shelter](https://kops.uni-konstanz.de/bitstream/handle/123456789/36982/Berdahl_0-387565.pdf?sequence=1) and [modulate responsiveness to risk](https://www.pnas.org/content/pnas/116/41/20556.full.pdf), even though individuals' information is [spatially autocorrelated](https://rspatial.org/raster/analysis/3-spauto.html), which [prevents the wisdom of the crowds](http://thekaolab.com/inc/papers/Kao_ProcB_2014.pdf).

Unfortunately, [there aren't easy answers to these questions](https://core.ac.uk/download/pdf/82291278.pdf)! The field of collective behavior is hard at work trying to understand how simple local interactions give rise to complex group-level behaviors. But there are two classes of machine learning algorithms that I think can explain some aspects of how fish schools do what they do.

**The first is [_boosting_ ensemble learning](https://quantdare.com/what-is-the-difference-between-bagging-and-boosting/).** A random forest uses bagging, which involves training each model independently in parallel. Methods like [AdaBoost](https://blog.paperspace.com/adaboost-optimizer/) and [XGBoost](https://machinelearningmastery.com/gentle-introduction-xgboost-applied-machine-learning/), on the other hand, train models _sequentially_, with later models learning from the errors of earlier models. Schooling fish [rapidly learn to identify predators](https://d1wqtxts1xzle7.cloudfront.net/38450274/Manassa_and_McCormick_2012b.pdf?1439341938=&response-content-disposition=inline%3B+filename%3DSocial_learning_and_acquired_recognition.pdf&Expires=1622730506&Signature=HAbYEHdliiZBK3N-aEQrqrquAcQEGr10BJutxdWqY9vX-WzY9VWGhQnucCIY9pfMSeVx75dD~u-mJEpd9mrMOv2v1miXZdTlsGTQE4ljmUeIODE3InJ9gypfgEFcmXyyi4Ilxe87SP~xr0iZLwpXzU-g1fB8F8LEfyG4c4V6aKvrEWVe-ZQXQXuSPnT9xkz2HGt7Odv431L-sVoziQ7KrGE8PxlxsljWU71mdGOxrnheXoXMED5YUEvf89n9KeFEuKSkMIVTvkkgJXtGhWQrPGxZZNex3Lknz2UvGzaUfmvUTLZOpNlPudHRY5gVRY9cplglDYiw7Kd87OIfRZ4grw__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA) from the mistakes of others, and fish that understand environmental cues usually end up [driving the direction of group movement](https://www.researchgate.net/profile/Stephan-Reebs/publication/285599716_Can_a_minority_of_informed_leaders_determine_the_foraging_movements_of_a_fish_shoal/links/5a33f2ba45851532e82c989a/Can-a-minority-of-informed-leaders-determine-the-foraging-movements-of-a-fish-shoal.pdf).

The second possibility is that **fish schools act as a massive neural network.**  (From biological neurons to artificial neural networks to fish schools... we've come full circle!) When it comes to avoiding predation, many fish species perform startle responses, a super-fast, reflexive burst of swimming away from an alarming stimulus.<sup>[[2]](#2-the-fish)</sup> These responses are contagious, often leading to _cascades_ of startles that move faster than attacking predators.

<img src="{{  site.baseurl  }}/images/theory/coll_beh/startle_cascade.png">
<span style="font-size: 12px"><i>A startle cascade. Image from <a href="https://www.pnas.org/content/pnas/early/2015/03/24/1420068112.full.pdf?with-ds=yes">Rosenthal et al. 2015</a>.</i></span>

The interesting wrinkle here is that the _outputs_ of group members (i.e. whether or not they startle) serve as the _inputs_ to neighboring fish for whether they should startle. Especially for fish deep in the group, with little personal information to verify whether a wave is a false alarm or oncoming predator, responding appropriately to these social cues can mean life or death.

We typically think of artificial neural networks as modeled off of _biological_ neural networks, but in a way, _the entire school_ acts a set of neurons when processing information about risk in its environment. But what's even more fascinating is that **these neurons can _change the structure of their network_ to change how information is processed.**

In [one of my papers](https://www.pnas.org/content/pnas/116/41/20556.full.pdf), my colleagues and I showed that shiners modulate their responsiveness to threats by changing the _spacing_ between individuals rather than the internal calculations for whether or not to respond to a neighboring startle. This means the group structure itself, rather than individuals, controls whether random startles spiral into full cascades or die out as false alarms.

<img src = "{{  site.baseurl  }}/images/theory/coll_beh/fish_network.png">
<span style="font-size: 12px"><i>A neural network of neural networks decides where to eat.</i></span>

## Conclusions
How can animal groups perform behaviors the individuals aren't capable of? This is the central question the field of collective behavior chews on all day, bringing together biology, psychology, physics, and computer science to try to answer. In this post we covered a simple example of collective intelligence, where independent estimates of an ox's weight led to a more accurate estimate overall. We then skimmed the surface of collective computation in fish schools, whose amorphous structure changes constantly as it processes information about its surroundings.

Interested in learning more? Check out how [baboons make movement decisions democratically](https://science.sciencemag.org/content/348/6241/1358/tab-pdf), [innovative behavior is retained across generations in wild birds](https://www.researchgate.net/profile/Lucy-Aplin/publication/269189563_Experimentally_induced_innovations_lead_to_persistent_culture_via_conformity_in_wild_bird/links/5735d90808ae298602e0920b/Experimentally-induced-innovations-lead-to-persistent-culture-via-conformity-in-wild-bird.pdf), or how [slime molds recreated the Tokyo subway map by optimizing resource allocation](https://math.mit.edu/~dunkel/Teach/18.S995_2014F/paper_suggestions/science_tero.pdf). And be sure to check out the [Collective Behavior department](https://collectivebehaviour.com/) at the Max Planck Institute for Animal Behavior for the latest cool collective behavior research.

Best,<br>
Matt

## Footnotes
#### 1. [The theory](#the-theory)
If you _never_ encounter a different worldview online, or you only ever see it framed as belonging to an idiot, then you're likely in an echo chamber. A lot of this is inevitable as [social networks tend to self-segregate](https://www.pnas.org/content/118/7/e2022761118), meaning it's on you to seek out the diverse viewpoints necessary for a more objective worldview.

#### 2. [The fish](#the-fish)
To get super in the weeds, there may actually be multiple neural pathways for startles, some with finer motor control. Shiners, at least, can startle with varying intensity. But when quantifying the spread of information in a group, it's a fine approximation to binarize startles into "yes, this fish startled" vs. "no, they didn't."
