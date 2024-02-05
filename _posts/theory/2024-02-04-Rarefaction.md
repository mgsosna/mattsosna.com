---
layout: post
title: Rarefaction curves as an analogy for learning
author: matt_sosna
tag: statistics careers
---

Whenever you start at a new company or team, or pick up a project in an area you know nothing about, there can be a steep learning curve.

[Rarefaction](https://en.wikipedia.org/wiki/Rarefaction_(ecology)) is a technique used in ecology to estimate the number of species in an area.

The idea is that you sample individuals from an area and record what their species is. The more individuals you sample, the more species you'll encounter.


On the learning side: when you start, everything you learn is new. But the more time you put into it, the more you start to see repeating concepts.

{% include header-python.html %}
```python
import numpy as np

# Generate population params
n_concepts = 100
concepts = range(n_concepts)

# Top 20 concepts get you 80% of the way there
probs = np.concatenate(
    [
      np.repeat(0.04, 20),
      np.repeat(0.0025, 80)
    ]
)
```

Now let's learn.

{% include header-python.html %}
```python
n_samples = 100
learn = np.random.choice(concepts, n_samples, p=probs)
```

Now let's visualize it.

{% include header-python.html %}
```python
import matplotlib.pyplot as plt

# Generate the y-axis
got_it = set()
response = []
current = 0

for x in learn:
    if x not in got_it:
        got_it.add(x)
        current += 1
    response.append(current)

plt.plot(range(1, n_samples+1), response)
plt.xlabel("N samples")
plt.ylabel("N concepts learned")
plt.show()
```
