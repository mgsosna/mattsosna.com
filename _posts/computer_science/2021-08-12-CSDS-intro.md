---
layout: post
title: Intro to data structures
author: matt_sosna
---

What makes a piece of software good versus great? Solving for the present is usually straightforward $-$ there are usually dozens of ways to write a script that dutifully performs some task. But how do we write our code so that it's ready for the _future_, one where we may be faced with 10x or 100x the amount of data to process? And how do we create a program that someone else can quickly learn?

One major differentiator between good and great code is the proper choice of **data structures**, or methods for organizing data. Consider these a set of tools whose utility vary depending on how, specifically, we need to interact with data. In this post, we'll cover a set of data structures that can handle a range of use cases.

## Table of contents
* [**Getting started**](#getting-started)
  - [Data structures vs. abstract data types](#data-structures-vs-abstract-data-types)
  - [Big-O notation](#big-o-notation)
* [**Arrays**](#arrays)
  - [Theory](#theory)
  - [Implementation](#implementation)
  - [Questions](#questions)
* [**Stacks and queues**](#stacks-and-queues)
  - [Theory](#theory-1)
  - [Implementation](#implementation-1)
  - [Questions](#questions-1)
* [**Linked lists**](#linked-lists)
  - [Theory](#theory-2)
  - [Implementation](#implementation-2)
  - [Questions](#questions-2)
* [**Trees**](#trees)
  - [Theory](#theory-3)
  - [Implementation](#implementation-3)
  - [Questions](#questions-3)
* [**Graphs**](#graphs)
  - [Theory](#theory-4)
  - [Implementation](#implementation-4)
  - [Questions](#questions-4)
* [**Hash maps**](#hash-maps)
  - [Theory](#theory-5)
  - [Implementation](#implementation-5)
  - [Questions](#questions-5)

## Getting started
Before we can cover the types of data structures, we need to understand what they are and how to compare them. We'll start by distinguishing between the tools (data structures) and how we use them (abstract data types), as well as Big-O notation, a metric for comparing the read and write speed of data structures and algorithms.

### Data structures vs. abstract data types
In programming $-$ as well as in real life! $-$ there are generally many ways to accomplish a task. Let's say, for example, that you want to visit your friend across town. You can ride a bike, scooter, or motorcycle to get there. Here, the _vehicle_ is an abstract data type $-$ a means of transportation. _How that's actually implemented_ is the data structure $-$ here the bike, scooter, or motorcycle.

We'll cover each of these concepts in a moment, but here's a programming example if you're itching for something more relevant. A queue is an abstract data type that can have elements added sequentially, as well as elements removed _in the order they were added_. There are multiple ways to actually implement this, such as with a linked list or array. 

### Big-O notation
What makes a data structure better or worse than another? A data structure is a way of organizing data, and depending on how you're planning on interacting with that data, structures vary tremendously in how efficiently you can _read_ and _write_ to them.

Here's a simple analogy. Imagine you have a hamper of clean laundry and need to put away the clothes. A method with _low write time_ but _high read time_ would be to dump all the clothes into a pile on the ground. While this is blazing fast, it will then take extra time to actually find the shirt you want because you have to search through the pile.

An alternate method would be to neatly arrange your clothes in your dresser and closet. This method would have a _slow write time_ but _fast read time_, as it would take longer to put away your clothes (especially compared to dumping them on the ground), but when you need a particular item you know exactly where to find it and it's easy to access.

It's not enough to say how fast a certain operation or algorithm takes on our computer. What if your neighbor has a slower or faster computer? Rather, we need a common scale to be able to compare algorithms. For this, we use Big-O notation. This is a measure of the worst-case scenario.

<img src="{{  site.baseurl  }}/images/computer_science/big_o.png">

One example of a runtime on the high end is $O(2^n)$. Finding all subsets of an array is an algorithm with this time complexity. For each element in the set, we have two options: include or exclude the element. A set of three elements, e.g. `[A,B,C,D]`, will therefore have $2^4$, or sixteen, subsets:
* `[]`, `[A]`, `[B]`, `[C]`, `[D]`
* `[A,B]`, `[A,C]`, `[A,D]`, `[B,C]`, `[B,D]`, `[C,D]`
* `[A,B,C]`, `[A,B,D]`, `[A,C,D]`, `[B,C,D]`
* `[A,B,C,D]`

But an even worse runtime is $O(n!)$. Permutations are a classic example of n-factorial complexity. For each element in the set, we can rearrange all following elements. Our previous array `[A,B,C,D]` will have $4 * 3 * 2 * 1$, or 24, permutations:
* `[A,B,C,D]`, `[A,B,D,C]`, `[A,C,B,D]`, `[A,C,D,B]`, `[A,D,B,C]`, `[A,D,C,B]`
* `[B,A,C,D]`, `[B,A,D,C]`, `[B,C,A,D]`, `[B,C,D,A]`, `[B,D,C,A]`, `[B,D,A,C]`
* `[C,A,B,D]`, `[C,A,D,B]`, `[C,B,A,D]`, `[C,B,D,A]`, `[C,D,B,A]`, `[C,D,A,B]`
* `[D,A,B,C]`, `[D,A,C,B]`, `[D,B,A,C]`, `[D,B,C,A]`, `[D,C,A,B]`, `[D,C,B,A]`


## Arrays
### Theory
Coming from Python, it's a little hard to understand the limitations of arrays. But their limitations are a central aspect of languages like Java and C. In Python, a `list` is actually a series of pointers to different locations in memory that can still be easily indexed. In terms of usability, it combines the best elements of arrays and linked lists.

Reading from an array takes $O(1)$ time because we know exactly where in the array to go. Searching, meanwhile, is $O(n)$ because in the worst case, we need to scan through the entire array.

### Implementation

{% include header-python.html %}
```python
class Array:
    def __init__(self, n: int):
        self.length = n
        self.vals = [None] * n

    def __repr__(self):
        non_null = 0

        for val in self.vals:
            if val:
                non_null += 1

        return f"Array of length {len(self.vals)} with " + \
               f"{non_null} non-null values"

    def get(self, i):
        return self.vals[i]

    def append(self, val):
        n = self.length

        for i in range(n):
            if not self.vals[i]:
                self.vals[i] = val
                return None

        print(f"Insufficient space; doubling array size ({n} -> {2*n})")
        self.vals = self.vals + [None] * n
        self.length = 2 * n

        for i in range(n, len(self.vals)):
            if not self.vals[i]:
                self.vals[i] = val
                return None
```

We can play around with it a bit now.

{% include header-python.html %}
```python
arr = Array(10)
arr
# Array of length 10 with 0 non-null values

arr.append(5)
arr
# Array of length 10 with 1 non-null values

for x in [10]*20:
    arr.append(x)
# Insufficient space; doubling array size (10 -> 20)
# Insufficient space; doubling array size (20 -> 40)

print(arr.length)
# 40
```

### Questions
This is a little different if you're coming straight from Python. But in the spirit of a constant array size, we could have some questions like these:

{% include header-python.html %}
```python
def duplicate_zeros(arr: List[int]) -> None:
    """
    Duplicate all zeros in an array, maintaining the length
    of the original array. e.g. [1, 0, 2, 3] -> [1, 0, 0, 2]
    """
    i = 0

    while i < len(arr):
        if arr[i] == 0:
            arr.insert(i, 0)
            arr.pop()
            i += 1
        i += 1
```

We use a `while` rather than a `for` loop because we're modifying the array as we move through it, so we want to manually control our index `i`. This is important when we're inserting zeros because we either will double-count our zero (if we insert into the array at or past our index), or the array will move without us if we insert it before. Our logic is therefore that we progress through our array like a normal `for` loop, incrementing `i` each time. But if we encounter a zero, we insert a zero and then increment `i` again, skipping the zero we added to avoid double-counting.

We also don't return anything because we're modifying the array in-place.


## Linked lists
### Theory
What if the elements of our array didn't need to be right next to each other in memory? And what if we didn't have to know beforehand how big our array would be $-$ we could just grow it dynamically without worrying?

This is what a singly linked list looks like.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/ll1.png" height="50%" width="50%">
</center>

Each node in a list consists of some data, as well as pointer to the location of the next node in the list. So technically, it looks something like the diagram below. The red line of blocks is a section of your computer's RAM. The blue blocks are the nodes of our list, which consist of some data (the number in each block) and an orange _pointer_ to the location in memory for the next node of the list. The last node's pointer points to nowhere, indicating the end of the list.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/ll2.png">
</center>

* Singularly linked lists
* Doubly linked lists

### Implementation
{% include header-python.html %}
```python
class ListNode:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode with val {self.val}"

class SinglyLinkedList:
    def __init__(self, head=None):
        self.head = ListNode(head)

    def __repr__(self):
        vals = []
        node = self.head
        while node:
            vals.append(node.val)
            node = node.next
        return f"SinglyLinkedList with vals {vals}"

    def insert_end(self, val):
        node = self.head
        while node.next:
            node = node.next
        node.next = ListNode(val)

    def insert_front(self, val):
        head = ListNode(val)
        head.next = self.head
        self.head = head
```

Then we can play around a bit with it.

{% include header-python.html %}
```python
LL = SinglyLinkedList(0)

LL.insert_end(5)
LL.insert_end(10)
LL.insert_front(100)

LL
# SinglyLinkedList with vals [100, 0, 5, 10]
```

Now for a doubly linked list, we just add a `prev` attribute to the `ListNode` that points to the previous node.

{% include header-python.html %}
```python
class ListNode:
    def __init__(self, val=None, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

class DoublyLinkedList:
    def __init__(self, head=None):
        self.head = ListNode(head)

    def insert_end(self, val):
        node = self.head

        while node.next:
            node = node.next

        node.next = ListNode(val)

        prev_node = node
        node = node.next
        node.prev = prev_node

    def insert_front(self, val):
        head = ListNode(val)
        head.next = self.head
        self.head = head
```

### Questions
Some common questions:
* Find the middle
* Find whether the list has a cycle
* Reverse

{% include header-python.html %}
```python
def find_middle(head: ListNode) -> Optional[ListNode]:
    """
    Return middle node of linked list. If even numbers, returns second
    """
    if not head:
        return None

    slow = head
    fast = head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow  
```

Whenever dealing with Leetcode questions, I like to draw out examples and make sure I'm doing what I think I'm doing. For example, it can be hard to remember if we should initialize `fast` to `head` or to `head.next`. If you draw out a simple list where you know what the middle should be, you can quickly confirm that `head.next` is the right option.

```bash
# List: A -> B -> C -> D -> E, middle = C

# Start at same place: incorrect
# Slow: A -> B -> C -> D
# Fast: A -> C -> E -> null

# Start apart: correct
# Slow: A -> B -> C
# Fast: B -> D -> null
```

Here's another example: whether the list has a cycle. We can't use `while fast and fast.next` anymore, since we would never exit the loop for a list with a cycle. Rather, we'll again instantiate `slow` and `fast` to the first and second nodes, then move them through the list at different speeds until they match. If we reach the end of the list, we return `False`; if the two pointers ever point to the same node, we return `True`.

{% include header-python.html %}
```python
def has_cycle(head: ListNode) -> bool:
    """
    Determines whether a linked list has a cycle
    """
    if not head:
        return False

    slow = head
    fast = head.next

    while slow != fast:

        # Reach end of list
        if not fast or fast.next:
            return False

        slow = slow.next
        fast = fast.next.next

    return True
```



## Trees
### Theory
A tree is similar to a linked list, but rather than having only one next node, you can have several. A common type of tree is a _binary_ tree, where each node has at most two children.

There are various types of binary trees. Below is a **binary search tree**. For every node in the tree, every node in its _left_ subtree must contain a smaller value, and every node in its _right_ subtree must contain a larger value.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/tree1.png" height="65%" width="65%">
</center>

Searching a binary search tree for a value takes on average $O(logn)$ time, meaning they can find a given value among millions or billions of records very rapidly. Databases often use binary search on table indices to efficiently find queried terms.

### Implementation
{% include header-python.html %}
```python
class TreeNode:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Questions
Traversal is a common question. There are different ways to do it, both with recursion and iteration.

* Print values in pre-order, in-order, post-order, and level-order traversal
* Determine whether tree is symmetric

{% include header-python.html %}
```python
def traverse_in_order(root: TreeNode) -> List[int]:
    """
    Traverse a binary tree, returning list of values in order
    """
    if not root:
        return None

    answer = []
    stack = [(root, False)]

    while stack:
        node, visited = stack.pop()

        if node:

            if visited:
                answer.append(node.val)
            else:
                stack.append(node.right, False)
                stack.append(node, True)
                stack.append(node.left, False)

    return answer
```

And the recursive method:

{% include header-python.html %}
```python
class Solution:
    def __init__(self):
        self.answer = []

    def traverse_inorder(self, root: TreeNode) -> List[int]:
        """
        Traverse a binary tree, returning list of values in-order
        """
        self.traverse(root)
        return self.answer

    def traverse(self, node: Optional[TreeNode]) -> None:
        if not node:
            return None

        self.traverse(node.left)
        self.answer.append(node.val)
        self.traverse(node.right)
```

Changing the traversal between pre-order, in-order, and post-order is simply a matter of rearranging lines 16-18. The `self.answer.append(node.val)` comes first in pre-order, second in in-order, and third in post-order. The rest of the code remains unchanged. Simple!


## Graphs
### Theory
Graphs often represented as adjacency matrices. Let's say you want to describe the network of friend connections on Facebook. A link between two people means they're friends. If you have 5 people, you'd have 5x5 matrix where the five people were on the rows and columns, and each cell corresponded to whether there was a link between the row and column person. More formally, we'd say $A_{ij} = 1$ if the individual in row $i$ and individual in column $j$ were connected, and $A_{ij} = 0$ if they're not.

Here's an example of a graph.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/graph1.png" height="50%" width="50%">
</center>

We would represent this graph with the following adjacency matrix.


### Implementation
Implementation is straightforward since we're only dealing with a matrix of 1s and 0s.

{% include header-python.html %}
```python
class Graph:
    def __init__(self, n: int):
        self.graph = [[0]*n for _ in range(n)]

    def connect(self, a: int, b: int) -> List[List[int]]:
        """
        Updates self.graph to connect individuals A and B.
        """
        self.graph[a][b] = 1
        self.graph[b][a] = 1
        return self.graph

    def disconnect(self, a: int, b: int) -> List[List[int]]:
        """
        Updates self.graph to disconnect individuals A and B.
        """
        self.graph[a][b] = 0
        self.graph[b][a] = 0
        return self.graph
```


### Questions
A common graph question is to return the number of connected components, or sub-clusters. For example, in the below graph, we can identify three distinct components.

<center>
<img src="{{  site.baseurl  }}/images/computer_science/graph2.png" height="40%" width="40%">
</center>


{% include header-python.html %}
```python
def get_n_provinces(self, mat: List[List[int]]) -> int:
    """
    Given an adjacency matrix, returns the number of connected components
    """
    q = []
    cities = [*range(len(mat))]

    answer = 0

    while q or cities:

        if not q:
            q.append(cities.pop(0))
            answer += 1

        focal = q.pop(0)
        i = 0

        while i < len(cities):
            city = cities[i]

            if mat[focal][city] == 1:
                q.append(city)
                cities.remove(city)
            else:
                i += 1

    return answer
```


## Hash maps
### Theory
A hash map is a data structure with $O(1)$ retrieval time, pretty much regardless of how many elements there are (assuming you have a good hash function). The idea is that for any input, you pass it through a hash function to get some output. Then you look at a location in memory corresponding to that hashed output. If your hash function can produce enough unique hashes, you can instantly retrieve any key's value.

### Implementation

{% include header-python.html %}
```python
from string import ascii_lowercase as alphabet

def hash_function(name: str) -> int:
    """
    Converts a string to a number distributed in the range 0-9
    """
    output = sum([alphabet.index(char.lower()) for char in name])

    # Add depending on even/odd
    output += 1 if len(name) % 2 == 0 else 0

    # Multiply depending on first char
    char_idx = alphabet.index(name[0].lower())

    if char_idx < 10:
        output *= 3
    elif char_idx < 20:
        output *= 4
    else:
        output *= 5

    return output % 10
```

### Questions
