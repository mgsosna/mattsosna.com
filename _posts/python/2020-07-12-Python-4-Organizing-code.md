---
layout: post
title: Learning Python - 4. Organizing your code
author: matt_sosna
---

In any programming language, as the amount of code grows, you need to start organizing it all. The typical levels of organization are as follows:

**1. No organization** <br>
Just individual scripts that exist in a vacuum, performing simple commands in sequence. You're either not using any custom functions, or you're defining those functions in the script itself.

```python
import pandas as pd
df = pd.read_csv('weather.csv')
df = df.drop_na(axis=1)
df_pivot = df.pivot_table(index=['month', 'state'], values='rainfall',
                          aggfunc=sum)
df.to_csv('weather_pivot.csv', index=False)
```

**2. Functions** <br>
Place code you're using multiple times into functions, then just call the functions.<br>
```python
from our_functions import clean_data, fit_model

df_clean = clean_data(df, drop_duplicates=False)
mod = fit_model(df_clean, n_iter=3)
```

**3. Classes** <br>
Group similar functions into classes. Import classes as a whole into different files, e.g. a "temperature converter" class with methods for Fahrenheit -> Celsius, Celsius -> Fahrenheit, Celsius -> Kelvin, etc.<br>
```python
from our_classes import DataCleaner, LMFitter

dc = DataCleaner()
lmf = LMFitter()

df_clean = dc.prep_for_model(df)
mod = lmf.fit(df_clean)
```

**4. Modules** <br>
Group similar classes into modules that can be imported as a whole. <br>
```python
# pipeline.py
from data_cleaners import ModelPrepper
from model_fitters import LMBuilder
from models import LinearMod

class Pipeline:

    def __init__(self):
        self.mp = ModelPrepper()
        self.lmb = LMBuilder()

    def run(self, df: pd.DataFrame):
        """
        | Runs the data cleaning and outputs model
        """
        df_clean = self.mp.clean_df_for_model(df)
        mod = self.lmb.fit(df_clean)

```
Then in another file:
```python
# main.py
from pipeline import Pipeline
p = Pipeline()

p.run(df)
```
