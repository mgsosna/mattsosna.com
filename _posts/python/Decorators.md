---
layout: post
title: Intro to decorators in Python
author: matt_sosna
---

### Quick primer on decorators
Here's an example of a simple decorator that doubles the values of `a` and `b` of whatever function is passed in.

```python
# Our decorator
def double(func):

    def func_w_doubled_args(*args):
        doubled_args = [2*arg for arg in args]
        return func(*doubled_args)

    return func_w_doubled_args
```

Then we can do some stuff.

```python
# Normal multiply
def normal_multiply(a, b):
    return a * b

# Decorated multiply
@double_args
def double_multiply(a, b):
    return a * b
```
