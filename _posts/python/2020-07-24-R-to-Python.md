---
layout: post
title: Perspectives on Python after R
author: matt_sosna
summary: An R user's journey into the depths of Python
image: images/r-python.png
---
![]({{ site.baseurl }}/images/r-python.png)
My first programming language was R. I fell in love with the nuance R granted for visualizing data, and how with a little practice it was straightforward to pull off complex statistical analyses. I coded in R throughout my Ph.D., but I needed to switch to Python for my first non-academic job. Picking up a second language went much faster than the first, but there was a lot to get used to when I transitioned.

This post outlines some of the major differences between R and Python, as well as why those differences exist.

## Table of contents
* [How do I actually get started?](#how-do-i-actually-get-started)
* [The `.` suddenly has significance](#the--suddenly-has-significance)
* [Where are all the built-in functions?](#where-are-all-the-built-in-functions)
* [Zero-indexing](#zero-indexing)
* [Variables can be linked!](#variables-can-be-linked)
* [Final thoughts](#final-thoughts)
* [Footnotes](#footnotes)

## How do I _actually_ get started?
Thanks to the explosion of interest in data science over the last decade, there are tons of excellent online classes for getting started with R and Python for free. (I can vouch for the content from [DataCamp](https://www.datacamp.com/courses/free-introduction-to-r) and [Codecademy](https://www.codecademy.com/learn/learn-python) especially.) A major convenience of these classes is that you can type code directly into a terminal on the screen, as opposed to needing to install R or Python on your computer first. While this is handy for the very first steps of learning a language, you still need to actually install the program once the course is over if you want to keep coding.

To start programming in R on your own, you download R and [RStudio](https://rstudio.com/)... and then you're done. Once in the comfort of RStudio, you can do pretty much anything R-related you'd want: write and test code, create and run entire scripts, install and update packages, produce and export visuals, build and share Markdown files that export to PDF, etc.

Getting started with Python, meanwhile, feels like you're in a maze. My first goal after the intro Python Codecademy class ended was to find **_"the"_** IDE (Integrated Development Environment) that Python developers use. For R, the answer is without a doubt RStudio. In Python... well, is it PyCharm, Jupyter, Anaconda, Spyder, Atom, or Sublime<sup>[[1]](#footnotes)</sup>? The short answer is "yes!" **Python's versatility as a language means developers can use it as a tool for a staggering range of applications.** That's great for Python (and society, I guess!), but it left me lost among the dozens of tools for coding in the language.

I ended up just picking the text editor Sublime and was at least able to create Python scripts. But I quickly encountered a second roadblock: **how to quickly test ideas in Python**. Coming from RStudio, I was used to analyses with a high level of feedback: you execute one line, inspect the variable, execute a few more lines, check again, etc. I couldn't figure out how to execute just one line in a Python file in Sublime - I had to execute the entire script. A work-around I found was to open up Command Prompt (I was using Windows), type `python` to open Python, and then get feedback on one-line snippits of code... but that was impractical for testing code with multiple lines, like a function.

<img align="right" src="{{ site.baseurl }}/images/jupyter.png" height="20%" width="20%">It wasn't until well into learning Python that a colleague helped me install [Jupyter](https://jupyter.org/), a notebook environment that is now the main way I test out ideas. Another great option is [Spyder](https://www.spyder-ide.org/), which looks just like RStudio. After trying out Jupyter and Spyder, I ended up actually preferring Jupyter, and eventually I even gave up RStudio in favor of using Jupyter to write R code, too.

These days, I use Terminal to quickly check bits of Python code, Jupyter for exploratory analyses and testing ideas, and [PyCharm](https://www.jetbrains.com/pycharm/) for writing production-level code.

## The `.` suddenly has significance
In R, you can treat the `.` like any other character. This means that `student_grade` and `student.grade` are both valid names for variables.

```r
# R
student_grade <- 1
student.grade <- 2
```

In Python, though, the `.` has special significance. The reason for this touches upon a major difference in how code in R and Python is organized: the prevalence of **classes.**

When we type `student.grade`, we're telling Python we want _the attribute `grade` of the object `student`._ This is because everything in Python is an object, and objects have _attributes_ that are accessed with the `.` operator. In the example below, we'll create an object `kid` that's an instance of the `Student` class.

```python
# Python
class Student:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print("Hi")

kid = Student('Matt')
print(kid.name)   # 'Matt'
kid.say_hi()      # 'Hi'
```

`Student` is a class with `name` and `say_hi` attributes. We create an instance of `Student` called `kid`. To get `kid`'s name, we type `kid.name`. To call the `say_hi` method, we type `kid.say_hi()`.

**Because the `.` is used to access properties of an object, it can't be used as part of a variable name.**

While everything in R [is also technically an object](https://stackoverflow.com/questions/34376318/whats-the-real-meaning-about-everything-that-exists-is-an-object-in-r), and there are [multiple ways to create classes](https://study.com/academy/lesson/classes-in-r-programming-definition-examples.html) with attributes and methods, I've personally never encountered R code that uses custom-created classes. Sure, there are plenty of online resources for _learning how to use these classes_, most notably [Hadley Wickham's _Advanced R_ textbook](https://adv-r.hadley.nz/). But actually seeing them in action? Nope. To be transparent, maybe it's me: the R code I've read was either from 1) me, 2) an academic collaborator sharing their analyses, or 3) data science-focused online classes and blog posts. Maybe R classes are a bigger deal in the workflows of large collaborative teams, or in industries I don't have much exposure to. (I've found surprisingly little from searching on Google for who these teams or what these industries could be, though.)

Regardless, the absence of classes is in sharp contrast to Python, where classes are an integral part of organizing your code. Keep an eye out for a future Intro to Python series, where I'll go further into detail on this.

## Where are all the built-in functions?
Especially for a first programming language, I really appreciated how much functionality comes out of the box with R as soon as you start a session. Let's say you want to load a CSV and plot some data. Here's what it looks like in R:

```r
# R
setwd("/Users/matt/Desktop")
df <- read.csv("data.csv")
plot(df$date, df$n_cases)
```

And here's what it looks like in Python:

```python
# Python
import os
import pandas as pd
import matplotlib.pyplot as plt

os.chdir("/Users/matt/Desktop")
df = pd.read_csv("data.csv")
plt.scatter(df['date'], df['n_cases'])
plt.show()
```

The number of libraries you need to import to do _anything_ in Python came as a surprise. Want to work with dataframes? Need to import `pandas`. How about arrays? Need `numpy`. Visualizations? `matplotlib`. Literally changing the working directory? `os`. I couldn't believe how bare-bones Python's core is. What functionality is actually there when you boot it up?

It took some learning about the broader programming context Python comes from for me to understand what's up with this approach. Like [its predecessor C](http://www2.cs.uregina.ca/~hilder/cs833/Other%20Reference%20Materials/The%20C%20Programming%20Language.pdf), Python is designed to be extremely slim. Your program doesn't need to change the directory? The `os` functions aren't taking up memory. No vector operations needed? No `numpy`. One way to keep your programs fast and flexible is to have only the absolute essentials loaded when you open Python. Being bare-bones also means that whenever core Python developers put out a new version of Python, it's less likely to break something downstream for developers of libraries like `numpy` or `pandas`. [As with classes](#the--suddenly-has-significance), libraries are just the next level of organization for your code.

## Zero-indexing
Something that drove me absolutely crazy when switching to Python was dealing with its zero-indexing. R is 1-indexed, _the way normal people think_. (I'm still bitter!) To explain, let's say you have a vector of numbers called `vector`, and you want to access the **2nd through 4th elements.** In R, this couldn't be easier:
```r
# R
vector[2:4]  # 2nd through 4th elements
```

Python, however, is zero-indexed, meaning you have to start counting at zero. Ranges in Python are also **_exclusive_** on the right, meaning you don't count the last value in the range. So to get the 2nd through 4th elements, you need to write this:

```python
# Python
vector[1:4]  # 2nd through 4th elements
```

This means you:
* Skip the first element (index `0`)
* Count the second, third, and fourth elements (indices `1`, `2`, and `3`)
* Then go one extra step because the range is exclusive (end on index `4`).

So what's going on? It turns out Python's zero-indexing also harkens to some deep-rooted computer science history, going as far back as [BCPL](https://en.wikipedia.org/wiki/BCPL), a precursor to C. In any programming language, **a variable is just some text that points to an address in the computer's memory.** So when we say `x = 'abc'` in R or Python, we are:
1. setting aside some space in the computer's memory,
2. filling that space with machine code for `'abc'`,
3. and then _pointing_ the text `x` towards that space in memory.

Then, whenever you type `x`, R or Python actually see a pointer that _points towards the location in memory with `'abc'` in it_.

**A vector in R or list in Python is just a sequence of pointers to different addresses in memory.** In C, these regions are right next to one another. When you define a variable in C, you have to tell C how much memory that variable requires, so C can find a contiguous block of memory big enough to hold that variable. Then, because all of the components of the array are right next to each other, the pointer to the array actually just needs to point to the _start_ of the array, plus remember how long the array is.

For example, let's say you have a string called `"hello"`. C treats this as an array of characters. If you assign `"hello"` to the variable `message`, `message` is really just a pointer to the first letter of the `"hello"`, plus the length of the string. You can see this below<sup>[[2]](#footnotes)</sup>: `*message` and `*(message+0)` are identical. (`*` accesses the value the pointer is pointing to.)

```c
// C
#include <stdio.h>

int main()
{
  char message[] = "Hello";

  printf("%c \n", *message);      // 'H'
  printf("%c \n", *(message+0));  // 'H'

  return 0;
}
```
To access the rest of the string, you just type `*(message+1)` to get `e`, `*(message+2)` to get `l`, `*(message+3)` to get the next `l`, and so on.

In Python, despite the fact that the pointers in an iterable can point to addresses in memory that aren't next to one another, we still index the elements of an array as if they were indeed sitting next to each other. This zero-indexing is the norm for many languages, such as Java, JavaScript, Go, PHP, Ruby, Swift... but there are notable exceptions, like MATLAB, Julia, and of course R.

## Variables can be linked!
Whenever you create two variables, you have two independent variables, right? In the physical world, even identical twins are separate entities living independent lives. Well, that may be the case in the real world and in R, but it's not always the case in Python.

```r
# R
a <- c(1, 2, 3)
b <- a

a[2] <- 5

print(a)  # 1 5 3
print(b)  # 1 2 3
```
No qualms with this in R. We set `b` to whatever `a` is, `a` changes, but `b` stays the same. Great. But what happens if we try this in Python?

```python
# Python
a = [1, 2, 3]
b = a

a[1] = 5

print(a)  # [1, 5, 3]
print(b)  # [1, 5, 3]   <- O_O
```

*Cue hours of confusion that don't end even after you find the bug.*

So to understand what's going on here, we have to go [back to pointers](#zero-indexing). Certain data types in Python are **_mutable_**, meaning variables of that type can be _updated_ without changing the address in memory. This is what happens when you do `.append` to a list, or `.update` to a dictionary - you don't need to do `my_list = my_list.append(5)`; you just do `my_list.append(5)` and the list is updated.<sup>[[3]](#footnotes)</sup>

In contrast, other data types are **_immutable_**, meaning your variable changes location in memory when it's updated. This is the case with all variables in R<sup>[[4]](#footnotes)</sup> - even when we assign `b` equal to `a`, `b` gets an entirely new address in memory, making it independent from `a`. In Python, this is only the case for immutable data types, such as strings, tuples, or floats.

To visualize this better, let's ask Python to return the memory address for objects as we update them. `id` returns the memory address of an object, and `is` returns whether two objects have the same address. Here it is for **immutable** strings:

```python
# Python
a = 'Hello'
b = a

print(id(a))   # 140530884633008
print(id(b))   # 140530884633008
print(a is b)  # True

a = 'Hi'

print(id(a))   # 140530913364592   <- changed
print(id(b))   # 140530884633008   <- didn't change
print(a is b)  # False
```

And here it is for **mutable** lists:
```python
# Python
a = [1, 2]
b = a

print(id(a))   # 140530885072448
print(id(b))   # 140530885072448
print(a is b)  # True

a.append(3)

print(id(a))   # 140530885072448   <- didn't change
print(id(b))   # 140530885072448   <- didn't change
print(a is b)  # True
```

With mutable data types, you need to be really careful if multiple variables are pointing to the same location in memory. In line 3 above, `b` is **NOT** being set to a unique copy of `[1, 2]`... it's being set to the same list that `a` is pointing to! That means that whenever `a` makes a change to that list, you'll see the change reflected in `b`, too.

One solution to this is to use the `.copy` method Python provides for mutable data types <sup>[[5]](#footnotes)</sup>.

```python
# Python
a = [1, 2]
b = a.copy()   # <- sets aside new memory for b

print(id(a))   # 140530913380224
print(id(b))   # 140530912645440   <- different
print(a is b)  # False

a.append(3)

print(a)       # [1, 2, 3]
print(b)       # [1, 2]
print(a is b)  # False
```

So why on earth would we allow any language to have linked variables? Well, it's far more memory-efficient to only create new variables when needed. If you're updating a list with the contents of a long `for` loop, you don't want to create a new list with the contents of the entire previous list on every iteration; **you just want to update the list you currently have.**

(This is actually a major performance tip for beginner R users: never write a `for` loop with something like `vec <- c(vec, new_value)`! It's much better to pre-allocate a vector of NaNs as long as your loop, then fill in each index of the vector as the loop progresses.)

There are also some times when we actually may want to update multiple variables simultaneously. As a toy example, let's imagine we have some video game where a diamond, ruby, and sapphire are buried in different locations on a virtual island. To find the treasure, we have instances of a `TreasureFinder` class that search the island. The bots follow different rules for finding the different gems: sapphires tend to be by water, while volcanoes often hide rubies. If the sapphire is found, for example, we should stop searching the island coast. If we have multiple instances of `TreasureFinder`, whenever one instance finds a gem, it can alert all instances of `TreasureFinder` to stop searching for that gem. To do this, we'd use a class method that updates a shared list.

```python
class TreasureFinder:
    chest = []

    def update_chest(self, treasure):
        self.chest.append(treasure)

tf1 = TreasureFinder()
tf2 = TreasureFinder()

# Code where they roll around, searching for treasure...

# Treasure found!
tf1.update_chest('ruby')
print(tf1.chest)  # ['ruby']
print(tf2.chest)  # ['ruby']
```

Even though we have multiple instances of `TreasureFinder`, the `chest` list is initialized when the class `TreasureFinder` is defined, meaning all of the instances' `chest` lists are actually copies that point to the same location in memory.

## Final thoughts
Having now spent a few years coding in both R and Python, I've gotten a better picture of their pros and cons when it comes to analytics and data science. If you're only doing analytics, it's hard to beat R's simplicity, especially if you're starting without a programming background. For fields like ecology and political science, R also tends to be the standard language to use, meaning you can find plenty of support for exactly how to carry out even highly complex analyses. Finally, when it comes to statistics, R is still my go-to language. For [Sosna et al. 2019](https://www.pnas.org/content/pnas/early/2019/09/17/1905585116.full.pdf), I used R to carry out L<sub>1</sub>-penalized logistic regression with nested random effects. I was able to use the [glmmlasso](https://cran.r-project.org/web/packages/glmmLasso/glmmLasso.pdf) package for this, but I haven't found anything similar in Python.

Once you've finished [actually getting set up](#how-do-i-actually-get-started) with Python, though, Python's versatility really shines. (Pro tip for beginners: choose an online class that includes setting up Python on your computer.) While I think Python falls short of R when it comes to ease of analyzing data<sup>[[6]](#footnotes)</sup>, the number of things you can do with Python is eye-opening. Once you're comfortable with Python fundamentals, it's a small leap to start [pulling web data](https://requests.readthedocs.io/en/master/), interacting with [cloud storage](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), building [your own API](https://flask.palletsprojects.com/en/1.1.x/), creating [interactive visualizations](https://docs.bokeh.org/en/latest/index.html), or building [computer vision applications](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html). As you start writing code that you want to have others interact with, you'll find built-in support for Python in developer tools like [Heroku](https://www.heroku.com/) (a hosting platform) and [Amazon Web Services](https://aws.amazon.com/) (cloud storage, compute, and more), but you won't see such support for R.

Ultimately, what really matters is what sort of task you're trying to accomplish with coding, and what language you enjoy writing in. The R and Python communities are bustling and constantly pushing to fill gaps in their languages. If you're a die-hard R afficionado and you want Heroku to add R support, let them know! You're [not the only R developer](https://medium.com/@DaveQuartey/how-i-installed-r-on-heroku-ff8286233d2c) thinking the same thing. (Here's [Heroku's contact page](https://www.heroku.com/contact) if you're serious.) The important thing is to keep learning and not be bound to any one tool. Some other language will inevitably overtake R and Python someday, and future generations will shake their heads wondering why we ever bothered with software that couldn't read our minds.

Best, <br>
Matt


## Footnotes
1. [[How do I actually get started?]](#how-do-i-actually-get-started) Python's "all-in-one" solution is arguably [Anaconda](https://www.anaconda.com/), and I probably would have saved myself many headaches by being more patient with Anaconda's documentation and user guide. In my defense, the number of additional programs needed to run Python is super confusing for a newcomer - and don't get me started on accidentally having some Python libraries saved via [pip](https://pip.pypa.io/en/stable/) versus the `conda` environment.

2. [[Zero-indexing]](#zero-indexing) If you have a Mac, you can easily run C code yourself. Save the example code in a file called e.g. `hello.c`, then in Terminal, navigate to the directory, type `cc hello.c -o hello` to compile the program, then type `./hello`.

3. [[Variables can be linked]](#variables-can-be-linked) `my_list.append(5)` actually returns `None` since it just modifies `my_list`, so `my_list = my_list.append(5)` would introduce a whole other bug that'd be hard to figure out.

4. [[Variables can be linked]](#variables-can-be-linked) Actually, _almost_ all objects in R are immutable. There are [some esoteric exceptions](https://win-vector.com/2014/04/01/you-dont-need-to-understand-pointers-to-program-using-r/) involving closures. But the vast majority of the time when you're programming in R, you don't have to worry about linked variables. This is because virtually all objects in R have unique addresses in memory, which means you can easily get a string of the variable name, like below:
    ```r
    # R
    a <- c(1, 2, 3)
    b <- a

    deparse(substitute(a))  # 'a'
    deparse(substitute(b))  # 'b'
    ```
This is [essentially impossible in Python](https://stackoverflow.com/questions/1534504/convert-variable-name-to-string/3683258) because objects can share addresses in memory. There's no built-in function for converting a variable into _the string of a variable name_, since when you give Python a variable, all Python sees is an address in memory, where multiple variables can point to. In other words, **Python fundamentally expects a many-to-one relationship between variables and addresses in memory. R, meanwhile, expects a one-to-one relationship.** In Python, the best we can do is scan the dictionary returned by `globals()` for keys that match the value of our variable.
    ```python
    # Python
    a = [1, 2, 3]
    b = a

    [var for var, key in globals().items() if key == [1, 2, 3]]
    # ['a', 'b']
    ```

5. [[Variables can be linked]](#variables-can-be-linked) There are a few other ways you can accidentally avoid updating `b` when `a` updates, making the variable linking even harder to catch:

    ```python
    a = [1, 2, 3]

    # Option 1: create a new list for b, with same elements of a
    b1 = list(a)
    b2 = a[:]
    print(b1 is a)   # False
    print(b2 is a)   # False

    # Option 2: break the link by not using .append to update a
    b3 = a
    a = a + [4]      # Creates new list for a
    print(b3 is a)   # False

    # BUT watch out! += modifies the original list
    a1 = [1, 2, 3]
    b = a1
    a1 += [4]   # instead of a1 = a1 + [4]
    print(b is a1)   # True
    ```
6. [[Final thoughts]](#final-thoughts) A few examples of how data manipulation is a little simpler in R:

* Subset a dataframe
```r
# R
df_filt <- subset(df, Sex == 'M' & Age > 50)
```
```python
# Python
df_filt = df[(df['Sex'] == 'M') & (df['Age'] > 50)]
```
<br>
* Create a vector where all values are NaNs except Nth values
```r
# R
vec <- c()
for(i in seq(3, 9, by=3)){
    vec[i] <- 10
}
print(vec)  # NA NA 10 NA NA 10 NA NA 10
```
```python
# Python
import numpy as np
vec = np.full(9, np.nan)  # <- need to pre-allocate
for i in range(2, 9, 3):
    vec[i] = 10
print(vec)   # nan nan 10 nan nan 10 nan nan 10
```
