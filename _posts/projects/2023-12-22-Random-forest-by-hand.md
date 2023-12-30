---
layout: post
author: matt_sosna
title: Building a Random Forest by Hand
tags: machine-learning
---

From [drug discovery](https://www.sciencedirect.com/science/article/abs/pii/S0957417416306819) to [species classification](https://www.mdpi.com/2072-4292/4/9/2661), [credit scoring](https://journals.sagepub.com/doi/abs/10.1177/2278533718765531) to [cybersecurity](https://www.sciencedirect.com/science/article/pii/S1877050916311127) and more, the random forest is a powerful algorithm for modeling our complex world. Its versatility and predictive prowess would seem to require cutting-edge complexity, but if we dig into what a random forest actually is, we see a shockingly simple set of rules working in tandem.







Random forests are one of the most popular machine learning algorithms for both classification and regression due to their flexibility, interpretability, and performance. To gain an intuition on how they work, let's build one by hand, starting with manually implementing a decision tree class followed by the entire forest. It sounds complicated, but there are really only a few concepts -- how to iteratively partition the data and how to quantify how well they partition that data -- that are core to understanding the algorithm.

## Background
### Decision tree
A decision tree is a supervised learning algorithm that identifies **a set of simple rules that map features to labels.** In contrast to a model like logistic regression where the output is an equation, the algorithm is [nonparametric](https://machinelearningmastery.com/parametric-and-nonparametric-machine-learning-algorithms/), meaning it doesn't make strong assumptions on the relationship between features and labels. This means that trees are free to evolve however to best map to the dataset they're modeling.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/tree1.png" height="80%" width="80%">
</center>

* Talk about ensemble algorithms


[sklearn docs](https://scikit-learn.org/stable/modules/tree.html)
* Don't need to pre-process the data as much, but will want to balance the data first.
* Downside: small variations in data can result in totally different trees being produced.


(For simplicity, we'll just talk about classification for now and revisit regression later.)


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

Josh Starmer's [excellent video on how decision trees are built](https://www.youtube.com/watch?v=_L39rN6gz7Y)


* Check what impurity metrics are offered by sklearn's `DecisionTreeClassifier` and `RandomForestClassifier` classes (and what the defaults are).
* See if there's a cleaner way than needing two classes (`Node` and `NodeProcessor`). Maybe it should be like `NodeData` and `Node` does the work? We should also have some way to trigger the whole process (i.e., the actual decision tree). Maybe `DecisionTree`.
