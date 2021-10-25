---
layout: post
title: A deep dive on stacks and queues
author: matt_sosna
---

In an [earlier post]({{  site.baseurl  }}/CSDS-intro), we covered _data structures_, or the ways that programming languages store data in memory. We touched upon **abstract data types**, an abstract "task" to be implemented by a specific data structure. A vehicle is an abstract data type, for example, while a car is a data structure that implements the concept of "vehicle."

In this post, we'll do a deep dive on two common abstract data types for arrays and linked lists: **stacks** and **queues**. We'll again visit some Leetcode questions that seem challenging at the outset but solve simply when using a stack or queue, and we'll do other stuff too.

Why should you care about stacks and queues?

A **stack** is an array-like object where

## Stacks
We can create a simple stack implementation in Python like below. The main methods are adding an item to the top of the stack, removing an item from the top, or peeking at the top item.

```python
class Stack:
    def __init__(self):
        self.vals = []
        self.count = 0

    def insert(self, val: Any):
        self.vals.append(val)
        self.count += 1

    def pop(self) -> Any:
        if self.vals:
            self.count -= 1
            return self.vals.pop()
        raise ValueError("Stack is empty")

    def peek(self):
        if self.vals:
            return self.vals[-1]
        raise ValueError("Stack is empty")

    def __len__(self):
        return self.count
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
