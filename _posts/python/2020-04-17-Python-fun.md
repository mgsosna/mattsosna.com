---
layout: post
title: Random Python fun
author: matt_sosna
---

# Tips for total beginners
* It's hard to use Python without some additional support. Running Python in the command line is pretty spartan, and not a great way to learn the program.
* You need an Integrated Development Environment (IDE). These include Spyder, Pycharm, etc. I recommend using Jupyter notebooks. They let you execute little sections of code, combine normal text and code, visualize tables and plots, etc.


{% include numpy_sin.html %}


Some little tricks:
```python
x = 5
y = 5

x = x + 1
y += 1  

print(x)  # 6
print(y)  # 6
```

Pointing to the same locations in memory.

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
do_math(1, 2, 3, 4, operator=add)       # 10
do_math(1, 2, 3, 4, operator=multiply)  # 24
```

You need to use a keyword argument for `add` or `multiply` to distinguish it from the positional arguments.

### Another cool example
```python
def func(a, b):
    return a + b

arg_tuple = (1, 2)
arg_dict = {'a': 1, 'b': 2}

func(*arg_tuple)
func(**arg_dict)

```

# Magic methods
Let's say we have an `Item` class. An instance of the class will have `name` and `price` attributes.

```python
class Item:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
```

Let's say in our shopping cart we have three items:

```python
hammer = Item("hammer", 15.99)
cheeseburger = Item("nails", 9.99)
hat = Item("hat", 1099.99)
```

Normally, if we want to add the costs of a few items, we need to access their prices directly, as such:

```python
total_price = hammer.price + cheeseburger.price
```

Enter the `__add__` magic method. This lets us tell Python what to do when your class sees the `+` operator.

```python
class Item:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __add__(self, other: Item):
        return self.price + other.price
```

Now, instead of needing to do `hammer.price` and `cheeseburger.price`, we can just add `hammer` and `cheeseburger` directly.

```python
total_price = hammer + cheeseburger
```

But something surprising happens when you try to add more than two `Item` objects together.

```python
total_price = hammer + cheeseburger + hat
# TypeError: unsupported operand type(s) for +: 'int' and 'Item'
```

 Even with our cool new `__add__` method, we get `TypeError: unsupported operand type(s) for +: 'int' and 'Item'` when we try to add multiple items.

What's going on? Well, Python's order of operations is biting us. When you type `1 + 2 + 3` in Python, what you actually get is `(1 + 2) + 3`. This normally never matters, but it _does_ when we're trying to add our objects together. `hammer + cheeseburger` returns a float. But Python's built-in float object doesn't know what to do when it encounters our handmade `Item` object and is asked to be added with it. So Python returns a special value called `NotImplemented` (which we don't see) which ends up throwing a `TypeError` (which we _do_ see).

To solve this, we need to add is another magic method: `__radd__`. This method is executed when Python returns a `NotImplemented`. For us, we know that we're probably getting this error because an integer or float is being asked to interact with our `Item` class, so we can write a method that handles this.

```python
class Item:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __add__(self, other: Item):
        return self.price + other.price

    def __radd__(self, other: Union[float, int]):
        return self.price + other

```

Now, we can happily add however many items together.

```python
hammer = Item('hammer', 15.99)
cheeseburger = Item('cheeseburger', 9.99)
hat = Item('hat', 1099.99)

hammer + cheeseburger  # 25.98
hammer + 4  # 23.99
4 + hammer  # 23.99
hammer + cheeseburger + hat # 1125.97
```

# __str__ and __repr__
We can also make our classes nicer to interact with. Let's say that we want to be able to print out a string explaining the instance of the object.

```python
class Student:
    def __init__(self, name, grades=None):
        self.name = name
        self.grades = [] if not grades else grades

```

```python
mark = Student("Mark", grades=[100, 100, 100])

mark         # <__main__.Student at 0x1263c8c10>
print(mark)  # <__main__.Student object at 0x1263c8c10>
repr(mark)   # '<__main__.Student object at 0x1263c8c10>'

```
That's not very helpful. Let's create a new class, `FancyStudent`, that has magic methods that give us info about the student when you call the object outright, print it, or ask for Python's representation of it.

```python
class FancyStudent:
    def __init__(self, name, grades=None):
        self.name = name
        self.grades = [] if not grades else grades

    def __str__(self):
        return f"Student with name {self.name} and grades {self.grades}"

    def __repr__(self):
        return f"Student(name='{self.name}', grades={self.grades})"

```

```python
# Create an instance of Student
elizabeth = FancyStudent("Elizabeth", grades=[100, 100, 100])

mark         # Student(name='Elizabeth', grades=[100, 100, 100])
print(mark)  # Student with name Elizabeth and grades [100, 100, 100]
repr(mark)   # "Student(name='Elizabeth', grades=[100, 100, 100])""
```

`__str__` replaces what happens when you call `print` on `mark`. `__repr__`, meanwhile, replaces what happens when you just call `mark` outright.

Then you can do:
```python
mark = Student("Mark", grades=[100, 100, 100])

str(mark)   # 'Student with name Mark and grades [100, 100, 100]'
repr(mark)  # 'Student(name='Mark', grades=[100, 100, 100])'

```

`repr` is like how to recreate the object in Python.


```python
import datetime as dt

date = dt.date(2020, 1, 1)
str(date)   # '2020-01-01'
repr(date)  # 'datetime.date(2020, 1, 1)'
date        # datetime.date(2020, 1, 1)  # no quotes
```



# Treating everything as an object
```python
class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"Item with name {self.name} and price {self.price}"

    def __repr__(self):
        return f"Item('{self.name}', {price})"

    def __int__(self):
        return int(self.price)

    def __float__(self):
        return float(self.price)

```


# Some other fancy stuff
```python
# Instantiate a dict with keys and values
keys = ['a', 'b']
values = [1, 2]

d = dict(zip(keys, values))
print(d)  # {'a': 1, 'b': 2}

# If they're all the same value
d = {}.fromkeys(keys, 1)
print(d)   # {'a': 1, 'b': 1}

```
