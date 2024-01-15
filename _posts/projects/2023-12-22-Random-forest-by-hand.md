---
layout: post
author: matt_sosna
title: Building a Random Forest by Hand
tags: machine-learning
---

From [drug discovery](https://www.sciencedirect.com/science/article/abs/pii/S0957417416306819) to [species classification](https://www.mdpi.com/2072-4292/4/9/2661), [credit scoring](https://journals.sagepub.com/doi/abs/10.1177/2278533718765531) to [cybersecurity](https://www.sciencedirect.com/science/article/pii/S1877050916311127) and more, the random forest is a popular and powerful algorithm for modeling our complex world. Its versatility and predictive prowess would seem to require cutting-edge complexity, but if we dig into what a random forest actually is, we see a shockingly simple set of rules working in tandem.

I find that the best way to learn something is to play with it. So to gain an intuition on how random forests work, let's build one by hand in Python, starting with a decision tree and expanding to the full forest. We'll see first-hand how flexible and interpretable this algorithm is for both classification and regression applications. And while this project may sound complicated, there are really only a few core concepts we'll need to learn: 1) how to iteratively partition data, and 2) how to quantify how well data is partitioned.

## Background
### Decision tree inference
A decision tree is a supervised learning algorithm that identifies **a set of simple rules that map features to labels.** The model outputted by the algorithm (also called a decision tree) takes in a feature vector and outputs a label (for classification) or continuous value (for regression). A model that predicts whether a shopper will buy a product they viewed online, for example, might look like this.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/tree1.png" height="75%" width="75%">
</center>

Starting with the **root**, each node in the tree asks a binary question (e.g., _"Was the session length longer than 5 minutes?"_) and passes the feature vector to one of two child nodes depending on the answer. If there are no children -- i.e., we're at a **leaf node** -- then the tree returns a response.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/tree2.png" height="75%" width="75%">
</center>

(We'll focus on classification in this blog post, but a decision tree regressor would look identical but with continuous values returned rather than class labels.)

### Decision tree training
_Inference_, or this prediction process, is pretty straightforward. But _building_ this tree is much less obvious. How is the binary rule in each node determined? Which features are used in the tree, and in what order? Where does a threshold like 0.5 or 1 come from?

To understand how decision trees are built, let's imagine we're trying to partition a large dataset of shapes (squares and triangles) into smaller datasets of _only squares_ or _only triangles_ based on their features. In the ideal case, there's some categorical feature that perfectly separates the shapes.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/partitioning1.png" height="55%" width="55%">
</center>

But it's never _that_ easy. If you're lucky, maybe there's a continuous feature that has some threshold that perfectly separates the shapes instead. It takes a couple tries to find the exact threshold, but then you have your perfect split. (Phew!)

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/partitioning2.png">
</center>

Well... it's never really that easy, either. In this toy example, all triangles and squares are identical, meaning it's trivial to separate their feature vectors. (Find one rule that works for one triangle and it works for all triangles!)

**But in the real world, features don't map so neatly to labels.** Going back to our e-commerce example, a feature like _time spent on the site_ in a session might not be able to perfectly partition the classes even at any threshold.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/partitioning3.png">
</center>

So what do we do if no feature at any threshold can perfectly split our data? In this case, **we need a way to quantify how _"mixed"_ a set of labels is.** One common metric is [**Gini impurity**](https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity), which is calculated with the following equation:

$$G = 1 - \sum_{k=1}^{m}{p_k}^2$$

Here, $p_k$ is the probability of a randomly-drawn sample belonging to class $k$ among our $m$ classes. For our squares and triangles, since we only have two classes and the probabilities must sum to 1, we can just define the whole equation in terms of $p_k$.

$$G = 1 - {p_k}^2 - (1-p_k)^2$$

Below is a visual representation of the Gini impurity as a function of $p_\checkmark$, the probability of randomly selecting a positive label from the set. (We've just replaced $p_k$ with $p_\checkmark$ to indicate that the checkmarks are the positive class.) The lowest impurity is when the elements in the set are either all _not_ checkmarks (i.e., x's) or all checkmarks. The impurity peaks when we have equal numbers of x's and checkmarks.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/gini_impurity2.png" height="80%" width="80%">
</center>
<center>
<i>Image adapted from <a href="https://www.oreilly.com/library/view/data-science-for/9781449374273/" target="_blank">Data Science for Business: What You Need to Know about Data Mining and Data-Analytic Thinking</a></i>
</center>

When identifying rules to partition our classes, then, we can simply **select a split such that we _minimize the weighted Gini impurity_ of the subsets.** (Each subset has its own impurity, so we take the average weighted by the number of samples in each subset.) For a given feature, we can split the data on all possible values of that feature, record the weighted Gini impurity of the subsets, and then select the feature value that resulted in the lowest impurity.

Below, splitting the feature _Age of account_ on 35 days best separates users who buy a product from those who don't (in our fake dataset).

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/gini_split.png" height="70%" width="70%">
</center>

We can repeat this process for all features and **select the feature whose optimal split resulted in the lowest impurity.** Below, we see that the optimal split for _Session length_ results in a lower Gini impurity than the best splits for _Age of account_ and _Is frequent shopper_. _Is frequent shopper_ is a binary feature, so there's only one value to split with.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/gini_split_multiple.png">
</center>

**Splitting on _Session length > 5 min_ therefore becomes the first fork in our decision tree.** We then repeat our process of iterating through features and values and choosing the feature that best partitions the data for each subset, then _their_ subsets, and so on until we either have perfectly partitioned data or our tree reaches a maximum allowed depth. (More on that in the next section.)

Below is the tree we saw earlier but with the training data displayed in each node. Notice how the positive and negative classes become progressively isolated as we move down the tree. Once we reach the bottom of the tree, the leaf nodes simply output the class in their nodes.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/tree_data.png" height="70%" width="70%">
</center>

### Random forests
The decision tree above partitions the data until the subsets contain only labels of one class (i.e., Gini impurity = 0). While this maximizes our model's ability to explain its training data, we risk **overfitting** our model to our data. **Think of it like the model _memorizing_ every feature-label combination rather than learning the _underlying patterns_.** An overfit model struggles to generalize to new data, and classifying new data is usually our goal in the first place.

There are a few ways to combat overfitting. One option is to **limit the depth of the tree**. If we limited the above tree to only two levels, for example, we would end the left branch at the _Is frequent shopper_ split.

<center>
<img src="{{  site.baseurl  }}/images/projects/decision_tree/tree_data2.png" height="60%" width="60%">
</center>

The leaf nodes on the left branch now have mixed labels in their subsets. Allowing for this "impurity" might seem suboptimal, but it's a strong defense against noisy features: **if _Time idle_ and _Age of account_ were actually only correlated with our labels due to chance, a model that excluded those features would be better at generalizing to new data.** We also see that the tree uses the majority class (rather than the only class) to return a classification from the leaves.


Examples:
* Feature that's almost always 0, but happens to be 1 for a handful of cases and is biased towards positive class in the training data. Model would be like "whoa, I can get 100% purity by splitting here" (fairly low in the tree).




So we can limit the depth of the tree. But another approach is to leverage the strengths of **ensemble learning**. It turns out that when you take a lot of trees together, their errors cancel out. But need to have random allocations. Otherwise the same tree is trained every time.




In contrast to models like logistic regression where the output is an equation, the algorithm is [nonparametric](https://machinelearningmastery.com/parametric-and-nonparametric-machine-learning-algorithms/), meaning it doesn't make strong assumptions on the relationship between features and labels. This means that trees are free to grow in whatever way best describes the dataset they're given.

* Talk about ensemble algorithms


[sklearn docs](https://scikit-learn.org/stable/modules/tree.html)
* Don't need to pre-process the data as much, but will want to balance the data first.
* Downside: small variations in data can result in totally different trees being produced.


(For simplicity, we'll just talk about classification for now and revisit regression later.)



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
from typing_extensions import Self

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

Now let's add the logic for iterating through the values of a feature and identifying the threshold that minimizes the Gini impurity in the child nodes.

{% include header-python.html %}
```python
class Node:
    ...

    def split_on_feature(
        self,
        feature: str
    ) -> tuple[float, int|float, Self, Self]:
        """
        Iterate through values of a feature and identify split that minimizes
        weighted Gini impurity in child nodes. Returns tuple of weighted Gini
        impurity, feature threshold, and left and right child nodes.
        """
        values = []

        for thresh in self.df[feature].unique():
            if thresh == self.df[feature].max():
                pass
            values.append(self._process_split(feature, thresh))

        values = [v for v in values if v[1] is not None]
        if values:
            return min(values, key=lambda x: x[0])
        return None, None, None, None

    def _process_split(
        self,
        feature: str,
        threshold: int|float
    ) -> tuple[float, int|float, Self|None, Self|None]:
        """
        Splits df on the feature threshold and generates nodes for the data
        subsets.
        """
        df_lower = self.df[self.df[feature] <= threshold]
        df_upper = self.df[self.df[feature] > threshold]

        # If threshold doesn't split the data at all, end early
        if len(df_lower) == 0 or len(df_upper) == 0:
            return self.gini, None, None, None

        node_lower = Node(df_lower, self.target_col)
        node_upper = Node(df_upper, self.target_col)

        prop_lower = len(df_lower) / len(self.df)
        prop_upper = len(df_upper) / len(self.df)

        weighted_gini = node_lower.gini * prop_lower + node_upper.gini * prop_upper

        return weighted_gini, threshold, node_lower, node_upper
```

Let's quickly test it out. Below, we instantiate a node and have it find the optimal split for the data. `split_on_feature` returns the weighted Gini impurity of 0.0 in the child nodes because we can perfectly partition the labels at a value of 2 (the second returned value). The third and fourth values are the left and right child nodes from the partitioning.

{% include header-python.html %}
```python
import pandas as pd
df = pd.DataFrame({'feature': [1, 2, 3], 'label': [0, 0, 1]})
node = Node(df, 'label')

print(f"pk: {round(node.pk, 2)}, gini: {round(node.gini, 2)}")
# pk: 0.33, gini: 0.44

print(node.split_on_feature('feature'))
# (0.0, 2,
# <__main__.Node object at 0x137c279d0>,
# <__main__.Node object at 0x137c24160>)
```

### Decision tree
The next step is to arrange nodes in a tree to best partition training data and most accurately classify new data. Let's start with the basic structure, then the ability to train the classifier (i.e., build the tree) and generate predictions. We store our `decision_tree.py` file in the same directory as `node.py` and import `Node` from the file.

{% include header-python.html %}
```python
import numpy as np
import pandas as pd

from .node import Node

class DecisionTree:
    """
    Tree of nodes, with methods for building tree in a way that minimizes
    Gini impurity.
    """
    def __init__(
        self,
        df: pd.DataFrame,
        target_col: str,
        max_depth: int = 4
    ) -> None:
        self.root = Node(df, target_col)
        self.max_depth = max_depth
```

This tree begins with the root, which is a `Node` we instantiate with `df` and `target_col`. We can also set a maximum depth our tree can grow, which helps prevent overfitting.

Now let's write the logic to process a split.

Tree could be just one node if there's one rule that completely partitions the classes.


Josh Starmer's [excellent video on how decision trees are built](https://www.youtube.com/watch?v=_L39rN6gz7Y)


* Check what impurity metrics are offered by sklearn's `DecisionTreeClassifier` and `RandomForestClassifier` classes (and what the defaults are).

# Footnotes
#### 1. [Decision Tree Training](#1-decision-tree-training)
If you limit the depth of the tree, you'll end up with leaf nodes that are still a mixture of the classes. This is ok!
