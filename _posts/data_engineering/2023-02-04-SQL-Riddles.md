---
layout: post
title: SQL Riddles to Test You
author: matt_sosna
tags: sql
---

## Dependent vs. independent filters
I came across this one recently. The goal of the query is to filter out all rows that meet _any one_ of three conditions. In the table below, for example, let's say that we want to only return active users, i.e., ones who _have_ logged in during the last 28 days, _have_ posted before, and are _not_ a new account.

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

How should we structure the `WHERE` clause of our query? Think for a minute -- **we need to be careful not to return rows where _any_ of the columns is `False`.** When you're ready, take a look at the options below.

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

**Option 2.** This was the filter I initially thought was correct. 
