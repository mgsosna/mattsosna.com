---
layout: post
title: How to enter data science II - the skillset
author: matt_sosna
summary: The skills needed to succeed in data science
image: ""
---

This is the second post in a series.
1. [Identify the target]({{ site.baseurl }}/DS-transition-i)
2. Build up the skillset

## A shift in perspective
Regardless of where you're aiming on the data science spectrum
So let's say you've made it through the last section and you're still excited to throw yourself into the industry. The next thing to consider is the **mentality** you'll need. **There's a shift in how you view yourself as a coder** that's required for you to succeed in industry:

> **What you might be thinking:** <br>"I can code anything I want." <br><br>
> **What industry wants:** <br>"I can code anything someone asks me."

Especially in open-ended Ph.D. programs in the U.S., you have the flexibility to choose the research questions you pursue, as well as how you go about answering those questions. This makes it easy to gravitate towards questions and methods you're comfortable with and get _really good_ at a narrow set of skills. In a way, that's what a Ph.D. is all about: you choose a very precise question to answer, and you work until you know more about this sliver of knowledge than anyone else in the world.

You don't have the luxury of a narrow skill set when you're a data scientist, *especially* if you're at a smaller company. There's a term called ["full-stack"](https://www.w3schools.com/whatis/whatis_fullstack.asp) in software engineering - it refers to programmers who can code professionally in both the front-end and back-end environments, which require entirely different languages, perspectives, and skill sets. Data science is like being a full-stack engineer: you need to be comfortable rotating between different skill sets. It's a generalist position between data analyst and data engineer.


* You need to love programming. For most of your day, for most of your days, you're going to be reading and writing code.
* You need to love learning. There is a staggering amount to programming languages and frameworks out there. There's also a huge number of ways to get a job done, ranging from barely getting the job done to being computationally optimized and able to handle any attempt at forcing an error. Like the Red Queen in *Alice and Wonderland*, you can't stay still - you need to always be learning. (Or you'll eventually end up only able to write code in increasingly esoteric situations, like Maryland's recent call for COBOL programmers...)




On the other end, you have entirely self-sufficient full-stack developers. They're good at moving data around. But what do you do with that data? To derive meaningful insights from the data, you need to dip into the stats / machine learning bucket. Something like "the average time spent on our website is 1.5 minutes" is easy to calculate. Something like "we can predict where a user will click next based on their activity" is a much harder question.




* Need to constantly be learning and improving
* New technologies and frameworks will come, and you'll need to learn them to stay relevant.

I found it so easy to stay in the areas of R and statistics that I already knew well. I didn't want to get out of my comfort zone, because it would require me to face the scary concept that I _don't_ actually have that wide a grasp on stats and coding.



<span style='color:red'> Think about mentioning boot camps, like the [Insight Fellowship](https://insightfellows.com/data-science) </span>


There's also huge variation in what "data science" means. On one end, it's close to analytics. You're not dealing with a huge amount of data. Basically a data analyst with solid programming skills, so they can interact with cloud storage, write pipelines, etc. On the other end, you can be doing deep learning with computer vision to make self-driving cars safer.

**How many other programming languages interact with your output?**




This learning checklist is what I consider the basics. Data science is a broad field that is still iterating towards a solid distinction from data analytics, data engineering, and software engineering.






### Your learning checklist
* **Python**
- [ ] Dataframes and arrays: `pandas`, `numpy`
- [ ] Visualization: `matplotlib`, `seaborn`
- [ ] Machine learning: `scikit-learn`, `keras`
- [ ] Working with dates: `datetime`
- [ ] Interacting with cloud storage: `boto3`
- [ ] Interacting with APIs: `requests`
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

## Python
### Dataframes
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

### Visualizations
```python
import matplotlib.pyplot as plt

plt.scatter(df['date'], df['age'])
plt.xlim([dt.date(2020, 1, 1), dt.date(2020, 5, 1)])
plt.ylim([df['a'].min(), df['a'].max()])
plt.show()
```

### Machine learning
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

### Working with dates
```python
import pandas as pd
import datetime as dt

today = dt.date.today()
yesterday = today - dt.timedelta(days=1)

df = pd.DataFrame({'data': [100]*60]},
                  index=pd.date_range('2020-01-01', '2020-02-29'))

df_new = df.resample('M').sum()
```

### Interacting with cloud storage
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

### Interacting with APIs
An API, or Application Programming Interface, is like the entrance to a hotel. If you want to enter, you need to follow a certain set of rules - maybe you need the right security credentials. <span style='color:red'>Think about this analogy a bit more. Bank = better? </span>

```python
import requests

url = ""  # some free data from Google or something

json = requests.get(url)

```


### Object-oriented programming
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

## Software engineering
### Version control
Version control is crucial. I wish this was a bigger part of my workflow during the Ph.D. It's essential when you're a member of a team. The main idea is that there is some "master" version of code, and you only ever modify _copies_ (branches) of the code. Changes to the master branch are only allowed after

```bash
git checkout -b DS-123-Add-outlier-check
git push --set-upstream origin DS-123-Add-outlier-check

git add preprocessor.py
git commit -m "Add outlier check"
git push
```
### Writing tests


### SQL
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

## Statistics

### Linear regression
You should be able to explain the following equation again and again:

$$ h(x) = \sum_{j=1}^{n}\beta_jx_j $$

**Linear regression** is one of the most common statistical model you'll encounter in industry, and you need to understand its ins and outs. Make sure you have a solid understanding of what **residuals** are, **least squared error**, and $$R^2$$.

### Logistic regression
The below equation for logistic regression might not come up as frequently, but you should understand it and be able to explain it, as well.

$$ P(y) = \frac{1}{1+e^{-h(x)}} $$

For least squares:
$$ y = \sum_{i=1}^{m}(h(x_i)-y_i)^2 $$

## Business
### Explainability

### Company focus
