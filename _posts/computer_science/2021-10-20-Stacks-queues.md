---
layout: post
title: A deep dive on stacks and queues
author: matt_sosna
---

In an [earlier post]({{  site.baseurl  }}/CSDS-intro), we covered _data structures_, or the ways that programming languages store data in memory. We touched upon **abstract data types**, a theoretical entity that can be _realized_ in multiple ways 


such as "vehicle" that is then _implemented_ by a data structure, like a car.

In this post, we'll do a deep dive on two common abstract data types: **stacks** and **queues**. We'll again visit some Leetcode questions that seem challenging at the outset but solve simply when using a stack or queue, and we'll do other stuff too.

## Overview
Stacks and queues both deal with an array-like collection of values, like `[1, 2, 3]` or `[a, b, c]`. But while arrays can access any element in $O(1)$ time, with queues and stacks we can only access the first or last element, respectively, in $O(1)$ time.

<img src="{{  site.baseurl  }}/images/computer_science/stack.png">

Visuals can be helpful here. Above, we see the process of adding and removing a value from a **stack**. We notice that block C is added to the stack, then popped off. The term for this is [**Last In First Out**](https://www.geeksforgeeks.org/lifo-last-in-first-out-approach-in-programming/) pattern: the last element to be added to the stack is the first to be removed. The classic analogy is a stack of plates: the plate on top was the last one added, and it'll be the first one removed.

<img src="{{  site.baseurl  }}/images/computer_science/queue.png">

Meanwhile, a **queue** is [**First In First Out**](https://www.geeksforgeeks.org/fifo-first-in-first-out-approach-in-programming/). Block A was added first, so it's the first to leave. A common example of a queue would be the checkout line at a grocery store $-$ of all the people waiting in line, the person who was there the earliest will be the one who's seen next (i.e. "first come first served"). (An even more common example of a queue, if you speak British English, is just a literal queue!)



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
