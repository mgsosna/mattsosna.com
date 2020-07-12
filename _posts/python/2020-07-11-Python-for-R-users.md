---
layout: post
title: Python for R users
author: matt_sosna
---
My first programming language was R. I fell in love with the nuance R granted for visualizing data, and how with a little practice it was straightforward to pull off complex statistical analyses. I coded in R throughout my Ph.D., but the team I joined in my first job outside of academia solely coded in Python. Picking up a second language went much faster than the first, but there was a lot to get used to when I transitioned. I've compiled some of the major differences in this post.

## Table of contents
* [Where is my all-in-one solution?](#where-is-my-all-in-one-solution)
* [The `.` suddenly has significance](#the--suddenly-has-significance)
* [Where are all the built-in functions?](#where-are-all-the-built-in-functions)
* [Zero-indexing](#zero-indexing)
* [Variables can be linked!](#variables-can-be-linked)
* [Final thoughts](#final-thoughts)

## Where is my all-in-one solution?
To get started with R, you download R and RStudio, and then you're done. Once in the comfort of RStudio, you can do pretty much everything R-related you'd want: install and update packages, produce visuals, create Markdown files that export to PDF, etc.

Getting started with Python, meanwhile, feels like you're in a maze. Once my Codecademy intro Python class was over, was I supposed to download PyCharm, Jupyter, Anaconda, Spyder, Atom, or Sublime? Which of these were just text editors and which could actually execute Python code? Once I chose an editor, why did I have to exit that editor, go to Terminal, and use a _different_ program ([pip](https://pip.pypa.io/en/stable/)) to download a Python package? Even after downloading [Anaconda](https://www.anaconda.com/), arguably Python's "all-in-one" solution, I was left not really knowing what to do. (Reading Anaconda's documentation or user guide probably would have helped, but I was too impatient for that!)

The second roadblock I encountered was figuring out **how to quickly test ideas in Python**. Coming from RStudio, I was used to analyses with a high level of feedback: you execute one line, inspect the variable, execute a few more lines, check again, etc. If I opened up Terminal, typed `python` and then started coding, I could get feedback on one-line snippits of code... but for something like a function, was I seriously going to try to type out everything one line at a time? An alternative was to just type out a whole script in Atom, then run the entire thing at once from Terminal with `python script.py`... but then all these extra lines were being run even though I just wanted to test out one small change at the end.

It wasn't until well into learning Python that a colleague helped me install [Jupyter](https://jupyter.org/), a notebook environment that is now the main way I test out ideas. Another great option is [Spyder](https://www.spyder-ide.org/), which looks just like RStudio. After trying out Jupyter and Spyder, I ended up actually preferring Jupyter, and eventually I even gave up RStudio in favor of using Jupyter to write R code, too.

These days, I use Terminal to quickly check bits of Python code, Jupyter for exploratory analyses and testing ideas, and [PyCharm](https://www.jetbrains.com/pycharm/) for writing production-level code.

## The `.` suddenly has significance
In R, you can treat the `.` like any other character. This means that `student_grade` and `student.grade` are both valid names for variables.

```r
# R
student_grade <- 1
student.grade <- 2
```

In Python, though, the `.` has special significance. The reason for this touches upon a major difference in how code in R and Python is organized: the prevalence of **classes.**

When we type `student.grade`, we're telling Python we want _the attribute `grade` of the object `student`._ This is because everything in Python is an object, and objects have _attributes_ that are accessed with the `.` operator. In the example below, we'll create an object `matt` that's an instance of the `Student` class.

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

Because the `.` is used to access properties of an object, it can't be used as part of a variable name.

While everything in R [is also technically an object](https://stackoverflow.com/questions/34376318/whats-the-real-meaning-about-everything-that-exists-is-an-object-in-r), and there are [multiple ways to create classes](https://study.com/academy/lesson/classes-in-r-programming-definition-examples.html) with attributes and methods, I've personally never encountered R code that uses custom-created classes. Sure, there are plenty of online resources for _learning how to use these classes_, most notably [Hadley Wickham's _Advanced R_ textbook](https://adv-r.hadley.nz/). But actually seeing them in action? Nope. To be transparent, maybe it's me: the R code I've read was either from 1) me, 2) an academic collaborator sharing their analyses, or 3) data science-focused online classes and blog posts. Maybe R classes are a bigger deal in the workflows of large collaborative teams, or in industries I don't have much exposure to. (I've found surprisingly little from searching on Google for who these teams or what these industries could be, though.)

Regardless, the absence of classes is in sharp contrast to Python, where classes are an early part of learning how to organize your code. I talk about this in [Part 4]({{ site.baseurl }}/Python-4-Organizing-code) of the "Learning Python" track.

## Where are all the built-in functions?
Especially for a first programming language, I really appreciated how much functionality comes "out of the box" with R as soon as you start a session. Let's say you want to load a CSV and plot some data. Here's what it looks like in R:

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

The number of libraries you need to import to do _anything_ in Python came as a frustrating surprise. Want to work with dataframes? Need to import `pandas`. How about arrays? Need `numpy`. Visualizations? `matplotlib`. Machine learning models? `sklearn`. Literally changing the working directory? `os`. I couldn't believe how bare-bones base Python was. What's actually there when you first boot up Python?

It took some learning about the broader programming context Python comes from for me to understand what's up with this approach. Like [its predecessor C](http://www2.cs.uregina.ca/~hilder/cs833/Other%20Reference%20Materials/The%20C%20Programming%20Language.pdf), Python is designed to be extremely slim. Your program doesn't need to change the directory? The `os` functions aren't taking up memory. No vector operations needed? No `numpy`. One way to keep your programs fast and flexible is to have only the absolute essentials booted up when you load Python. Being bare-bones also means that whenever core Python developers put out a new version of Python, it's less likely to break something downstream for developers of libraries like `numpy` or `pandas`.

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
* Then go one extra location because the range is exclusive (end on index `4`).

This also harkens to some deep-rooted computer science history, going as far back as [BCPL](https://en.wikipedia.org/wiki/BCPL), a precursor to C. In any programming language, **a variable is just some text that points to an address in the computer's memory.** So when we say `x = 5` in R or Python, we are:
1. setting aside some space in the computer's memory,
2. filling that space with machine code for `5`,
3. and then _pointing_ the text `x` towards that space in memory.

Then, whenever you type `x`, R or Python actually see a pointer that _points towards the location in memory with `5` in it_.

**A vector in R or list in Python is just a sequence of pointers to different addresses in memory.** In C, these regions are right next to one another. When you define a variable in C, you have to tell C how much memory that variable requires, so C can find a contiguous block of memory big enough to hold that variable. Then, because all of the components of the array are right next to each other, the pointer to the array actually just needs to point to the _start_ of the array, plus remember how long the array is.

For example, let's say you have a string called `"hello"`. C treats this as an array of characters. If you assign `"hello"` to the variable `message`, `message` is really just a pointer to the first letter of the `"hello"`, plus the length of the string. You can see this below<sup>[[1]](#footnotes)</sup>: `*message` and `*(message+0)` are identical. (`*` accesses the value the pointer is pointing to.)

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

In Python, despite the fact that the pointers in an iterable can point to addresses in memory that aren't next to one another, we still index the elements of an array as if they were indeed sitting next to each other. This zero-indexing is the norm for many languages, e.g. Java, JavaScript, Go, PHP, Ruby, Swift... but there are notable exceptions, like MATLAB, Julia, and of course R.

## Variables can be linked!
Whenever you create two variables, you have two independent variables, right? In the physical world, even identical twins are separate entities living independent lives. Well, that may be the case in the real world and in R, but it's not always the case in Python.

```python
# Python
a = 'Hello'
b = a
a = 'Hi'

print(a)  # 'Hi'
print(b)  # 'Hello'
```
So far so good, right? This makes sense - we set `a` to `'Hello'`, set `b` to `a` so it's also `'Hello'`, change `a` to `'Hi'`, and `b` stays the same. Great.

But what happens if `a` is a list?

```python
# Python
a = [1, 2]
b = a

a.append(3)

print(a)  # [1, 2, 3]
print(b)  # [1, 2, 3]   <- O_O
```

*Cue hours of confusion that don't end even after you find the bug.*

So to understand what's going on here, we have to go [back to pointers](#zero-indexing). Certain data types in Python are **_mutable_**, meaning the contents of a variable of that type can change without needing to redefine the variable. This is what happens when you do `.append` to a list, or `.update` to a dictionary - you don't need to do `my_list = my_list.append(5)`; you just do `my_list.append(5)` and the list is updated.<sup>[[2]](#footnotes)</sup>

In contrast, other data types are **_immutable_**, meaning your variable needs to point to a totally different location in memory when it's updated. This is the case with the strings in the first code block: strings in Python are immutable, so when `a` is changed to `'Hi'`, it stops pointing to the location in memory for `'Hello'`.

You can see this more clearly if you ask Python to show you the memory address for objects as you update them. We can do this with the `id` function.

```python
# Python
a = 'Hello'
b = a

print(id(a))   # 140530884633008
print(id(b))   # 140530884633008

a = 'Hi'

print(id(a))   # 140530913364592   <- changed
print(id(b))   # 140530884633008   <- didn't change

##############################################
a = [1, 2]
b = a

print(id(a))   # 140530885072448
print(id(b))   # 140530885072448

a.append(3)

print(id(a))   # 140530885072448   <- didn't change
print(id(b))   # 140530885072448   <- didn't change
```

With mutable data types, you need to be really careful if multiple variables are pointing to the same location in memory. In line 15 above, `b` is **NOT** being set to a unique copy of `[1, 2]`... it's being set to the same list that `a` is pointing to! That means that whenever `a` makes a change to that list, you'll see the change reflected in `b`, too.

One solution to this is to use the `.copy` method Python provides for mutable data types.

```python
# Python
a = [1, 2]
b = a.copy()   # <- sets aside new memory for b

print(id(a))   # 140530913380224
print(id(b))   # 140530912645440   <- different

a.append(3)

print(a)  # [1, 2, 3]
print(b)  # [1, 2]
```

So why on earth would we allow any language to have linked variables? Well, it's far more memory-efficient to only create new variables when needed. If you're updating a list with the contents of a long `for` loop, you don't want to create a new list with the contents of the entire previous list on every iteration; you just want to update the list you currently have.

(This is actually a major performance tip for beginner R users: never have a `for` loop with something like `vector <- c(vector, new_value)`! It's much better to pre-allocate a vector of NaNs as long as your loop, then fill in each index of the vector as the loop progresses.)

There are also some times when we actually may want to update multiple variables simultaneously. Let's imagine we have some video game where a diamond, ruby, and sapphire are buried in different locations on a virtual island. To find the treasure, we have instances of a `TreasureFinder` class that search the island. The bots follow different rules for finding the different gems: sapphires tend to be by water, while volcanoes often hide rubies. If the sapphire is found, for example, we should stop searching the island coast. If we have multiple instances of `TreasureFinder`, whenever one instance finds a gem, it can alert all instances of `TreasureFinder` to stop searching for that gem. To do this, we'd use a class method that updates a shared list.

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
Having now spent a few years coding in both R and Python, I've gotten a better picture of their pros and cons when it comes to analytics and data science. If you're only doing analytics, it's hard to beat R's simplicity. If you don't have a programming background, it's much easier to start analyzing data with R than with Python. For fields like ecology and political science, R also tends to be the standard language to use, meaning you can find plenty of support for how exactly to carry out some analysis. Finally, when it comes to complex stats, R is still my go-to language. For [Sosna et al. 2019](https://www.pnas.org/content/pnas/early/2019/09/17/1905585116.full.pdf), I used R to carry out L1-penalized logistic regression with nested random effects. There are plenty of packages in R that can deal with random effects, but seemingly none in Python.

If the output you create isn't a report (as a dashboard, report, visualization, etc.), though, Python is a better bet.



## Footnotes
[1.](#zero-indexing) If you have a Mac, you can easily run C code yourself. Save the code in a file called e.g. `hello.c`, then in Terminal, navigate to the directory, type `cc hello.c -o hello` to compile the program, then type `./hello`.

[2.](#variables-can-be-linked) There are a few ways you can accidentally avoid updating `b` when `a` updates, making the variable linking even harder to catch:
```python
a = [1, 2, 3]

# Option 1: create a new list for b, with same elements of a
b1 = list(a)
print(b1 is a)   # False

# Option 2: break the link by not using .append to update a
b2 = a
a = a + [4]      # Creates new list for a
print(b2 is a)   # False
```
