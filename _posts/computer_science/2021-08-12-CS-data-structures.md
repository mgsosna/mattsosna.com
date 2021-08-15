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
* [**Linked lists**](#linked-lists)
  - [Theory](#theory-1)
  - [Implementation](#implementation-1)
  - [Questions](#questions-1)
* [**Trees**](#trees)
  - [Theory](#theory-2)
  - [Implementation](#implementation-2)
  - [Questions](#questions-2)
* [**Graphs**](#graphs)
  - [Theory](#theory-3)
  - [Implementation](#implementation-3)
  - [Questions](#questions-3)
* [**Hash maps**](#hash-maps)
  - [Theory](#theory-4)
  - [Implementation](#implementation)
  - [Questions](#questions)

## Data structures
### Big-O notation
What makes a data structure better or worse than another? A data structure is a way of structuring data.

Here's a simple analogy. Imagine you have a hamper of clean laundry and need to put away the clothes. A method with _low write time_ but _high read time_ would be dump all the clothes into a pile on the ground. While this is blazing fast, it will then take extra time to actually find the shirt you want because you have to search through the pile.

An alternate method would be to


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

* Duplicate zeros
* Two-sum

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

## Trees
### Theory
There actually is no theory.

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
def

```


## Graphs
### Theory

### Implementation

### Questions
* Number of islands
* Number of provinces

## Hash maps
### Theory

### Implementation

### Questions
