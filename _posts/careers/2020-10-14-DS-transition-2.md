---
layout: post
title: How to enter data science II - the skill set
author: matt_sosna
summary: The skills needed to succeed in data science
image: ""
---
In [the last post]({{ site.baseurl }}/DS-transition-1), we defined data science as being about 1) deriving insights from data and 2) communicating those insights to others. Despite the huge diversity in how these key features are expressed in actual data scientist roles, there is a core skill set that will serve you well no matter where you go. This post will outline the _**technical**_, _**business**_, and _**personal**_ skills needed to be successful as a data scientist.

## Table of contents
* [**Technical skills:** knowing _**how**_ to do it](#technical-skills-knowing-how-to-do-it)
* [**Business skills:** knowing _**what**_ to do and _**why**_](#business-skills-knowing-what-to-do-and-why)
* [**Personal skills:** knowing how to _**consistently deliver**_](#personal-skills-knowing-how-to-consistently-deliver)


## Technical skills: knowing *how* to do it
Data science is a broad field that is still iterating towards a solid distinction from data analytics, data engineering, and software engineering, so it's hard to create a definitive skill set that's applicable for all data scientist roles. Someone working all day with building statistical models out of spreadsheets, for example, is going to need a different set of skills than someone improving autonomous vehicles! But consider this learning checklist as a set of fundamental skills that will get you started for your role, no matter where you go. In the rest of this section, we'll cover a bit of each topic and provide code examples.

### Your learning checklist
* **Python**
- [ ] Dataframes and arrays: `pandas`, `numpy`
- [ ] Visualization: `matplotlib`, `seaborn`
- [ ] Descriptive statistics: `numpy`
- [ ] Machine learning: `scikit-learn`, `keras`
- [ ] Working with dates: `datetime`
- [ ] Interacting with cloud storage: `boto3`
- [ ] Interacting with APIs: `requests`, `flask`
- [ ] Object-oriented programming (i.e. classes, module imports) <br><br>
* **Software engineering**
- [ ] Version control: [Git](https://git-scm.com/)
- [ ] Writing tests, e.g. `pytest`
- [ ] SQL for querying databases (e.g. PostgreSQL)
- [ ] Servers and deployment <br><br>
* **Statistics**
- [ ] Linear regression
- [ ] Logistic regression <br><br>
{: style='list-style-type: none'}

### Python
#### Dataframes
Dataframes are at the core of data analytics and a huge range of data science applications. At their core, they're a table of rows and columns, where each row is a "record" and each column is an attribute of that record. You can have a table of employees, for example, where each row is a person and there are columns for their first and last names, their home address, their salary, etc. Because dataframes will play a huge role in your job, you'll need to master visualizing and manipulating the data within them. `pandas` is the key library here.

The basics include being able to load, clean, and write out CSVs.

```python
# Example 1: loading, cleaning, and writing out CSVs
import os
import pandas as pd

# Load the data
os.chdir("~/client/")
df = pd.read_csv("data.csv")

# Remove rows with missing states, duplicates
df_filt = df[df['state'].notna()]
df_filt.drop_duplicates(['customer_id', 'store_id'], inplace=True)

# Reformat columns and save data
df_filt = df_filt.astype({'price': float, 'age': int})
df_filt.to_csv("cleaned.csv", index=False)
```

The next level of difficulty involves iteration and appending data.
```python
# Example 2: iterating and appending data
df_final = pd.DataFrame()
for tup in df.itertuples():
    df_iter = some_function(tup.age, tup.start_date)
    df_final = df_final.append(df_iter, ignore_index=True)
```

Finally, we have merging and groupbys. These are some skills that overlap with SQL.
```python
# Example 3: merging, groupbys
df_merged = pd.merge(df1, df2, on=['account_id', 'service_id'],
                     how='left')
df_agg = df_merged.groupby('id').sum()
print(df_agg.loc[123, 'illinois'])
```

#### Visualizations
After dataframes, the next most crucial data science skill is data visualization. Visualizing the data is one of the first steps in an analysis, as well as some of the final steps, when results are being communicated to stakeholders.

```python
import datetime as dt
import matplotlib.pyplot as plt

plt.scatter(df['date'], df['age'])
plt.xlim([dt.date(2020, 1, 1), dt.date(2020, 5, 1)])
plt.ylim([df['a'].min(), df['a'].max()])
plt.show()
```

If you want to get fancy, you can look into interactive dashboarding tools like [Bokeh](https://bokeh.org/) or [Plotly](https://plotly.com/).

#### Working with dates
At least with data analytics, you most likely won't be able to escape working with dates. `pandas` has great functionality for working with dates when you set the dataframe index to datetime.

```python
import pandas as pd
import datetime as dt

today = dt.date.today()
yesterday = today - dt.timedelta(days=1)

df = pd.DataFrame({'data': [100]*60]},
                  index=pd.date_range('2020-01-01', '2020-02-29'))

df_new = df.resample('MS').sum()
```

#### Machine learning
Finally, we have machine learning. While ML has the most hype of data science, you won't use it nearly as much as you think you will, unless you're in a really specialized role. Maybe in a really established company, or as a data science consultant.

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

#### Interacting with cloud storage

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

#### Interacting with APIs
An API, or Application Programming Interface, is like the entrance to a hotel. If you want to enter, you need to follow a certain set of rules - maybe you need the right security credentials. <span style='color:red'>Think about this analogy a bit more. Bank = better? </span>

```python
import requests

url = ""  # some free data from Google or something

json = requests.get(url)

```


#### Object-oriented programming
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

### Random, hm...
* Skills: https://medium.com/opex-analytics/top-seven-hard-skills-for-aspiring-data-scientists-7dcc1842024
* Don't skip the stats: https://www.kdnuggets.com/2017/11/10-statistical-techniques-data-scientists-need-master.html






## Business skills: knowing *what* to do and *why*
A word to the wise, though... programming skills are often easier to pick up than domain knowledge. There are dozens of resources out there for learning coding. Not so many for getting hands-on experience with Building Automation Systems, or legal documentation, or whatever. Think about what you would need a professional to teach you vs. what you can learn on your own.

Now let's say you've identified where on the analytics-engineering spectrum you fall and what level of computational complexity you're comfortable with. (Maybe better: identify what field or big-picture challenge you want to work on, and then see what the people in that field need.)

* **Business**
- [ ] Strong ability to explain technical concepts
- [ ] Focus on how to best deliver business value <br><br>


### Explainability
Should this fall under personal skills? I guess it's a business skill.

### Company focus

## Personal skills: knowing how to *consistently deliver*
For it to be impactful, it needs to be relevant. There's a philosophy/lifestyle for successful people in tech: you need to constantly be learning. There's a sort of humility in knowing that the in-demand tools of the day will keep changing. It's like resting on a slowly-moving treadmill... stop moving and you'll gradually slip away.


* You need to love programming. For most of your day, for most of your days, you're going to be reading and writing code.
* You need to love learning. There is a staggering amount to programming languages and frameworks out there. There's also a huge number of ways to get a job done, ranging from barely getting the job done to being computationally optimized and able to handle any attempt at forcing an error. Like the Red Queen in *Alice and Wonderland*, you can't stay still - you need to always be learning. (Or you'll eventually end up only able to write code in increasingly esoteric situations, like Maryland's recent call for COBOL programmers...)



* Need to constantly be learning and improving
* New technologies and frameworks will come, and you'll need to learn them to stay relevant.
