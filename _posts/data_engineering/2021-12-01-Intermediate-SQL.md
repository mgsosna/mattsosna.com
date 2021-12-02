---
layout: post
title: Intermediate SQL
author: matt_sosna
---

When I was learning SQL, I found it hard to progress beyond the absolute basics.

So here's something we can do. We can stay in Python and create a SQLite DB, then run queries against it. Or we can install an RDBMS like PSequel or whatever and execute queries there.

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
