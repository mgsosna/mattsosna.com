---
layout: post
title: How to enter data science - <br>4. The engineering
author: matt_sosna
summary: The software engineering skills needed to succeed in data science
image: ""
---

Welcome to the fourth post in our series on how to enter data science! So far, we've covered [the range of data science roles]({{  site.baseurl  }}/DS-transition-1), some [inferential statistics fundamentals]({{  site.baseurl  }}/DS-transition-2), and [manipulating and analyzing data]({{  site.baseurl  }}/DS-transition-3). This post will focus on software engineering concepts that are essential for data science.

---
**How to enter data science:**
1. [The target]({{  site.baseurl  }}/DS-transition-1)
2. [The statistics]({{  site.baseurl  }}/DS-transition-2)
3. [The analytics]({{  site.baseurl  }}/DS-transition-3)
4. **The engineering**
5. The people *(coming soon)*

---

## The code *around* your code
The programming concepts in the [last post]({{  site.baseurl  }}/DS-transition-3) covered how to work with data once it's sitting in front of you. If your role involves clicking and dragging a CSV from a shared Google Drive onto your desktop, analyzing it in a Jupyter Notebook, then typing up a report and sending an email, then the last post is probably sufficient for your role.

Yet, what happens when you start a project that requires combining data from *hundreds* of CSVs? Clicking and dragging can only get you so far $-$ even if you have the patience, your manager likely doesn't, and it's only a matter of time before you have to access data through an [API](#interacting-with-apis) that doesn't have a nice user interface.

Similarly, maybe you're assigned to a project with *an existing codebase*, with programmers that expect best practices when handling the code. While one-off scripts might have cut it during school,<sup>[[1]](#1-the-code-around-your-code)</sup> [you're living on borrowed time](https://en.wikipedia.org/wiki/Technical_debt) if you don't organize your code in a way that's easily read, reused, and modified by others.

This is where programming skills *outside* of analyzing data come in. Returning to our [drilling machine example]({{  site.baseurl  }}/DS-transition-3/#machine-learning) from the last post, this post is about building the machinery *around* the drill that is analytics. We'll cover **Software Engineering** in this post; **Inferential Statistics** was [two posts ago]({{  site.baseurl  }}/DS-transition-2), and **Analytics** was [the last post]({{  site.baseurl  }}/DS-transition-3).

* **Inferential Statistics**
- [ ] [Experimental design]({{  site.baseurl  }}/DS-transition-2/#experimental-design)
- [ ] [Comparisons between groups]({{  site.baseurl  }}/DS-transition-2/#comparisons-between-groups)
- [ ] [Predictive modeling]({{  site.baseurl  }}/DS-transition-2/#predictive-modeling)
- [ ] [Model internals]({{  site.baseurl  }}/DS-transition-2/#model-internals) <br><br>
* **Analytics**
- [ ] [Dataframes]({{  site.baseurl  }}/DS-transition-3/#programming)
- [ ] [Arrays]({{  site.baseurl  }}/DS-transition-3/#arrays)
- [ ] [Visualizations]({{  site.baseurl  }}/DS-transition-3/#visualizations)
- [ ] [Descriptive statistics]({{  site.baseurl  }}/DS-transition-3/#descriptive-statistics)
- [ ] [Working with dates and time]({{  site.baseurl  }}/DS-transition-3/#working-with-dates-and-time)
- [ ] [Machine learning]({{  site.baseurl  }}/DS-transition-3/#machine-learning) <br><br>
* **Software engineering**
- [ ] [Accessing data](#accessing-data)
- [ ] [Version control](#version-control)
- [ ] [Object-oriented programming](#object-oriented-programming)
- [ ] [Virtual environments](#virtual-environments)
- [ ] [Writing tests](#writing-tests)
- [ ] [Servers and deployment](#servers-and-deployment) <br><br>
{: style='list-style-type: none'}

### Accessing data
We'll start with a skill that spans the entire [analytics-engineering spectrum]({{  site.baseurl  }}/DS-transition-1/#the-scalpel-versus-the-shovel), but I'd argue is more of an "engineering" skill than an analytical one. As a data scientist, you'll rarely access data through the click-based graphical user interfaces of Google Drive or Dropbox. Instead, the majority of the data you'll access will reside in SQL (Structured Query Language) databases or at APIs (Application Programming Interfaces).

#### SQL
Unless your company is tiny, it's going to have more data than can fit onto one laptop. Further, the data will need to be organized in a way that optimizes storage space and retrieval time, as well as lets multiple users read (and write) the data simultaneously. The main way to do this is with [relational databases](https://en.wikipedia.org/wiki/Relational_database), which you query with SQL.<sup>[[2]](#2-sql)</sup>

There isn't a huge amount to SQL, and it's an area that you'll repeatedly use, so it's good to polish this skill. While you likely won't be *creating* databases or tables $-$ that's more in the realm of a [data engineer](https://www.xplenty.com/blog/data-engineering-what-does-a-data-engineer-do-how-do-i-become-one/) $-$ you'll definitely be querying data, and possibly writing to the database. We'll focus on how to query here: joining data from multiple tables, filtering rows, and performing aggregations.

The below query is a simple example in [Postgres](https://www.postgresql.org/), one of the major SQL dialects.

```sql
    SELECT u.name AS user_name,
           AVG(g.score) AS avg_score
      FROM users AS u
INNER JOIN grades AS g
        ON u.id = g.user_id
     WHERE AVG(g.score) > 90
  GROUP BY u.id
  ORDER BY u.name;
```

Make sure you're comfortable with the difference between an `INNER JOIN`, `LEFT JOIN` and `RIGHT JOIN`, and `OUTER JOIN`. The main thing to remember is which rows you want to make sure are present after the join: only the ones that are in both tables (`INNER`), all in the left (`LEFT`) or right (`RIGHT`), or all in both (`OUTER`).

```sql
-- Don't drop any rows in 'users'
   SELECT *
     FROM users AS u
LEFT JOIN transactions AS t  
       ON u.id = t.user_id;

-- Don't drop any rows in either table
    SELECT *
      FROM users AS u
OUTER JOIN transactions AS t
```

For more complex queries, you'll want to bring in the `WITH {tab} AS` structure, which let you work with the output of nested queries. In the below query, we filter the table on the latest purchase for each user.

```sql
WITH latest_purchase AS (
    SELECT user_id,
           MAX(purchase_date) AS max_date
      FROM purchases
  GROUP BY user_id
)
    SELECT p.user_id,
           p.purchase_date
      FROM purchases AS p
INNER JOIN latest_purchase AS lp  -- Filter on each ID's latest purchase
        ON p.user_id = lp.user_id
       AND p.purchase_date = lp.max_date;
```

For writing to databases, maybe you'll use an ORM (e.g. `SQLAlchemy`) or just an API. But this is probably more of a software engineering thing than data science $-$ you'll want to have strict rules on what can be written and who has write permission to a database. (No one should have write permission to Prod!)

#### Interacting with APIs
Aside from SQL, the other main way you'll access data is via **APIs**, or Application Programming Interfaces.<sup>[[3]](#3-interacting-with-apis)</sup>

An API is like the entrance to a bank: it's (hopefully) the only way to access the contents of the bank, and you have to follow certain rules to enter: you can't bring in weapons, you have to enter on foot, you'll be turned away if you're not wearing pants, etc. Another way to think of it is like an electrical outlet - you can't access electricity unless your chord plug is in the correct shape.

The `requests` library lets us query APIs straight from Python. The process is simple for APIs without any security requirements: you just need the API's location on the internet, i.e. their [URL](https://en.wikipedia.org/wiki/URL), or Universal Resource Locator. All we do is pose an HTTP `GET` request to the URL, then decode the JSON returned from the server servicing the API.

```python
import requests

url = "https://jsonplaceholder.typicode.com/todos/1"
data = requests.get(url).json()
```

But sometimes we need some additional steps to access the data. When accessing a company's proprietary data, there are (or should be!) strict restrictions on who is authorized to interact with the data. In the example below, we use `boto3` to access a file in [Amazon Web Services S3](https://aws.amazon.com/s3/), the [cloud storage](https://aws.amazon.com/what-is-cloud-storage/) market leader. Notice how we need to pass in security credentials (stored in the `os.environ` object) when we establish a connection with S3.

```python
import os
import json
import boto3
import pandas as pd
from io import StringIO

# Get credentials
access_key = os.environ['AWS_ACCESS_KEY_ID'],
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']

# Establish a connection
client = boto3.client(aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      region_name='us-east-1')

# Get the file
obj = client.get_object(Bucket="my_company", Key='datasets/data.json')

# Convert the file to a dataframe
body = obj['Body'].read()
string = body.decode(encoding='utf-8')
df = pd.DataFrame(json.load(StringIO(string)))
```

What if you want to collect data from an external website that doesn't provide a convenient API? This is a job for [web scraping](https://www.scrapinghub.com/what-is-web-scraping/), and Python's [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) module is our answer.

```python
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Web_scraping"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html')

for heading in soup.findAll('h2'):
    print(heading.text)  
    # Contents, History[edit], Techniques[edit]...
```

### Version control
When you work on a coding project that can't be finished in one sitting, you need checkpoints to save the progress you've made. Even once the project is seemingly complete, you might not want to modify the working version with a new idea you have, but rather a copy of the project where you can make changes and compare them to the original.

This is where version control systems like [Git](https://git-scm.com/) come in. In contrast to having dozens of files called `my_project.py`, `my_project_final.py`, `my_project_final2.py`, `my_project_final2_REAL.py`, etc. floating in a folder on your computer, you instead have a tree-shaped **repository** of your project. There's one "master" (also called "main") version of the code, and you only ever modify _copies_ (**branches**) of it. All changes to the code are automatically labeled whenever you push a **commit** to a branch, and changes to the main branch require a review by at least one other person. (Technically they don't, but this is the case in virtually any professional setting.)

The structure of the repository might look something like this over time. (Source: [Stack Overflow](https://stackoverflow.com/questions/1057564/pretty-git-branch-graphs))

![]({{ site.baseurl }}/images/careers/git.png)

The gray line is the `master` branch (now called `main`<sup>[[4]](#4-version-control)</sup>), and the blue and yellow lines are copies (`develop` and `myfeature`) that branched off at different points, were modified, and then were merged back into `master`. You can have dozens of branches running simultaneously at larger companies, which is essential for letting teams of developers work on different aspects of the same codebase simultaneously.

The actual code behind using Git is straightforward. Below are some commands in [bash](https://opensource.com/resources/what-bash) in the Mac Terminal, where we:
1. Switch from whatever branch we were on onto the `main` branch
2. Create a new branch, `DS-123-Add-outlier-check`<sup>[[5]](#5-version-control)</sup>, that is a copy of `main`
3. Push the branch from our local computer and into the cloud

```bash
git checkout main
git checkout -b DS-123-Add-outlier-check
git push --set-upstream origin DS-123-Add-outlier-check
```

Now, on our new branch, we're free to make whatever changes to the code we'd like. Let's say we modify `preprocessor.py` by adding a step that removes outliers. When we want to save our changes, we type the following into the Terminal.

```bash
git add preprocessor.py
git commit -m "Add outlier check"
git push
```

These steps are only reflected on `DS-123-Add-outlier-check`, not `main`. This lets us prepare the code until it's ready to be pushed to `main`. This process is called a **pull request,** and usually it's required that other developers review your work. A pull request may also initiate automated tests that run on your code to verify that your changes didn't break anything. If they did, that's ok $-$ you can change them before updating `main`, which is often the customer-facing branch.  


### Object-oriented programming
Finally, object-oriented programming is a skill that's probably not strictly necessary but will

```python
import logging
import pandas as pd
from typing import Optional, List

from ..services import DataLoader

N_SD_THRESH = 5


class Preprocessor:
    """
    | Functions for preprocessing data
    """
    def __init__(self, max_tries: int = MAX_TRIES):
        self.max_tries = MAX_TRIES
        self.dl = DataLoader()

    def remove_outliers(self,
                        df: pd.DataFrame,
                        cols: Optional[List[str]] = None,
                        n_sd_thresh: int = N_SD_THRESH) -> pd.DataFrame:
        """
        | Remove outliers from cols in df. If cols not specified,
        | all columns in df are processed.
        |
        | -------------------------------------------------------
        | Parameters
        | ----------
        |  df : pd.DataFrame
        |    Df with columns ['a', 'b', 'c']
        |
        |  cols : list or None
        |    Columns to check
        |
        |  n_sd_thresh : int
        |    Number of standard deviations from mean above/below
        |    which a value is excluded
        |
        |
        | Returns
        | -------
        |  pd.DataFrame
        |    Original df with outliers removed
        """
        bad_idx = []

        cols_to_check = cols if cols is not None else list(df)

        for col in cols_to_check:
            bad_idx.append(self._find_outliers(df[col], n_sd_thresh))

        df_filt = df[~df.index.isin(bad_idx)].reset_index(drop=True)

        if df_filt.empty:
            logging.error("df has no rows without outliers")
            return df

        return df_filt
```
This code block is quite a bit longer than the others, and it doesn't even include the helper function or using `DataLoader`. For production-level coding, there's a lot more architecture you need to build _around_ your core functions to ensure that your code:
1. Can be read and modified by others, not just you
2. Is modular enough to be used in pipelines and multiple contexts
3. Doesn't grind those pipelines to a halt if it gets some unexpected input and breaks

If you're interested in a deeper dive on these concepts and a step-by-step explanation of the (truncated) code above, stay tuned for a longer post on writing production-level Python code.

### Virtual environments

### Writing tests
There are lots of testing frameworks out there, but a solid one (and the one I'm most familiar with) is `pytest`.

### Servers and deployment



## Footnotes
#### 1. [The code *around* your code](#the-code-around-your-code)
This is aimed at me as much as at anyone else. In grad school, I had R scripts that were hundreds of lines long, and rerunning them to process data differently always felt like performing surgery. It shouldn't be that way! Looking back, it's amazing how much easier the Ph.D. would have been with some basic software engineering and project management best practices in place. Maybe for the next doctorate...

#### 2. [SQL](#sql)
A popular alternative to relational databases is [NoSQL](https://www.mongodb.com/nosql-explained), or non-relational databases (a.k.a. "Not Only SQL.") In contrast to tables with strictly defined relationships, NoSQL databases like [MongoDB](https://www.mongodb.com/) allow much more flexibility in how data are stored. You can store arrays or nested dictionaries, or even add fields to documents ("tables") in the database on the fly. [A major disadvantage](https://stackoverflow.com/questions/5244437/pros-and-cons-of-mongodb) to this flexibility, however, is that complex queries are less flexible, especially joining data from separate documents together. While NoSQL databases are popular, [traditional relational databases are still more common](https://scalegrid.io/blog/2019-database-trends-sql-vs-nosql-top-databases-single-vs-multiple-database-use/) so I'll focus on them here.

#### 3. [Interacting with APIs](#interacting-with-apis)
APIs and SQL go hand-in-hand, actually. When you request data from an API, your request is most likely converted to a SQL query that is then executed on a database.

#### 4. [Version control](#version-control)
In October 2020, [GitHub renamed the default branch](https://www.zdnet.com/article/github-to-replace-master-with-main-starting-next-month/) for new repositories from `master` to `main` to remove unnecessary references to slavery.

#### 5. [Version control](#version-control)
A best practice naming convention for Git branches is to refer to them by their [JIRA](https://www.atlassian.com/software/jira) ticket ID. If your company integrates Git with JIRA, other developers will see whether the branch is in development, has an active pull request, or has been merged into `main`. An even better ("best"-er?) practice is to include in the branch name whether it is a [hotfix](https://en.wikipedia.org/wiki/Hotfix), support request, part of the [roadmap](https://roadmunk.com/roadmap-templates/software-roadmap), etc.
