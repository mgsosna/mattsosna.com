---
layout: post
title: Intro to big data with PySpark
author: matt_sosna
---


We're used to dealing with data that can be stored on our machine. But what if you have a lot more?

In one of my previous roles, I analyzed IRS tax returns for nonprofits. That is... I analyzed _700,000_ tax returns. Each tax return was an XML document that was about XXXX KB. So in total, that was XXX GB on my computer... more than my RAM could handle.

Another example was a CSV with 4 million rows. Just trying to load it into a `pandas` dataframe caused Jupyter to slow to a crawl and my fan to spin like crazy.



 This was an amount of data that's hard to

Apache Spark is useful. Let's build a short intuition. Dealing with RDDs: resilient distributed datasets. Distributed across machines.

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

```python
%%timeit
rdd.map(Counter).reduce(lambda x, y: x + y).most_common(5)
# 2.58 s +/- 208 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)
```

Versus in base Python:
```python
%%timeit
reduce(lambda x, y: x + y, (Counter(val) for val in novel)).most_common(5)
# 7.98 s +/- 77.9 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)
```

So with PySpark, we're about 67.7% faster than using base Python. Sweet! I'm still deciding what to do with these extra four seconds...


## Calculating $\pi$

There are [lots of great tutorials](https://www.cantorsparadise.com/calculating-the-value-of-pi-using-random-numbers-a-monte-carlo-simulation-d4b80dc12bdf) on how to calculate pi using random numbers. The brief summary is that we generate random x-y coordinates between (0,0) and (1,1), then calculate the proportion of those points that fall within a circle with radius 1. We can then solve for $\pi$ by multiplying this proportion by 4.

<


We add some chunking.

```python
def calculate_pi(n_samples):

    means = []

    # Chunk the calculation
    for _ in np.arange(0, n_samples, n_samples/10):

        x = np.random.rand(n_samples)
        y = np.random.rand(n_samples)

        means.append(np.mean(np.sqrt(x**2 + y**2) < 1))

    return np.mean(means) * 4
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
