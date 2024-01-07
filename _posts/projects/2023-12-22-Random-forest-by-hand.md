---
layout: post
author: matt_sosna
title: Building a Random Forest by Hand
tags: machine-learning
---

From [drug discovery](https://www.sciencedirect.com/science/article/abs/pii/S0957417416306819) to [species classification](https://www.mdpi.com/2072-4292/4/9/2661), [credit scoring](https://journals.sagepub.com/doi/abs/10.1177/2278533718765531) to [cybersecurity](https://www.sciencedirect.com/science/article/pii/S1877050916311127) and more, the random forest is a popular and powerful algorithm for modeling our complex world. Its versatility and predictive prowess would seem to require cutting-edge complexity, but if we dig into what a random forest actually is, we see a shockingly simple set of rules working in tandem.

I find that the best way to learn something is to play with it. So to gain an intuition on how random forests work, let's build one by hand in Python, starting with a decision tree and expanding to the full forest. We'll see first-hand how flexible and interpretable this algorithm is for both classification and regression applications. And while this project may sound complicated, there are really only a few core concepts we'll need to learn: 1) how to iteratively partition data, and 2) how to quantify how well data is partitioned.

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
### Tree Nodes
Let's start with a `Node` class that will serve as a node in our decision tree. The class will have the following attributes used for training:
* A dataframe representing the data (or subset) the node held during training.
* The proportion of positive labels and Gini impurity of the dataframe.
* Pointers to left and right child nodes, set to `None` if the node is a leaf.

The class will also have the following attributes for classifying new data:
* Information on which node to go to next (if the node is not a leaf) or which label to return.

We can construct a `Node` class that meets these criteria with the below code. Because we calculate Gini impurity by assuming the dataframe target column is 1s and 0s, we have a `_check_df` method to ensure the data is in the correct format. The other methods just calculate $p_k$ and the Gini impurity.

{% include header-python.html %}
```python
import numpy as np
import pandas as pd

class Node:
    """
    Node in a decision tree.

    Parameters
    ----------
    df : pd.DataFrame
      The dataframe (or subset) this node holds. Used for training.
      All columns except target_col are assumed to be features.
    target_col : str
      The column in the dataframe with labels. Must be 0s and 1s, with
      1s being the positive class.
    pk : float
      Proportion of node's df that contain the positive class.
    gini : float
      The node's Gini impurity.
    left : Node
      The left child of the node. None if no child.
    right : Node
      The right child of the node. None if no child.
    feature : str
      The column in the df whose splitting led to the largest reduction
      in weighted Gini impurity in the child nodes.
    threshold : float | int
      The value of the feature column to split the df.
    """
    def __init__(
        self,
        df: pd.DataFrame,
        target_col: str
    ) -> None:
        # For training
        self.df = self._check_df(df, target_col)
        self.target_col = target_col
        self.pk = self._set_pk()
        self.gini = self._set_gini()

        # For training/inference
        self.left = None
        self.right = None

        # For inference
        self.feature = None
        self.threshold = None

    def _check_df(
        self,
        df: pd.DataFrame,
        target_col: str
    ) -> pd.DataFrame:
        assert len(list(df)) > 1, \
            "df must have features"
        assert not set(df[target_col]).difference({0,1}), \
            "target column cannot have values besides {0,1}"
        return df

    def _set_pk(self) -> float:
        """
        Sets pk, the proportion of samples that are of the positive class.
        Assumes samples is a list of ints, where 1 is the positive class
        and 0 is the negative class.
        """
        return np.mean(self.df[self.target_col].values)

    def _set_gini(self) -> float:
        """
        Sets the Gini impurity.
        """
        return 1 - self.pk**2 - (1 - self.pk)**2
```

We can instantiate a node like this.

{% include header-python.html %}
```python
import pandas as pd
df = pd.DataFrame({'feature': [1, 2, 3], 'label': [0, 0, 1]})
node = Node(df, 'label')

print(f"pk: {round(node.pk, 2)}, gini: {round(node.gini, 2)}")
# pk: 0.33, gini: 0.44
```


### Decision tree


Tree could be just one node if there's one rule that completely partitions the classes.


Josh Starmer's [excellent video on how decision trees are built](https://www.youtube.com/watch?v=_L39rN6gz7Y)


* Check what impurity metrics are offered by sklearn's `DecisionTreeClassifier` and `RandomForestClassifier` classes (and what the defaults are).
* See if there's a cleaner way than needing two classes (`Node` and `NodeProcessor`). Maybe it should be like `NodeData` and `Node` does the work? We should also have some way to trigger the whole process (i.e., the actual decision tree). Maybe `DecisionTree`.
