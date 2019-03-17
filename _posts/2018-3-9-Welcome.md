---
layout: post
title: Welcome to Matt Sosna's site!
---

## Testing out the code blocks and syntax highlighting
Let's keep trying things... trying again.

![_config.yml](https://raw.githubusercontent.com/mgsosna/mgsosna.github.io/master/images/config.png)

A code snippit just for fun:

```python
import pandas as pd
import numpy as np

# Set seed
np.random.seed(1)

# Create dataframe
df = pd.DataFrame({'salary': np.random.uniform(10000, 100000, 100),
                   'food_perc': np.random.uniform(0.1, 0.9, 100)})

# Try some other things
for i, col in enumerate(list(df)):
    print(f"Col {i}: {col}")
```

When you look at the code above, you can see that `df` is a variable. You can access the columns with `df['salary']` and `df['food_perc']`.
