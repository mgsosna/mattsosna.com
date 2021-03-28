---
layout: post
title: SQL vs. NoSQL in Python
author: matt_sosna
---

How do you store data when it's too large too fit on a hard drive? How can you make it possible for multiple people to view *and modify* the data simultaneously? Databases are the answer here.

But there are a few flavors of databases, i.e. SQL vs. NoSQL. They're different takes on the question of how to best store data. This post will first cover the theory before going through some code for you to create and play with databases in Python.

While all this makes sense, I find it's useful to play around with it to get a feel.

## Theory
Nope

## Playtime

### SQL
We start by loading in the necessary stuff.

{% include header-python.html %}
```python
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import Session

# Methods for abstracting classes to tables
from sqlalchemy.ext.declarative import declarative_base

# Use default declarative base
Base = declarative_base()
```

We then create our class, which is also a table. Then we create instances of that class... which serve as rows. It's a little weird to wrap your head around.

{% include header-python.html %}
```python
# Create Student class / Student table
class Student(Base):
    __tablename__ = 'student'
    _id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    hobby = Column(String(255))

# Create instances of Student / rows for database
matt = Student(name='Matt', hobby='eating')
john = Student(name='John', hobby='running')
```

Now we do this other thing.

{% include header-python.html %}
```python
session = Session(bind=engine)

session.add(matt)
session.add(john)
session.commit()
```

We can view it like this.

{% include header-python.html %}
```python
student_list = session.query(Student)
print("id\tName\tAge\tHobby")
print("-"*30)
for s in student_list:
    print(f"{s._id}\t{s.name}\t{s.age}\t{s.hobby}")

# id    Name	Age    Hobby
# ----------------------------
# 1     Matt    abc    eating
# 2     John	15     running
```

### NoSQL
Now let's work with MongoDB.

{% include header-python.html %}
```python
import pymongo

# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a DB and collection
db = client.classDB
classroom = db.classroom.find()

# Confirm nothing there
for student in classroom:
    print(student)  # nothing
```

Now what's up.

{% include header-python.html %}
```python
db.classroom.insert_one(
  {
    'name': 'John',
    'age': 15,
    'hobbies': {'exercise': 'running',
                'reading': 'comedy'}
  })

db.classroom.insert_one(
  {
    'name': 'Matt',
    'age': 30,
    'hobbies': {'exercise': 'swimming',
                'reading': 'comedy'}
  })
```

{% include header-python.html %}
```python
classroom = db.classroom.find()

for student in classroom:
    print(student)
# {'_id': ObjectId('605e3627df0f9a3c4d8a3ffa'), 'name': 'John', 'age': 15, 'hobbies': {'exercise': 'running', 'reading': 'comedy'}}
# {'_id': ObjectId('605e3627df0f9a3c4d8a3ffb'), 'name': 'Matt', 'age': 30, 'hobbies': {'exercise': 'swimming', 'reading': 'comedy'}}
```

Now we can do some cool nested querying.

{% include header-python.html %}
```python
for student in db.classroom.find({'hobbies.exercise': 'running'}):
    print(student)
# {'_id': ObjectId('605e3627df0f9a3c4d8a3ffa'), 'name': 'John', 'age': 15, 'hobbies': {'exercise': 'running', 'reading': 'comedy'}}
```

Check out new fields being added dynamically.

{% include header-python.html %}
```python
db.classroom.insert_one(
  {
    'name': 'Wonder Woman',
    'age': 'infinite',
    'favorite_food': 'pizza'
  })
```

Now when we look at the data

{% include header-python.html %}
```python
classroom = db.classroom.find()

for student in classroom:
    print(student)

# {'_id': ObjectId('605e3627df0f9a3c4d8a3ffa'), 'name': 'John', 'age': 15, 'hobbies': {'exercise': 'running', 'reading': 'comedy'}}
# {'_id': ObjectId('605e3627df0f9a3c4d8a3ffb'), 'name': 'Matt', 'age': 30, 'hobbies': {'exercise': 'swimming', 'reading': 'comedy'}}
# {'_id': ObjectId('605e36a2df0f9a3c4d8a3ffc'), 'name': 'Wonder Woman', 'age': 'infinite', 'favorite_food': 'pizza'}
```

## Conclusions
In conclusion, databases are *fantastic.* 10/10.


## Footnotes
#### 1. [SQL](#sql)
SQLAlchemy [doesn't do type validation or coercion](https://stackoverflow.com/questions/8980735/how-can-i-verify-column-data-types-in-the-sqlalchemy-orm). This means it's possible to create nonsensical instances of `Student` and actually write them to a database, like this:

{% include header-python.html %}
```python
bad_student = Student(name=123)  # name wrong, no hobby
session.add(bad_student)
session.commit()  # no problem!

for student in session.query(Student):
    print(student)
# > normal student
# > student with messed up attributes
```

Not really an issue, at least for SQLite. But stuff won't show up in filtering.

One way to ensure things are good is to do type checking when the instance of `Student` is first created. We can do this with the `__init__` method.

{% include header-python.html %}
```python
class Student(Base):
    __tablename__ = 'student'
    _id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    hobby = Column(String(255))

    def __init__(self, name, hobby):
        assert isinstance(name, str),
            f"name is type {type(name)}; must be str"
        assert isinstance(hobby, (str, type(None))),
            f"hobby is type {type(hobby)}; must be str or None"

        self.name = name
        self.hobby = hobby
```
Now if you try to create the thing, it stops you in your tracks.

{% include header-python.html %}
```python
bad_student1 = Student(123)
# TypeError: __init__() missing 1 required positional argument: 'hobby'

bad_student2 = Student(123, 'abc')
# AssertionError: name is type <class 'int'>; must be str
```

#### 2. [NoSQL](#nosql)
Postgres lets you save and query JSONs. [link](https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/)
