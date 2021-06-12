---
layout: post
title: A hands-on demo of big data with PySpark
author: matt_sosna
---

We're used to dealing with data that can be stored on our machine. But what if you have a lot more?

There's a lot of data out there, with IoT, click streams, etc. In 2020,

[Cloud company Domo estimates](https://web-assets.domo.com/blog/wp-content/uploads/2020/08/20-data-never-sleeps-8-final-01-Resize.jpg) that for every minute in 2020, WhatsApp users shared 41.7 million messages, Netflix streamed 404,000 hours of video, consumers spent $1 million online, and 69,000 people applied for jobs on LinkedIn.

In that firehose of data are patterns that can elevate a company in its market if acted upon $-$ or cause a company's downfall if ignored. 


make or break business trajectories.

businesses salivate over being able to make de


Big data is important. But how can you actually practice big data processing if you're not already at a company with access to terabytes or petabytes of data? In this post, we'll keep things simple by generating large datasets ourselves on the fly, then processing them with PySpark. The nice thing is that the code in this post can be used verbatim on datasets hundreds or thousands of times larger than what we'll be dealing with $-$ just replace the lines for initializing Spark with whatever's needed to access the dozens or hundreds of machines you'll have at your fingertips when you're a data engineer at Google!


In one of my previous roles, I analyzed IRS tax returns for nonprofits. That is... I analyzed _700,000_ tax returns. Each tax return was an XML document that was about XXXX KB. So in total, that was XXX GB on my computer... more than my RAM could handle.

Another example was a CSV with 4 million rows. Just trying to load it into a `pandas` dataframe caused Jupyter to slow to a crawl and my fan to spin like crazy.



 This was an amount of data that's hard to

[Apache Spark](https://spark.apache.org/) is useful. Let's build a short intuition. Dealing with RDDs: resilient distributed datasets. Distributed across machines.

The real strength of Spark comes in being able to distribute your problem across nodes. These nodes can be cores inside a machine, or entire machines. The idea is that you have a coordinator node that allocates tasks to "worker" nodes.

An example I've heard is counting the number of books in a library. The "vertical scaling" approach would be to train a person to count books faster and faster $-$ they'd spend years training to count while running as fast as possible. But a more scalable, fault-tolerant, and cheaper option would be to just bring 20 friends, assign each person a section of the library, and have them count the books in their section. In the end, you would just need to add their answers together to get the total sum.



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

We see that `.parallelize` created one partition per paragraph. Let's now count how often each character (e.g. `a`, `b`, `c`, etc.) occurs in each paragraph in our RDD. `Counter` is a built-in Python class that's optimized for this. We'll **map** the `Counter` command to each string with `rdd.map(Counter)`.

{% include header-python.html %}
```python
from collections import Counter

# Nothing happens
rdd.map(Counter)
# PythonRDD[12] at RDD at PythonRDD.scala:53

# We force the execution by asking to display 1st two results
rdd.map(Counter).take(2)
# [Counter({'A': 2,
#           ' ': 88,
#           'c': 22,
#           ...
#           ',': 3,
#           '(': 1,
#           ')': 1}),
#  Counter({'A': 1,
#           ' ': 60,
#           'b': 3,
#           ...
#           'h': 6,
#           'C': 1,
#           'I': 1})]
```

Note that we need to do `.take(2)` at the end because PySpark does **lazy evaluation** - it won't actually run any commands we give it until forced to. This is because if we give a set of instructions and only at the end force Spark to execute the commands, it optimizes the task allocation at the end.

Finally, let's finish what we originally set out to do: finding the 10 most common letters on the Wikipedia page.

{% include header-python.html %}
```python
rdd.map(Counter).reduce(lambda x, y: x + y).most_common(10)
# [(' ', 8017),
#  ('e', 4933),
#  ('t', 3584),
#  ('a', 3241),
#  ('o', 3104),
#  ('i', 2900),
#  ('r', 2896),
#  ('n', 2835),
#  ('s', 2593),
#  ('c', 1817)]
```

Somewhat unsurprisingly, a space is the most common character, followed by `e`, `t`, and a couple vowels.

You might have heard of Google's MapReduce, which is basically what's happening here.

(Worth comparing to the letter distribution in tons of data?)

## Trying it on really massive data
This works fine, but it's not much faster than running it without PySpark. Let's try really creating a massive dataset. We can create a thing that has a thing. We'll generate the text ourselves; the [*lorem ipsum*](https://loremipsum.io/) Python packages I found were a little inconsistent, and I don't want to hit the very funny [Bacon Ipsum API](https://baconipsum.com/json-api/) with a request for 100,000 paragraphs.

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

Writing a novel has never been so easy! Now let's create our RDD, then time how long it takes to count all the letters using PySpark versus Python's built-in functions.

{% include header-python.html %}
```python
from functools import reduce
from collections import Counter
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder.getOrCreate()

# Partition novel into RDD
rdd = spark.sparkContext.parallelize(novel)
```

Then in _separate_ Jupyter notebook cells, we can run the following code. The `%%timeit` line is an [IPython magic command](https://ipython.readthedocs.io/en/stable/interactive/magics.html) that is super useful for timing how long a piece of code takes to run.

{% include header-python.html %}
```python
%%timeit
rdd.map(Counter).reduce(lambda x, y: x + y).most_common(5)
# 2.58 s +/- 208 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)
```

Versus in base Python:

{% include header-python.html %}
```python
%%timeit
reduce(lambda x, y: x + y, (Counter(val) for val in novel)).most_common(5)
# 7.98 s +/- 77.9 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)
```

So with PySpark, we're about 67.7% faster than using base Python. Sweet! I'm still deciding what to do with these extra four seconds...


## Calculating $\pi$
There are [lots of great tutorials](https://www.cantorsparadise.com/calculating-the-value-of-pi-using-random-numbers-a-monte-carlo-simulation-d4b80dc12bdf) on how to calculate pi using random numbers. The brief summary is that we generate random x-y coordinates between (0,0) and (1,1), then calculate the proportion of those points that fall within a circle with radius 1. We can then solve for $\pi$ by multiplying this proportion by 4. In the visualization below, we would divide the number of blue points by the total number of points to get $\frac{\pi}{4}$.

<center>
<img src="{{  site.baseurl  }}/images/data_engineering/pyspark/calculate_pi.png" loading="lazy" height="45%" width="45%">
</center>

The more points we generate, the more accurate our estimate gets for $\pi$. This is an ideal place for PySpark to come in.

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
