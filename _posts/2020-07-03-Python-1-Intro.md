---
layout: post
title: Learning Python - 1. Introduction
---

So everyone seems to be talking about Python. It's quickly become a wildly popular language, especially for data science, and it's refreshingly easy to read and use. (While HTML is pretty easy to learn, I would argue Python is even easier.)

Python is really popular for [AI and ML](https://www.heliossolutions.co/blog/why-choose-python-for-artificial-intelligence-and-machine-learning/).

In contrast to the [**Introduction to R**]({{ site.baseurl }}/R-1-Intro/) series, this series is going to assume you're not a complete newcomer to programming<sup>[1](#footnotes)</sup>. There's a bonanza of great Intro to Python tutorials out there, plenty with


## Try things out
If you can't be bothered to download Python but still want to play with it, try out a website like [repl.it](https://repl.it). You'll be able to write and execute Python code straight from your browser. Pretty easy!


## Tips for getting better
* Try things out.
* Start getting exposed to Python tips. [Real Python](https://realpython.com/) is a _fantastic_ resource - I follow them on Twitter, along with [Daily Python tip](https://twitter.com/python_tip) and a few others. The idea is to pick up tips here and there. That won't create your foundational knowledge, but it'll give you the little breakthroughs for making a bit of code more efficient. There's lots of ways to carry out a task, and as you become more experienced it's about narrowing down to the paths that are most readable and efficient.
* To that end, get exposed to professional Python. The wonderful thing about open-source code is that you can just pick it up and read it. It's not hidden behind a paywall or carefully guarded on a secret server. It's right [here]()








**Note:** much of this posts is a slightly-modified version of the ["Intro to R" series]({{ site.baseurl }}/R-1-Intro/).

# Getting started
* Download Python
* Download Jupyter probably...

```python
5
# 5
```

Yes, literally type `5` into the terminal. Unsurprisingly, Python tells you `5` back, confirming that `5 = 5` after all. Great work.

```python
x = 5
x
# 5
```

# Getting data into Python
If you're coming from R, you might be surprised how little functionality comes out of the box with Python. You literally need to import a library, `os`, to load a file... and another library, `pandas`, to save it into a dataframe! But that's ok.

```python
import os
import pandas as pd

```


# Footnotes
1. If you _are_ a newcomer to programming, great! I recommend the free Python classes on [Codecademy]((https://www.codecademy.com/learn/learn-python)) and [DataCamp]((https://www.datacamp.com/courses/intro-to-python-for-data-science)). Codecademy was how I first learned Python. Once you're ready to try it on your own, you can check out the [Getting Started guide](https://www.python.org/about/gettingstarted/) from the Python Foundation.
