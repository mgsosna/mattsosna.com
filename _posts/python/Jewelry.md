---
layout: post
title: Jewelry - Python decorators for data science
author: matt_sosna
---

* What are decorators?
* `jewelry` is a Python repo I've created for this. Please contribute.


## Main functionaliteis

### `ArgChecker`
#### `enforce_type_hints`
* Verify that inputs to a function match the type hints.

```python
def multiply(a, b):
    return a * b

@ac.enforce_type_hints
def safe_multiply(a: int, b: int):
    return a * b

# Good behavior
multiply(1, 2)       # 2
safe_multiply(1, 2)  # 2

# Diverges
multiply('1', 2)     # '11'
safe_multiply('1', 2)  # AssertionError: a is type <class 'str'>
```



#### `.colcheck`

```python
@ac.colcheck(df, ['a', 'b'])
def add_cols(df: pd.DataFrame):
    return df['a'] + df['b']
```

Makes sure that cols `a` and `b` are present, raises an `AssertionError` if not.

### `DataChecker`
I guess this is kind of like Great Expectations, so I'd want to see how it differs... but could do something simple.

```python
def check_thing(df, cols):
    for col in cols:
        assert df[col].max() - df[col].min() > 5
```
