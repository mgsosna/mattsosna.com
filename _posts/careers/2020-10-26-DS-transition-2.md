---
layout: post
title: How to enter data science II - the skill set
author: matt_sosna
summary: The skills needed to succeed in data science
image: ""
---
In [the last post]({{ site.baseurl }}/DS-transition-1), we defined the key elements of data science as 1) deriving insights from data and 2) communicating those insights to others. Despite the huge diversity in how these elements are expressed in actual data scientist roles, there is a core skill set that will serve you well no matter where you go. This post will outline the _**technical**_, _**business**_, and _**personal**_ skills needed to be successful as a data scientist.

## Table of contents
* [**Technical skills:** knowing _**how**_ to do it](#technical-skills-knowing-how-to-do-it)
  - [Programming](#programming)
  - Architecture
* [**Business skills:** knowing _**what**_ to do and _**why**_](#business-skills-knowing-what-to-do-and-why)
* [**Personal skills:** knowing how to _**consistently deliver**_](#personal-skills-knowing-how-to-consistently-deliver)


## Technical skills: knowing *how* to do it
Data science is a broad field that is still iterating towards a solid distinction from data analytics, data engineering, and software engineering, so it's hard to create a definitive skill set that's applicable for all data scientist roles. Someone working all day with building statistical models out of spreadsheets, for example, is going to need a different set of skills than someone improving autonomous vehicles! But consider this learning checklist as a set of fundamental skills that will get you started for your role, no matter where you go. In the rest of this section, we'll cover a bit of each topic and provide code examples.

### Programming
* **Python**
- [ ] Dataframes and arrays: `pandas`, `numpy`
- [ ] Visualization: `matplotlib`, `seaborn`
- [ ] Descriptive statistics: `numpy`, `scipy`
- [ ] Working with dates: `datetime`, `dateutil`
- [ ] Machine learning: `scikit-learn`, `keras`
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
Dataframes are at the core of data analytics and a huge range of data science applications. They're essentially just a table of rows and columns, typically where each row is a _**record**_ and each column is an _**attribute**_ of that record. You can have a table of employees, for example, where each row is a person with columns for their first and last names, their home address, their salary, etc. Because dataframes will play a central role in your job, you'll need to master visualizing and manipulating the data within them. `pandas` is the key library here.

The basics include being able to load, clean, and write out [CSV files](https://en.wikipedia.org/wiki/Comma-separated_values). Cleaning data can involve removing rows with missing values or duplicated information, correcting erroneous values, and reformatting columns into different data types.

```python
# Example 1: loading, cleaning, and writing out CSVs
import os
import pandas as pd

# Load the data
os.chdir("~/client/")
df = pd.read_csv("data.csv")

# Fix issues with 'state' column
df['state'].replace({'ill': 'IL', 'nan': None}, inplace=True)
df_filt = df[df['state'].notna()]

# Remove duplicates and reformat columns
df_filt.drop_duplicates(['customer_id', 'store_id'], inplace=True)
df_filt = df_filt.astype({'price': float, 'age': int})

# Save data
df_filt.to_csv("cleaned.csv", index=False)
```

The next level of difficulty involves vectorized and iterative data transformations. For simple operations like adding every value in two columns together, `pandas` lets you simply add the two columns together like `df['col1'] + df['col2']`. For more nuanced operations, such as handling missing values that would otherwise cause columnwise operations to fail, you can use `.apply`. Below, we use a lambda to apply a custom function, `safe_divide`, to the `col1` and `col2` fields of each row. For logic that can't be easily passed into a lambda, we just iterate through the dataframe rows using `itertuples`.

```python
# Example 2: iterating and appending data

# Vectorized transformations
df['added'] = df['col1'] + df['col2']
df['divided'] = df.apply(lambda x: safe_divide(x['col1'], x['col2']),
                         axis=1)

# Iterated transformations
df_final = pd.DataFrame()
for tup in df.itertuples():

    # Logic that can't easily be passed into a lambda
    if tup.Index % 2 == 0 and tup.is_outdated:
        df_iter = some_function(tup.age, tup.start_date)
    else:
        df_iter = some_other_fuction(tup.age, tup.pet_name)

    df_final = df_final.append(df_iter, ignore_index=True)
```

Finally, we need the ability to combine data from multiple dataframes, as well as run aggregate commands on the data. In the code below, for example, we merge two dataframes, making sure not to drop any rows in `df1` by specifying that it's a left merge. Then we create a new dataframe, `df_agg`, that has the sums of all the columns for each user. We can then print out how much user `123` spent at Target, for example.

```python
# Example 3: merging, groupbys
df_merged = pd.merge(df1, df2, on='user_id', how='left')
df_agg = df_merged.groupby('user_id').sum()
print(df_agg.loc[123, 'target'])
```

#### Arrays
`pandas` dataframes are actually built on top of `numpy` arrays, so it's helpful to have some knowledge on how to efficiently use `numpy`. `numpy`, or [Numerical Python](https://numpy.org/), is a library with classes built specifically for efficient mathematical operations. R users will find `numpy` arrays familiar, as they share a lot of coding logic with R's vectors. Below, I'll highlight some distinctions from Python's built-in `list` class.

First, we have simple filtering of a vector. Python's built-in `list` requires either a list comprehension, or the `filter` function plus a lambda and unpacking (`[*...]`). `numpy`, meanwhile, just requires the array itself.

```python
# Example 1: filtering
import numpy as np

# Create the data
list1 = [1, 2, 3, 4, 5]
array1 = np.array([1, 2, 3, 4, 5])

# Filter for elements > 3
## The list way
[val for val in list1 if val > 3]  # [4, 5]
[*filter(lambda x: x > 3, list1)]  # [4, 5]

## The numpy way
array1[array1 > 3]   # array([4, 5])
```

A second major distinction is mathematical operations. The `+` operator causes lists to concatenate. `numpy` arrays, meanwhile, interpret `+` as elementwise addition.

```python
# Create the data
list1 = [1, 2, 3]
list2 = [4, 5, 6]
array1 = np.array([1, 2, 3])
array2 = np.array([4, 5, 6])

# Addition
## Lists: concatenation
list1 + list2   # [1, 2, 3, 4, 5, 6]

## Arrays: elementwise addition
array1 + array2 # array([5, 7, 9])
```

To do elementwise math on Python lists, you need to use something like a list comprehension with `zip` on the two lists. For `numpy`, it's just the normal math operators. You can still get away with manually calculating simple aggregations like the mean on lists, but we're nearly at the point where you should just use `numpy`.

```python
# Elementwise multiplication
## Lists: list comprehension
[x * y for x, y in zip(list1, list2)]  # [4, 10, 18]

## Arrays: just the * operator
array1 * array2  # array([4, 10, 18])

# Get the mean of an array
sum(list1)/len(list1)  # 2.0
array1.mean()          # 2.0
```

Finally, if you're dealing with data in higher dimensions, don't bother with lists of lists - just use `numpy`.

```python
# List of lists vs. matrix
list_2d = [[1, 2, 3],
           [4, 5, 6]]
arr_2d = np.array(list_2d)

# Get mean of each row
[np.mean(row) for row in list_2d]  # [2.0, 5.0]
arr_2d.mean(axis=1)                # array([2.0, 5.0])

# Get mean of each column
[*map(np.mean, zip(*l_2d))]   # [2.5, 3.5, 4.5]
arr_2d.mean(axis=0)           # array([2.5, 3.5, 4.5])
```

#### Visualizations
After dataframes and arrays, the next most crucial data science skill is data visualization. **Visualizing the data is one of the first and last steps of an analysis:** when Python is communicating the data to you, and when you're communicating the data to stakeholders. The main Python data visualization libraries are `matplotlib` and `seaborn`. I'll show some simple `matplotlib` examples below.

```python
import matplotlib.pyplot as plt

# Create a 2-panel plot
plt.subplot(1,2,1)
plt.plot(df['date'], df['age'])
plt.title('My age over time', fontweight='bold')

plt.subplot(1,2,2)
plt.hist(df['age'], color='blue')
plt.title('Distribution of my ages', fontweight='bold')

plt.show()

# Iteratively add data to a plot
for group in df['treatment'].unique():
    df_group = df[df['treatment'] == group]
    plt.scatter(df_group['age'], df['tumor_size'], label=group)
plt.show()
```

If you want to get fancy, look into interactive dashboarding tools like [Bokeh](https://bokeh.org/) or [Plotly](https://plotly.com/). These tools let the user interact with the plot, such as getting more information about a point by hovering over it, or regenerating data in the plot by clicking on drop-down menus or dragging sliders.

#### Descriptive statistics
While you may be chomping at the bit to get to machine learning, I think a solid understanding of descriptive statistics should come first. You'll often need to efficiently describe data to others, which is where descriptive stats comes in. Thankfully, the basics should cover you for most data science applications.

It's critical to be able to quantify what the data looks like. Is the data normally distributed, unimodal or bimodal, skewed left or right? What's a typical value, and how much do the data vary from that value? Think of descriptive stats as the "hard numbers" pair to data visualization. Being able to quickly communicate these data metrics will provide an intuition for the data that helps identify outliers, such as data quality issues.

```python
import numpy as np
from scipy.stats import sem, normaltest

# Generate random data
data = np.random.normal(50, 3, 1000)

# Summarize mean and standard error
print(data.mean())  # 50.053
print(sem(data))    # 0.094

# Is the data normally distributed?
print(normaltest(data))  
# NormaltestResult(statistic=3.98, pvalue=0.137) -> Yes
```

#### Working with dates
At least with data analytics, you most likely can't escape working with dates. The built-in `datetime` library is the standard, with expanded methods in the `dateutil` library. Thankfully, `pandas` has excellent functionality for working with dates when the index is set to datetime.

```python
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta

# Play with dates
today = dt.date.today()
yesterday = today - dt.timedelta(days=1)
last_year = today - relativedelta(years=1)

# Generate sample data with datetime index
df = pd.DataFrame({'data': [100]*60]},
                  index=pd.date_range('2020-01-01', '2020-02-29'))

# Sum the data for each month
df_new = df.resample('MS').sum()
```

#### Machine learning
Finally, we have machine learning. Of all the things a data scientist does, machine learning receives the most hype *but is likely the smallest aspect of the job.*

Think of being a data scientist as building a machine that can drill through concrete. The tip of the drill is machine learning - it lets you accomplish your task of breaking through that concrete, and there are always new and improved drill tips coming out that can break tougher concrete.

**But the majority of your time will probably be spent building out _the rest of the machinery_** - the frame, levers, screws, etc. - and identifying *where* to apply the drill. (If you're in a particularly engineering-strapped organization, you might also end up building the front end: the seat and controls for the user!) If you only care about the drill tip instead of the whole machine, you'll likely find yourself disillusioned by many data science jobs. But if you find enjoyment in the whole process of building the machine, and creating something that truly helps people break that concrete, then you'll love your work.

At any rate, you *will* need some knowledge of machine learning. I wouldn't stress very much about the specifics of different machine learning algorithms (e.g. random forests vs. support vector machines vs. XGBoost) unless your role is deep in research, education, or specialized consulting. Rather, you'll get a lot farther if you have a good understanding of the necessary steps *before and after* you use a machine learning algorithm.

The main concepts to know, I'd argue, are:
1. Training data vs. testing data
2. Feature engineering
3. Evaluating model fit (and whether your model is overfit).

When you're building a predictive model, it's critical to know how accurate it is. This is where **training data versus testing data** come in. The main idea is to subset your data into "training" data that's fed into the model, and "testing" data that's used to evaluate model accuracy. Once your model learns the relationship between input and output, you give it the testing data and see how its predictions compare to the true outputs.

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
