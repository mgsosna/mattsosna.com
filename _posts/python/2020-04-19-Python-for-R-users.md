---
layout: post
title: Python for R users
---

My first programming language was R. I fell in love with the nuance R granted for visualizing data, and how with a little practice it was straightforward to pull off complex statistical analyses. I coded in R throughout my Ph.D., but the team I joined in my first job outside of academia solely coded in Python. Picking up a second language went much faster than the first, but there was a lot to get used to when I transitioned. I've compiled some of the major differences in this post. The two main takeaways are that:
* Python is a diverse language that is becoming increasingly popular for data analysis/science
* R is a language for stats that is now diversifying


# The `.` suddenly has significance
In R, you can treat the `.` like any other character. This means that `our_test` and `our.test` are both valid names for variables.

```r
# R
our_test <- 1
our.test <- 2
```

In Python, though, the `.` has special significance. The reason for this touches upon a major difference in how code in R and Python is organized: the prevalence of **classes.**

When we type `our.test`, we're telling Python we want _the attribute `test` of the object `our`._ This is because everything in Python is an object, whose _attributes_ are accessed with the `.` operator. Objects are instances of _classes_, which are basically _templates_ of code. A simple example will make this clearer:

```python
# Python
class Student:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print("Hi")

me = Student('Matt')
print(me.name)   # 'Matt'
me.say_hi()      # 'Hi'
```
Here, we have a class called `Student`. We create an instance of the class, `me`, that is initialized with a name `'Matt'`. `'Matt'` gets assigned to `.name` attribute of `me`. Our class also has a function that prints "Hi," which we access with `me.say_hi()`.

Because the `.` is used to access properties of an object, it can't be used as part of a variable name.

While everything in R [is also technically an object](https://stackoverflow.com/questions/34376318/whats-the-real-meaning-about-everything-that-exists-is-an-object-in-r), and there are [multiple ways to create classes](https://study.com/academy/lesson/classes-in-r-programming-definition-examples.html) with attributes and methods, I've personally never encountered R code that uses custom-created classes. Sure, there are plenty of online resources for _learning how to use these classes_, most notably [Hadley Wickham's _Advanced R_ textbook](https://adv-r.hadley.nz/). But actually seeing them in action? Nope. To be transparent, maybe it's me: the R code I've read was either from 1) me, 2) an academic collaborator sharing their analyses, or 3) data science-focused online classes and blog posts. Maybe R classes are a bigger deal in the workflows of large collaborative teams, or in industries I don't have much exposure to. (I've found surprisingly little from searching on Google for who these teams or what these industries could be, though.)

Regardless, the absence of classes is in sharp contrast to Python, where classes are an early part of learning how to organize your code. I talk about this in [Part 4]({{ site.baseurl }}/Python-4-Organizing-code) of the "Learning Python" track.

##



You can create a library in R that is a set of functions. When you import the library, all the functions are imported at once. In Python, in contrast, you can import specific _classes_ from a library, which have functions that belong to them.

While R _does_ have classes, in my experience they're nowhere near as central to a data analyst or data scientist's workflow as classes are in Python.

## Where are all the built-in functions?
One surprise with coming from R is that the first thing I need to do when I start an analysis in Python is import at least four or five libraries. Want to work with dataframes? Need to import `pandas`. Want to work with arrays? Need `numpy`. Visualizations? `matplotlib`. Literally changing the working directory? Boot up `os`. Machine learning models? `sklearn`. I couldn't believe how bare-bones base Python was. What's actually there when you first boot up Python?

It took some learning about the broader programming context Python comes from for me to understand what's up with this approach. Python by design is meant to be extremely slim. Your program doesn't need to change the directory? The `os` functions aren't taking up memory. No vector operations needed? No `numpy`. One way to keep your programs fast and flexible is to have only the absolute essentials booted up when you load Python.  

## Zero-indexing
Something that drove me absolutely crazy when switching to Python was dealing with its zero-indexing. R is 1-indexed, _the way that normal people think_. (I'm still bitter!) To explain, let's say you have a vector of numbers called `vector`, and you want to access the **2nd through 4th elements.** In R, this couldn't be easier:
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
* Skip the first element (`0`)
* Count the second, third, and fourth elements (`1`, `2`, and `3`)
* Then go one extra location because the range is exclusive (end on element `4`).

This also harkens to Python's programming routes. This is the way it's done in C and other languages.

## You have to run blocks of code all at once
Coming from RStudio, it was weird to think about needing to run entire blocks of code at once. I would always just run an analysis one line at a time, with lots of inspection to make sure I was doing what I thought I was doing.

* Ways to get around it: Jupyter, Spyder


## There isn't an easy all-in-one solution except maybe Anaconda
In R, you download R and RStudio, and then you're done. From there, you can do pretty much everything from the comfort of RStudio: install and update packages, produce visuals, create Markdown files that export to PDF, etc.

Python is so broad.

* Package management...

## Variables can be linked!
```python
a = [1, 2]
b = a

a.append(3)
print(a)  # [1, 2, 3]
print(b)  # [1, 2, 3]
```
