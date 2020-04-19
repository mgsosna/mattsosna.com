---
layout: post
title: Learning R - 4. Functions and if statements
---
A critical step in growing up is learning to think for yourself. With so much conflicting information available from polarized media outlets, non-interacting academic schools of thought, and corporations with various shades of biased self-interest, the definition of the "right thing to do" or the "truth" is rarely clear or may not even objectively exist. Being able to think critically and independently is therefore a crucial skill to develop for academia, industry, and yourself.

Anyway, in this post you'll follow along with my code and let me do the thinking for you, as we put off being a free thinker for another day. But in a baby step towards independent thought, in this post you'll learn how to create your own functions and if statements, as opposed to relying on code that someone in the past already wrote for you. So let's get started with reading code that someone in the past already wrote for you. ;-)

**This is the fourth in a series of posts on R. This post covers:**
- Creating your own functions
- If statements
- *(Briefly: logical operators)*
- Integrating functions and if statements into for loops

Previous posts included 1) [an introduction to R](https://mgsosna.github.io/R-1-Intro/), 2) using R to understand distributions, plotting, and linear regression; and 3) for loops and random walks. The most important code from those posts is shown below.

```r
c()            # Concatenate
x <- c(5, 10)  # Assign the vector (5, 10) to the variable "x"
x[x > 7]       # Subset the values of x that are greater than 7

# Assign 100 randomly-drawn values from a normal distribution with
# mean=0 and sd=1 to the object "data"
data <- rnorm(100)   

# Plot a histogram of the data
hist(data)           

# Assign 100 randomly-drawn values from a uniform distribution with
# minimum=0 and maximum=1 to the object "y"
y <- runif(100)       

# Make scatterplot of the variable "y" as a function of "data"
plot(y ~ data)       

# For "i" in the sequence "1 to the length of x", print "i"
for(i in 1:length(x)){  
  print(i)                
}
```

# Creating functions
A function is basically a box with some machinery inside. You give a function an input, the box rumbles around for a bit, and then it returns an output. Here's an example of a simple function:

$f(x) = x + 1$

Here, f(x) is the output and x is the input. If your input was 5, the function would look like this:

$f(x) = x + 1$
$f(5) = 5 + 1$
$f(5) = 6$

In R, we can give this function a name and then call on it later.

```r
add_one <- function(x){x + 1}
```

`add_one` is the name of our function. `function` is the command in R that says "I'm going to make a function." The stuff inside the curly brackets is the function we wrote. Similarly to how for loops find wherever you wrote an `i` and replace it with a number, your function will find wherever you wrote `x` and replace it with the value or vector you feed into it. (You also don't have to use `x.` `function(N){N + 1}` is identical to our `add_one`.)

What's nice about writing a function is that now you can just say `add_one(5)` or `add_one(1:1000)` and R will run your inputs (here: `5` and `1:1000` (1, 2, 3, ... , 1000) through that equation for you. And if you ever forget the code that went into creating this function, just type `add_one` and R will print the full machinery. *[I find this a nice contrast to Python.]*

## Our own mean function
Here's something slightly more complicated. R has a built-in function for finding the mean of a vector or matrix, but we can easily write our own version.

```r
our_mean <- function(x){sum(x) / length(x)}
```

We can check it by creating a vector with some values and comparing the outputs from R's mean and our own.

```r
values <- seq(from = 4, to = 6, by = 0.5)
our_mean(values)
mean(values)    
```

## More advanced mechanics
You are essentially unhindered in what you make into a function. You can have multiple inputs that interact with each other, you can specify default values, you can nest functions within each other... let your imagination go nuts.

```r
multiply <- function(x, y){x * y}
multiply(5, 1:5)

mega_multiply <- function(x, y){multiply(x, y) * x * y}
mega_multiply(1e5, 1e-5)

super.duper <- function(x, y, z = 1){ (x + y) / z }  
```

In super.duper, the x and y inputs are required, but z is optional. If you don't include it, R will automatically set z = 1. Conversely, if you write function(x, y, z) and then don't specify z when you call the function (e.g. super.duper(1, 1)), R will give you an error message.

# If statements
Let's say you want R to run a command only if a certain condition is met. You're curious if 1 + 1 is less than 5, for example, because you skipped that day of kindergarten and you're finally ready to address this gap in your knowledge... using R.

```r
if(1 + 1 < 5){print("Yup, less than 5")}
```

R will print the statement only if 1+1 is less than 5. To avoid spoilers, I won't post the output from R; it's on you to figure this one out! ;-)

We can easily turn this `if` statement into a function that checks whether any input is less than 5:

```r
less.than.five <- function(x){if(x < 5){return("Yup, less than 5")}}
less.than.five(3)
less.than.five(10)
```

(We use `return` here instead of print for a subtle distinction that I'm not sure I fully understand... both will take an output from the internal environment of the function (whatever is inside the curly brackets) and bring it into the global environment for you to see. Functions in R have hidden return commands that give you the result of the last calculation performed by the function; mean, for example, doesn't show you the calculations it does to find the average, it just gives you the average. Specifically writing `return` is useful in case there are multiple calculations required but you care about a particular one. print just announces its contents if triggered, which caused me some trouble in the for loop we'll go through at the end of the post. Here's some more info from a Code Academy forum on some Python thing called PygLatin.)

Note that nothing happens when the input to `less.than.five` is greater or equal to five. That's because we didn't tell R what to do if this situation occurs, so it does nothing. (Computationally, this can be pretty useful in a script, like if you want to make a change to a variable if a condition is met but to just move on if the condition isn't met.) Here, a little extra code will address what happens when $x \geq 5$:

```r
less.than.five <- function(x){
  if(x < 5){
    return("Yup, less than 5")} else if (x == 5) {
    return("No, it's 5")} else {
    return("No, greater than 5")}}  
```

In English, this reads as:
 - If x < 5, return "Yup, less than 5."
 - If x is not less than 5, check if x = 5. If it does, return "No, it's 5."
 - If neither of the previous conditions were met, return "No, greater than 5."

The `else if` statement is basically another `if` statement, but it also incorporates the previous `if` statement. This isn't crucial here, but it'd be important if, for example, you had one `if` statement looking for "anything less than 10" and another looking for "anything greater than 5." The values 5 through 9 would trigger both `if` statements, which could be a problem if they have conflicting actions. Here, `else if` is saying "if the previous `if` statement wasn't met, check if x equals 5." Finally, the `else` tells R that if neither of the previous if statements were met, follow this action.

In point #2, we use x == 5  because that notation asks R if the statement is true or false. If we wrote x = 5, we'd be assigning the value 5 to x, which causes an error within the if statement. You can use the logical operators <, >, <=, >=, ==, |, &, and ! to ask R if a statement is true.

x == 4                                       # "x equals 4, true or false?"
     x != 4                                        # "x does not equal 4, true or false?"
     x > mega.multiply(10, 4)  # "x is greater than the output of this function, true or
                                                         # false?"
     x < 4 | x > 2                             # "x is less than 4 OR x is greater than 2, true or false?"
     x < 4 & x > 2                           # "x is less than 4 AND x is greater than 2, true or
                                                        # false?"    
