---
layout: post
title: Building a full-stack spam catching app - 2. Backend
title-clean: Building a full-stack spam catching app <div class="a2">2. Backend</div>
author: matt_sosna
image: "images/projects/spamcatch-demo.png"
---

![]({{  site.baseurl  }}/images/projects/spamcatch-demo.png)

Welcome back! The [last post]({{  site.baseurl  }}/spamCatch-1) covered the theory for why we'll use NLP and machine learning for spam classification. This blog post will go through how to build a spam classifier with a sleek frontend. In short, here are the steps:
1. Train a [TF-IDF](https://monkeylearn.com/blog/what-is-tf-idf/) vectorizer on a corpus of [ham and spam text messages](https://www.kaggle.com/uciml/sms-spam-collection-dataset), removing stop words and performing [lemmatization](https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html) to make it easier for a model to understand the content of each document
2. Train a [random forest](https://stackabuse.com/random-forest-algorithm-with-python-and-scikit-learn/) classifier to distinguish between "spam" and "ham" TF-IDF vectors
3. Build a simple [Flask](https://flask.palletsprojects.com/en/1.1.x/) app with endpoints for webpages and the random forest classifier
4. Write the HTML and CSS for the user-facing pages
5. Write the JavaScript to communicate between the user-facing pages and the spam classifier
6. Deploy to [Heroku](https://www.heroku.com/about) so others can use your app

**Make sure to [check out the actual app](https://spam-catcher.herokuapp.com)!** (If it takes a minute to load, that's because the dyno went to sleep. The free plan only gets you so far!) You can also view the source code [here](https://github.com/mgsosna/spamCatch).

---
<span style="font-size:18px">**1. Background** ([last post]({{  site.baseurl  }}/spamCatch-1))</span>
  - [Spam]({{  site.baseurl  }}/spamCatch-1/#spam)
  - [Strings to vectors]({{  site.baseurl  }}/spamCatch-1/#strings-to-vectors)
  - [Why random forest?]({{  site.baseurl  }}/spamCatch-1/#why-random-forest)
  - [What is Flask?]({{  site.baseurl  }}/spamCatch-1/#what-is-flask)<br><br>

<span style="font-size:18px">**2. Backend** (this post)</span>
  - [**Python**](#python)
    - [The TF-IDF vectorizer](#the-tf-idf-vectorizer)
    - [The classifier](#the-spam-classifier)
    - [Flask](#flask)

<span style="font-size:18px">**3. Frontend and Deployment** ([next post]({{  site.baseurl  }}/spamCatch-3))</span>
  - [**The front-end**]({{  site.baseurl  }}/spamCatch-3/#the-front-end)
    - [HTML]({{  site.baseurl  }}/spamCatch-3/#html)
    - [JavaScript]({{  site.baseurl  }}/spamCatch-3/#javascript)
  - [**Deployment**]({{  site.baseurl  }}/spamCatch-3/#deployment)

---
## Python
The core of the app is a Python class called [SpamCatcher](https://github.com/mgsosna/spamCatch/tree/main/static/python/spam_catcher.py) that has two main components: a **TF-IDF vectorizer** that converts strings to TF-IDF vectors, and a **random forest classifier** that outputs the probability that a TF-IDF vector is spam. Both components must first be *trained* before they can output vectors or spam probabilities.

We start by creating a Python class with a few attributes initialized to `None`. These attributes $-$ the TF-IDF vectorizer, the random forest model, and the model's accuracy and top features $-$ will be referenced repeatedly in different contexts (e.g. training the model vs. generating predictions), so it's convenient to have them in a location any function within and outside `SpamCatcher` can easily reference.

{% include header-python.html %}
```python
class SpamCatcher:
    """Methods for training a ham-spam classifier"""

    def __init__(self):
        self.tfidf_vectorizer = None
        self.model = None
        self.accuracy = None
        self.top_features = None
```

Now let's write the methods that will actually update these attributes.

### The TF-IDF vectorizer
Rather than coding a TF-IDF vectorizer ourselves, we'll let Scikit-learn's `TfIdfVectorizer` do all the hard work for us. There are essentially only two steps we need to worry about: training our vectorizer on the sample text messages (so it learns the vector space of term frequencies across all documents), and generating TF-IDF vectors once the vectorizer is trained.

The method `extract_features` accomplishes the first goal for us.

{% include header-python.html %}
```python
def extract_features(self,
                     labels: pd.Series,
                     docs: pd.Series) -> pd.DataFrame:
    """
    | Create dataframe where each row is a document and each column
    | is a term, weighted by TF-IDF (term frequency - inverse document
    | frequency). Lowercases all words, performs lemmatization,
    | and removes stopwords and punctuation.
    |
    | ----------------------------------------------------------------
    | Parameters
    | ----------
    |  labels : pd.Series
    |    Ham/spam classification
    |
    |  docs : pd.Series
    |    Documents to extract features from
    |
    |
    | Returns
    | -------
    |  pd.DataFrame
    """
    if not self.tfidf_vectorizer:
        self.set_tfidf_vectorizer(docs)

    # Transform documents into TF-IDF features
    features = self.tfidf_vectorizer.transform(docs)

    # Reshape and add back ham/spam label
    feature_df = pd.DataFrame(features.todense(),
                              columns=self.tfidf_vectorizer.get_feature_names())
    feature_df.insert(0, 'label', labels)

    return feature_df
```

The first step checks whether there's already a vectorizer present in `self.tfidf_vectorizer`. If there isn't, `self.set_tfidf_vectorizer` is called. This function initializes a `TfidfVectorizer`, removes English stop words, and then trains the vectorizer on the documents.<sup>[[1]](#1-the-tf-idf-vectorizer)</sup>

{% include header-python.html %}
```python
def set_tfidf_vectorizer(self,
                         training_docs: pd.Series) -> None:
    """
    | Fit the TF-IDF vectorizer. Updates self.tfidf_vectorizer
    |
    | ---------------------------------------------------------
    | Parameters
    | ----------
    |  training_docs : pd.Series
    |    An iterable of strings, one per document, to use for
    |    fitting the TF-IDF vectorizer
    |
    |
    | Returns
    | -------
    |  None
    """
    self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    self.tfidf_vectorizer.fit(training_docs)
    return None
```

The next step in `extract_features` uses `self.tfidf_vectorizer` to transform each document into a TF-IDF vector. We then turn the output into a dataframe and insert a column for the "ham" vs. "spam" labels.

### The classifier
The second core piece of our app is the classifier that takes in a TF-IDF vector and outputs a probability of spam. Like the TF-IDF vectorizer, there are two main roles: 1) training our model, and 2) using it to classify messages.

We start with the aptly-titled `train_model`. This function takes in a dataframe where the first column is the spam/ham labels and the remaining columns are the elements of each document's TF-IDF vector. Setting `X` to be the second column onward is convenient, as none of this code needs to change if we update our training set and change the number of terms in our vocabulary.

In line 24 we manually specify that our target class is `spam`. (Pro tip for avoiding mysterious bugs where your model is actually predicting *the opposite* class!)

In lines 26 onward, we split our data into training and testing, fit our classifier, and then update the `model`, `accuracy`, and `top_features` attributes of our class.

{% include header-python.html %}
```python
def train_model(self,
                df: pd.DataFrame) -> None:
    """
    | Train a random forest classifier on df. Assumes first column
    | is labels and all remaining columns are features. Updates
    | self.model, self.accuracy, and self.top_features
    |
    | ------------------------------------------------------------
    | Parameters
    | ----------
    |  df : pd.DataFrame
    |    The data, where first column is labels and remaining columns
    |    are features
    |
    |
    | Returns
    | -------
    |  None
    """
    X = df.iloc[:, 1:]
    y = df.iloc[:, 0]

    # Set spam as target
    y.replace({'ham': 0, 'spam': 1}, inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, y_train)

    self.model = rf
    self.accuracy = round(accuracy_score(rf.predict(X_test), y_test), 4)
    self.top_features = self._get_top_features(list(X_train))
    return None
```

`self._get_top_features` creates a dataframe from the columns in `X_train` and the feature importances from `self.model`; it's not essential to our story so check out this footnote<sup>[[2]](#2-the-classifier)</sup> if you want more info.

To actually train our model, we use a CSV stored in the `static/data/` directory. This location is hard-coded as a [global variable](https://en.wikipedia.org/wiki/Global_variable), `DATA_PATH`, at the top of the script (not shown here). We also use this directory to save a pickle file of our model once it's been trained. When we instantiate our class and run `set_model`, we'll load the model if it already exists, otherwise we'll train a new one.

{% include header-python.html %}
```python
def set_model(self,
              save_on_new: bool = True) -> None:
    """
    | Set self.model. Uses existing model at MODEL_PATH if one exists,
    | otherwise calls self.load_and_train. Model saved to MODEL_PATH
    | if save_on_new is True.
    |
    | ---------------------------------------------------------------
    | Parameters
    | ----------
    |  save_on_new : bool
    |    If self.load_and_train invoked, whether the new model should
    |    be saved to MODEL_PATH
    |
    |
    | Returns
    | -------
    |  None
    """
    if os.path.isfile(MODEL_PATH):
        logging.debug(f"Using existing model at {MODEL_PATH}")
        with open(MODEL_PATH, "rb") as input_file:
            obj = pickle.load(input_file)
            self.tfidf_vectorizer = obj['tfidf_vectorizer']
            self.model = obj['model']
            self.accuracy = obj['accuracy']
            self.top_features = obj['top_features']

    else:
        logging.debug(f"No model at {MODEL_PATH}; training new model")
        self.load_and_train()

        if save_on_new:
            logging.debug(f"Saving new model to {MODEL_PATH}")
            with open(MODEL_PATH, "wb") as output_file:
                pickle.dump(vars(self), output_file)

    return None
```

The final "main" function of this class is one that actually predicts whether a text message is spam. Our first step is to convert the string to a TF-IDF vector. **It's critical that this vector has the same features our model was trained on,** so we use the same `TFIDFVectorizer` instance that was used to create our training set. This is one major advantage of object-oriented programming; we can easily refer to both this original vectorizer and our random forest classifier by making them attributes of `SpamCatcher`.

{% include header-python.html %}
```python
def classify_string(self,
                    text: str) -> float:
    """
    | Get the probability that a string is spam. Transforms the
    | string into a TF-IDF vector and then returns self.model's
    | prediction on the vector.
    |
    | ---------------------------------------------------------
    | Parameters
    | ----------
    |  text : str
    |    A raw string to be classified
    """
    if not self.tfidf_vectorizer:
        raise ValueError("Cannot generate predictions; must first "
                         " set self.tfidf_vectorizer")

    vec = self.tfidf_vectorizer.transform([text])
    return self.model.predict_proba(vec)[0][1]
```

### Summary
Congrats! We've just built our machine learning spam classifier. To review, here's a schematic for what our `SpamCatcher` class looks like. (For the full code, check out the file [here](https://github.com/mgsosna/spamCatch/blob/main/static/python/spam_catcher.py).)

```
< imports >
< global variables >

class SpamCatcher:
    <attributes>
        - TF-IDF vectorizer
        - Random forest model
        - Model accuracy
        - Top features

    <methods>
        - set_model
        - load_and_train
        - extract_features
        - set_tfidf_vectorizer
        - train_model
        - _get_top_features
        - classify_string
```

At this point, we could load `SpamCatcher` into another Python file and actually use it to generate predictions. If we have a Python file in the same directory as `spam_catcher.py`, we could load and use our model like this:

{% include header-python.html %}
```python
from .spam_catcher import SpamCatcher

sc = SpamCatcher()
sc.set_model()
sc.classify_string("Hello")  # 0.0
```

While this works nicely for local development, we're pretty constrained in how we can use our model. In the next section, we'll use Flask to build out a web server that lets us interact with our model from other Python environments or even outside of Python.

### Flask
#### Set up
Let's build the architecture to *serve* our model's outputs. We'll accomplish this by building [a Flask app](app.py). We'll start by organizing our project like this:

```bash
spamCatch
|   app.py
|   static
|      data
|         data.csv
|         model.pkl
|      python
|         __init__.py
|         spam_catcher.py
```

Our `__init__.py` looks like this:

{% include header-python.html %}
```python
from .spam_catcher import SpamCatcher
```

Python [\_\_init_\_ files](https://stackoverflow.com/questions/448271/what-is-init-py-for) let us treat directories as packages. This lets us load `SpamCatcher` more easily.

#### app.py
Now let's build out `app.py`. We begin by loading the required libraries, instantiating `SpamCatcher`, and creating our application.

{% include header-python.html %}
```python
from flask import Flask, render_template, jsonify
from static.python import SpamCatcher

spam_catcher = SpamCatcher()
spam_catcher.set_model(save_on_new=True)

app = Flask(__name__)
```

We then define our endpoints. We'll have two endpoints that just serve HTML pages: our main page with the classifier, and a short "About" page.

{% include header-python.html %}
```python
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")
```

For fun, I included an "inspect" endpoint, where we can actually get information about our random forest classifier, which is otherwise inaccessible to us.

{% include header-python.html %}
```python
@app.route("/inspect")
def inspect():
    return jsonify({'top_features': spam_catcher.top_features,
                    'accuracy': spam_catcher.accuracy})
```

Finally, the main attraction: the classifier endpoint itself. I wasn't sure whether I'd be able to get away with just storing the text to classify in the URL itself - would the model get confused by spaces getting converted to `%20`, for example? It turned out to be a non-issue. For debugging, I included a `print` statement, which updates the console when serving the app locally.

{% include header-python.html %}
```python
@app.route("/classify/<string:text>")
def classify(text):
    print(spam_catcher.classify_string(text))
    return jsonify(spam_catcher.classify_string(text))
```

And of course, we need the following code to actually start our app once we type `python app.py` in the Terminal.

{% include header-python.html %}
```python
if __name__ == "__main__":
    app.run(debug=True)
```

## Conclusions
This post covered the backend. In the next post, we'll cover the frontend and deployment. See you there!

## Footnotes
#### 1. [The TF-IDF vectorizer](#the-tf-idf-vectorizer)
We're assuming the documents being passed in are our training set if `self.tfidf_vectorizer` hasn't been fulfilled. In a production context, it'd be safer to have an explicit `train_vectorizer` function so it's harder to accidentally train the vectorizer on documents you didn't intend to.

#### 2. [The classifier](#the-classifier)
Here's the code for `_get_feature_importances`.

```python
def _get_top_features(self,
                      features: list) -> list:
    """
    | Return features sorted by importances from self.model. Number
    | limited to N_TOP_FEATURES.
    |
    | -------------------------------------------------------------
    | Parameters
    | ----------
    |  features : list
    |    List of feature names from X_train
    |
    |
    | Returns
    | -------
    |  list
    |    list of tuples in format (term, weight)
    """
    tuple_list = [*zip(features, self.model.feature_importances_.round(4))]
    sorted_list = sorted(tuple_list, key=lambda x: x[1], reverse=True)

    return sorted_list[:N_TOP_FEATURES]
```

We start by zipping the `X_train` column names (`features`) with the random forest's `feature_importances_` attribute. We then sort by feature importances $-$ the second element in each tuple, hence the `key=lambda x: x[1]` argument in `sorted`. We specify `reverse=True` so the terms are sorted from most important to least. Finally, we return only the `N_TOP_FEATURES` terms to avoid returning a list of thousands of terms. `N_TOP_FEATURES` is a [global variable](https://en.wikipedia.org/wiki/Global_variable); a coding best-practice is to make these variables all uppercase and define them at the top of the script.
