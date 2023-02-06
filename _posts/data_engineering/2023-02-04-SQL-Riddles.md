---
layout: post
title: SQL Riddles to Test You
author: matt_sosna
tags: sql
---

### Riddle 1: Dependent vs. independent filters
I came across this one recently. The goal of the query is to **remove all rows that meet _any one_ of three conditions.** In the table below, for example, let's say that we want to only return active users, i.e., ones who _have_ logged in during the last 28 days, _have_ posted before, and are _not_ a new account.

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

Let's start with the top of our query. We'll define these rows in a subquery so we don't need to create a new table just for this exercise. (But if you want to, check out [this post]({{  site.baseurl  }}/Intermediate-SQL).)

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

How should we structure the `WHERE` clause of our query? Think for a minute -- **we need to be careful not to return rows where _any_ of the columns is `False`.** When you're ready, take a look at the options below. Two are correct and two are wrong.

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

Ready for the answers? Alright, here we go.

**Option 1.** This one tripped me up a bit. A data scientist on my team submitted a PR with this filter, which I was convinced would pull in rows 2-8 because the query would require a user to have `False` values for all three columns. But to my surprise, Option 1 actually works **because the three filters are evaluated independently.** ✅

**Option 2.** This was the filter I initially thought was correct, since I didn't realize the filters would be evaluated independently. But this filter will actually return users 2-8, since anyone who has at least one `True` for `no_login_l28`, `has_never_posted`, and `is_new_account` will be allowed through. ❌

**Option 3.** This was how I initially thought the filter needed to be worded. If a user has `True` for _any_ of `no_login_l28`, `has_never_posted`, or `is_new_account`, then lines 3-5 evaluate to `True`, the `NOT` flips this to `False`, and those rows are ultimately excluded. Indeed, this works, and I find this easier to understand than Option 1, but both are valid. ✅

**Option 4.** This returns the same incorrect result as Option 2. Lines 3-5 evaluate to `True` only for user 1, meaning that when we flip the boolean with `NOT`, all remaining users are pulled through. ❌

### Riddle 2: Joins with `WHERE` vs. `ON`
Take a look at the query below. We have two tables, `customers` and `reviews`. `customers` contains customer IDs and their total spend. `reviews` contains information about reviews left by customers: the review ID, customer ID, and whether the review was reported as spam.

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

Now let's say we want a query that adds the number of non-spam reviews written by each customer. Since not each customer has left a review, we'll want to left join `reviews` to `customers`. We can structure our query like this:

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

Wait a minute. Where did users 200, 300, and 400 go? Looking closely, we can see that users 200 and 300 have never left any reviews. 400 only has spam reviews, but they were completely removed as well. Since we did a left join, these users should still be in the table and have a 0 for `n_reviews`. Instead, our left join [behaved like an inner join](https://trevorscode.com/why-is-my-left-join-behaving-like-an-inner-join-and-filtering-out-all-the-right-side-rows/).

The issue, it turns out, is due to [**the order of filtering in `WHERE` vs. `ON`**](https://mode.com/sql-tutorial/sql-joins-where-vs-on/)**.** Normally, filtering occurs after the tables are joined. But sometimes you want to filter the two tables before they join. When there's a filter in `ON`, then it's like a `WHERE` that's applied to only one of the tables.

To do this properly, we need to pre-filter `reviews` before joining with `customers`. We can do this by adding `AND NOT r.reported_as_spam` to the `LEFT JOIN` block. See below:

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
