---
layout: post
title: Surprises from starting an MLE job in big tech
author: matt_sosna
---

What I thought I'd need:
* Expertise in the details of Docker, AWS, etc.

What I actually need:
* Expert investigative skills
  - Logs!
  - Documentation
  - Not being afraid to ask people
* Extreme patience
  - There's no real way around it: onboarding is challenging. There's just so much to learn.

### 1. Expert-level investigative skills
The thing to remember

* Absolute fearlessness when it comes to looking through logs
* "Getting to the bottom of it." Following the trail.
* No one actually knows everything. If they do, they're probably extremely busy and high-up. (If they are and they're willing to talk to you, hold onto them! Set up 1:1's if you can.)

### 2. Really good at SQL
SQL queries will become super complex. There are some I've dealt with that are over 500 lines. This is just how it is when dealing with big data $-$ you need to perform as much of the processing as possible at the database level before moving things to your machine. (Or the one you've comandeered in the cloud.) One of the queries I ran joined a table with over 1.5 trillion rows.

Your queries also need to become efficient. e.g.

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

While it looks good on paper, that's probably the least-efficient way to find the ten highest-scoring IDs. The `ORDER BY` line sorts the entire table, an operation that takes $O(nlogn)$ time.

Rather, you need to use additional information wherever possible. Do you know the distribution of the predictions? Then try using a `WHERE` clause to filter out rows below a threshold.

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

Another thing is randomly sampling rows. There are also multiple ways to do this that vary in efficiency.

Also getting good at Airflow / DAGs. Pipelines will have dependencies, which will have dependencies. Being able to follow the trail is important.
