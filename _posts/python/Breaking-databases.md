---
layout: post
title: Adventures in breaking my databases
author: matt_sosna
---

### SQL injection attack

```python
import pandas as pd

url = "; SELECT * FROM users;"

pd.read_sql_query(url)
```

Looks like two queries. Even if 1st fails, then you can just do 2nd one.


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


For MongoDB, you can't write an instance of a Python class to the DB.

```python
class Fireball:
    def __init__(self):
        self.temperature = 5000

db.classroom.insert_one({
    'name': 'Matt',
    'passion': Fireball()
})
# InvalidDocument: cannot encode object: <__main__.Fireball object at 0x11828c350>, of type: <class '__main__.Fireball'>
