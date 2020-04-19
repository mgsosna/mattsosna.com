---
layout: post
title: Random Python fun
---

Some little tricks:
```python
x = 5
y = 5

x = x + 1
y += 1  

print(x)  # 6
print(y)  # 6
```

```python
x = 5
y = 5
z = x

x == y  # True
x == z  # True

x is y  # False
x is z  # True
```
# `*args` and `**kwargs`
With unpacking, `args` itself is a tuple. `*args` is each argument, one after the other.


```python
def add(*args):
    result = 0
    for arg in args:
        result += arg
    return result

def multiply(*args):
    result = 1
    for arg in args:
        result *= arg
    return result
```

What that does:
```python
print(add(1, 2, 3, 4))      # 10
print(multiply(1, 2, 3, 4)) # 24
```

But we can have some fun with it, taking advantage of the fact that everything in Python is an object. You can pass functions into other functions, too.

```python
def do_math(*args, operator):
  return operator(*args)
```

You can then do:
```python
do_math(1, 2, 3, 4, operator=add)
do_math(1, 2, 3, 4, operator=multiply)
```

You need to use a keyword argument for `add` or `multiply` to distinguish it from the positional arguments.
