---
layout: post
title: Exploring stacks and queues
author: matt_sosna
---

In our [last post]({{  site.baseurl  }}/CSDS-intro), we covered _data structures_, or the ways that programming languages store data in memory. We touched upon **abstract data types**, a theoretical entity that can be _implemented_ via a data structure. The concept of a "vehicle" can be viewed as an abstract data type, for example, with a "bike" being the data structure.

In this post, we'll explore two common abstract data types: **stacks** and **queues**. We'll start with the theory behind these abstract types before implementing them in Python. Finally, we'll visit some [Leetcode](https://leetcode.com/) questions that may initially seem challenging, but which neatly unravel into a clean solution when using a stack or queue. Let's get started!

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
### Creating a linked list
Since we don't need immediate access to every element, let's actually use a linked list rather than an array to create Python `Stack` and `Queue` classes.

We start by defining the node in a linked list. The node consists of a value (`self.val`) and pointer to the next node in the list (`self.next`). We also add a `__repr__` magic method to make it easier to visualize the node contents.

{% include header-python.html %}
```python
from typing import Any, Optional

class ListNode:
    def __init__(self, val: Any, next: Optional[ListNode]=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode with val {self.val}"
```

We can create linked lists by chaining `ListNode` instances together. Here's a simple example of creating and visualizing a list with the values `1`, `2`, and `3`.

{% include header-python.html %}
```python
# Create list
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)

# Visualize list
node = head
while node:
    print(node)
    node = node.next

# ListNode with val 1
# ListNode with val 2
# ListNode with val 3
```

With the list node structure in place, we have the central building block for our stack and queue classes.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/stacks_queues/linked_list.png" height="70%" width="70%">
</center>

### Creating stacks
As we've already seen, a main operation for stacks is adding or removing the most recent element, also called [**pushing** and **popping**](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)). It's also often helpful to view the top element in the stack without immediately removing it, a concept called "peeking."

Let's get started. Below, we define a `Stack` class with one attribute, `_stack`, which contains our linked list. We then define our `push`, `peek`, and `pop` methods. To achieve these operations in $O(1)$ time, we place the most recent element in the stack at the _head_ of the linked list in our `Stack` class, so it's always easy to access.

{% include header-python.html %}
```python
class Stack:
    def __init__(self):
        self._stack = None

    def push(self, val: Any) -> None:
        """
        Add a value to the stack
        """
        new_head = ListNode(val)
        new_head.next = self._stack
        self._stack = new_head

    def peek(self) -> Any:
        """
        Return the top value of the stack. Does not modify
        the stack.
        """
        head = self._stack

        if head:
            return head.val

    def pop(self) -> Any:
        """
        Return the top value of the stack, modifying the stack.
        """
        head = self.peek()

        if head:
            self._stack = self._stack.next
            return head
```

Our `push` method creates a node for the new value, sets the existing `self._stack` to the new node's `next` attribute, then points `self._stack` to the new head of the list.

`peek` and `pop` require some control flow to avoid raising an error if you call them on an empty stack. Both only allow us to call the `val` and `next` attributes if `self._stack` isn't empty, which would otherwise throw an error.<sup>[[1]](#1-creating-stacks)</sup>

Our methods return `None` if the stack is empty, but it'd be convenient to have a way to explicitly state if the stack has data. Let's therefore add an `is_empty` method. We'll also add methods that traverse the list: one that determines if the stack contains a requested value (`contains`), and one that prints the list contents (`__repr__`). Note that the traversal methods will execute in $O(n)$ time $-$ the longer the list, the longer it takes to scan or print all elements.<sup>[[2]](#2-creating-stacks)</sup>

(We could get fancy and achieve $O(1)$ time for `contains` by referencing a `dict` that keeps track of the number of instances of each value we add, but let's keep things simple for now.)

{% include header-python.html %}
```python
class Stack:
    def __init__(self):
        self._stack = None

    def push(self, val: Any) -> None:
        """
        Add a value to the stack
        """
        new_head = ListNode(val)
        new_head.next = self._stack
        self._stack = new_head

    def peek(self) -> Any:
        """
        Return the top value of the stack. Does not modify
        the stack.
        """
        head = self._stack

        if head:
            return head.val

    def pop(self) -> Any:
        """
        Return the top value of the stack, modifying the stack.
        """
        head = self.peek()

        if head:
            self._stack = self._stack.next
            return head

    def is_empty(self) -> bool:
        """
        Return whether the stack is empty
        """
        return self._stack is None

    def contains(self, val: Any) -> bool:
        """
        Returns whether the stack contains the requested value
        """
        node = self._stack
        while node:
            if node.val == val:
                return True
            node = node.next
        return False

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

`is_empty` simply checks whether `self._stack` has any values. `contains` and `__repr__` use a `while` loop to iteratively move through the list, setting `node` to its `next` attribute after either checking whether the node's value is equal to the value we're searching for, or appending the value to a list.

Below, we play around with our class and confirm it works as expected.

{% include header-python.html %}
```python
# Create stack
s = Stack()
print(s.is_empty())  # True

# Add to stack
s.push(1)
s.push('abc')
print(s.is_empty())  # False

# Visualize contents
print(s.peek())      # 'abc'
print(s)             # 'Stack: [abc, 1]'

# Modify stack
print(s.pop())       # 'abc'
print(s)             # 'Stack: [1]'
print(s.pop())       # 1
print(s.is_empty())  # True
```

<img src="{{  site.baseurl  }}/images/computer_science/stacks_queues/stack_example.png">

### Creating queues
As with stacks, our `Queue` class will need a way to quickly add and remove elements. But while both element addition and removal occur at the _head_ of the list for stacks, these operations occur on _opposite ends_ of the list for queues.

So should the head of our linked list be the newest or oldest element in the queue? If it's the newest, then addition will take $O(1)$ time but removal will take $O(n)$. If the head is the oldest element, then removal will be fast but addition slow.

**This is actually a false dichotomy** $-$ we can achieve both in $O(1)$ time if we store pointers to both the head and tail of our list. Below, we kick off our `Queue` class with `_head` and `_tail` attributes, as well as methods to `enqueue` (add), `peek`, and `dequeue` (remove) elements.

{% include header-python.html %}
```python
class Queue:
    def __init__(self):
        self._head = None
        self._tail = None

    def enqueue(self, val: Any) -> None:
        """
        Add an element to the end of the queue
        """
        new_tail = ListNode(val)

        # If empty, set pointers to new node
        if not self._head:
            self._head = new_tail
            self._tail = new_tail

        # Otherwise connect nodes and update tail
        else:            

            if self._head is self._tail:
                self._head.next = new_tail

            self._tail.next = new_tail
            self._tail = new_tail

    def dequeue(self) -> Any:
        """
        Remove an element from the front of the queue
        """
        if not self._head:
            return None

        # Save head's val before it disappears, then update head
        val = self._head.val
        self._head = self._head.next

        return val

    def peek(self) -> Any:
        """
        View the next element to be dequeued
        """
        if self._head:
            return self._head.val
```

These operations are a little more complicated than our stack, especially when our `_head` and `_tail` pointers point to the same node. We therefore use additional logic to handle when the queue is empty or has only one element.

```python
class Queue:
    def __init__(self):
        self._head = None
        self._tail = None

    def enqueue(self, val: Any) -> None:
        """
        Add an element to the end of the queue
        """
        new_tail = ListNode(val)

        # If empty, set pointers to new node
        if not self._head:
            self._head = new_tail
            self._tail = new_tail

        # Otherwise connect nodes and update tail
        else:            

            if self._head is self._tail:
                self._head.next = new_tail

            self._tail.next = new_tail
            self._tail = new_tail

    def dequeue(self) -> Any:
        """
        Remove an element from the front of the queue
        """
        if not self._head:
            return None

        # Save head's val before it disappears, then update head
        val = self._head.val
        self._head = self._head.next

        return val

    def peek(self) -> Any:
        """
        View the next element to be dequeued
        """
        if self._head:
            return self._head.val

    def is_empty(self) -> bool:
        """
        Return whether the queue is empty
        """
        return self._head is None

    def contains(self, val: Any) -> bool:
        """
        Returns whether the queue contains the requested value
        """
        node = self._head
        while node:
            if node.val == val:
                return True
            node = node.next
        return False

    def __repr__(self) -> str:
        """
        Visualize the contents of the queue
        """
        vals = []
        node = self._head

        while node:
            vals.append(str(node.val))
            node = node.next

        return "Queue: [" + ", ".join(vals) + "]"
```

Notice how the `is_empty`, `contains`, and `__repr__` methods are identical to our `Stack` class. The one difference is that `__repr__` will print our elements in the order they were received for a queue, versus printing in reverse order for the stack. In either case, they're printed in the order they will be removed.

We can now play with our `Queue` class like this:

{% include header-python.html %}
```python
# Create queue
q = Queue()
print(q.is_empty())  # True

# Add values
q.enqueue(1)
q.enqueue('abc')
print(q.is_empty())  # False

# Visualize queue
print(q.peek())      # 1
print(q)             # 'Queue: [1, abc]'

# Modify queue
print(q.dequeue())   # 1
print(q)             # 'Queue: [abc]'
print(q.dequeue())   # 'abc'
print(q.is_empty())  # True
```

<img src="{{  site.baseurl  }}/images/computer_science/stacks_queues/queue_example.png">

## Use cases
Above, we defined Python classes for stacks and queues, using linked lists to store the objects' contents. In this section, we'll demonstrate the power of these abstract data types by solving a few Leetcode questions. At least to me, these questions seemed like an impossible puzzle when I first saw them. Once I understood how stacks and queues work, though, the puzzle neatly unfolded into a clean solution. Hopefully I can share some of that "ah-ha" feeling in this post.

### Stacks
One area where stacks are incredibly useful is code inspection. As you undoubtedly know if you're still reading this blog post, programming languages utilize parentheses (`( )`), square brackets (`[ ]`), and curly brackets (`{ }`) for functions, indexing, loops, and more. Every open bracket needs a matching closed bracket, and you can't have a closed bracket before an open bracket.

How do you keep track of all the open and closed brackets, and whether they're curved, square, or curly, without going crazy? How can we automatically tell that the brackets on the below left are correct, but the ones on the right are wrong?

<center>
<img src="{{  site.baseurl  }}/images/computer_science/stacks_queues/parentheses.png" height="80%" width="80%">
</center>

This question, [**LC 20:** Valid Parentheses](https://leetcode.com/problems/valid-parentheses/), is painful without a stack, and trivial with one. Below, we'll write a function that takes in a string of brackets and returns a boolean of whether the brackets are valid.

Our solution works like this at a high level: any time we see an open bracket, we add it to the stack. Any time we see a closing bracket, we check if the last open bracket we saw matches the closing bracket. If it doesn't, we know the string isn't valid. If it does, we pop that element off the stack and continue scanning the string. If we make it to the end, the final check is to confirm the stack is empty, i.e. there are no unmatched open brackets.

{% include header-python.html %}
```python
def is_valid(string: str) -> bool:
    """
    Determines whether string has correct matching brackets
    """
    stack = []

    matches = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    # Iterate through string
    for char in string:

        # If open bracket - (, [, { - add to stack
        if char in matches.values():
            stack.insert(char)

        # If close bracket - ), ], } - inspect stack
        elif char in matches:
            if stack:
                last_open = stack.pop()
            else:
                return False  # Stack is empty

            # Confirm close bracket matches open bracket
            if matches[char] != last_open:
                return False

    # Confirm no extra open brackets
    return len(stack) == 0
```

For simplicity, we use a built-in Python `list` for our stack, remembering to always push and pop from the end. We also utilize a Python `dict` as a lookup for our closing brackets $-$ whenever we see a closing bracket, we can quickly look up its corresponding open bracket.

We keep track of two cases where we can exit the `for` loop and declare that the string is invalid: 1) if we come across a closing bracket and the stack is empty, and 2) if the last open bracket doesn't match our closing bracket. The final check is to ensure the stack is empty once we've made it through the string. If it's empty, then the string has passed all checks and is valid code.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/stacks_queues/parentheses2.png" height="70%" width="70%">
</center>

Let's try a slightly tougher variation of this question. In [**LC 1249:** Minimum Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/), rather than output a simple "yes/no" boolean for whether the string is valid, **we need to _make_ the string valid by removing the misplaced brackets.** The strings will also contain a mixture of letters and brackets, but as a minor concession, we only have to deal with parentheses. In the image above, you can see the number of brackets we'd need to remove to make each string valid.

Here's how we'd do it. At a high level, we'll move through the string, adding to the stack when we see an open bracket and removing from the stack when we see a closing bracket. If we encounter a closing bracket with no open bracket, we immediately remove it $-$ there's no open bracket later on that could match this closed bracket. Once we've gone through the string, we remove all remaining open brackets, since they had no matching closing brackets.

{% include header-python.html %}
```python
def make_valid(string: str) -> str:
    """
    Return a string 'fixed' of misplaced parentheses
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

Let's look at the code more closely. We start by converting the string to a list, since it's much easier to modify elements in [mutable](https://medium.com/@meghamohan/mutable-and-immutable-side-of-python-c2145cf72747) lists than immutable strings. (We'd have to create a new string each time, versus modifying the list in-place.)

We then actually store the _indices_ of open brackets in our stack, rather than the brackets themselves, as we'll need to know where exactly to remove a misplaced bracket. We address misplaced closing brackets as we move through the string, as we know from the empty stack that there are no matching open brackets from earlier in the string. For open brackets, we need to pass through the entire string before knowing if they have a matching closing bracket.

"Removal" occurs by replacing the bracket with an empty string $-$ because we're tracking the index of misplaced brackets, shifting the indices of existing elements while we're moving through the list could cause a huge headache. Instead, we remove all empty strings in the final step, when we convert the list to a string with `''.join(s)`.

### Queues
Let's now shift our attention to use cases for queues. One common question where queues are useful is **level-order traversal** for trees. How can we print the value of every node in a tree, level by level? We're usually provided only the root node, so we have no idea ahead of time what the tree looks like. We therefore want to process the tree correctly _as we're exploring it._

<center>
<img src="{{  site.baseurl  }}/images/computer_science/intro/tree_traversals_2.png" height="35%" width="35%">
</center>

As in our [previous post]({{  site.baseurl  }}/CSDS-Intro), we'll use the following implementation for a tree node. This node will be a _binary_ node in that it has at most two children, but our level-order traversal algorithm can easily extend to nodes with any number of children.

{% include header-python.html %}
```python
class TreeNode:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

With our `TreeNode` defined, let's write a function that provides level-order traversal, given the root node of a tree. The solution is delightfully short if you use a queue. At a high level, we start by enqueuing the root node. We dequeue the node, append its value to our answer, then enqueue its children. Then we simply repeat this process until we've processed all nodes. That's it!

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

As with our stack examples, we again use a built-in `list`, this time remembering to always enqueue at the end (i.e. `.append`) and dequeue from the front (i.e. `.pop(0)`).

Because we always enqueue at the end and dequeue from the front, we're guaranteed that all nodes on a level are processed before nodes from lower levels.


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

## Conclusions
This post looked at a lot. Thanks for reading.

Best,<br>
Matt

## Footnotes
#### [1. Creating stacks](#creating-stacks)
The linked list in our `Stack` class has an underscore in front, signaling to other developers that this attribute should be considered [private](https://stackoverflow.com/questions/2620699/why-private-methods-in-the-object-oriented) and not called direclty outside the class. But Python doesn't enforce this rule; we can easily modify the contents and wreak havoc.

{% include header-python.html %}
```python
class BankAccount:
    def __init__(self, password):
        self._password = password

b = BankAccount(password='abc123')
print(b._password)   # 'abc123'

b._password = 'something else'
print(b._password)   # 'something else'
```

There's actually no real way to protect against this in Python. The closest we can get is to obfuscate a bit using the `@property` decorator. We can write rules for how the user can access an _alias_ of `_password`, such as by blocking read access or requiring that the input meet some criteria before it overwrites `_password`. But if the user requests `_password` directly, we can't stop them from viewing or modifying it.

{% include header-python.html %}
```python
import logging

class BankAccount:
    def __init__(self, password):
        self._password = password

    @property
    def password(self):
        logging.error("Not authorized to access password")
        return None

    @password.setter
    def password(self, value: str):
        if not isinstance(value, str):
            logging.error("Password must be string")
            return None
        self._password = value

# Create a new account
ba = BankAccount(password='abc123')

# Our getter and setter are working...
print(ba.password)  # Not authorized to access password
ba.password = 123   # Password must be string

# ...but then the user "hacks" their way in
ba._password = 123  
print(ba._password)  # 123
```

#### 2. [Creating stacks](#creating-stacks)
You might wonder why searching for a value in a stack takes $O(n)$ time. If the value we're looking for is randomly distributed throughout the list, it would take on average _half_ the list length to find, or $O(\frac{n}{2})$.

However, we ignore constants like $\frac{1}{2}$ in big O notation. The idea is that as $n$ approaches infinity, constants that are added or multiplied to $n$ become irrelevant. Big O notation also cares about the _worst case_ efficiency, not the average. The worst case in searching for an element is that the element is the last element we check, meaning we need to check all $n$ elements to find it.
