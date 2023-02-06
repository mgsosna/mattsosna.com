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
Take a look at the query below. We have two tables, `customers` and `orders`. `customers` contains customer IDs and the "tier" they're in -- bronze, silver, or gold. `orders` contains order ID, customer ID, a review of the item purchased, and its purchase price.

```sql
WITH customers(id, tier) AS (
    VALUES
    (100, 'bronze'),
    (200, 'gold'),
    (300, 'gold'),
    (400, 'silver')
),
orders(id, customer_id, review, price) AS (
    VALUES
    (1, 100, 'It was great!', 99.99),
    (2, 100, 'I loved it!', 49.99),
    (3, 200, NULL, 99.99),
    (4, 300, NULL, 129.99),
    (5, 300, 'Free pills! Click here.', 199.99),
    (6, 400, 'Loved it!', 39.99),
    (7, 400, NULL, 39.99),
    (8, 400, 'Hated it!', 39.99)
)
...
```

Now let's say we want to calculate the total dollars spent by customer tier. We filter the `orders` table to remove a spam review about pills before joining.

Predict what the resulting query will look like.

{% include header-sql.html %}
```sql
...
SELECT
    c.tier,
    SUM(o.price)
FROM customers c
LEFT JOIN orders o
    ON c.id = o.customer_id
WHERE
    o.review != 'Free pills! Click here.'
GROUP BY
    1
ORDER BY
    1
```

Ready? Here's what comes out.

| **tier** | **sum** |
| --- | --- |
| bronze | 149.98 |
| silver | 79.98 |
{:.mbtablestyle}  

Wait a minute. Where did gold tier go? The calculation for silver tier is also wrong: it should be $119.17.

The issue, it turns out, is due to [**the order of filtering in `WHERE` vs. `ON`**](https://mode.com/sql-tutorial/sql-joins-where-vs-on/)**.** Normally, filtering occurs after the tables are joined. But sometimes you want to filter the two tables before they join. When there's a filter in `ON`, then it's like a `WHERE` that's applied to only one of the tables.

What happens above is that NULLs are filtered out. But watch what we get when we do it this way.

Example [here](https://trevorscode.com/why-is-my-left-join-behaving-like-an-inner-join-and-filtering-out-all-the-right-side-rows/) is really good.
