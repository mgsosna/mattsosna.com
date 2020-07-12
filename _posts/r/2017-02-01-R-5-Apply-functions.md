---
layout: post
title: Learning R <br> 5. The apply functions
author: matt_sosna
---
We've reached the point in learning R where we can now afford to focus on efficiency over "whatever works." A prime example of this is the `apply` functions, which are powerful tools to quickly analyze data. The functions can find slices of data frames, matrices, or lists and rapidly perform calculations on them. These functions make it simple to perform analyses like finding the variance of all rows of a matrix, or calculating the mean of all individuals that meet conditions X, Y, and Z in your data, or to feed each element of a vector into a complex equation. With these functions in hand, you will have the tools to move beyond introductory knowledge of R and into more specialized or advanced analyses.

*[An obligatory comment before we get started: I initially framed this post as a counter to how slow for loops are, but to my surprise, for loops were actually consistently faster than apply. The catch is that the for loop has to be written well, i.e. with pre-allocated space and avoiding overwriting variables on every iteration. I'll go into detail on this in the next series of R posts: "Random R." Stay tuned.]*

**This is the fifth in a series of posts on R. This post covers:**
- `apply`, `sapply`, `lapply`, `tapply` (pronounced "apply," "s-apply," "l-apply," and "t-apply")
- `sweep`

**Previous posts included:**
1. [An introduction to R]({{ site.baseurl }}/R-1-Intro/)
2. Using R to understand [distributions, plotting, and linear regression]({{ site.baseurl }}/R-2-Plotting/)
3. [For loops and random walks]({{ site.baseurl }}/R-3-For-loops)
4. [Functions and if statements]({{ site.baseurl }}/R-4-Functions)

The most important code from those posts is shown below:

```r
c()             # Concatenate
x <- c(5, 10)   # x is now a two-element vector
x[x > 7]        # Subset the values of x that are greater than 7

# Assign to the object "data" 100 randomly-drawn values from a normal
# distribution with mean zero and standard deviation 1
data <- rnorm(100)   

# Plot a histogram of the "data" object
hist(data)           

# Assign to the object "y" 100 randomly-drawn values from a uniform
# distribution with minimum zero and maximum 1
y <- runif(100)

# Make a scatterplot of y as a function of data
plot(y ~ data)                 

for(i in 1:length(x)){    # For i in the sequence 1 to the length of x...
   print(i)               # ...print i
}

# Create our own mean function
our.mean <- function(x){sum(x) / length(x)}

# Print the statement "Yup, less than 5" if 1 + 1 < 5 is true
if(1 + 1 < 5){print("Yup, less than 5")}
```

# Apply
The simplest of the apply functions is the one the family is named after. Let's revisit the following plot from the [third R post on for loops]({{ site.baseurl }}/R-3-for-loops).

![]({{ site.baseurl }}/images/R-3-for-loops/random_multiple.png)

A random walk, if you remember, is a series of random steps. The walk can be in as many dimensions as you want; the ten walks shown above are in one dimension (where there's only one movement axis: here, it's up/down). It seems like the variance in the walks increases with time: the more you move to the right, the more spread out the walks are. How could we quantify this?

In case you missed it, here's how we generated the data up there. But this time, let's run 100 random walks instead of 10.

```r
start <- 0
mean.step <- 0
sd.step <- 1
n.steps <- 100000
n.walks <- 100             # The number of random walks you want to run

# Create an empty matrix that we'll fill with the random walk values
WALKS <- matrix(NA, nrow = n.walks, ncol = n.steps)

# Start all the walks at the origin
WALKS[, 1] <- start

# Perform the random walks
for(i in 2:n.steps){
    WALKS[, i] <- WALKS[, i-1] +        # Take the previous positions...
    rnorm(n.walks, mean.step, sd.step)  # ...and add a step to each one
}
```
*[Note: if you did `rnorm(1, ...)`, you would generate 100 identical random walks because the same value would be added to each walk. That's why we need to specify the number of random walks in the first argument in `rnorm`]*

We have a 100 x 100,000 matrix, where each row is a random walk and each column is a time step. To show how the variance of the walks changes over time, we want to take the variance of each column. One way to do this would be to create a for loop that iterates over each column. Below, WALKS is our matrix with the random walk data.

```r
walk.variance <- c()
for(i in 1:ncol(WALKS)){
   walk.variance[i] <- var(WALKS[, i])
   print(i)
}
```

This works, but there's a simpler way to do this. Let's use `apply`, which only requires one line of code.

```r
walk.variance <- apply(WALKS, 2, var)
```

`apply`'s inputs are the matrix, whether you want rows (`apply(..., 1, ...)`) or columns (`apply(..., 2, ...)`), and the function you want to apply to that dimension of the matrix, which for us is `var`.

*[Note: you can also do this for higher-dimensional arrays, e.g. a 3-dimensional "book" where you want to summarize each "page." That would be `apply(..., 3, ...)`]*

If we plot that out, we see a nice linear relationship between the variance and how long we've run the random walk.

![]({{ site.baseurl }}/images/R-5-apply/var-randomwalk.png)

You're also not limited in what function you run across each column or row (as long as the function can take a vector input). Using what we learned in [post 4 of our R series]({{ site.baseurl }}/R-4-functions), let's apply a more complicated function to each row of the matrix. This function will find the mean of the six highest values of each random walk, then subtract it from the range. No real reason why. Just flexing a little R muscle!

```r
# Find the mean of the six highest values of the input,
# then subtract it from the range
fun.times <- function(x){
    return(mean(head(x)) - (range(x)[2] - range(x)[1]))
}    

lots.of.fun <- apply(WALKS, 1, fun.times)
```

# sweep
`apply` is great for performing a calculation on each row or column of a matrix, but what if you want to, say, subtract _an entire vector_ across each column of a matrix? You don't just have one value that's getting subtracted by the whole matrix. You have a bunch of values, and the different rows/columns in the matrix get a different value applied to them. For this, you'll want `sweep`.

Here's a simple example that doesn't require `sweep`. You're subtracting one value from the entire matrix.

```r
WALKS.adjusted <- WALKS - mean(WALKS)
```

Here, the new object (`WALKS.adjusted`) has been centered around the mean of `WALKS`. This isn't incredibly informative, though, because the mean of `WALKS` condenses the information from all the random walks and all the time points of those walks into one value.

With `sweep`, we can be more nuanced. Let's create a new matrix, `WALKS.adjusted2`, where all of the walks are centered around the mean of all the random walks for that particular time point. Walks that are have particularly high values will have positive values, average walks will be around zero, and walks with low values will have negative values.

```r
WALKS.adjusted2 <- sweep(WALKS, 2, colMeans(WALKS), "-")
```

# sapply
`apply` works great on matrices, but it doesn't work if you want to perform a calculation on every element of a vector, or if you want to perform a calculation on only select columns of a matrix or data frame. `sapply` is the answer here.

First, a vector example. Say you have a list of probabilities, and you want to simulate outcomes based on those probabilities. You have 50 people, and they each have some probability of marathoning the eight _Harry Potter_ movies back to back in a massive sleepover party with two B-list celebrities of their choosing, friendly law enforcement officers, and young adult science fiction _Animorphs_ author K.A. Applegate in attendance.

```r
# 50 random values drawn from a uniform distribution between 0 and 1
probs <- runif(50, 0, 1)

# The possible outcomes
outcomes <- c("It's marathon time!",
              "Sorry, I actually already have plans...")

# A function that takes a probability of watching the movie and randomly
# chooses whether you see it or not based on your probability
choose_outcome <- function(x){sample(outcomes, 1, prob = c(x, 1-x))}

# The outcomes
sapply(probs, FUN = choose_outcome)
```

Note that the outcomes will differ a bit every time because you're dealing with *probabilities*, and so there's an element of randomness with who gets chosen. A probability of 0.5 will give a "marathoning" outcome 50% of the time and a "sorry" outcome the other half, for example.

Great. Now let's say that we're hosting our *Harry Potter* marathon. It's a great party, Halle Berry and Officer Chuck are enjoying the homemade marshmallow snacks, we're content. But a nagging thought persists: *could we use `sapply` to find the sums of the numeric columns of a data frame that's has columns with numbers, factors, and characters?*

When we Google those exact words, Google asks if we meant `lapply`, which makes us uncomfortable because we haven't gotten that far into this blog post yet. Fortunately, we _can_ use `sapply` to analyze solely the numeric columns.

As an ambitious high school student, we don't have any data to brag to K.A. Applegate about, so we'll just have to use a random number generator to create some.

```r
M <- data.frame(rnorm(20),   # A random variable: height change
rnorm(20,2),                 # A random variable: weight change
sort(rep(c("A","B"),10)),    # The treatment: A or B
rep(1:5, 4))                 # The trial number
colnames(M) <- c("height_change", "weight_change", "treatment", "trial")

# Tell R that the trial column is a category, not numbers
M$trial <- as.factor(M$trial)
```

If we try to use `apply(M, 2, sum)`, we'll get an error because not all of the columns are numeric. We can specify which columns we want with `sapply`.

```r
num.cols <- sapply(M, is.numeric)

sapply(which(num.cols == T), function(x){sum(M[, x])})
```

Alternatively, we could also get our result with `apply(M[1:2, ], 2, sum)`. If we tried just doing `sum(M[1:2, ])`, it would give us one value: the grand sum of all the values in all columns.

# tapply
While you can use `sapply` on data frames, `tapply` is a friendlier tool. Let's say we accidentally spilled salsa all over our phone when the tortilla chip broke mid-conversation with K.A. Applegate. We know we shouldn't have been using our phone as a plate, that was so silly, the creator of *Animorphs* who inspired millions, possibly billions of children and young adults to pursue biology and never give up against insurmountable odds is suddenly pretending she has to take an important call. Well, at least we still have R.

So here we are, salsa-drenched phone in hand. Let's say we want to conduct an experiment examining how difficult it is to read The Headbanging Behaviorist on phones slathered in different brands, spiciness, colors, and quantities of salsa. We measure difficulty reading in seconds required to quickly scroll through the blog post and then give a "Like" on Facebook. (Side note: it may be necessary to remove values of infinity from the data set.)

With `tapply`, we can cut up our data frame to look at just the effects of Tostitos at all quantities, or *just* "Very Hot" Green Mountain Gringo. We can apply summary statistics to see if there's an effect of red versus clear salsa when your phone is so buried in salsa the screen has gone black ( > 3.0 kg). As you'll see, `tapply` is fantastic for data frames because it can "read" characters within the data frame, as opposed to `apply` or `sapply` which can only look at the column or row level.

```r
# Generate the data by replicating the character inputs (rep)
# and then scrambling them (sample)
our.salsas <- sample(rep(c("Tostitos", "Green Mountain Gringo",
                           "Newman's Own", "Goya", "Old El Paso"), 200))
spiciness <- sample(rep(c("Mild", "Medium", "Hot", "Very Hot!"), 250))
colors <- sample(rep(c("Red", "Green", "Clear"), 250))
quantities <- sample(rep(c("0 - 1.0 kg", "1.0 - 2.0 kg",
                           "2.0 - 3.0 kg", "> 3.0 kg"), 250))  
time_to_read <- rpois(1000, 2)

the.data <- data.frame(our.salsas, spiciness, colors,
                       quantities, time_to_read)

# Convert every variable (except time_to_read) to factors
our.salsas <- as.factor(our.salsas)
spiciness <- as.factor(spiciness)
colors <- as.factor(colors)
quantities <- as.factor(quantities)
```

Now let's use `tapply` to find the mean time to read column as a function of the spiciness column.

```r
with(M, tapply(time_to_read, spiciness, mean))
```

To keep the code clean, I've used the `with` command. Otherwise, because `time_to_read` and spiciness aren't global variables (they're columns within the variable `M`); we'd have to write `the.data$time_to_read` and `the.data$spiciness` to call them. Just a bit cleaner this way.

The first argument in `tapply` is the numeric data column you're interested in. The second argument is how you want to cross-section those data, and the third argument is the calculation you're performing.

By editing the second argument a bit, we can have `tapply` provide us a more nuanced answer:

```r
with(M, tapply(time_to_read, list(spiciness, color_of_salsa), mean))
```

With the code above, we can see the mean time to read as a function of the spiciness and color of our salsa.

# lapply
The last function I'll mention is `lapply`. With `lapply`, you can perform a calculation on every object in a list. Lists are vectors containing objects that can be vectors themselves as well, or matrices, or character strings, etc. Here's an example of a list:

```r
opinions <- c("I loved it!", "It was ok...", "Nah.")
random_numbers <- rnorm(10)
the.matrix <- matrix(runif(100, 0, 1), ncol = 5, nrow = 10)

our.list <- list(opinions, random_numbers, the.matrix)
```

When you run our.list, you'll see the three objects, one after the other. If you had some function that could operate on the three objects in the list, you could use lapply on them. But I really think we need some closure on our *Harry Potter* viewing party, so let's go back there.

In an effort to get on the front page of [/r/dataisbeautiful](https://reddit.com/r/dataisbeautiful), we decide to collect some data at our party. Every 30 minutes, we poll the audience on how much fun they're having. (It'd be solid 10/10's throughout the night, but play along and imagine there's some variation.) With these data, we build a matrix where each row is a party participant and each column is a time point (3:10am, 3:20am, etc.). The data are how much fun person `i` is having at time point `j`.

```r
have.fun <- matrix(round(runif(5000, 0, 10)), ncol = 100, nrow = 50)
```

What if we want to know what moments each person was having at least 9/10 fun?  We could just write `which(have.fun > 9)`, but that would convert `have.fun` into a vector and then give us the indices of the vector where the value is greater than 9. So for our 100 x 50 matrix, we'd get answers like "9" and "738" and "2111," which don't have any identifying information on who was happy when.

This sounds like a job for apply, so we run this:

```r
passed.threshold <- apply(have.fun, 1, function(x){which(x > 9)})
```

We now have a list, where each object is a person, and the values are the time points at which they scored at least a 9/10 on having fun. However, we can now use `lapply` to get more nuanced information from `passed.threshold`.

```r
# Find the first time point that passed the threshold
lapply(passed.threshold, min)

# Get a summary of the time points for each person that
# passed the threshold
lapply(passed.threshold, summary)   
```

Note that these commands return their contents as a list. If you'd prefer they were returned as a vector, we can use `sapply` instead.

```r
sapply(passed.threshold, min)  
```

# Conclusions
Thanks for reading the "Introduction to R" series! Next up will be "Random R," where I'll take on random projects (like quantifying the computation time of for loops versus apply). Stay tuned.

Cheers, <br>
-Matt
