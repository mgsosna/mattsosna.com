---
layout: post
author: matt_sosna
title: Building a Random Forest by Hand
tags: machine-learning
---

Random forests are one of the most popular machine learning models due to their interpretability and robustness against overfitting. To gain an intuition on how they work, we'll build one by hand, starting with manually implementing a decision tree class followed by the entire forest.

## Background
### Decision tree
Our goal is to find a path through our features that allow us to perfectly separate our classes.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/tree1.png" height="80%" width="80%">
</center>

A few things to note:
* Not all branches of the tree are equally long. For some combinations of features, we can reach a decision quickly. For others, we need to partition our data multiple times before we can cleanly separate the classes.


Our tree will be fit to our training data. If we let it grow as long as possible, it will be able to perfectly categorize every point in our training data. But then it won't be able to generalize to new data well.  

We need a way to evaluate how well our tree partitions our labels. One common metric is **gini impurity**, which is calculated with the following equation:

$$G = 1 - \sum_{k=1}^{m}{p_k}^2$$

Here, $p_k$ is the probability of a randomly-drawn sample belonging to class $k$ among our $m$ classes. A node with zero impurity would be one where all samples belong to one class.

If we only have two classes, the negative class probability is just the inverse of the positive class probability, so we can define the impurity solely in terms of $p_k$ like below.

$$G = 1 - {p_k}^2 - (1-p_k)^2$$

Total Gini impurity of the tree: weighted average.

Below is a plot of the Gini impurity as a function of $p_▲$, the probability of randomly selecting a triangle from the node. The lowest impurity is one where all elements in the node are either _not_ triangles (i.e., squares) or all triangles. As the node becomes mixed, the impurity increases.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/gini_impurity.png" height="75%" width="75%">
</center>
<center>
<i>Image adapted from Provost, Foster; Fawcett, Tom. Data Science for Business: What You Need to Know about Data Mining and Data-Analytic Thinking</i>
</center>

## Implementation
### Decision tree

Tree could be just one node if there's one rule that completely partitions the classes.

{% include header-python.html %}
```python
import numpy as np
import pandas as pd

class Node:
    """
    Node in a decision tree. Assumes self.df has a column
    called 'label' that consists of 0s and 1s.
    """
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = self._check_df(df)
        self.pk = self.set_pk()
        self.gini = self.set_gini()

    def _check_df(self, df: pd.DataFrame) -> pd.DataFrame:
        assert 'label' in df.columns, "df needs 'label' column"
        assert not set(df['label']).difference({0,1}), "label column cannot have values besides {0,1}"
        return df

    def set_pk(self) -> float:
        """
        Sets pk, the proportion of samples that are of the positive class.
        Assumes samples is a list of ints, where 1 is the positive class
        and 0 is the negative class.
        """
        return np.mean(self.df['label'].values)

    def set_gini(self) -> float:
        """
        Sets the Gini impurity.
        """
        return 1 - self.pk**2 - (1 - self.pk)**2

class NodeProcessor:
    def __init__(self, node: Node) -> None:
        self.node = node
        self.df = node.df

    def split_on_feature(self, feature: str) -> tuple[int|float, Node, Node]:
        """
        Iterate through values of a feature and identify
        """
        values = []

        # Skip last value, since it includes all rows
        for thresh in self.df.sort_values(feature)[feature].unique()[:-1]:
            values.append(self._process_split(thresh, feature))

        return min(values, key=lambda x: x[0])

    def _process_split(
        self,
        threshold: int|float,
        feature: str
    ) -> tuple[int|float, Node, Node]:
        """
        Actually do the work...
        """
        df_lower = self.df[self.df[feature] <= threshold]
        df_upper = self.df[self.df[feature] > threshold]

        node_lower = Node(df_lower)
        node_upper = Node(df_upper)

        prop_lower = len(df_lower) / len(self.df)
        prop_upper = len(df_upper) / len(self.df)

        weighted_gini = node_lower.gini * prop_lower + node_upper.gini * prop_upper

        return weighted_gini, node_lower, node_upper
```
