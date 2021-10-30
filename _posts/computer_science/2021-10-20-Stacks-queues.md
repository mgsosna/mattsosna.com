---
layout: post
title: A deep dive on stacks and queues
author: matt_sosna
---

In an [earlier post]({{  site.baseurl  }}/CSDS-intro), we covered _data structures_, or the ways that programming languages store data in memory. We touched upon **abstract data types**, a theoretical entity that can be _implemented_ via a data structure. The concept of a "vehicle" could be viewed as an abstract data type, for example, with a "bike" being the data structure.

In this post, we'll do a deep dive on two common abstract data types: **stacks** and **queues**. We'll start with the theory behind these abstract types before implementing them in Python. Finally, we'll visit some [Leetcode](https://leetcode.com/) questions that may initially seem challenging, but which neatly unravel into a clean solution when using a stack or queue. Let's get started!

## Overview
Stacks and queues are an array-like collections of values, like `[1, 2, 3]` or `[a, b, c]`. But unlike an array, where any value in the collection can be accessed in $O(1)$ time, stacks and queues have the restriction that only _one_ value is immediately available: the first element (for queues) or last element (for stacks). For both stacks and queues, values are always added to the end.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/stack2.png" height="70%" width="70%">
</center>

Visuals can be helpful here. Above, we see the process of adding and removing a value from a **stack**. Block C is added to the stack, then popped off. Stacks follow a [**Last In First Out**](https://www.geeksforgeeks.org/lifo-last-in-first-out-approach-in-programming/) pattern: the last element to be added to the stack is the first to be removed. The classic analogy is a stack of plates: the plate on top was the last one added, and it'll be the first one removed.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/queue2.png" height="70%" width="70%">
</center>

Meanwhile, a **queue** is [**First In First Out**](https://www.geeksforgeeks.org/fifo-first-in-first-out-approach-in-programming/). Block A was added first, so it's the first to leave. A common example of a queue would be the checkout line at a grocery store $-$ of all the people waiting in line, the person who was there the earliest will be the one who's seen next (i.e. "first come first served"). (An even more common example of a queue, if you speak British English, is just a literal queue!)

Being unable to access only the first or last element in $O(1)$ time seems like a real disadvantage compared to arrays. Why restrict ourselves? Well, this is where the distinction between a data structure and an abstract data type becomes important.

We _can_ implement a stack or queue with an array. But in languages like Java or C, when we run out of space in an array, we need to find a larger region of memory and copy everything over. (This happens with Python lists too, I believe.) And if we're specifically choosing to use a stack or queue, we might not _want_ to be able to access any element in $O(1)$ time $-$ the code may be cleaner by using an object that is tailored exactly to how we plan to use it.

Linked lists.



Stack use cases include:
* Undo mechanisms in text editors
* Compiler syntax checking for matching brackets and braces
* Behind the scenes to support recursion by keeping track of previous function calls
   * Once a function call is actually executed, pop it off the stack and go to the next call to be made
* Depth-first search (DFS) on a graph

Queue use cases include:
* Modeling real-world waiting lines
* Web server request management for first come first serve
* Keeping track of `N` most recently added elements
   * Say you only want to look at 5 most recent news stories. As new one comes in, dequeue the oldest one
* Breadth-first graph traversal



## Stacks
We can create a simple stack implementation in Python like below. The main methods are adding an item to the top of the stack, removing an item from the top, or peeking at the top item.

```python
class Stack:
    def __init__(self):
        self.vals = []
        self.count = 0

    def insert(self, val: Any) -> None:
        """
        Insert a value onto the stack
        """
        self.vals.append(val)
        self.count += 1

    def peek(self):
        """
        Return the top value of the stack
        """
        if self.vals:
            return self.vals[-1]
        raise ValueError("Stack is empty")

    def pop(self) -> Any:
        """
        Remove the top value from the stack
        """
        if self.vals:
            self.count -= 1
            return self.vals.pop()
        raise ValueError("Stack is empty")

    def __len__(self):
        return self.count
```

### Questions
A great example of a stack is a code inspector for parentheses. [**LC 20:** Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) looks something like this:
> Given a string consisting of parentheses determine whether the string is valid.

The string `{[]}` would be fine, for example, but `{[}` wouldn't.

We'll start with a dictionary that keeps track of the correct matching pair for each item.

{% include header-python.html %}
```python
def is_valid(string: str) -> bool:
    """
    Determines whether string has correct matching parentheses
    """
    stack = []

    matches = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    for char in string:

        # Open chars: (, [, {
        if char in matches.values():
            stack.insert(char)

        # Close chars: ), ], }
        elif char in matches:
            if stack:
                last_open = stack.pop()
            else:
                return False  # stack is empty

            # Confirm closing char matches open char
            if matches[char] != last_open:
                return False

    # Confirm no extra chars
    return len(stack) == 0
```

Here's a slightly tougher variation on that question. [**LC 1249:** Minimum Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/). The strings here only have parentheses, but they also have chars.

Examples:
* `ab(c)de` -> `ab(c)de` (no change needed).
* `ab(cde` -> `abcde` (remove the open parenthesis).
* `ab(c))de` -> `ab(c)de` (remove the close parenthesis).

Here's how we'd do it. We'll actually store the _indices_ of open parentheses, rather than the parentheses themselves.

{% include header-python.html %}
```python
def is_valid(string: str) -> str:
    """
    Determine if string has correct matching parentheses.
    """
    s = list(string)
    stack = []

    for i, char in enumerate(s):
        if char == '(':
            stack.insert(i)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                s[i] = ''  # Remove the ) if no corresponding (

    # Remaining ( to remove since no )
    while stack:
        s[stack.pop()] = ''

    return ''.join(s)
```

## Queues

Let's implement a queue in Python. Notice how `insert` is identical to `Stack`.

```python
class Queue:
    def __init__(self):
        self.vals = []
        self.count = 0

    def insert(self, val: Any):
        self.vals.append(val)
        self.count += 1

    def pop(self) -> Any:
        if self.vals:
            self.count -= 1
            return self.vals.pop(0)
        raise ValueError("Queue is empty")

    def peek(self):
        if self.vals:
            return self.vals[0]
        raise ValueError("Queue is empty")
```

You'll notice that the code for a queue is almost identical to our `Stack` class. The only difference is where we remove elements from: the front (queue) or back (stack).

### Questions
One common question regarding trees is level-order traversal. How could you print out the value of every node in a tree, moving level by level? You just have the root node.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/tree_traversals_2.png" height="35%" width="35%">
</center>

Again, we use the following implementation for a tree node:

{% include header-python.html %}
```python
class TreeNode:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

The solution is delightfully simple if you use a queue.

{% include header-python.html %}
```python
from typing import List

def level_order_traversal(root: TreeNode) -> List[int]:
    """
    Return a list of tree node values from a level-order
    traversal
    """

    q = [root]
    answer = []

    while q:
        node = q.pop(0)

        if node:
            answer.append(node.val)
            q.append(node.left)
            q.append(node.right)

    return answer
```

Trickier questions will play with variations on this theme, such as having the nodes listed from right to left, or seeing if the tree is symmetric.
