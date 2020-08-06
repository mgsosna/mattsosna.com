---
layout: post
title: How to be fancy with comparisons in R
author: matt_sosna
---
Welcome to another episode of "Random R," where we'll ask random programming and statistical questions and answer them with R. Today, for whatever reason, let's say we want to dive into methods for comparing values. We'll start simple (e.g. is 5 greater than 4? Read on to find out.) and then work our way towards trickier element-wise comparisons among multiple matrices.

## Comparing scalars
Let's say we have two **scalars**, which means they each hold only one value (as opposed to a vector or matrix), and we want to see which one is larger. We can use either the `max` function or `ifelse`.

```r
# Create the variables
a <- 5
b <- 4

# Method 1: max
max(a, b)   # 5

# Method 2: ifelse
ifelse(a > b, yes = a, no = b)  # 5
```

The above code is pretty straightforward. `max(a, b)` finds the maximum value in the arguments `a` and `b`. `ifelse` reads like this: "Is a greater than b? If yes, return a. If no, return b."

Note that `ifelse` gives us more flexibility because we can specify what happens when the logical statement `a > b` is either true or false. The below code is a small modification that prints a string of the name of the larger variable, instead of the value of that variable.<sup>[[1]](#footnotes)</sup>

```r
# Return the identity of the larger variable
ifelse(a > b, yes = "a", no = "b")
```

While `ifelse` has this nice flexibility here, `max` excels when you have more than two variables (and for some reason you're determined to keep them all separate variables and not combine them into a vector, matrix or list... more on that later). Say that instead of just `a` and `b`, for example, we have a whole bunch of variables we want to find the maximum for.

```r
# Find the maximum among 5 variables
a <- 5 ; b <- 4 ; c <- 10 ; d <- 8 ; e <- 10
max(a, b, c, d, e)
```

The above code lets us find the maximum of the five separate scalars, but identifying which scalar(s) is the maximum would be a nightmare. (We'd probably need to use nested `if` statements, where it's easy to make a logical or grammatical mistake, for all the comparisons. Later on we use nested `if` statements for just three variables and it already starts getting lengthy.) Let's try a different approach.

## Comparing vectors and matrices
Finding the identity of the max value above when we're determined to keep the data as separate scalars is needlessly confusing and giving me a headache... it's much simpler if we let R know that these variables are related somehow (e.g. they're all height measurements, or time increments, or number of people moshing at a random moment in a metal show, etc.). We can do that by combining them into a vector. The elements of the vector are our variables.

```r
# Combine the 5 variables into a vector called "data"
a <- 5 ; b <- 4 ; c <- 10 ; d <- 8 ; e <- 10
data <- c(a, b, c, d, e)
```

Now we can find the max and ask which position in our vector corresponds to that maximum value. Because our variables are just named after sequential letters in the alphabet, we can just index the built-in `letters` variable. (If your variables had other names, like `location1`, `location2`, etc., you'd need to define a separate vector of names that you'd then index.)

```r
# Find the maximum and its position(s) in the vector
max(data)  # 10
which(data == max(data))  # 3 5

# Instead of the vector index, how about the variable name?
letters[which(data == max(data))]  # "c" "e"
```

So far, we've just been comparing scalars to each other. Our last step involved combining multiple scalars into a vector and then finding the max of that vector. But what if we have multiple vectors?

If we want to still just find the single maximum value among whatever we feed into the max function, we'll do exactly what we did before.

```r
# Create the variables (letting R generate random numbers)
vector1 <- runif(n = 10, min = 0, max = 100)
vector2 <- runif(n = 10, min = 0, max = 100)
vector3 <- runif(n = 10, min = 0, max = 100)

# What's the maximum value out of those 10 values?
max(vector1, vector2, vector3)   # 99.78804
```

But let's say that instead of wanting to find the _**single maximum value**_, we want to compare _**each element of the vectors**_ to each other and keep the largest value. So we want to look at the first element of `vector1`, `vector2`, and `vector3` and keep the biggest one, then compare their second elements and keep the largest one, then do the same for the third, etc. For this, we'll need to use the `pmax` function, which finds the **parallel maxima** of the vector inputs it receives. Basically, it performs the `max` function for each element of the set of vectors you give it.

```r
# Find the parallel maxima of our vectors
pmax(vector1, vector2, vector3)  # 99.78804 84.98018 48.77183...
```

The output of `pmax` is another vector, this one consisting of the largest value at each index in `vector1`, `vector2`, and `vector3`.

As a final example, we can extend this thinking from vectors to matrices and still use `pmax`.

```r
# Create the matrices
m1 <- round(matrix(rnorm(n = 100), ncol = 10), 1)
m2 <- round(matrix(rnorm(n = 100), ncol = 10), 1)
m3 <- round(matrix(rnorm(n = 100), ncol = 10), 1)

# Make a new matrix with the parallel maxima of the three inputs
max_m <- pmax(m1, m2, m3)

# View subsets of the matrices
m1[1:2, 1:2]
#      [,1] [,2]
# [1,]  0.0  0.8
# [2,] -1.4  1.2

m2[1:2, 1:2]
#      [,1] [,2]
# [1,] -0.2  1.7
# [2,] -0.8  0.5

m3[1:2, 1:2]
#      [,1] [,2]
# [1,]  0.4  0.6
# [2,]  0.9 -0.2

# View the parallel maxima
max_m[1:2, 1:2]
#      [,1] [,2]
# [1,]  0.4  1.7     # m3 m2
# [2,]  0.9  1.2     # m3 m1
```

## Comparing vectors and matrices to a constant
So far, we've compared scalars, vectors, and matrices to each other. But what if we have some *external value*, and we want to keep the values that are closest to it?

For this, we'll return to `ifelse`. Our external value will be zero. (For a different value, replace `abs(v1)` and `abs(v2)` with `abs(other_value - v1)` and `abs(other_value - v2)` below.) To keep things simple, we'll compare two vectors and find the distances that their elements are from zero.

```r
# Create the vectors
v1 <- round(rnorm(n = 10, mean = 5, sd = 1), 1)
v2 <- round(rnorm(n = 10, mean = 5, sd = 2), 1)

# Make a new vector with the elements of v1 and v2 closest to zero
new_v <- ifelse(abs(v1) < abs(v2), yes = v1, no = v2)

# Visualize vectors
v1     # 7.6 4.2 5.6 ...
v2     # 6.6 7.4 7.3 ...
new_v  # 6.6 4.2 5.6 ...  v2 v1 v1 ...
```

The nice thing with `ifelse` is that it's a concise function for when you have one of two possible outcomes. The story gets more complicated if we want to compare more than two vectors: our "no" criterion for the `ifelse` becomes _**another**_ `ifelse` that evaluates the next vector.

```r
# Generate three vectors
v1 <- round(rnorm(3), 1)
v2 <- round(rnorm(3), 1)
v3 <- round(rnorm(3), 1)

n <- 4
v1 <- round(rnorm(n), 1)
v2 <- round(rnorm(n), 1)
v3 <- round(rnorm(n), 1)

ifelse(abs(v1) < abs(v2) & abs(v1) < abs(v3), v1,
       ifelse(abs(v2) < abs(v1) & abs(v2) < abs(v3), v2,
              v3))

# Compare the vectors
v1     #  1.1 -0.3  0.2  1.1
v2     # -0.9  0.4  0.1  0.7
v3     #  0.6 -2.3  0.9  1.2
new_v  #  0.6 -0.3  0.1  0.7   v3 v1 v2 v2
```

## Comparing vectors and matrices to a vector or matrix
For our final comparison, let's say that instead of some constant, e.g. zero, we have a whole set of numbers that we want to compare our vectors or matrices to. The `ifelse` line is identical for vectors and matrices, so let's use matrices to be fancy.

```r
# Create our matrices
m1 <- round(matrix(rnorm(100), ncol = 10), 1)
m2 <- round(matrix(rnorm(100), ncol = 10), 1)

# Create the reference matrix
ref_m <- round(matrix(rnorm(100), ncol = 10), 1)

# Make a new matrix with the elements of A and B closest to C
new_m <- ifelse(abs(ref_m - m1) < abs(ref_m - m2), yes = m1, no = m2)

# View original matrices
m1[1:2, 1:2]
#      [,1] [,2]
# [1,]  0.1  0.3
# [2,] -0.7  0.6

m2[1:2, 1:2]
#      [,1] [,2]
# [1,]  1.9 -0.3
# [2,] -0.7  2.0

# View reference matrix
ref_m[1:2, 1:2]
#      [,1] [,2]
# [1,]  0.6  1.0
# [2,] -0.3 -1.2

# View new matrix
new_m[1:2, 1:2]
#      [,1] [,2]
# [1,]  0.1  0.3    m1  m1
# [2,] -0.7  0.6    m2  m1
```

Last example, and it's a weird one. Let's say that instead of comparing vectors to vectors or matrices to matrices, we want to compare a vector and a matrix. We'll return to `pmax` to keep things simple and just ask which values are larger. With a bit of careful arranging, we can treat a matrix as a set of vectors arranged one after the other, and then we can just let `pmax` do its thing.

```r
# Create the variables
vec <- round(runif(n = 3, min = 0, max = 10), 1)
mat <- round(matrix(rnorm(6, mean = 5), nrow = length(vec)), 1)

# Visualize them
vec   # 5.7 0.5 9.3
mat
#      [,1] [,2]
# [1,]  4.7  8.2
# [2,]  4.0  4.8
# [3,]  5.4  5.0

# Find the larger value
pmax(vec, mat)  # 5.7 4.0 9.3 8.2 4.8 9.3
```
`pmax` compares `vec` to each column in `mat`, doing an element-wise comparison and returning the larger element. `pmax`'s first three values (5.7, 4.0, 9.3) come from:
1. `vec[1]`, which is larger than `mat[1,1]`
2. `mat[2,1]`, which is larger than `vec[2]`
3. `vec[3]`, which is larger than `mat[3,1]`.

For the second half of the vector (8.2, 4.8, 9.3), `pmax` returns:
1. `mat[1,2]`, which is larger than `vec[1]`
2. `mat[2,2]`, which is larger than `vec[2]`
3. `vec[3]`, which is larger than `vec[3,2]`

Note **R makes comparisons down each column, _not across each row_, when it compares a matrix to a vector.** In other words, R compares `vec[1]` to `mat[1,1]`, then `vec[2]` to `mat[2,1]`, then `vec[3]` to `mat[3,1]`, etc. So even if `our_mat` was arranged so the number of columns was equal to the length of `vec`, R would still run down the rows _and wrap along the columns_, which is most likely not what you're trying to do. This is why **it's incredibly important to visualize these sorts of comparisons with toy examples,** where you can easily verify that you're making the correct comparison, before unleashing your analysis on real data.

Thanks for reading, and shoot me a message if you have any ideas for a fun Random R project.

Best, <br>
Matt

## Footnotes
1. [[Scalars]](#scalars) [In contrast to Python]({{ site.baseurl }}/R-to-Python/#variables-can-be-linked), virtually all objects in R have unique addresses in memory, so we can be fancy with our `ifelse` like so:
    ```r
    ifelse(a > b,
        deparse(substitute(a)),
        deparse(substitute(b)))
    # 'a'
    ```
Check out [the footnotes in this blog post]({{ site.baseurl }}/R-to-Python/#footnotes) for an interesting comparison of R and Python on the relationship between variables and addresses in memory.
