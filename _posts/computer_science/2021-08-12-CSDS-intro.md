---
layout: post
title: Fundamental data structures
author: matt_sosna
---

A good program gets the job done, while an excellent program also sets you up for success as the amount of data grows or business needs evolve. A major differentiator between good and excellent is the choice in **data structure**, or method for organizing data.

As a data scientist without a computer science background, I'm most familiar with dataframes. But as I was transitioning to machine learning engineering, I was exposed to much more fundamental structures.

## Table of contents
* [**Data structures**](#data-structures)
  - [Big O](#big-o)
  - [Abstract data structures](#abstract-data-structures)
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

## Data structures
### Big-O notation
What makes a data structure better or worse than another? A data structure is a way of organizing data, and depending on how you're planning on interacting with that data, structures vary tremendously in how efficiently you can _read_ and _write_ to them.

Here's a simple analogy. Imagine you have a hamper of clean laundry and need to put away the clothes. A method with _low write time_ but _high read time_ would be to dump all the clothes into a pile on the ground. While this is blazing fast, it will then take extra time to actually find the shirt you want because you have to search through the pile.

An alternate method would be to neatly arrange your clothes in your dresser and closet. This method would have a _slow write time_ but _fast read time_, as it would take longer to put away your clothes (especially compared to dumping them on the ground), but when you need a particular item you know exactly where to find it and it's easy to access.


(Maybe recreate that common plot of the different time complexities)

### Abstract data structures
There are multiple ways to accomplish a task. Let's say you have a stack. How do you do this?

* Stacks, queues


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


## Trees
### Theory
A tree is similar to a linked list, but rather than having only one next node, you can have several. A common type of tree is a _binary_ tree, where each node has at most children.

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

Changing the traversal between pre-order, in-order, and post-order is simply a matter of rearranging lines 16-18


## Graphs
### Theory
Graphs often represented as adjacency matrices. Let's say you want to describe the network of friend connections on Facebook. A link between two people means they're friends. If you have 5 people, you'd have 5x5 matrix where the five people were on the rows and columns, and each cell corresponded to whether there was a link between the row and column person. More formally, we'd say $A_{ij} = 1$ if the individual in row $i$ and individual in column $j$ were connected, and $A_{ij} = 0$ if they're not.

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
A common graph question is to return the number

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

### Questions
