---
layout: post
title: Intermediate SQL
author: matt_sosna
---

When I started learning SQL, I found it hard to progress beyond the absolute basics. I loved [DataCamp's courses](https://www.datacamp.com/courses/introduction-to-sql) because I could just type the code directly into a console on the screen. But once the courses ended, how could I practice what I learned? And how could I continue improving, when all the tutorials I found just consisted of code snippits, without an underlying database I could query myself?

I found myself in a "chicken or egg" problem $-$ I needed access to a database so I could practice SQL and continue learning, but I needed to be good at SQL to get hired and be granted access to databases to practice on.

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

The first step is to install SQL on your computer. We'll use [PostgreSQL (Postgres)](https://www.postgresql.org/), a common dialect. We go to the [download page](https://www.postgresql.org/download/), select our operating system (e.g. Windows), and then run the installation. If you set a password on your database, keep it handy for the next step!  (Since our database won't be public, it's fine to use a simple password like `admin`.)

<center>
<img src="{{  site.baseurl  }}/images/data_engineering/intermediate_sql/download.png" width="70%" height="70%">
</center>

The next step is to install [PGAdmin](https://www.pgadmin.org/), a graphical user interface (GUI) that makes it easy to interact with our PostgreSQL database(s). We do this by going to the [installation page](https://www.pgadmin.org/download/), clicking the link for our operating system, and then following the steps.

Once it's installed, we open PGAdmin and click on "Add new server." This step actually sets up a connection to an _existing_ server, which is why we needed to install Postgres first. I named my server `home` and passed in the password I defined during the Postgres installation.

We're now ready to create some tables! To do so, click on `home` > Databases (1) > postgres > Schemas (1) > Public > Tables > Create > Table.

<img src="{{  site.baseurl  }}/images/data_engineering/intermediate_sql/pgadmin1.png">

Let's start with a table called `student` with the columns `id`, `name`, and `classroom_id`. `id` will be the primary key and therefore non-nullable. In other words, for a student to be added to this table, he or she needs an `id` for the write to complete. We'll create a sequence that auto-increments for us.

We can do this with the GUI, but it's more reproducible and I think easier and quite a bit faster if we write it with code. Right click on tables and select "Query Editor." Then type this:

{% include header-sql.html %}
```sql
-- Create incrementing sequence
CREATE SEQUENCE student_seq;

-- Define 'student' table
CREATE TABLE student (
    id INT DEFAULT nextval('student_seq'::regclass),
	name VARCHAR,
	classroom_id INT
);

-- Insert rows
INSERT INTO student
 	(id, name, classroom_id)
 VALUES
 	(1, 'Adam', 1),
 	(2, 'Betty', 1),
 	(3, 'Caroline', 2);

-- Pull rows
SELECT * FROM student;
```

Let's now create a `classroom` table and relate the two.

{% include header-sql.html %}
```sql
-- Create another sequence
CREATE SEQUENCE classroom_seq;

-- Create classroom table
CREATE TABLE classroom (
	id INT DEFAULT nextval('classroom_seq'::regclass),
	teacher VARCHAR
);

-- Insert rows
INSERT INTO classroom
	(teacher)
VALUES
	('Mary'),
	('Jonah');

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
