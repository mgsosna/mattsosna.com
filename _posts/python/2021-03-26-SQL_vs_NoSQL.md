---
layout: post
title: SQL vs. NoSQL databases in Python
author: matt_sosna
---

From ancient government, library, and medical records to present-day video and [IoT streams](https://en.wikipedia.org/wiki/Internet_of_things), we have always needed ways to efficiently store and retrieve data. Yesterday's filing cabinets have become today's computer [**databases**](https://www.oracle.com/database/what-is-database/), with two major paradigms for how to best organize data: the *structured* (relational) versus *unstructured* (non-relational) approach.

Databases are essential for any organization, so it's useful to wrap your head around where each type is useful. We'll start with a brief primer on the history and theory behind SQL and NoSQL. But memorizing abstract facts can only get you so far $-$ we'll then actually create each type of database in Python to get a hands-on intuition for how they work. Let's do it!

## A time series of databases
### Relational databases
Databases arrived shortly after businesses [began adopting computers in the 1950s](https://www.dataversity.net/brief-history-database-management/), but it wasn't until 1970 that **relational** databases appeared. The main idea with a relational database is to avoid duplicating data by storing it *only once*, with different aspects of that data stored in *tables* with formal *relationships.* The relevant data can then be extracted from different tables, filtered, and rearranged with queries in SQL, or [Structured Query Language](https://en.wikipedia.org/wiki/SQL).

Say we're a school and are organizing our data on the students, their grades, and their classrooms. We *could* have one giant table that looks like this:

<img src="{{  site.baseurl  }}/images/projects/sql_v_nosql/main_table.png" loading="lazy" alt="Table of data">

This is a pretty inefficient way to store data, though. Because students have multiple exam scores, **storing all the data in one table requires duplicating info we only need to list once,** like Jerry's hobby, classroom ID, and teacher. If you only have a handful of students, it's no big deal. But as the amount of data grows, all those duplicated values end up costing storage space and making it harder to extract the data you actually want from your table.

Instead, it'd be far more efficient to break out this information into separate *tables*, then *relate* the info in the tables to one another. This is what our tables would look like:

<img src="{{  site.baseurl  }}/images/projects/sql_v_nosql/multi_table.png" loading="lazy" alt="Multiple tables">

That's only 30 cells compared to 42 in the main table $-$ **a 28.5% improvement!** For this particular set of fields and tables, as we increase the number of students, say to 100 or 1,000 or 1,000,000, the improvement actually stabilizes at **38%.** That's more than a third less storage space just by rearranging the data!

But it's not enough to just store the data in separate tables; we still need to model their relationships. We can show this with an [entity-relationship diagram](https://www.visual-paradigm.com/guide/data-modeling/what-is-entity-relationship-diagram/) like the one below. This diagram shows that one classroom consists of multiple students, and each student has multiple grades.

<img src="{{  site.baseurl  }}/images/projects/sql_v_nosql/erd.png" loading="lazy" alt="Entity-Relationship Diagram">

### Nonrelational databases
SQL databases are great. However, relational databases operate on the [assumption of a single server](https://www.cockroachlabs.com/blog/history-of-databases-distributed-sql/). Painful to scale.

Relational = vertical scaling (add more compute to the server). Nonrelational scaling = horizontal.


NoSQL apparently only since 2009?
> Johan Oskarsson had organised a meetup to discuss distributed non-relational databases. To popularise this meetup, he used a hashtag #NoSQL on twitter and this gave birth to NoSQL databases.





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
