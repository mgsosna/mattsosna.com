---
layout: post
title: Intermediate SQL
author: matt_sosna
---

When I started learning SQL, I found it hard to progress beyond the absolute basics. I loved [DataCamp's courses](https://www.datacamp.com/courses/introduction-to-sql) because I could just type the code directly into a console on the screen. But once the courses ended, how could I practice what I learned? And how could I continue improving, when all the tutorials I found just consisted of code snippits, without an underlying database I could query myself?

I found myself in a "chicken or egg" problem $-$ I needed access to a database so I could continue learning, but I needed to be good at SQL to get hired and access databases to practice on.

In this post, we'll create a database for you to play with. Then we'll explore a few intermediate SQL topics, the sort of techniques you'll likely utilize as a data scientist. If you understand the below query, then you're prepared for the rest of this post.

{% include header-sql.html %}
```sql
SELECT
    s.id AS student_id,
    e.score
FROM
    students AS s
LEFT JOIN
    exams AS e
    ON s.id = e.student_id
WHERE
    e.grade > 90;
```

## Setting up
When learning a new language, practice is critical. It's one thing to read this post and nod along, and another to be able to explore ideas on your own. So let's first set up a database on your computer. While it sounds intimidating, it'll actually be straightforward.

The first step is to install SQL on your computer. We'll use [PostgreSQL (Postgres)](https://www.postgresql.org/), a common dialect in data science. We go to the [download page](https://www.postgresql.org/download/), select our operating system (e.g. Windows), and then run the installation. If you set a password on your database, keep it handy for the next step!  (Since our database won't be public, it's fine to use a simple password like `admin`.)

<center>
<img src="{{  site.baseurl  }}/images/data_engineering/intermediate_sql/download.png" width="70%" height="70%">
</center>

The next step is to install [PGAdmin](https://www.pgadmin.org/), a graphical user interface (GUI) that makes it easy to interact with our PostgreSQL database(s). We do this by going to the [installation page](https://www.pgadmin.org/download/), clicking the link for our operating system, and then following the steps.

Once it's installed, we open PGAdmin and click on "Add new server." This step actually sets up a connection to an _existing_ server, which is why we needed to install Postgres first. I named my server `home` and passed in the password I defined during the Postgres installation.

We're now ready to create some tables! Let's create a set of tables that describe the data a school might have: students, classrooms, and grades. We'll model our data such that a classroom consists of multiple students, each which has multiple grades.

We could do all this with the GUI, but we'll instead write code to make our workflow repeatable. To write the queries that will create our tables, we'll right click on postgres (under home > Databases (1) > postgres) and then click on Query Tool.

<img src="{{  site.baseurl  }}/images/data_engineering/intermediate_sql/pgadmin1.png">

Let's start by creating the `classrooms` table. We'll keep this table simple: it'll just consist of an `id` and the `teacher` name. Type the following code into the query tool and hit run.

{% include header-sql.html %}
```sql
DROP TABLE IF EXISTS classrooms;

CREATE TABLE classrooms (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    steacher VARCHAR(100)
);
```

The first line, `DROP TABLE IF EXISTS classrooms`, deletes the `classrooms` table if it already exists. Adding a `DROP TABLE IF EXISTS` line before `CREATE TABLE` opens us up to codifying our database schema in one script, which is particularly handy if we decide to change our database in some way down the road $-$ ad a table, change the datatype of a column, etc. We can simply store the instructions for generating our database in a script, update that script when we want to make a change, and then rerun it. The `DROP TABLE` line(s) will clean up the previous versions of our table(s).

(Note: codifying our database is an engineering best practice, but this doesn't pertain to the _data_ in those tables $-$ for that, we'll want to periodically back up our data. we'll still want to store _backups_ of our data, since we don't want to codify each row!)

Line 4 may also catch your eye: here we specify that `id` is the primary key, meaning each row must contain a value in this column, and that each value must be unique. `GENERATED ALWAYS AS IDENTITY` is an alternative to the [sequence](https://www.postgresql.org/docs/9.5/sql-createsequence.html) syntax $-$ since we don't want to have to keep track of which `id` values have already been used, we allow Postgres to handle setting the `id`. As a result, when inserting data into this table, we only need to provide the `teacher` names.

Finally, on line 5 we specify that `teacher` is a string with a maximum length of 100 characters.<sup>[[1]](#1-setting-up)</sup>.

Let's now create the `students` table. Our table will consist of a unique `id`, the student's `name`, and a [**foreign key**](https://www.postgresqltutorial.com/postgresql-foreign-key/) that points to `classrooms`.

{% include header-sql.html %}
```sql
DROP TABLE IF EXISTS students;
CREATE TABLE students (
	id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(100),
	classroom_id INT,
	CONSTRAINT fk_classrooms
		FOREIGN KEY(classroom_id)
		REFERENCES classrooms(id)
);
```

The foreign key is important. If we try to insert a row into `students` and refernece a classroom that doesn't yet exist, we'll get an error.

{% include header-sql.html %}
```sql
INSERT INTO students (name, classroom_id)
VALUES ('Matt', 1);
/*
ERROR:  insert or update on table "students" violates foreign key constraint "fk_classrooms"
DETAIL:  Key (classroom_id)=(1) is not present in table "classrooms".
SQL state: 23503
*/
```

So let's first create some classrooms and view the results.

{% include header-sql.html %}
```sql
-- Insert rows
INSERT INTO classrooms
    (teacher)
VALUES
    ('Mary'),
    ('Jonah');

SELECT * FROM classrooms;
/*
  id  | teacher
  --- | -------
    1 | Mary
    2 | Jonah
 */
```

Now we can create students that belong to classrooms.

{% include header-sql.html %}
```sql
-- Insert rows
INSERT INTO students
    (name, classroom_id)
 VALUES
    ('Adam', 1),
    ('Betty', 1),
    ('Caroline', 2);

-- Pull rows
SELECT * FROM students;
/*
  id  | name     | classroom_id
  --- | -------- | ------------
    1 | Adam     |           1
    2 | Betty    |           1
    3 | Caroline |           2
 */
```

{% include header-sql.html %}
```sql
-- Join the tables
SELECT
    *
FROM
    student AS s
INNER JOIN
    classroom AS c
    ON s.classroom_id = c.id;
```


So here's something we can do. We can stay in Python and create a SQLite DB, then run queries against it. Or we can install an RDBMS like PSequel or whatever and execute queries there.

We'll also focus on `SELECT` queries, the "Read" in CRUD.

Good "reading list" of beginner vs. intermediate SQL: https://softwareengineering.stackexchange.com/questions/181651/are-these-sql-concepts-for-beginners-intermediate-or-advanced-developers

Can also think about self joins: https://www.w3schools.com/sql/sql_join_self.asp


## Basic SQL
Check out [this post on SQL vs. NoSQL databases]({{  site.baseurl  }}/SQL_vs_NoSQL) to learn more about database theory.

## Filters
`WHERE` is applied before aggregation steps, while `HAVING` is applied after.

{% include header-sql.html %}
```sql
SELECT
    id,
    AVG(grade)
FROM
    students
WHERE
    classroom_id = 5
GROUP BY
    id
HAVING
    AVG(grade) > 90;
```

## `CASE WHEN`
It's common to need to perform some kind of `if`-`else` logic on a column. You could do something like this:

{% include header-sql.html %}
```sql
SELECT
    id,
    grade,
    CASE
        WHEN grade < 60 THEN 'F'
        WHEN grade < 70 THEN 'D'
        WHEN grade < 80 THEN 'C'
        WHEN grade < 90 THEN 'B'
        ELSE 'A'
    END AS letter_grade
FROM
    students;

/*
| id  | grade | letter_grade |
| --- | ----- | ------------ |
| 123 |  A    | 93           |
| 817 |  C    | 77           |
| 550 |  B    | 89           |
| ... | ...   | ...          |
*/
```

You can also use it for exact equality, or `IN` statements.

```sql
SELECT
    CASE
        WHEN name IN ('Matt', 'John') THEN 'Friends'

```

## `WITH`
Queries can become long, especially when you're joining data from multiple tables, and you want to apply filters or aggregations to tables before joining. Sometimes you have the luxury of being able to perform part of the query in SQL and the remainder in Python, or to perform multiple queries (e.g. on temporary tables). But when you don't, you need to _nest_ queries.

Let's say we're trying to find all the names in the `cats` table that also appear in the `dogs` table. Our query will require a subquery: finding all the names in dogs.

There are two ways to get these dog names. We'll start with the method I try to avoid.

{% include header-sql.html %}
```sql
SELECT
    name
FROM
    cats
WHERE
    name IN (
        SELECT
            name
        FROM
            dogs
    );
```

Above, our query does X.

But we can make our query more modular and hence easier to read with the `WITH` clause.

{% include header-sql.html %}
```sql
WITH dog_names AS (
    SELECT
        name
    FROM
        dogs
)
SELECT
    name
FROM
    cats
WHERE
    name IN (SELECT name FROM dog_names);
```

This might seem like more work compared to above, but it serves two purposes: making our code easier to understand by separating out our subqueries, and setting us up to build more complex queries.

Let's say, for example, that our subquery isn't simply selecting a row from a table. Perhaps it has some groupby's and joins with another subquery's table.

{% include header-sql.html %}
```sql
WITH top_students AS (
    SELECT
        id,
        AVG(grade)
    FROM
        students
    WHERE
        grade IS NOT NULL
        AND classroom_id IS NOT NULL
    GROUP BY
        id
    ORDER BY
        AVG(grade) DESC
    LIMIT
        10
),
chicago_classrooms AS (
    SELECT
        id
    FROM
        classrooms
    WHERE
        city = 'Chicago'
)
SELECT
    name
FROM
    students
WHERE
    id IN (
        SELECT id FROM top_students
    )
    AND classroom_id IN (
        SELECT id FROM chicago_classrooms
    );
```

[**LC 1412:** Find the Quiet Students in All Exams](https://leetcode.com/problems/find-the-quiet-students-in-all-exams). The premise is that we have `Student` and `Exam` tables, and we want to find the students who meet the following criteria:
1. Took at least one exam
2. Never scored the highest or lowest on an exam.

{% include header-sql.html %}
```sql
-- Get the highest and lowest exam scores
WITH hl_exams AS (
    SELECT
        exam_id,
        MIN(score) AS min_score,
        MAX(score) AS max_score
    FROM
        Exams
    GROUP BY
        exam_id
),

-- Get the students who scored highest or lowest on the exams
hl_students AS (
    SELECT
        student_id
    FROM
        Exam
    INNER JOIN
        hl_exams
    ON
        Exam.exam_id = hl_exams.exam_id
        AND
        (Exam.score = hl_exams.min_score
        OR Exam.score = hl_exams.max_score)
)

SELECT
    student_id,
    student_name
FROM
    Student
WHERE
    -- Student took at least one exam
    student_id IN (
        SELECT student_id FROM Exams
    )
    AND
    -- Student not highest or lowest score
    student_id NOT IN (
        SELECT student_id FROM hl_students
    )
```

## Self joins
Let's say we want to match all users from a city that are together.

## Conclusions
This post was an overview of some SQL skills that become useful once you're beyond the basics.

## Footnotes
#### 1. [Setting up](#setting-up)
We specified the `teacher` column as a string with a max of 100 characters since we don't think we'll run into names longer than this. But are we actually saving on storage space if we limit rows to 100 characters versus 200 or 500?

In Postgres it turns out it [technically doesn't matter](https://stackoverflow.com/questions/1067061/does-a-varchar-fields-declared-size-have-any-impact-in-postgresql) whether we specify 10, 100, or 500. So specifying a limit might be more of a best practice for communicating to future engineers (including yourself) what your expectations are for the data in this column.

But in MySQL [the size limit _does_ matter](https://stackoverflow.com/questions/1962310/importance-of-varchar-length-in-mysql-table): temporary tables and `MEMORY` tables will store strings of equal length padded out to the maximum specified in the table schema, meaning a `VARCHAR(1000)` will waste a lot of space if none of the values approach that limit.
