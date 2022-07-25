---
layout: post
title: Intro to Haskell
author: matt_sosna
---

Key features:
* Compiled
* Strongly typed
* Lazy evaluation. Can have infinite data structures, like an infinitely long list.

## Types
Haskell is strongly typed, meaning that we need to define every variable before we use it, and functions will throw an error if they receive an argument of the wrong type.

Let's start by defining a bunch of variables. The first line of the definition names the variable and its type, with the syntax `name :: Type`. Then we actually define the variable on the next line.

{% include header-haskell.html %}
```haskell
our_int :: Int
our_int = 5

our_double :: Double
our_double = 1.2

our_char :: Char
our_char = 'a'  -- Single quotes

our_string :: String
our_string = "hello"  -- Double quotes

our_bool :: Bool
our_bool = True
```

We can then compile this and inspect the contents. `:t` lets us check the type.

{% include header-haskell.html %}
```haskell
:t our_int     -- our_int :: Integer
:t our_double  -- our_double :: Double
:t our_char    -- our_char :: Char
:t our_string  -- our_string :: String
:t our_bool    -- our_bool  :: Bool
```

Arrays are defined similarly. We just wrap the element type in brackets when defining. Note that all elements must be the same type.

{% include header-haskell.html %}
```haskell
our_int_list :: [Int]
our_int_list = [1, 2, 3]

our_double_list :: [Double]
our_double_list = [1.1, 2.2, 3.3]

our_char_list :: [Char]
our_char_list = ['a', 'b', 'c']

our_string_list :: [String]
our_string_list = ["abc", "def", "ghi"]

our_bool_list :: [Bool]
our_bool_list = [True, False, True]
```

We can look at lists with `head` and `tail`.

```haskell
head our_bool_list    -- True :: Bool
tail our_string_list  -- ["def", "ghi"] :: [String]
```

Can bind variables with `let`. `let x = 4` is the expression, and `x * x` is the body. Separated by `in`.

```haskell
let x = 4 in x * x
-- 16

let age = (28, "matt") in fst villain
-- 28

let name = (28, "matt") in snd villain
-- "matt"

let square x = x * x in square 10
-- 100
```

`:` can construct a list for you.

```haskell
'a' : []  -- "a"
'a' : 'b' : []  -- "ab"
['a', 'b']  -- "ab"

```

## Functions
Let's start with a basic function. We'll just create a function that adds two numbers.

{% include header-haskell.html %}
```haskell
-- Adds two numbers
add :: Int -> Int -> Int
add x y = x + y
```

We first define what types the function will take, followed by the actual definition. Note that Haskell doesn't require commas to separate arguments. This might feel uncomfortable coming from Python or R, but it's like how bash works if that's any comfort.


The `$` adds parentheses to the rest of the line.

{% include header-haskell.html %}
```haskell
add 1 2  -- 3
add 1 2 3 -- error

add 1 (2 + 3)    -- 6
add 1 $ 2 + 3    -- 6
add 1 $ add 2 3  -- 6
```


### Map
```haskell
our_list :: [Int]
our_list = [1, 2, 3]

add_one :: Int -> Int
add_one x = x + 1

map add_one our_list
-- [2, 3, 4]
```

We can use `let` to test things out in the terminal.

```haskell
let square x = x * x in map square [1, 2, 3]
-- [1, 4, 9]
```

We can also use `map` when dealing with strings. `toUpper` converts a char from lowercase to uppercase, but we need to use `map` when dealing with a string (which is an array of chars).

```haskell
toUpper 'a'  -- 'A'
map toUpper "hello"  -- "HELLO"
```

### Filter
We can also filter our lists.

```haskell
filter (>2) our_list  -- [3]
filter (==1) our_list  -- [1]
```

### Reduce (fold)
Reduce is called `fold`.

```haskell
add :: Int -> Int -> Int
add x y = x + y

fold add our_list  -- 6
fold (+) our_list  -- 6
```

### Random stuff:

{% include header-haskell.html %}
```haskell
-- String concatenation
"abc" ++ "def"
-- "abcdef"
```
