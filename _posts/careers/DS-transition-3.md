---
layout: post
title: How to enter data science - <br>3. Programming
author: matt_sosna
summary: The software engineering skills needed to succeed in data science
image: ""
---

In the last post...


---
**How to enter data science:**
1. [The target]({{  site.baseurl  }}/DS-transition-1)
2. [The statistics]({{  site.baseurl  }}/DS-transition-2)
3. **The programming**
4. [The engineering]({{  site.baseurl  }}/DS-transition-4)
5. [The people]({{  site.baseurl  }}/DS-transition-5)

---


## Programming
While plenty of data science roles rely solely on R, this post will demonstrate coding concepts with Python. Python's versatility makes it an "all-in-one" language for a huge range of data science applications, from dataframe manipulations to computer vision. Python also lets you more easily dip into [the software engineering side of the analytics-engineering spectrum]({{  site.baseurl  }}/DS-transition-1#the-scalpel-versus-the-shovel).

### Dataframes
Dataframes are at the core of data science and analytics. They're essentially just a table of rows and columns, typically where each row is a _**record**_ and each column is an _**attribute**_ of that record. You can have a table of employees, for example, where each row is a person with columns for their first and last names, their home address, their salary, etc. Because dataframes will play a central role in your job, you'll need to master visualizing and manipulating the data within them. `pandas` is the key library here.

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

The next level of difficulty involves vectorized and iterative data transformations. For simple operations like adding every value in two columns together, `pandas` lets you simply add the two columns together like `df['col1'] + df['col2']`.

For more nuanced operations, such as handling missing values that would otherwise cause columnwise operations to fail, you can use `.apply`. Below, we use a lambda to apply a custom function, `safe_divide`, to the `col1` and `col2` fields of each row. (`numpy`'s `divide` function is pretty similar, but let's say we want `np.nan` instead of `Inf` when dividing by zero.)

For logic that can't be easily passed into a lambda, we just iterate through the dataframe rows using `itertuples`.

```python
# Example 2: iterating and appending data
def safe_divide(x, y):
    """
    | Divide x by y. Returns np.nan if x or y are null
    | or y is zero.
    """
    if pd.isna([x, y]).any() or y == 0:
        return np.nan
    return x / y

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

### Arrays
`pandas` dataframes are actually built on top of `numpy` arrays, so it's helpful to have some knowledge on how to efficiently use `numpy`. Many operations on `pandas.Series` (the array-like datatype for rows and columns) are identical to `numpy.array` operations, for example.

`numpy`, or [Numerical Python](https://numpy.org/), is a library with classes built specifically for efficient mathematical operations. R users will find `numpy` arrays familiar, as they share a lot of coding logic with R's vectors. Below, I'll highlight some distinctions from Python's built-in `list` class. A typical rule of thumb I follow is that it's better to use Python's built-in classes whenever possible, given that they've been highly optimized for the language. In data science, though, `numpy` arrays are generally a better choice.<sup>[[1]](#footnotes)</sup>

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

Finally, if you're dealing with data in higher dimensions, don't bother with lists of lists - just use `numpy`. I'm still scratching my head trying to figure out how exactly `[*map(np.mean, zip(*l_2d))]` works, whereas `arr_2d.mean(axis=1)` clearly indicates we're taking the mean of each column (axis 1).

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

### Visualizations
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

### Descriptive statistics
While you may be chomping at the bit to get to machine learning, I think a solid understanding of [descriptive statistics](https://conjointly.com/kb/descriptive-statistics/) should come first. In contrast to inferential statistics, descriptive statistics involves summarizing the data you have, as opposed to making inferences about a broader population.
<span style='color:red'>Work on this... </span> You'll often need to efficiently describe data to others, which is where descriptive stats comes in. Thankfully, the basics should cover you for most data science applications.

It's critical to be able to quantify what the data looks like. Is the data normally distributed, unimodal or bimodal, skewed left or right? What's a typical value, and how much do the data vary from that value? Think of descriptive stats as the "hard numbers" pair to data visualization. Being able to quickly communicate these metrics will provide an intuition for the data that helps identify outliers, such as data quality issues.

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

### Working with dates
At least with data analytics, you most likely won't escape working with dates. Dates form the backbone of [time series analysis](https://en.wikipedia.org/wiki/Time_series), which is ubiquitous in fields with continuous data streams like the [Internet of Things](https://www.wired.co.uk/article/internet-of-things-what-is-explained-iot).

The built-in `datetime` library is Python's standard, with expanded methods in the `dateutil` library. Thankfully, `pandas` has excellent functionality for working with dates when the index is set to datetime, meaning you can stay in `pandas` for most types of data analysis in Python.

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

### Machine learning
Finally, we have machine learning. Of all the things a data scientist does, machine learning receives the most hype *but is likely the smallest aspect of the job.*

Think of being a data scientist as building a machine that can drill through concrete. The drill itself is the eye-catching bit - the fancy statistics and analytics - and the tip is machine learning. The drill tip gets a lot of attention - it gets all the credit for breaking through the concrete, and there are always new and improved drill tips coming out that can break tougher concrete.

**But the majority of your time will probably be spent building out _the rest of the machinery_** - the frame, levers, screws, etc. - and identifying *where* to apply the drill. (If you're in a particularly engineering-strapped organization, you might also end up building the front end: the seat and controls for the user!) If you only care about the drill tip instead of the whole machine, you'll likely find yourself disillusioned by many data science jobs. But if you find enjoyment in the entire process of building the machine and creating something that truly helps people break that concrete, then you'll love your work.

At any rate, you *will* need some knowledge of machine learning. I wouldn't stress very much about the specifics of different machine learning algorithms (e.g. [random forests](https://en.wikipedia.org/wiki/Random_forest) vs. [support vector machines](https://en.wikipedia.org/wiki/Support_vector_machine) vs. [XGBoost](https://xgboost.readthedocs.io/en/latest/)) unless your role is deep in research, education, or machine learning consulting.<sup>[[2]](#footnotes)</sup> Rather, you'll get a lot farther if you have a good understanding of the necessary steps *before and after* you use a machine learning algorithm.

The main concepts to know, I'd argue, are:
1. Training data vs. testing data
2. Feature engineering
3. Evaluating model fit (and whether your model is overfit)
4. The difference between machine learning and statistics

#### Training data vs. testing data
When you're building a predictive model, it's critical to know how accurate it is. This is where **training data versus testing data** come in. The main idea is to subset your data into "training" data that's used to create the model, and "testing" data that's later used to evaluate model accuracy. Once your model learns the relationship between input and output, you use the testing data to see how the model's predictions compare to the true outputs.<sup>[[3]](#footnotes)</sup>

```python
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.processing import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data.csv")

# Split into predictors vs. target
X = df[['temp', 'humidity']]
y = df['is_raining']

# Split into training and testing data
X_train, y_train, X_test, y_test = train_test_split(X, y)

# Instantiate and fit random forest model
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

# Evaluate accuracy
accuracy_score(rf.predict(X_test), y_test)
```

#### Feature engineering
Our raw data alone is often not sufficient to build a strong model. Let's say, for example, that we're trying to predict the number of items sold each day in an online store. We already know that sales are higher on weekends than weekdays, so we want our model to incorporate a weekday/weekend distinction to be more accurate. A weekday/weekend distinction isn't explicitly present in our data, though - we just have the date a sale occurred. A linear model will certainly have no idea what to do with raw dates. *Maybe* a complex deep learning model can pick up a cyclic pattern in sales related to dates, but it would likely need a lot of data to figure this out.

A much simpler option is to **engineer** an `is_weekend` **feature** by asking whether each sale occurred on a Saturday or Sunday vs. the rest of the week. The `is_weekend` feature now serves as an unambiguous flag giving our model a heads up that something may be different between weekdays and weekends. Similarly, while the raw number of items in users' shopping carts is not an informative predictor, perhaps the square root or logarithm of those items actually is. (I actually have no idea. Send me a message if there's some transformation all the data scientists in e-commerce use!)

```python
df['is_weekend'] = df['date'].dt.dayofweek.isin([5, 6])
df['sqrt_n_cart_items'] = df['n_cart_items'].apply(np.sqrt)
```

Ultimately, feature engineering is a way to incorporate domain expertise into your model, giving it more useful tools for making sense of your data. Expect to spend a good amount of time trying to identify and engineer the most informative features for your models. After precise data, relevant features are *the* most important component of an accurate machine learning model - far more than the exact algorithm used or time spent tuning [hyperparameters](https://towardsdatascience.com/understanding-hyperparameters-and-its-optimisation-techniques-f0debba07568).

#### Evaluating model fit
The final machine learning theory we need to understand is evaluating how well your model describes your data... as well as whether it describes the data *too* well. The graphic below visualizes this nicely. (Source: [Educative.io](https://www.educative.io/edpresso/overfitting-and-underfitting).)

![]({{  site.baseurl  }}/images/careers/model_fit.png)

A model is a simplified representation of the real world. If the model is *too simple*, it will represent neither the training data nor the real world (underfit). If it's *too complex*, on the other hand, it will describe the data it's trained on but won't generalize to the real world (overfit).

Think of a model as the underlying "rules" converting inputs to outputs - the more you study (input), the better you score on the exam (output), for example. Our model would be how we convert *hours studied* into *exam score*. We can make the model more accurate if we start including features like *whether the student ate breakfast* and *hours of sleep*. But the more features we have, the more data we need to accurately calculate each feature's contribution to input vs. output, *especially if the features aren't perfectly uncorrelated.* In fact, [researchers have estimated](https://academic.oup.com/bioinformatics/article/21/8/1509/249540) that when we have correlated features, our model shouldn't have more than $$\sqrt{n}$$ features in our model (where *n* is the number of observations). Unless you have data on thousands of students, this drastically cuts down on the number of features your model should have.

When we pack our model with correlated features like *hours of sleep yesterday* and *hours of sleep two days ago*, we squeeze out some extra accuracy in describing our data, but we also steadily create a picture like the top right, where our model doesn't translate well to the real world. To combat this, we need to employ techniques like [feature selection](https://machinelearningmastery.com/feature-selection-with-real-and-categorical-data/), [k-fold cross validation](https://machinelearningmastery.com/k-fold-cross-validation/), [regularization](https://explained.ai/regularization/index.html), and [information criteria](https://www.sciencedirect.com/science/article/abs/pii/S0167947313002776). These techniques enable us to create the most parsimonious representation of the real world, based on only the most informative features.

#### Machine learning versus statistics
The main way to partition machine learning from statistics is whether you're trying to [explain versus predict](https://healthcare.ai/machine-learning-versus-statistics-use/). There are some fundamental concepts you'll want to make sure you have a good grasp on.

## Concluding thoughts


## Footnotes
1. [[Arrays]](#arrays) One clear exception to the rule of using `numpy` arrays over lists is if you want your array to store values of different types. `numpy.array` and `pandas.Series` have type forcing, which means that [all elements must be the same type](https://numpy.org/doc/stable/user/quickstart.html#the-basics), and they'll be forced into the same type upon creation of the array. <br><br>Below, the `numpy` version of `our_list1` converts `1` and `2` to floats to match `3.0`. (Integers are converted to floats to preserve the information after the decimal in floats.) For `our_list2`, there's no clear integer of float version of `'a'`, so instead `1` and `2.0` are converted to strings. If you want your array to store data of different types for some reason, you're therefore better off sticking with Python's `list` class.

    ```python
    import numpy as np

    # Create mixed-type lists
    our_list1 = [1, 2, 3.0]
    our_list2 = [1, 'a', 2.0]

    # Convert to single-type arrays
    np.array(our_list1)  # array([1., 2., 3.])
    np.array(our_list2)  # array(['1', 'a', '2.0'])
    ```
2. [[Machine learning]](#machine-learning) As someone who loves figuring out the nuts and bolts of how things work, I'd personally recommend digging into the distinctions between algorithms like random forests and XGBoost! I find it fascinating, and the knowledge makes it easier for me to demystify machine learning to curious consumers of model outputs. But overall, my ability to deliver business value hasn't improved much from digging into these specifics; the real benefit is the personal satisfaction of understanding the nuances.

3. [[Training data vs. testing data]](#machine-learning) Note that this is for supervised learning problems, where there is a "correct" output for each input. Evaluating model accuracy is [more complicated for unsupervised learning problems](https://www.researchgate.net/post/Which_are_the_methods_to_validate_an_unsupervised_machine_learning_algorithm).  
