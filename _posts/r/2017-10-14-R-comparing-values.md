---
layout: post
title: How to be fancy with comparisons
author: matt_sosna
---
Welcome to another episode of "Random R," where we'll ask random programming and statistical questions and answer them with R. Today, for whatever reason, let's say we want to dive into methods for comparing values. We'll start simple (e.g. is 5 greater than 4? Read on to find out.) and then work our way towards trickier element-wise comparisons among multiple matrices.

## Comparing scalars
Let's say we have two variables, and we want to see which one is larger. The variables are called scalars because they're just one value each. We can use either the `max` function or `ifelse`.

```r
# Create the variables
a <- 5
b <- 4

# Method 1: max
max(a, b)

# Method 2: ifelse
ifelse(a > b, yes = a, no = b)
```

The above code is pretty straightforward. `max(a, b)` finds the maximum value in the arguments `a` and `b`. `ifelse` reads like this: "Is a greater than b? If yes, return a. If no, return b."

Note that `ifelse` gives us more flexibility because we can specify what happens when the logical statement a > b is either true or false. The below code is a small modification that gives us the identity of the variable that's larger, instead of the value of that variable.

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

Now we can find the max and ask which position in our vector corresponds to that maximum value. Because our variables are just named after sequential letters in the alphabet, we can just index the built-in `letters` variable. (If your variables had other names, like `location1`, `location2`, etc., you'd need to have a separate vector of names that you'd then index.)

```r
# Find the maximum and its position(s) in the vector
max(data)
which(data == max(data))

# Instead of the vector index, how about the variable name?
letters[which(data == max(data)]
```

So far, we've just been comparing scalars to each other. We ended by combining multiple scalars into a vector and then finding the max of that vector. But what if we have multiple vectors?

If we want to still just find the single maximum value among whatever we feed into the max function, we'll do exactly what we did before.

```r
# Create the variables (letting R generate random numbers)
vector1 <- runif(n = 10, min = 0, max = 100)
vector2 <- runif(n = 10, min = 0, max = 100)
vector3 <- runif(n = 10, min = 0, max = 100)

# What's the maximum value out of those 30 values?
max(vector1, vector2, vector3)
```

But let's say that instead of wanting to find the single maximum value, we want to compare each element of the vectors to each other and keep the largest value. So we want to look at the first element of `vector1`, `vector2`, and `vector3` and keep the biggest one, then compare their second elements and keep the largest one, then do the same for the third, etc. For this, we'll need to use the `pmax` function, which finds the **parallel maxima** of the vector inputs it receives. Basically, it performs the `max` function for each element of the set of vectors you give it.

```r
# Find the parallel maxima of our vectors
pmax(vector1, vector2, vector3)
```

The output of `pmax` is another vector, this one consisting of the parallel maxima of each element in `vector1`, `vector2`, and `vector3`.

As a final example, we can extend this thinking from vectors to matrices and still use `pmax`.

```r
# Create the matrices
matrix1 <- matrix(rnorm(n = 100), ncol = 10))
matrix2 <- matrix(rnorm(n = 100), ncol = 10))
matrix3 <- matrix(rnorm(n = 100), ncol = 10))

# Make a new matrix with the parallel maxima of the three inputs
new.matrix <- pmax(matrix1, matrix2, matrix3)

# Look at a subset of each matrix and confirm it worked
matrix1[1:3, 1:3]
matrix2[1:3, 1:3]
matrix3[1:3, 1:3]
new.matrix[1:3, 1:3]
```

## Comparing vectors and matrices to a constant
So far, we've been comparing scalars, vectors, and matrices to each other. But what if we have some external value, and we want to keep the values that are closest to it?

For this, we'll return to `ifelse`. Our external value will be zero. To keep things simple, we'll compare two vectors and find the distances that their elements are from zero.

```r
# Create the vectors
A <- rnorm(n = 10, mean = 5, sd = 1)
B <- rnorm(n = 10, mean = 5, sd = 2)

# Make a new vector with the elements of A and B closest to zero
C <- ifelse(abs(0 - A) < abs(0 - B), yes = A, no = B)

# Check to make sure it worked
A
B
C
```

The nice thing with `ifelse` is that it's a concise function for when you have one of two possible outcomes. The story gets more complicated if we want to compare more than two vectors.

```r
# Create the three variables
A <- rnorm(4)
B <- rnorm(4)
C <- rnorm(4)

# Run the nested if statements
if( abs(0 - A) < abs(0 - B) &
    abs(0 - A) < abs(0 - C)){D <- A} else
    if( abs(0 - B) < abs(0 - A) &
        abs(0 - B) < abs(0 - C)){D <- B} else
        {D <- C}

# Compare the vectors to confirm it worked
A
B
C
D
```

## Comparing vectors and matrices to a vector or matrix
For our final comparison, let's say that instead of some constant, e.g. zero, we have a whole set of numbers that we want to compare our vectors or matrices to. The `ifelse` line is identical for vectors and matrices, so let's use matrices to be fancy.

```r
# Create our matrices
A <- matrix(rnorm(100), ncol = 10)
B <- matrix(rnorm(100), ncol = 10)

# Create the reference matrix
C <- matrix(rnorm(100), ncol = 10)

# Make a new matrix with the elements of A and B closest to C
D <- ifelse(abs(C - A) < abs(C - B), yes = A, no = B)

# Check on a subset of the matrices to confirm it worked
A[1:3, 1:3]
B[1:3, 1:3]
C[1:3, 1:3]
D[1:3, 1:3]
```

Last example, and it's a weird one. Let's say that instead of comparing vectors to vectors or matrices to matrices, we want to compare a vector and a matrix. We'll return to `pmax` to keep things simple and just ask which values are larger. With a bit of careful arranging, we can treat a matrix as a set of vectors arranged one after the other, and then we can just let `pmax` do its thing.

```r
# Create the variables
our.vec <- runif(n = 5, min = 0, max = 10)
our.mat <- matrix(rnorm(10, mean = 5), nrow = length(our.vec))

# Visualize them
our.vec
our.mat

# Find the larger value
pmax(our.vec, our.mat)
```

_[Some clarification for the code above, because it's actually pretty easy to make a mistake here. It's important that the matrix is arranged so the number of rows is the same as the length of the vector, because **R makes comparisons down each column, not across each row, when it compares a matrix to a vector.** In other words, R will compare `our.vec[1]` to `our.mat[1,1]`, then `our.vec[2]` to `our.mat[2,1]`, then `our.vec[3]` to `our.mat[3,1]`, etc. So even if `our.mat` was arranged so the number of columns was equal to the length of `our.vec`, R would still run down the rows and wrap along the columns, which is most likely not what you're trying to do. Just a heads up.]_

Thanks for reading, and shoot me a message if you have any ideas for a fun Random R project.

Best, <br>
Matt
