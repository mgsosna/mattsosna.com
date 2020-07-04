---
layout: post
title: Transitioning to data science
---

If you're coming from academia, you've got

## Your learning checklist
* **Python**
- [ ] Dataframes and arrays: `pandas`, `numpy`
- [ ] Visualization: `matplotlib`, `seaborn`
- [ ] Machine learning: `scikit-learn`, `keras`
- [ ] Working with dates: `datetime`
- [ ] Interacting with cloud storage: `boto3`
- [ ] Object-oriented programming (i.e. classes, module imports) <br><br>
* **Software engineering**
- [ ] Version control: [Git](https://git-scm.com/)
- [ ] SQL for querying databases (e.g. PostgreSQL) <br><br>
* **Statistics**
- [ ] Linear regression
- [ ] Logistic regression
- [ ] Decision trees and random forests <br><br>
* **Non-technical**
- [ ] Strong ability to explain technical concepts
- [ ] Focus on how to best deliver business value <br><br>
{: style='list-style-type: none'}

# Python
## Dataframes
You're good if you understand this:
```python
import pandas as pd

# Example 1
df = pd.read_csv("data.csv")
df_agg = df.groupby('id').sum()
print(df_agg.loc[123, 'illinois'])

# Example 2
df_final = pd.DataFrame()
for tup in new_df.itertuples():
    df_iter = some_function(tup.age, tup.start_date)
    df_final = df_final.append(df_iter, ignore_index=True)
```

## Visualizations
```python
import matplotlib.pyplot as plt

plt.scatter(df['date'], df['age'])
plt.xlim([dt.date(2020, 1, 1), dt.date(2020, 5, 1)])
plt.ylim([df['a'].min(), df['a'].max()])
plt.show()
```

## Working with dates



* Make sure your Python chops are sharp!
* Learn Git. Version control is crucial. I wish this was a bigger part of my workflow during the Ph.D. It's essential when you're a member of a team.
* Learn SQL. You're almost guaranteed to be querying databases in your job. You won't need to be a pro unless you're in more of a data engineering role, but you should know it. DataCamp has some great courses.


# Statistics
You should feel comfortable explaining this:

$$ y = 5 $$
$ y = \sum_{i=1}^{m}(h(x_i)-y_i)^2 $
<script type="math/tex"> y = \frac{5}{10}</script>

\[ x = 5 \]
\ x = 5 \
