---
layout: post
title: Transitioning to data science
author: matt_sosna
---

If you're in academia and looking to enter data science, you've likely able to distill interesting questions from large amounts of information, and you have the focus and analytical chops to find answers to those questions. These are incredibly valuable skills to have, but non-academic positions also require a fairly hefty set of skills _outside_ of the ones academics are most familiar in. This blog post will go through a checklist of those skills that will make you even more attractive as a candidate when applying to data science positions.

**But before we get started,** there's a shift in perspective that's required for you to succeed in industry:

> **What you might think:** <br>"I can code anything I want." <br><br>
> **What industry wants:** <br>"I can code anything someone asks me."

Especially in open-ended Ph.D. programs in the U.S., you have a lot of flexibility to choose the research questions you want to pursue, as well as how you go about answering those questions.


This learning checklist is what I consider the basics. Data science is a broad field that is still iterating towards a solid distinction from data analytics, data engineering, and software engineering.

## Your learning checklist
* **Python**
- [ ] Dataframes and arrays: `pandas`, `numpy`
- [ ] Visualization: `matplotlib`, `seaborn`
- [ ] Machine learning: `scikit-learn`, `keras`
- [ ] Working with dates: `datetime`
- [ ] Interacting with cloud storage: `boto3`
- [ ] Object-oriented programming (i.e. classes, module imports) <br><br>
* **Software engineering**
- [ ] Version control: [Git](https://git-scm.com/)
- [ ] Writing tests, e.g. `pytest`
- [ ] SQL for querying databases (e.g. PostgreSQL) <br><br>
* **Statistics**
- [ ] Linear regression
- [ ] Logistic regression <br><br>
* **Business**
- [ ] Strong ability to explain technical concepts
- [ ] Focus on how to best deliver business value <br><br>
{: style='list-style-type: none'}

# Python
## Dataframes
You're good if you understand this:
```python
import pandas as pd

# Example 1
df = pd.read_csv("data.csv")
df_agg = df.groupby('id').sum()
print(df_agg.loc[123, 'illinois'])

# Example 2
df_final = pd.DataFrame()
for tup in new_df.itertuples():
    df_iter = some_function(tup.age, tup.start_date)
    df_final = df_final.append(df_iter, ignore_index=True)
```

## Visualizations
```python
import matplotlib.pyplot as plt

plt.scatter(df['date'], df['age'])
plt.xlim([dt.date(2020, 1, 1), dt.date(2020, 5, 1)])
plt.ylim([df['a'].min(), df['a'].max()])
plt.show()
```

## Machine learning
```python
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.processing import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data.csv")

X = df[['temp', 'humidity']]
y = df['is_raining']

X_train, y_train, X_test, y_test = train_test_split(X, y)

rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

accuracy_score(rf.predict(X_test), y_test)
```

## Working with dates
```python
import pandas as pd
import datetime as dt

today = dt.date.today()
yesterday = today - dt.timedelta(days=1)

df = pd.DataFrame({'data': [100]*60]},
                  index=pd.date_range('2020-01-01', '2020-02-29'))

df_new = df.resample('M').sum()
```

## Interacting with cloud storage
```python
import os
import boto3

S3_BUCKET = "my_company"

client = boto3.client(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                      region_name='us-east-1')

obj = client.get_object(Bucket=S3_BUCKET, Key='datasets/data.json')

body = obj['Body'].read()
string = body.decode(encoding=encoding)
df = pd.DataFrame(json.load(StringIO(string)))
```
## Object-oriented programming
```python
import logging
import pandas as pd
from typing import Optional, List

from ..services import DataLoader

N_SD_THRESH = 5


class Preprocessor:
    """
    | Functions for preprocessing data
    """
    def __init__(self, max_tries: int = MAX_TRIES):
        self.max_tries = MAX_TRIES
        self.dl = DataLoader()

    def remove_outliers(self,
                        df: pd.DataFrame,
                        cols: Optional[List[str]] = None,
                        n_sd_thresh: int = N_SD_THRESH) -> pd.DataFrame:
        """
        | Remove outliers from cols in df. If cols not specified,
        | all columns in df are processed.
        |
        | -------------------------------------------------------
        | Parameters
        | ----------
        |  df : pd.DataFrame
        |    Df with columns ['a', 'b', 'c']
        |
        |  cols : list or None
        |    Columns to check
        |
        |  n_sd_thresh : int
        |    Number of standard deviations from mean above/below
        |    which a value is excluded
        |
        |
        | Returns
        | -------
        |  pd.DataFrame
        |    Original df with outliers removed
        """
        bad_idx = []

        cols_to_check = cols if cols is not None else list(df)

        for col in cols_to_check:
            bad_idx.append(self._find_outliers(df[col], n_sd_thresh))

        df_filt = df[~df.index.isin(bad_idx)].reset_index(drop=True)

        if df_filt.empty:
            logging.error("df has no rows without outliers")
            return df

        return df_filt
```
This code block is quite a bit longer than the others, and it doesn't even include the helper function or using `DataLoader`. For production-level coding, there's a lot more architecture you need to build _around_ your core functions to ensure that your code:
1. Can be read and modified by others, not just you
2. Is modular enough to be used in pipelines and multiple contexts
3. Doesn't grind those pipelines to a halt if it gets some unexpected input and breaks

If you're interested in a deeper dive on these concepts and a step-by-step explanation of the (truncated) code above, check out [this post]({{ site.baseurl }}/Python-5-Writing-production-level-Python).

# Software engineering
## Version control
Version control is crucial. I wish this was a bigger part of my workflow during the Ph.D. It's essential when you're a member of a team. The main idea is that there is some "master" version of code, and you only ever modify _copies_ (branches) of the code. Changes to the master branch are only allowed after

```bash
git checkout -b DS-123-Add-outlier-check
git push --set-upstream origin DS-123-Add-outlier-check

git add preprocessor.py
git commit -m "Add outlier check"
git push
```
## Writing tests


## SQL
You're almost guaranteed to be querying databases in your job. You won't need to be a pro unless you're in more of a data engineering role, but you should know it. DataCamp has some great courses.

```sql
SELECT
    u.name AS user_name,
    AVG(g.score) AS avg_score
FROM users AS u
INNER JOIN grades AS g
    ON u.id = g.user_id
WHERE AVG(g.score) > 90
GROUP BY u.id
ORDER BY u.name;
```

# Statistics

## Linear regression
You should be able to explain the following equation again and again:

$$ h(x) = \sum_{j=1}^{n}\beta_jx_j $$

**Linear regression** is one of the most common statistical model you'll encounter in industry, and you need to understand its ins and outs. Make sure you have a solid understanding of what **residuals** are, **least squared error**, and $$R^2$$.

## Logistic regression
The below equation for logistic regression might not come up as frequently, but you should understand it and be able to explain it, as well.

$$ P(y) = \frac{1}{1+e^{-h(x)}} $$

For least squares:
$$ y = \sum_{i=1}^{m}(h(x_i)-y_i)^2 $$

# Business
## Explainability

## Company focus
