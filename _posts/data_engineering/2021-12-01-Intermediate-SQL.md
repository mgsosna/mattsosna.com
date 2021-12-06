---
layout: post
title: Intermediate SQL
author: matt_sosna
---

When I was learning SQL, I found it hard to progress beyond the absolute basics.

So here's something we can do. We can stay in Python and create a SQLite DB, then run queries against it. Or we can install an RDBMS like PSequel or whatever and execute queries there.

We'll also focus on `SELECT` queries, the "Read" in CRUD.

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
