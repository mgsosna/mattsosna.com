---
layout: post
title: How to enter data science - <br>4. The engineering
author: matt_sosna
summary: The software engineering skills needed to succeed in data science
image: ""
---

Welcome to the fourth post in our series on how to enter data science! So far, we've covered [the range of data science roles]({{  site.baseurl  }}/DS-transition-1), some [inferential statistics fundamentals]({{  site.baseurl  }}/DS-transition-2), and [manipulating and analyzing data]({{  site.baseurl  }}/DS-transition-3). This post will focus on **software engineering** concepts that are essential for data science.

---
**How to enter data science:**
1. [The target]({{  site.baseurl  }}/DS-transition-1)
2. [The statistics]({{  site.baseurl  }}/DS-transition-2)
3. [The analytics]({{  site.baseurl  }}/DS-transition-3)
4. **The engineering**
5. The people *(coming soon)*

---

## The code *around* your code
The programming concepts in the [last post]({{  site.baseurl  }}/DS-transition-3) covered how to work with data once it's sitting in front of you. These concepts are sufficient if your responsibilities *around the analyses* involve something like clicking and dragging a CSV from Google Drive onto your laptop, analyzing the data, then attaching a PDF to a report.

Yet, what happens when you start a project that requires combining data from *hundreds* of CSVs? Clicking and dragging can only get you so far $-$ even if you have the patience, your manager likely doesn't! It's also only a matter of time before you have to access data through an [API](#interacting-with-apis) that doesn't have a nice user interface.

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
In this section, we'll cover _**how to use code to access data.**_ This is a skill that spans the entire [analytics-engineering spectrum]({{  site.baseurl  }}/DS-transition-1/#the-scalpel-versus-the-shovel), but I'd argue is more of an "engineering" skill than an analytical one.

As a data scientist, you'll rarely access data through the click-based graphical user interfaces of Google Drive or Dropbox. Instead, the majority of the data you'll access will reside in [**SQL**](#sql) (Structured Query Language) databases or at [**APIs**](#interacting-with-apis) (Application Programming Interfaces). It's also possible you'll use [**web scraping**](#web-scraping) to access data from websites that don't provide an API.

#### SQL
Unless your company is tiny, it's going to have more data than can fit onto a hard drive or two. And as the amount of data grows, it's critical for the data to be organized in a way that minimizes [redundancy](http://www.databasedev.co.uk/data-redundancy.html) and [retrieval time](https://use-the-index-luke.com/sql/testing-scalability/data-volume) and optimizes [security and reliability](https://looker.com/definitions/database-security#exit-popup); formally states [how different parts of the data are related to each other](https://www.ibm.com/cloud/learn/relational-databases); and lets [multiple users read (and write) data simultaneously](https://courses.lumenlearning.com/santaana-informationsystems/chapter/characteristics-and-benefits-of-a-database/).

The main way to do this is with [relational databases](https://en.wikipedia.org/wiki/Relational_database), which you query with SQL.<sup>[[2]](#2-sql)</sup> A relational database is essentially a set of tables with defined relationships between tables. You can have a table of `users`, for example, along with a table of `orders` for every purchase made at your store. Rather than needing to have every detail on a user stored alongside each of their orders in the `orders` table, you can just have a column called `user_id`, with values referencing rows in `users`. With SQL, you can easily and quickly pull in the relevant data from both tables, [even if the tables grow to have tens or hundreds of millions of rows](https://www.geeksforgeeks.org/introduction-of-b-tree-2/).<sup>[[3]](#3-sql)</sup>

You're likely to use SQL very frequently in your role, potentially every day, so I highly recommend investing time into polishing this skill. Luckily, SQL isn't a massive language, and you will probably only need to *query* data from databases as opposed to *creating* databases or tables, which is more in the realm of a [data engineer](https://www.xplenty.com/blog/data-engineering-what-does-a-data-engineer-do-how-do-i-become-one/). We'll focus on simple to intermediate querying in this post.

Below is a simple query written in [Postgres](https://www.postgresql.org/), one of the major SQL dialects. We select the `name` and `animal` columns from the table `students`, using the `AS` keyword to create [aliases](https://www.tutorialspoint.com/sql/sql-alias-syntax.htm), or temporary names, for the columns in our returned table. The final result is filtered so the only rows returned are those where a student's favorite animal is a walrus.<sup>[[4]](#4-sql)</sup>

```sql
SELECT name AS student_name,
       animal AS favorite_animal
  FROM students
 WHERE animal = 'Walrus';
```

We can use aliases for tables, too, which we do below for `users`, `sql_pros`, and `transactions`. We join the tables in two ways in this example; in the first query, we use a `LEFT JOIN`, which preserves all rows in `users` but drops rows in `sql_pros` that don't have an ID in `users`. In the second query, we perform an `OUTER JOIN`, which preserve all rows in both `users` and `transactions`.

```sql
-- Query 1: don't drop any rows in 'users'
   SELECT *
     FROM users AS u
LEFT JOIN sql_pros AS sp
    USING (id);  -- Same as "ON" if column exists in both tables

-- Query 2: don't drop any rows in either table
    SELECT *
      FROM users AS u
OUTER JOIN transactions AS t
        ON u.id = t.user_id;
```

The main thing to remember with the various joins is the rows you want to preserve after the join: only those that match in both tables (`INNER`), all in the left (`LEFT`) or right (`RIGHT`), or all in both (`OUTER`).

Aggregating data is another key SQL skill. Below, we create a table with students' names and their average grade. In this scenario, maybe data about students such as names and addresses exists only in the `students` table, while the `grades` table only has `student_id`. To be able to print the student's name next to their average grade, we need to join the tables.

```sql
    SELECT s.name,
           AVG(g.score) AS avg_score
      FROM students AS s
INNER JOIN grades AS g
        ON s.id = g.student_id
  GROUP BY s.id
  ORDER BY s.name;
```

While it's possible to join `users` and `grades`, save the data as a CSV, and *then* perform aggregations with `pandas` in Python, it's much more efficient (in both time and storage) to perform these calculations in SQL first before saving the data.

For more complex queries, you'll want to bring in the `WITH {tab} AS` structure, which lets you write queries that build on the outputs of other queries. In the below query, we first create a lookup table with the mean and standard deviation `price` *for each user.* We then join our lookup back into the original `orders` table, using our lookup to filter out any rows that don't fall within three standard deviations of each user's mean order price. This immediately flags outliers that we can examine more closely. Note that this is all one query, but we can logically treat it as two thanks to the `WITH` syntax.

```sql
-- Create a lookup with info on each user
WITH orders_lookup AS (
    SELECT user_id,
           AVG(price) AS avg_price
           STDDEV(price) AS sd_price
      FROM orders
  GROUP BY user_id
)

-- Use the lookup to filter the original table
     SELECT user_id,
            price
       FROM orders AS o
 INNER JOIN orders_lookup AS ol
      USING (user_id)
      WHERE price
NOT BETWEEN ol.avg_price - 3*ol.sd_price
        AND ol.avg_price + 3*ol.sd_price;
```

Finally, let's quickly mention *writing* to a database. Writing to a database, especially one in production, will most likely fall under the strict supervision of the software engineering team $-$ a good team will have procedures in place to [verify the written data matches the table schema](https://stackoverflow.com/questions/14051672/how-to-verify-datatype-before-entering-into-the-table/14051929), [prevent SQL injection attacks](https://www.acunetix.com/websitesecurity/sql-injection/), and [ensure all writes are logged](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html). But in case you *do* have full reign over a database you want to write to, here's the basic syntax for adding a row:

```sql
-- Add a row
INSERT INTO students (firstname, lastname, is_superhero)
     VALUES ("Jane", "Reader", true);
```

And here is the syntax for updating and deleting. Be *very* sure you know what you're doing, since there's no "undo" command!<sup>[[5]](#5-sql)</sup>
```sql
-- Update all rows that match criteria
UPDATE students
   SET age = age + 1
 WHERE name = 'Jimmy';

-- Delete all rows that match criteria
DELETE FROM students
      WHERE id = 10;
```

#### Interacting with APIs
Aside from SQL, the other main way you'll access data is via **APIs**, or Application Programming Interfaces.<sup>[[6]](#6-interacting-with-apis)</sup>

An API is like the entrance to a bank: it's (hopefully) the only way to access the contents of the bank, and you have to follow certain rules to enter: you can't bring in weapons, you have to enter on foot, you'll be turned away if you're not wearing a shirt, etc. Another way to think of it is like an electrical outlet $-$ you can't access electricity unless your chord plug is in the correct shape.

The `requests` library lets us query APIs straight from Python. The process is simple for APIs without any security requirements: you just need the API's location on the internet, i.e. their [URL](https://en.wikipedia.org/wiki/URL), or Universal Resource Locator. All we do is pose an [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) `GET` request to the URL, then decode the JSON returned from the server servicing the API.

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

#### Web scraping
What if you want to collect data from an external website that doesn't provide a convenient API? For this, we turn to [web scraping](https://www.scrapinghub.com/what-is-web-scraping/). The basic premise of web scraping is to write code that traverses the [HTML](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics) of a webpage, finding specified [tags](https://eastmanreference.com/complete-list-of-html-tags) (e.g. headers, tables, images) and recording their information. Scraping is ideal for automation because HTML has a highly regular, tree-based structure, with clear identifiers for all elements.

While scraping might sound complicated, it's actually fairly straightforward. We first mimic a web browser (e.g. Firefox, Chrome) by *requesting* the HTML from a website with `requests.get`. Then, we use Python's [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) module to organize the HTML into essentially a large nested dictionary. We can then extract the information we want from this object by specifying the HTML tags we're interested in. Below, we print out all `<h2>` headings for Wikipedia's web scraping page.

```python
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Web_scraping"

# Get the HTML from the page
response = requests.get(url)

# Parse the HTML
soup = BeautifulSoup(response.text, 'html')

# Print out each <h2> element
for heading in soup.findAll('h2'):
    print(heading.text)  
    # Contents, History[edit], Techniques[edit]...
```

### Version control
When you work on a project that can't be finished within a few minutes, you need checkpoints to save your progress. Even once the project is complete, maybe you get a great idea for an additional feature, or you find a way to improve a section of the code. Unless the change is tiny, **you won't want to modify <u><i>the version that works</i></u> but rather a <i><u>copy</u></i>** where you can make changes and compare them to the original. Similarly, for bigger projects **it's critical to be able to roll back to an old checkpoint if new changes break the code.** This is especially important if there are multiple people working on the same file!

This is where version control systems like [Git](https://git-scm.com/) come in. In contrast to having dozens of files called `my_project.py`, `my_project_final.py`, `my_project_final2.py`, `my_project_final2_REAL.py`, etc. floating in a folder on your computer, you instead have a tree-shaped **repository** of your project. There's one "main" version of the code, and you only ever modify _copies_ (**branches**) of it. All changes to the code are automatically labeled whenever you push a **commit** to a branch, and changes to the main branch require a review by at least one other person. (Technically they don't, but this is the case in virtually any professional setting.)

The structure of the repository might look something like this over time. (Source: [Stack Overflow](https://stackoverflow.com/questions/1057564/pretty-git-branch-graphs))

![]({{ site.baseurl }}/images/careers/git.png)

The gray line is the `master` branch (now called `main`<sup>[[7]](#7-version-control)</sup>), and the blue and yellow lines are copies (`develop` and `myfeature`) that branched off at different points, were modified, and then were merged back into `master`. You can have dozens of branches running simultaneously at larger companies, which is essential for letting teams of developers work on different aspects of the same codebase simultaneously.

The actual code behind using Git is straightforward. Below are some commands in [bash](https://opensource.com/resources/what-bash) in the Mac Terminal, where we:
1. Switch from whatever branch we were on onto the `main` branch
2. Create a new branch, `DS-123-Add-outlier-check`<sup>[[8]](#8-version-control)</sup>, that is a copy of `main`
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

These steps are only reflected on `DS-123-Add-outlier-check`, not `main`. This lets us prepare the code until it's ready to be pushed to `main`.

And if we broke something and want to revert to an old commit? We checkout to that commit using its [hash](https://www.mikestreety.co.uk/blog/the-git-commit-hash), tell Git to ignore the commit with errors, then push our changes to the branch.
```bash
git checkout abc123  # go to old checkpoint
git revert bad456    # "delete" the bad checkpoint
git push             # update the branch
```

### Object-oriented programming
As the amount of code in a project grows, it typically follows this pattern of increasing organization:
1. A script with **raw commands** one after the other
2. Code grouped into **functions**
3. Functions grouped into **separate scripts**
4. Functions within scripts grouped into [**classes**](https://www.programiz.com/python-programming/class)
5. Classes grouped into [**modules**](https://www.learnpython.org/en/Modules_and_Packages)

Production-level Python is best at the fifth level of organization, where code can easily be added, modified, and reused across contexts. A team's code will be organized into **classes**, which are templates of code with attributes and methods, that can be *instantiated*. Below is a brief example with a class called `Student`.

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def introduce(self):
        print(f"{self.name} is in grade {self.grade}")

john = Student("John", 3)
mary = Student("Mary", 5)

john.introduce()  # 'John is in grade 3'
mary.introduce()  # 'Mary is in grade 5'
```

Classes may be stored in `.py` files with the same name, grouped into directories with similar classes. The **module** consists of all the directories. We can have a `data_processing` module, for example, with a directory structure like this<sup>[[9]](#9-object-oriented-programming)</sup>:

```bash
preprocessors
| - init.py
| - data_cleaner.py
visualizers
| - init.py
| - error_logger.py
| - dashboarder.py
services
| - init.py
| - data_loader.py
| - database_writer.py
init.py
```

In the *preprocessors* directory, `datacleaner.py` contains a class, `DataCleaner`, with methods for cleaning data. The first 60 lines of `datacleaner.py` might look something like this:

```python
import logging
import pandas as pd
from typing import Optional, List

from ..services import DataLoader

# Global variables
N_SD_THRESH = 5  # N std devs from mean where value flagged as outlier
MAX_TRIES = 3    # N tries before function stops


class DataCleaner:
    """
    | Functions for cleaning data
    """
    def __init__(self, max_tries: int = MAX_TRIES):
        self.max_tries = MAX_TRIES
        self.dl = DataLoader()

    def remove_outliers(self,
                        df: pd.DataFrame,
                        cols: Optional[List[str]] = None,
                        n_sd_thresh: int = N_SD_THRESH) -> pd.DataFrame:
        """
        | Remove values > n_sd_thresh from mean of cols in df.
        | If cols not specified, all columns in df are processed.
        |
        | -------------------------------------------------------
        | Parameters
        | ----------
        |  df : pd.DataFrame
        |    The data
        |
        |  cols : list or None
        |    Columns to remove outliers from
        |
        |  n_sd_thresh : int
        |    Number of standard deviations from mean above/below
        |    which a row is excluded
        |
        |
        | Returns
        | -------
        |  pd.DataFrame
        |    Original df with rows with outliers removed
        """
        cols_to_check = cols if cols is not None else list(df)

        bad_rows = set()
        for col in cols_to_check:
            bad_rows.add(self._find_outliers(df[col], n_sd_thresh))

        df_filt = df[~df.index.isin(bad_idx)].reset_index(drop=True)

        if df_filt.empty:
            logging.warning("df has no rows without outliers")

        return df_filt
```
This code block is quite a bit longer than the others, and it doesn't even include the helper function `_find_outliers` or code that calls `DataLoader`. For production-level coding, there's a lot more architecture you need to build _around_ your core functions to ensure that your code:
1. Can be read and modified by others, not just you
2. Is modular enough to be used in pipelines and multiple contexts
3. Doesn't grind those pipelines to a halt if it gets some unexpected input and breaks

If you're interested in a deeper dive on these concepts and a step-by-step explanation of the (truncated) code above, stay tuned for a longer post on writing production-level Python code.

### Virtual environments

### Writing tests
There are lots of testing frameworks out there, but a solid one (and the one I'm most familiar with) is `pytest`.

```python
import pytest
import Preprocessor

class TestRemoveOutliers:
    """
    | Tests for Preprocessor.remove_outliers
    """

    def test_run(a, b):
        assert a == b

```

Then in bash, you would just navigate to the root directory of your project, then type `pytest tests`

```bash
cd my_project
pytest tests   # assuming all the test files are in this folder
```

### Servers and deployment



## Footnotes
#### 1. [The code *around* your code](#the-code-around-your-code)
This is aimed at me as much as at anyone else. In grad school, I had R scripts that were hundreds of lines long, and rerunning them to process data differently always felt like performing surgery. It shouldn't be that way! Looking back, it's amazing how much easier the Ph.D. would have been with some basic software engineering and project management best practices in place. Maybe for the next doctorate...

#### 2. [SQL](#sql)
A popular alternative to relational databases is [NoSQL](https://www.mongodb.com/nosql-explained), or non-relational databases (a.k.a. "Not Only SQL.") In contrast to tables with strictly defined relationships, NoSQL databases like [MongoDB](https://www.mongodb.com/) allow much more flexibility in how data are stored. You can store arrays or nested dictionaries, or even add fields to documents ("tables") in the database on the fly. [A major disadvantage](https://stackoverflow.com/questions/5244437/pros-and-cons-of-mongodb) to this flexibility, however, is that complex queries are less flexible, especially joining data from separate documents together. While NoSQL databases are popular, [traditional relational databases are still more common](https://scalegrid.io/blog/2019-database-trends-sql-vs-nosql-top-databases-single-vs-multiple-database-use/) so I'll focus on them here.

#### 3. [SQL](#sql)
Searching, inserting, and deleting records in a properly-indexed database [is expected to scale at $O(\log{n})$](https://cs.stackexchange.com/questions/59453/why-is-b-tree-search-olog-n). This means that *for every order of magnitude*, traversing the data requires *only one additional step!* I find this mind-boggling.

#### 4. [SQL](#sql)
In the research for this post, I stumbled across this (somewhat controversial) [SQL Style Guide](https://www.sqlstyle.guide/). It was an interesting read, and I decided to adopt some of the layout tips for the SQL examples in this post. The main thing I took away was having a blank "river" down the middle of your code, with SQL keywords on the left and the rest of the code on the right $-$ it makes it really easy to quickly scan what the query is doing. If I don't find an easy way to auto-format the code this way, though, I doubt I'll stick with it for quick analyses.

#### 5. [SQL](#sql)
If this actually happens to you, hopefully your company's engineering team regularly backs up the databases and can [roll back to an earlier version](https://www.codeproject.com/Questions/389399/how-to-do-undo-a-sql-query). If they don't, and you accidentally delete all your company's data, then [Quora recommends you resign](https://www.quora.com/What-would-you-do-if-you-accidentally-deleted-all-data-of-a-production-MySQL-database-at-the-first-day-as-a-backend-developer) and find a company with better engineering practices!

#### 6. [Interacting with APIs](#interacting-with-apis)
APIs and SQL go hand-in-hand, actually. When you request data from an API, your request is most likely converted to a SQL query that is then executed on a database.

#### 7. [Version control](#version-control)
In October 2020, [GitHub renamed the default branch](https://www.zdnet.com/article/github-to-replace-master-with-main-starting-next-month/) for new repositories from `master` to `main` to remove unnecessary references to slavery.

#### 8. [Version control](#version-control)
A best practice naming convention for Git branches is to refer to them by their [JIRA](https://www.atlassian.com/software/jira) ticket ID. If your company integrates Git with JIRA, other developers will see whether the branch is in development, has an active pull request, or has been merged into `main`. An even better ("best"-er?) practice is to include in the branch name whether it is a [hotfix](https://en.wikipedia.org/wiki/Hotfix), support request, part of the [roadmap](https://roadmunk.com/roadmap-templates/software-roadmap), etc.

#### 9. [Object-oriented programming](#object-oriented-programming)
The `init.py` files allow for classes to be imported from outside their directory. This is what allows `from ..services import DataLoader` to work. Similarly, [if you have your `data_processing` module installed](https://realpython.com/python-wheels/), you can be in any script and load `DataLoader` by typing:

```python
# With init files
from data_processing import DataLoader
```

Without the init files, you would need to type:

```python
# Without init files
from data_processing.services.data_loader import DataLoader
```

Not only is this far less convenient, it also runs the risk of external scripts breaking if you decide to rearrange the directories inside the `data_processing` module. You can read more about init.py files [here](https://stackoverflow.com/questions/448271/what-is-init-py-for).
