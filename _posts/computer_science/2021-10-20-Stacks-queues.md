---
layout: post
title: Exploring stacks and queues
author: matt_sosna
---

In our [last post]({{  site.baseurl  }}/CSDS-intro), we covered _data structures_, or the ways that programming languages store data in memory. We touched upon **abstract data types**, a theoretical entity that can be _implemented_ via a data structure. The concept of a "vehicle" can be viewed as an abstract data type, for example, with a "bike" being the data structure.

In this post, we'll explore two common abstract data types: **stacks** and **queues**. We'll start with the theory behind these abstract types before implementing them in Python. Finally, we'll visit some [Leetcode](https://leetcode.com/) questions that may initially seem challenging, but which neatly unravel into a clean solution when using a stack or queue. Let's get started!

<img src="{{  site.baseurl  }}/images/computer_science/intro/abstract_ds.png">

## Overview
Stacks and queues are array-like collections of values, like `[1, 2, 3]` or `[a, b, c]`. But unlike an array, where any value in the collection can be accessed in $O(1)$ time, stacks and queues have the restriction that only _one_ value is immediately available: the first element (for queues) or last element (for stacks). For both stacks and queues, values are always added to the end.

Visuals can help explain. Below, we see the process of adding and removing a value from a **stack**. Block C is added to the stack, then popped off. Stacks follow a [**Last In First Out**](https://www.geeksforgeeks.org/lifo-last-in-first-out-approach-in-programming/) pattern: the last element to be added to the stack is the first to be removed. The classic analogy is a stack of plates: the plate on top was the last one added, and it's the first one removed.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/stacks_queues/stack.png" height="70%" width="70%">
</center>

Meanwhile, a **queue** is [**First In First Out**](https://www.geeksforgeeks.org/fifo-first-in-first-out-approach-in-programming/). Below, we see that Block C is again added to the end of the queue. But this time, Block A leaves: it was the first one in, so it's the first one out. A common example of a queue is the checkout line at a grocery store $-$ of all the people waiting in line, the person who was there the earliest will be the one who's seen next (i.e. "first come first served").

<center>
<img src="{{  site.baseurl  }}/images/computer_science/stacks_queues/queue.png" height="70%" width="70%">
</center>

Immediate access to _only_ the first or last element seems like a major disadvantage over arrays. Yet we don't always _want_ access to every element. **There's often a distinct order that we want to process elements, meaning we only care about $O(1)$ access to the _next_ element.**

We can see this in the major use cases for stacks and queues. Stacks are used for [_undo_ and _redo_ operations in text editors](https://www.geeksforgeeks.org/implement-undo-and-redo-features-of-a-text-editor/), [compiler syntax checking](https://users.ece.cmu.edu/~koopman/stack_computers/sec1_4.html), [carrying out recursive function calls](https://users.ece.cmu.edu/~koopman/stack_computers/sec1_4.html), [depth-first search](https://en.wikipedia.org/wiki/Depth-first_search), and other cases where we care about **the _last_ action performed.**

Queues, meanwhile, are used for [asynchronous web service communication](https://aws.amazon.com/message-queue/), [scheduling CPU processes](https://en.wikipedia.org/wiki/Scheduling_(computing)), [tracking the `N` most recently added elements](https://stackoverflow.com/questions/5498865/size-limited-queue-that-holds-last-n-elements-in-java), [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search), and any time we care about servicing requests **in the order they're received.**

## Implementation
### Linked list
Since we don't need immediate access to every element, let's actually use a linked list rather than an array to create Python `Stack` and `Queue` classes.

We start by defining the node in a linked list. The node consists of a value (`self.val`) and pointer to the next node in the list (`self.next`).

{% include header-python.html %}
```python
from typing import Any

class ListNode:
    def __init__(self, val: Any, next=None):
        self.val = val
        self.next = next
```

We can create linked lists by chaining `ListNode` instances together. Here's a simple example of a chain with the values `1`, `2`, and `3`.

{% include header-python.html %}
```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
```

With the list node structure in place, we have the central building block for our stack and queue classes.

### Stack
We define a `Stack` class with `add`, `peek`, and `pop` methods. We also add a `__repr__` method to easily visualize the contents of the stack.

{% include header-python.html %}
```python
class Stack:
    def __init__(self):
        self._stack = None

    def add(self, val: Any) -> None:
        """
        Add a value to the stack
        """
        top = ListNode(val)
        top.next = self._stack
        self._stack = top

    def peek(self) -> Any:
        """
        Return the top value of the stack. Does not modify
        the stack.
        """
        node = self._stack

        if not node:
            return None

        return node.val

    def pop(self) -> Any:
        """
        Return the top value of the stack, modifying the stack.
        """
        node = self.peek()

        if node:
            self._stack = self._stack.next
            return node

    def __repr__(self) -> str:
        """
        Visualize stack contents
        """
        vals = []
        node = self._stack

        while node:
            vals.append(str(node.val))
            node = node.next

        return "Stack: [" + ", ".join(vals) + "]"
```

We can play with it like this:

{% include header-python.html %}
```python
# Create and add to stack
s = Stack()
s.add(1)
s.add('abc')

# Visualize contents
print(s.peek())  # 'abc'
print(s)         # 'Stack: [abc, 1]'

# Modify stack
print(s.pop())   # 'abc'
print(s)         # 'Stack: [1]'
```

### Queue
We define a queue with `enqueue`, `peek`, and `dequeue` methods. (_enqueue_ and _dequeue_ are fancy ways of saying "add" and "remove".)

{% include header-python.html %}
```python
class Queue:
    def __init__(self):
        self._queue = None

    def enqueue(self, val: Any) -> None:
        """
        Add an element to the end of the queue
        """
        node = self._queue

        if not node:
            self._queue = ListNode(val)
            return None

        while node.next:
            node = node.next

        node.next = ListNode(val)
        return None

    def dequeue(self) -> Any:
        """
        Remove an element from the front of the queue
        """
        node = self._queue

        if node:
            self._queue = self._queue.next

        return node.val

    def peek(self) -> Any:
        """
        View the next element to be dequeued
        """
        if self._queue:
            return self._queue.val
        return None

    def __repr__(self) -> str:
        """
        Visualize the contents of the queue
        """
        vals = []
        node = self._queue

        while node:
            vals.append(str(node.val))
            node = node.next

        return "Queue: [" + ", ".join(vals) + "]"
```

We can now play with our `Queue` class like this:

{% include header-python.html %}
```python
# Create and add to queue
q = Queue()
q.enqueue(1)
q.enqueue('abc')

# Visualize queue
print(q.peek())     # 1
print(q)            # 'Queue: [1, abc]'

# Modify queue
print(q.dequeue())  # 1
print(q)            # 'Queue: [abc]'
```

## Questions
### Stacks
A great example of a stack is a code inspector for parentheses. [**LC 20:** Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) looks something like this: _Given a string consisting of parentheses, determine whether the string is valid._

The string `{[]}` would be fine, for example, but `{[}` wouldn't.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/stacks_queues/parentheses.png" height="80%" width="80%">
</center>

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

<center>
<img src="{{  site.baseurl  }}/images/computer_science/stacks_queues/parentheses2.png" height="70%" width="70%">
</center>

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

### Queues
One common question regarding trees is level-order traversal. How could you print out the value of every node in a tree, moving level by level? You just have the root node.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/intro/tree_traversals_2.png" height="35%" width="35%">
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

Notice how all we're doing is iteratively adding a tree's children to the queue. Because we always add to the end and dequeue from the front, we're guaranteed that all nodes on a level will be processed before nodes from lower levels.

Trickier questions will play with variations on this theme, such as having the nodes listed from right to left, or seeing if the tree is symmetric.

Here's another one: determining the maximum depth of the tree. In other words, what's the largest distane

```python
def max_depth(root: TreeNode) -> int:
    """
    Determine the longest path between the root and a leaf node
    """
    answer = 1

    q = [(root, 1)]

    while q:
      	node, level = q.pop(0)

        if node:
            answer = max(answer, level)
            q.append((node.left, level+1))
            q.append((node.right, level+1))

    return answer
```
