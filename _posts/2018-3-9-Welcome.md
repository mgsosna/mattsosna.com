---
layout: post
title: Welcome to Matt Sosna's site!
---

## Welcome
We're just going to test out some ideas. Woo hoo!

![_config.yml](mgsosna.github.io/images/config.png)

A code snippit just for fun:

```python
import pandas as pd
import numpy as np

# Set seed
np.random.seed(1)

# Create dataframe
df = pd.DataFrame({'salary': np.round(np.random.uniform(10000, 100000, 100), 2),
                   'food_perc': np.round(np.random.uniform(0.1, 0.9, 100), 2)})

```

The easiest way to make your first post is to edit this one. Go into /_posts/ and update the Hello World markdown file. For more instructions head over to the [Jekyll Now repository](https://github.com/barryclark/jekyll-now) on GitHub.
