---
layout: post
title: SQL Riddles to Test You
author: matt_sosna
tags: sql
---

SQL is a deceptively simple language. Across its many dialects, you can query databases in a vernacular similar to English. **What you see is what you get... until you don't.**

Every now and then, I come across a query that produces a result completely different from what I expect, teaching me little nuances about the language. I've compiled three recent head-scratchers in this post, and I've arranged them as riddles to make them more interesting. Try to figure out the answer before reading the end of each section!

I've also included quick [**common table expressions (CTEs)**](https://learnsql.com/blog/what-is-common-table-expression/) to generate the table in each example, so you don't need to try querying your company's production tables! But to get really comfortable with SQL, I recommend creating your own database and tables. Check out [this post]({{  site.baseurl  }}/Intermediate-SQL) to learn how.

Finally, an obligatory side note that the actual data and topics in each query are just illustrative examples. 🙂

## Riddle 1: Timestamps
Imagine we have a table called `purchases` with purchase IDs, amounts, and times the purchase were made. Let's say it looks like this:

| **transaction_id** | **amount** | **dt** |
| --- | --- | -- |
| 1 | 0.99 | 2023-02-15 00:00:00 |
| 2 | 9.99 | 2023-02-15 07:15:00 |
| 3 | 15.99 | 2023-02-15 23:01:15 |
| 4 | 7.99 | 2023-02-16 14:22:09 |
{:.mbtablestyle}

As a CTE, this would look something like this. Note that we need to specify that the `dt` column is a timestamp so it isn't interpreted as a string. We also only need to specify the data types for one of the rows; the rest are inferred.

{% include header-sql.html %}
```sql
WITH purchases(transaction_id, amount, dt) AS (
    VALUES
    (1::bigint, 0.99::float, '2023-02-15 00:00:00 GMT'::timestamp),
    (2, 9.99, '2023-02-15 07:15:00 GMT'),
    (3, 15.99, '2023-02-15 23:01:15 GMT'),
    (4, 7.99, '2023-02-16 14:22:09 GMT')
)
...
```

Now let's calculate the sum of purchases made on Feb 15. We can write a query like the one below:

{% include header-sql.html %}
```sql
...
SELECT
    SUM(amount) AS sum
FROM purchases
WHERE
    dt = '2023-02-15'
```

We mysteriously receive the following response.

| **sum** |
| --- |
| 0.99 |
{:.mbtablestyle}

What happened? There were three purchases made on Feb 15: transaction IDs 1, 2, and 3. The sum should therefore be \$26.97. Instead, only the first purchase was counted.

### Hint
If you change the filter to `2023-02-16`, no rows are returned.

### Answer
The `dt` column is a timestamp that includes both date and time. Our `WHERE` filter only specifies the date. Rather than rejecting this query, Postgres automatically reformats the date string to `2023-02-15 00:00:00`. This matches only the first transaction in the table. We're therefore taking only the sum of one row.

If we wanted to select all rows corresponding to Feb 15, we should first cast the timestamp to date.

{% include header-sql.html %}
```sql
SELECT
    SUM(amount) AS sum
FROM purchases
WHERE
    DATE(dt) = '2023-02-15'
```

We now get the expected result.

| **sum** |
| --- |
| 26.97 |
{:.mbtablestyle}

## Riddle 2: Dependent vs. independent filters
Alright, next riddle. The goal of the query is to **remove all rows that meet _any one_ of three conditions.** In the table below, for example, let's say that we want to only return tenured and active users, i.e., ones who _have_ logged in during the last 28 days, _have_ posted before, and are _not_ a new account.

| **user_id** |**no_login_l28**| **has_never_posted** | **is_new_account** |
| -- | -- |
| 1 | True | True | True |
| 2 | True | True | False |
| 3 | True | False | True |
| 4 | True | False | False |
| 5 | False | True | True |
| 6 | False | True | False |
| 7 | False | False | True |
| 8 | False | False | False |
{:.mbtablestyle}  

In other words, we want our query to only user 8, who has False values for `no_login_l28`, `has_never_posted`, and `is_new_account`.

Let's start with the top of our query.

{% include header-sql.html %}
```sql
WITH tab(user_id, no_login_l28, has_never_posted, is_new_account) AS (
    VALUES
    (1, True, True, True),
    (2, True, True, False),
    (3, True, False, True),
    (4, True, False, False),
    (5, False, True, True),
    (6, False, True, False),
    (7, False, False, True),
    (8, False, False, False)
)
SELECT
    user_id
FROM tab
WHERE
    ...
```

How should we structure the `WHERE` clause of our query? Think for a minute -- **we need to be careful not to return rows where _any_ of the columns is `False`.**

When you're ready, take a look at the options below. **Two are correct and two are wrong.**

**Option 1: Multiple `AND NOT`**
{% include header-sql.html %}
```sql
WHERE
    NOT no_login_l28
    AND NOT has_never_posted
    AND NOT is_new_account
```

**Option 2: Multiple `OR NOT`**
{% include header-sql.html %}
```sql
WHERE
    NOT no_login_l28
    OR NOT has_never_posted
    OR NOT is_new_account
```

**Option 3: `NOT` + grouped `OR`**
{% include header-sql.html %}
```sql
WHERE
    NOT (
        no_login_l28
        OR has_never_posted
        OR is_new_account
    )
```

**Option 4: `NOT` + grouped `AND`**
{% include header-sql.html %}
```sql
WHERE
    NOT (
        no_login_l28
        AND has_never_posted
        AND is_new_account
    )
```

### Hint
When are conditions in a filter evaluated separately versus together? If they're evaluated together, can we condense all conditions down to one `True` or `False` value?

### Answer
**Option 1.** This one tripped me up a bit. A data scientist on my team submitted a PR with this filter, which I was convinced would pull in rows 2-8 because the query would require a user to have `False` values for all three columns. But to my surprise, Option 1 actually works **because the three filters are evaluated independently.** ✅

**Option 2.** This was the filter I initially thought was correct, since I didn't realize the filters would be evaluated independently. But this filter will actually return users 2-8, since anyone who has at least one `True` for `no_login_l28`, `has_never_posted`, and `is_new_account` will be allowed through. ❌

**Option 3.** This was how I initially thought the filter needed to be worded. If a user has `True` for _any_ of `no_login_l28`, `has_never_posted`, or `is_new_account`, then lines 3-5 evaluate to `True`, the `NOT` flips this to `False`, and those rows are ultimately excluded. This indeed works, and I find this easier to understand than Option 1, but both are valid. ✅

**Option 4.** This returns the same incorrect result as Option 2. Lines 3-5 evaluate to `True` only for user 1, meaning that when we flip the boolean with `NOT`, all remaining users are pulled through. ❌

## Riddle 3: Left joins acting like inner joins
Take a look at the query below. We have two tables, `customers` and `reviews`. `customers` contains customer IDs and their lifetime dollars spent on the platform.

| **id** | **total_spend** |
| --- | --- |
| 100 | 1583.49 |
| 200 | 8739.03 |
| 300 | 431.00 |
| 400 | 1.00 |
| 500 | 22.27 |
{:.mbtablestyle}

`reviews` contains information about reviews left by customers: the review ID, customer ID, and whether the review was reported as spam.

| **id** | **customer_id** | **reported_as_spam** |
| --- | --- | -- |
| 1 | 100 | False |
| 2 | 100 | False |
| 3 | 400 | True |
| 4 | 400 | True |
| 5 | 500 | False |
{:.mbtablestyle}

Here's the subquery to generate the two CTEs:

{% include header-sql.html %}
```sql
WITH customers(id, total_spend) AS (
    VALUES
    (100, 1583.49),
    (200, 8739.03),
    (300, 431.00),
    (400, 1.00),
    (500, 22.27)
),
reviews(id, customer_id, reported_as_spam) AS (
    VALUES
    (1, 100, False),
    (2, 100, False),
    (3, 400, True),
    (4, 400, True),
    (5, 500, False)
)
...
```

Now let's say we're curious about the relationship between a customer's total spend and the number of non-spam reviews they write. Since not each customer has left a review, we'll want to left join `reviews` to `customers`. We can structure our query like this:

{% include header-sql.html %}
```sql
...
SELECT
    c.id,
    c.total_spend,
    COALESCE(COUNT(r.id), 0) AS n_reviews
FROM customers c
LEFT JOIN reviews r
    ON c.id = r.customer_id
WHERE
    NOT r.reported_as_spam
GROUP BY
    1, 2
ORDER BY
    1
```

Ready? Here's what comes out.

| **id** | **total_spend** | **n_reviews** |
| --- | --- | --- |
| 100 | 1583.49 | 2
| 500 | 22.27 | 1
{:.mbtablestyle}  

Wait a minute. Where did users 200, 300, and 400 go? Why were they removed, and how can we bring them back in?

### Hint
If you create a CTE for `reviews` with spam reviews filtered out, _then_ join on this CTE, do we get the same result?

### Answer
Looking closely, we can see that users 200 and 300 have never left any reviews. 400 only has spam reviews, but they were completely removed as well. Since we did a left join, these users should still be in the table and have a 0 for `n_reviews`. Instead, our left join [behaved like an inner join](https://trevorscode.com/why-is-my-left-join-behaving-like-an-inner-join-and-filtering-out-all-the-right-side-rows/).

The issue, it turns out, is due to [**the order of filtering in `WHERE` vs. `ON`**](https://mode.com/sql-tutorial/sql-joins-where-vs-on/)**.** `WHERE` clauses are evaluated _after_ joins. Our left join brings in null values for `reported_as_spam` for users 200 and 300. The `WHERE` filter then removes all rows where `reported_as_spam` is True, which removes user 400. However, this filter also removes null values, so users 200 and 300 are also removed.

To do this properly, we need to pre-filter `reviews` before joining with `customers`. As the hint states, we can create a CTE for `reviews` and perform the filtering there. But more efficiently, let's perform the filtering _within_ the join.

We can do this by adding `AND NOT r.reported_as_spam` to the `LEFT JOIN` block. See below:

{% include header-sql.html %}
```sql
...
SELECT
    c.id,
    c.total_spend,
    COALESCE(COUNT(r.id), 0) AS n_reviews
FROM customers c
LEFT JOIN reviews r
    ON c.id = r.customer_id
    AND NOT r.reported_as_spam
GROUP BY
    1, 2
ORDER BY
    1
```

Now we get the expected result.

| **id** | **total_spend** | **n_reviews** |
| --- | --- | --- |
| 100 | 1583.49 | 2
| 200 | 8739.03 | 0
| 300 | 431.00 | 0
| 400 | 1.00 | 0
| 500 | 22.27 | 1
{:.mbtablestyle}
