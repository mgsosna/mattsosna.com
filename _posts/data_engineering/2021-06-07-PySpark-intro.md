---
layout: post
title: A hands-on demo of analyzing big data with Spark
author: matt_sosna
---

[Cloud services firm Domo estimates](https://web-assets.domo.com/blog/wp-content/uploads/2020/08/20-data-never-sleeps-8-final-01-Resize.jpg) that for every minute in 2020, WhatsApp users sent 41.7 million messages, Netflix streamed 404,000 hours of video, $240,000 changed hands on Venmo, and 69,000 people applied for jobs on LinkedIn. In that firehose of data are patterns those companies use to gauge user sentiment, predict the future, and ultimately stay alive in a hyper-competitive market.

But how is it possible to extract insights from datasets so large they freeze your laptop when you try to load them into `pandas`? When a dataset has more rows than [dollars the median household will earn in 50 years](https://www.census.gov/library/publications/2020/demo/p60-270.html)<sup>[[1]](#1-intro)</sup>, we _could_ head to BestBuy.com, go to their computers section, and sort by "most expensive."

Or we could try [**Apache Spark**](https://spark.apache.org/).

By the end of this post, you'll understand why you don't need expensive hardware to analyze massive datasets $-$ because you'll have already done it. We'll cover what Spark is before counting the frequency of each letter in a novel, calculating $\pi$ by hand, and processing a dataframe with 50 million rows.

### Table of contents
1. [The analytics framework for big data](#the-analytics-framework-for-big-data)
2. [Counting letter frequencies in a novel](#counting-letter-frequencies-in-a-novel)
3. [Calculating $\pi$](#calculating-pi)
4. [Spark dataframes](#spark-dataframes)

### The analytics framework for big data
**Spark is a framework for processing massive amounts of data.** It works by **_partitioning_** your data into subsets, **_distributing_** the subsets to workers (whether they're [CPU cores](https://www.computerhope.com/jargon/c/core.htm) on your laptop or entire machines in a network), and then **_coordinating_** the workers to analyze the data. In essence, Spark is a "divide and conquer" strategy.

A simple analogy can help visualize the value of this approach. Let's say we want to count the number of books in a library. The "expensive computer" approach would be to teach someone to count books as fast as possible, training them for years to accurately count while sprinting. While fun to watch, this approach isn't that useful $-$ even Olympic sprinters can only run so fast, and you're out of luck if your book-counter gets injured or decides to change professions!

The Spark approach, meanwhile, would be to get 100 random people, assign each one a section of the library, have them count the books in their section, and then add their answers together. This approach is more scalable, fault-tolerant, and cheaper... and probably still fun to watch.

Spark's main data type is the [**resilient distributed dataset (RDD)**](https://sparkbyexamples.com/spark-rdd-tutorial/). An RDD is an abstraction of data distributed in many places, like how the entity "Walmart" is an abstraction of millions of people around the world. Working with RDDs feels like manipulating a simple array in memory, even though the underlying data may be spread across multiple machines.

Spark is mainly written in [Scala](https://www.scala-lang.org/) but has support for Java, Python, R, and SQL. We'll use [PySpark](https://spark.apache.org/docs/latest/api/python/), the Python interface for Spark. Below is a simple snippit of creating an RDD of an array, visualizing the first two numbers, and printing out the maximum. With `.getNumPartitions`, we see that Spark allocated our array to eight worker nodes on my machine.

{% include header-python.html %}
```python
from pyspark.sql import SparkSession

# Start Spark connection
spark = SparkSession.builder.getOrCreate()

# Allocate the numbers 0-999 to an RDD
numbers = range(1000)
rdd = spark.SparkContext.parallelize(numbers)

# Visualize RDD
print(rdd.take(2))  # [0, 1]
print(rdd.max())    # 999
print(rdd.getNumPartitions())  # 8
```

With this basic primer, we're ready to start leveraging Spark to process large datasets. Since you probably don't have any terabyte- or petabyte-size datasets lying around to analyze, we'll need to get a little creative. Let's start with a novel.

### Counting letter frequencies in a novel
[Project Gutenberg](https://www.gutenberg.org/) is an online repository of books in the [public domain](https://fairuse.stanford.edu/overview/public-domain/welcome/), so we can pull a book from there to analyze. Let's do Fyodor Dostoyevsky's _War and Peace_ $-$ I've always wanted to read it, or at least know how frequently each letter in the alphabet appears! <sup>[[2]](#2-counting-letter-frequencies-in-a-novel)</sup>

Below, we get the HTML from the novel's webpage with the [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) Python library, tidy up the paragraphs, and then append them to a list. We then remove the first _382_ paragraphs that are just the table of contents! We're left with 11,186 paragraphs ranging from 4 characters to 4381. (The string kind of characters, but with _War and Peace_, maybe novel characters too.)

```python
import requests
import pandas as pd
import bs4 as BeautifulSoup

# Pull book
book_url = "https://www.gutenberg.org/files/2600/2600-h/2600-h.htm"
response = requests.get(book_url)
soup = BeautifulSoup(response.text, 'html')

# Create list to store clean paragraphs
pars = []

# Set minimum str length for paragraphs
MIN_PAR_LEN = 2

# Iterate through paragraphs
for par in soup.findAll('p'):

    # Remove newlines and returns
    par_clean = ''.join(par.text.split('\n'))
    par_clean = ''.join(par_clean.split('\r'))

    if par_clean == '':
        continue

    # Remove extra spaces
    par_clean = par_clean.split('  ')
    par_clean = ' '.join([p for p in par_clean if p != ''])

    # Add cleaned paragraph to list
    if len(par_clean) > MIN_PAR_LEN:
        pars.append(par_clean)

# Remove table of contents
pars = pars[383:]

# Visualize paragraph lengths
pd.Series([len(par) for par in pars]).describe().astype(int)
# count    11186
# mean       284
# std        337
# min          4
# 25%         84
# 50%        170
# 75%        347
# max       4381
```

Despite _War and Peace_ being a massive novel, we see that `pandas` can still process high-level metrics without a problem $-$ line 38 runs nearly instantly on my laptop. But we'll start to notice a substantial performance improvement with Spark when we start asking tougher questions, like the frequency of each letter throughout the book. This is because **the paragraphs can be processed independently from one another**; Spark will process paragraphs eight at a time, whereas Python and `pandas` will process them one by one.

As before, we start our Spark session and create an RDD of our paragraphs. We also load `Counter`, a built-in Python class optimized for counting, and `reduce`, which we'll use to demo the base Python approach later.

{% include header-python.html %}
```python
from functools import reduce
from collections import Counter
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder.getOrCreate()

# Partition novel into RDD
rdd = spark.sparkContext.parallelize(pars)
```

We then [map](https://en.wikipedia.org/wiki/Map_(higher-order_function)) the `Counter` command to each paragraph with `rdd.map(Counter)`. Note how nothing happens unless we add `.take(2)` to output the first two results $-$ Spark does [lazy evaluation](https://en.wikipedia.org/wiki/Lazy_evaluation), a method for optimizing chains of queries until a result actually needs to be returned.

{% include header-python.html %}
```python
# Nothing happens
rdd.map(Counter)
# PythonRDD[12] at RDD at PythonRDD.scala:53

# We force the execution by asking to display 1st two results
rdd.map(Counter).take(2)
# [Counter({'“': 1,
#           'W': 1,
#           'e': 40,
#           ...
#           '!': 1,
#           '?': 1,
#           '”': 1}),
#  Counter({'I': 1,
#           't': 19,
#           ' ': 79,
#           ...
#           'K': 1,
#           ';': 1,
#           'b': 3})]
```

`rdd.map(Counter)` gives us a new RDD with the letter frequencies for each paragraph, but we actually want the letter frequencies of the entire book. Fortunately, we can do this by simply adding the `Counter` objects together. ("Fortunately" because this is painfully hard with normal Python dictionaries!)  

We therefore simply tell Spark to add all the RDD elements together. We perform this [reduction](https://en.wikipedia.org/wiki/Fold_(higher-order_function)) from a multi-element object to a single output with the `.reduce` method, and we pass in an anonymous addition function to specify how to collapse the RDD.<sup>[[3]](#3-counting-letter-frequencies-in-a-novel)</sup> The result is a `Counter` object; we finish our analysis by using the `.most_common` method to print out the ten most common characters.

{% include header-python.html %}
```python
rdd.map(Counter).reduce(lambda x, y: x + y).most_common(10)
# [(' ', 554621),
#  ('e', 308958),
#  ('t', 217658),
#  ('a', 194793),
#  ('o', 186623),
#  ('n', 179202),
#  ('i', 162925),
#  ('h', 162216),
#  ('s', 158811),
#  ('r', 143914)]
```

And the winner is... space! Here's those same frequencies, but in a nice barplot.

<center>
<img src="{{  site.baseurl  }}/images/data_engineering/pyspark/war_and_peace_letters.png" height="85%" width="85%">
</center>

Was using Spark worth it? Let's end this section by timing how long it takes our task to run in Spark versus base Python. We can use the incredibly useful `%%timeit` [IPython magic command](https://ipython.readthedocs.io/en/stable/interactive/magics.html) in _separate_ Jupyter notebook cells to see how our methods compare.

In Spark:

{% include header-python.html %}
```python
%%timeit
rdd.map(Counter).reduce(lambda x, y: x + y).most_common(5)
# 272 ms ± 18.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

And in base Python:

{% include header-python.html %}
```python
%%timeit
reduce(lambda x, y: x + y, (Counter(val) for val in pars)).most_common(5)
# 806 ms ± 9.37 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

With Spark, we're about 67.7% faster than using base Python. Sweet! Now I need to decide what to do with that extra half second of free time.

## Calculating $\pi$
There are [lots of great tutorials](https://www.cantorsparadise.com/calculating-the-value-of-pi-using-random-numbers-a-monte-carlo-simulation-d4b80dc12bdf) on how to calculate pi using random numbers. The brief summary is that we generate random x-y coordinates between (0,0) and (1,1), then calculate the proportion of those points that fall within a circle with radius 1. We can then solve for $\pi$ by multiplying this proportion by 4. In the visualization below, we would divide the number of blue points by the total number of points to get $\frac{\pi}{4}$.

<center>
<img src="{{  site.baseurl  }}/images/data_engineering/pyspark/calculate_pi.png" loading="lazy" height="45%" width="45%">
</center>

The more points we generate, the more accurate our estimate gets for $\pi$.

[Monte Carlo simulations](https://www.ibm.com/cloud/learn/monte-carlo-simulation)

 This is an ideal place for PySpark to come in.

Here's a function for calculating pi. I tried striking a balance between 1) iterating through `n_samples` and generating one point each time (low memory intensity but takes long), versus 2) generating all samples at once and then calculating the mean (need to store all points in memory). A solution I found works pretty well is to break `n_samples` into several _chunks_, calculate the proportion of points within the circle for each chunk, and then get the mean of means at the end.

{% include header-python.html %}
```python
def calculate_pi(n_samples, n_chunks=11):

    means = []

    for _ in np.linspace(0, n_samples, n_chunks):

        x = np.random.rand(n_samples)
        y = np.random.rand(n_samples)

        means.append(np.mean(np.sqrt(x**2 + y**2) < 1))

    return np.mean(means) * 4
```

Now let's get Spark going. We'll have a bunch of nodes on our machine estimate pi simultaneously, then take the average of their estimates to get a final result.

{% include header-python.html %}
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

n_partitions = 100
n_samples = 100000

rdd = spark.sparkContext.parallelize(range(n_partitions),
                                     numSlices=n_partitions)

rdd.map(lambda x: calculate_pi(n_samples)).mean()
# 3.1411235
```

Not bad! Using `%%timeit` again, we see that on my machine, base Python takes 3.76 s $\pm$ 138 ms, while Spark takes 1.34 s $\pm$ 117 ms, a 64% improvement. Nice!


## Spark dataframes
Let's do one more example, this time using a nice abstration Spark provides on top of RDDs. In a syntax similar to `pandas`, we can use [Spark dataframes] to perform operations on data that's too large to fit into a `pandas` df.

You probably don't have a dataframe with a few million rows laying around, so we'll need to generate one.

Let's generate a dataframe with 50 million rows. We'll need to do this in pieces, iteratively saving CSVs to later ingest with PySpark.

{% include header-python.html %}
```python
import os
import pandas as pd

os.mkdir('datasets')

names = ['Abby', 'Brad', 'Caroline', 'Dmitry']
n_samples = 1000000

for i in range(1, 51):
    df = pd.DataFrame({'name': np.random.choice(names, n_samples),
                       'age': np.random.normal(50, 10, n_samples),
                       'height': np.random.rand(n_samples)})
    df.to_csv(f'datasets/big_df_{i}.csv', index=False)

    if i % 10 == 0:
        print(i)
```

Then we can create a Spark dataframe from the CSVs. Let's check the schema and number of rows.

{% include header-python.html %}
```python
rdd_df = spark.read.format('csv')\
            .option('header', 'true')\
            .option('inferSchema', 'true')\
            .load('datasets/big_df*')

rdd_df.printSchema()
# root
#  |-- name: string (nullable = true)
#  |-- age: double (nullable = true)
#  |-- height: double (nullable = true)

rdd_df.count()
# 50000000
```

Now let's analyze our data. Let's start by counting the number of rows for each person.

{% include header-python.html %}
```python
rdd_df.groupBy('name').count().orderBy('name').show()
# +--------+--------+
# |    name|   count|
# +--------+--------+
# |    Abby|12505506|
# |    Brad|12492586|
# |Caroline|12501527|
# |  Dmitry|12500381|
# +--------+--------+
```

Now let's find the average age and height by person. Note that these should be very close to the mean of the distribution `numpy` generated them from!

{% include header-python.html %}
```python
rdd_df.groupBy('name').mean().orderBy('name').show()
# +--------+------------------+------------------+
# |    name|          avg(age)|       avg(height)|
# +--------+------------------+------------------+
# |    Abby|50.003242502450576|0.5005356708258004|
# |    Brad|  49.9928861434274|0.4999207020891359|
# |Caroline| 50.00418138186213|  0.50003226601409|
# |  Dmitry| 49.99832431955308|0.4998001935985182|
# +--------+------------------+------------------+
```

What's curious is that if you run this a few times, the exact values you'll get will vary slightly, by about 0.001. Interesting...

To have those values be nice and rounded, we'll actually need to create a user-defined function. Check it out. The `DoubleType()` refers to the type of the returned value.

{% include header-python.html %}
```python
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import pandas_udf
from pyspark.sql.functions import PandasUDFType

@pandas_udf(DoubleType(), functionType=PandasUDFType.GROUPED_AGG)
def round_mean(vals):
    return round(vals.mean(), 4)

spark.udf.register("round_mean", round_mean)
```

Now we can apply it to our dataframe. Note that since we're using `.agg`, we'll need to pass in a dictionary with the columns we want to apply our thing to.

{% include header-python.html %}
```python
func_dict = {col: 'round_mean' for col in ['age', 'height']}

rdd_df.groupBy('name').agg(func_dict).orderBy('name').show()
# +--------+---------------+------------------+
# |    name|round_mean(age)|round_mean(height)|
# +--------+---------------+------------------+
# |    Abby|        49.9943|            0.5001|
# |    Brad|        50.0016|            0.4999|
# |Caroline|        49.9991|               0.5|
# |  Dmitry|        49.9955|            0.5001|
# +--------+---------------+------------------+
```





# Old
Note that the `\n` counts as a character, so we only get two letters back. Now let's save it as a text file.

{% include header-python.html %}
```python
with open('novel.txt', 'w') as file:
    file.write(our_novel)
```

Now it's time for some PySpark magic. Make sure you have [Java](https://java.com/en/download/manual.jsp) and PySpark installed.

I'll run this in a Jupyter notebook or Python instance.

{% include header-python.html %}
```python
import pyspark

sc = pyspark.SparkContext('local[*]')

# Load our file
txt = sc.textFile('novel.txt')
```

Now that our data is loaded in, let's run some analyses on it.

{% include header-python.html %}
```python
# N letters
print(txt.count())  # 1000000

# First 5 letters
print(txt.take(5))  # ['g', 't', 'o', 'k', 'h']

# N letters that are 'e'
print(txt.filter(lambda: letter == 'e').count())
# 38833
```


## Old 2
## Web scraping
Let's scrape the Wikipedia page for computers and find the 10 most common characters (e.g. `a`, `b`, etc.) on the page. We'll take a distributed approach by handing each paragraph to a separate Spark node. (?)

{% include header-python.html %}
```python
import requests
from bs4 import BeautifulSoup

response = requests.get('https://en.wikipedia.org/wiki/Computer')

soup = BeautifulSoup(response.text, 'html')
```

Then we want to convert the HTML into a list of the paragraphs. We can do so like this.

{% include header-python.html %}
```python
pars = []

for par in soup.findAll('p'):

    # Remove newline characters
    text = par.text.split('\n')[0]

    if len(text) > 0:
        pars.append(text)

print(len(pars))  # 90
```

Now we start our Spark stuff. We instantiate a Spark session, then create a [**resilient distributed dataset (RDD)**](https://sparkbyexamples.com/spark-rdd-tutorial/) of our list of strings. This RDD is the core data structure in Spark - it's what allows us to distribute our data to multiple workers who can execute a command in parallel.

Resilient = able to recompute missing or damaged partitions.
Mention `numSlices`?


{% include header-python.html %}
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
rdd = spark.sparkContext.parallelize(pars)

# Visualize number of partitions
print(rdd.count())   # 90
```

We see that `.parallelize` created one partition per paragraph.
You might have heard of Google's MapReduce, which is basically what's happening here.

(Worth comparing to the letter distribution in tons of data?)

## Footnotes
#### 1. [Intro](#)
The median household income in 2019 was \$68,703, according to [Census.gov](https://www.census.gov/library/publications/2020/demo/p60-270.html). Multiply this by 50 to get 3.43 million, which is smaller than some of the data we analyze in this post.

#### 2. [Counting letter frequencies in a novel](#counting-letter-frequencies-in-a-novel)
In earlier drafts of this post, I toyed around with generating the text for a "novel" myself. I looked at some [*lorem ipsum*](https://loremipsum.io/) Python packages, but they were a little inconsistent; I found the very funny [Bacon Ipsum API](https://baconipsum.com/json-api/) but didn't want to drown it with a request for thousands of paragraphs. The code below uses random strings to generates a "novel" 100,000 paragraphs long, or 8.6x _War and Peace_'s measely 11,000. Turns out writing a novel is way easier than I thought!

{% include header-python.html %}
```python
import numpy as np
from string import ascii_lowercase

# Create set of characters to sample from
ALPHABET = list(ascii_lowercase) + [' ', ', ', '. ', '! ']

# Set parameters
N_PARAGRAPHS = 100000
MIN_PAR_LEN = 100
MAX_PAR_LEN = 2000

# Set random state
np.random.seed(42)

# Generate novel
novel = []
for _ in range(N_PARAGRAPHS):

    # Generate and visualize our data
    n_char = np.random.randint(MIN_PAR_LEN, MAX_PAR_LEN)
    paragraph = np.random.choice(ALPHABET, n_char)

    novel.append(''.join(paragraph))

# Visualize first "paragraph"
print(our_novel[0]) # t. okh. ugzswkkxudhxcvubxl! fb, ualzv....
```

#### 3. [Counting letter frequencies in a novel](#counting-letter-frequencies-in-a-novel)
You can easily reduce RDDs with more complex functions, or ones you've defined ahead of time. But for much big data processing, the operations are usually pretty simple $-$ adding elements together, filtering by some threshold $-$ so it's a little overkill to define these functions explicitly outside the one or two times you use them.
