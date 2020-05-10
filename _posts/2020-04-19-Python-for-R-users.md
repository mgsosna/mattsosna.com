---
layout: post
title: Python for R users
---

My first programming language was R. I fell in love with the nuance R granted for visualizing data, and how with a little practice it was straightforward to pull off complex statistical analyses. I coded in R throughout my Ph.D., but the team I joined in my first job outside of academia solely coded in Python. Picking up a second language went much faster than the first, but there was a lot to get used to when I transitioned. I've compiled some of the major differences in this post. The two main takeaways are that:
* Python is a diverse language that is becoming increasingly popular for data analysis/science
* R is a language for stats that is now diversifying


## The `.` suddenly has significance
In R, you can treat the `.` like any other character. This means that `our_test` and `our.test` are both valid names for variables.

```r
our_test <- 1
our.test <- 2
```

In Python, though, the `.` has special significance. When we say `our.test`, we're telling Python we want _the function `test` of the object `our`._ This is because everything in Python is an object, which can have properties (attributes and functions (called "methods" when they belong to an object)). Everything in R is also an object, but we don't think of R objects quite the same way we do as Python objects.

In any programming language, as the amount of code grows, you need to start organizing it all. The typical levels of organization are as follows:
1. **No organization** <br>
Just individual scripts that exist in a vacuum, performing simple commands in sequence. <br><br>
2. **Functions** <br>
Place code you're using multiple times into functions, then just call the functions. <br><br>
3. **Classes** <br>
Group similar functions into classes. Import classes as a whole into different files, e.g. a "temperature converter" class with methods for Fahrenheit -> Celsius, Celsius -> Fahrenheit, Celsius -> Kelvin, etc. <br><br>
4. **Modules** <br>
Group similar classes into modules that can be imported as a whole.

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
