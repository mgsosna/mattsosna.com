---
layout: post
title: Fundamental data structures
author: matt_sosna
---

The difference between a good program and an excellent one is using the right tools for the job. Chief among these is choosing the right **data structure**, or way to organize data.

## Arrays
Coming from Python, it's a little hard to understand the limitations of arrays. But their limitations are a central aspect of languages like Java and C. In Python, a `list` is actually a series of pointers to different locations in memory that can still be easily indexed. In terms of usability, it combines the best elements of arrays and linked lists.

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

## Linked lists
What if the elements of our array didn't need to be right next to each other in memory? And what if we didn't have to know beforehand how big our array would be $-$ we could just grow it dynamically without worrying?

* Singularly linked lists
* Doubly linked lists

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

```python
LL = SinglyLinkedList(0)

LL.insert_end(5)
LL.insert_end(10)
LL.insert_front(100)

LL
# SinglyLinkedList with vals [100, 0, 5, 10]
```

Now for a doubly linked list, we just add a `prev` attribute to the `ListNode` that points to the previous node.

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

Some common questions:
* Find the middle
* Find whether the list has a cycle
* Reverse

## Trees

```python
class TreeNode:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

Traversal is a common question. There are different ways to do it, both with recursion and iteration.

* Print values in pre-order, in-order, post-order, and level-order traversal
* Determine whether tree is symmetric
