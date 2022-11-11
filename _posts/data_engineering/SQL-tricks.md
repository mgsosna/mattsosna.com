---
layout: post
title: SQL tricks
tags: sql
---

Your queries need to become efficient. For example, let's say we have a table of model predictions and we want to take the 100 highest-scoring rows. One approach would be to sort the table by `score`, then take the top 100.

{% include header-sql.html %}
```sql
SELECT
    id,
    score
FROM
    predictions
ORDER BY
    score DESC
LIMIT
    100;
```

While it looks good on paper, that's probably the least-efficient way to find the ten highest-scoring IDs. The `ORDER BY` line sorts the entire table, an operation that takes $O(nlogn)$ time. We're also processing a lot of rows we probably don't care about $-$ if our table is a million rows, 99.99% of our compute is essentially unnecessary.

Rather, you need to use additional information wherever possible. Do you know the distribution of the predictions? Then try using a `WHERE` clause to filter out rows below a threshold.

{% include header-sql.html %}
```sql
SELECT
    id,
    score
FROM
    predictions
WHERE
    score > 0.7
ORDER BY
    score DESC
LIMIT
    100;
```
