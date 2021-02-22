---
layout: post
title: Building a full-stack spam catching app
author: matt_sosna
image: "images/projects/spamcatch-demo.png"
---

![]({{  site.baseurl  }}/images/projects/spamcatch-demo.png)

[**SpamCatch**](https://spam-catcher.herokuapp.com) is a fun side project I did to bring together [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing), [Flask](https://flask.palletsprojects.com/en/1.1.x/), and [the front-end](https://blog.udacity.com/2014/12/front-end-vs-back-end-vs-full-stack-web-developers.html). Classifying spam text messages is a classic machine learning problem, but I'd never seen people test their classifier on raw strings of text. I'd also never seen a spam classifier hooked up to a nice user interface, where people could use the classifier without needing to know Python or Git.

This blog post will go through how to build a spam classifier with a sleek frontend. In short, here are the steps:
1. Create a [TF-IDF](https://monkeylearn.com/blog/what-is-tf-idf/) vectorizer on a corpus of ham and spam text messages
2. Train a random forest classifier on the TF-IDF vectors
3. Build a simple Flask app with endpoints for webpages and the random forest classifier
4. Write the HTML and CSS for the user-facing pages
5. Write the JavaScript to communicate between the user-facing pages and the spam classifier
6. Deploy to Heroku so others can see your app

**Make sure to [check out the actual app](https://spam-catcher.herokuapp.com)!** (If it takes a minute to load, that's because the dyno went to sleep. The free plan only gets you so far!) You can also view the source code [here](https://github.com/mgsosna/spamCatch).

## Table of contents
* [<span style="font-size:20px">**Background**</span>](#background)
  - [**Intro**](#intro)
  - [**Strings to vectors**](#strings-to-vectors)
* [<span style="font-size:20px">**How it works**</span>](#how-it-works)
  - [**Python**](#python)
    - [The classifier](#the-spam-classifier)
    - [Flask](#flask)
  - [**The front-end**](#the-front-end)
    - [HTML](#html)
    - [JavaScript](#javascript)
  - [**Deployment**](#deployment)

## Background
### Intro
Spam messages are at best a nuisance and [at worst dangerous](https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams). While malicious spam can be carefully tailored to the recipient to sound credible, the vast majority of spam out there is easily identifiable crap. You usually don't need to even read the entire message to identify it as spam $-$ there's a sense of urgency, money needed or offered, a sketchy link to click.

If spam is so predictable, let's just write some code to automatically identify it, throwing it in the trash before we even need to see it. Our first guess might be to write a bunch of rules, a series of `if` statements that get triggered when our classifier sees certain words in the message. Accepting the risk of losing out on a once in a lifetime, all-expenses-paid vacation, I could configure my classifier to automatically delete any message with the word `free` in it.

But that's not quite right... yes, the word `free` pops up a lot in spam, but it also appears in normal speech all the time, too. (*"Hey, are you free tonight?"*, for example.) We need more rules... lots more rules. As we added more and more rules, our classifier would quickly become incredibly complicated. We'd need dozens or hundreds of `if` statements, and we'd want their logic to be informed by research on how frequently certain words appear in spam versus normal messages (also called "ham"), and then we'd probably want some kind of scoring system based on all our rules. And perhaps most challenging of all... **we'd need to write all of this ourselves!**

<div style="text-align: center; font-weight: bold">
Quick! Click on <a src="https://en.wikipedia.org/wiki/Natural_language_processing">this link</a> to find a better way!
</div>

Just kidding. But that link *does* point us to a tempting alternative $-$ the field of NLP, or [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing). NLP is a subfield of artificial intelligence that uses computational techniques to understand human language. In essence, **NLP converts words to *numbers* so we can do math on them.** With NLP, we can reinterpret our messages as *vectors of numbers*, then train a machine learning classifier to identify patterns in the vectors that distinguish spam from normal messages.

### Strings to vectors
We first need to decide what kind of vector to turn each text message into. The simplest approach would be to create a [**bag of words**](https://towardsdatascience.com/a-simple-explanation-of-the-bag-of-words-model-b88fc4f4971) from our *documents* (a more general term for our text samples). In a bag of words approach, we first identify the *vocabulary* of unique words in our set of documents, then create a vector of word frequencies for each document. If our training set consisted of the three documents below, for example, our vocabulary would be `the`, `cat`, `sat`, `in`, `hat`, and `with`, and we could categorize each document by how frequently each word appears.

![]({{  site.baseurl  }}/images/projects/bag_of_words.png)
<span style="font-size:12px"><i>Source: [Victor Zhou](https://towardsdatascience.com/a-simple-explanation-of-the-bag-of-words-model-b88fc4f4971)</i></span>

But these "term frequency" vectors created by a bag of words aren't *that* informative. Yes, they tell us how many times the word `cat` appears in a document, for example. But knowing that `cat` appears once in *"the cat sat"* becomes meaningless when you realize `cat` appears once in *every* document! In fact, unless we looked at all the other documents, we wouldn't know whether `cat` appearing 100 or 1,000 times in a document is informative at all.<sup>[[1]](#1-strings-to-vectors)</sup>

It's therefore better to weight our term frequency vectors by **how frequently the terms occur across *all* documents**. If every document says the word `cat` 100 times, it's no big deal $-$ but if your document is the *only* one to mention `cat`, that's incredibly informative! These weighted vectors are called **term frequency - inverse document frequency (TF-IDF)** vectors.




## How it works
### Python
#### The classifier
The core of the app is the actual classifier, a Python class called [SpamCatcher](https://github.com/mgsosna/spamCatch/tree/main/static/python/spam_catcher.py). The class has methods for accomplishing a few key tasks:
* Training a TF-IDF vectorizer
* Converting strings to TF-IDF vectors
* Training a random forest classifier on TF-IDF vectors
* Passing a string to the classifier and returning the probability that a string is spam

One of the key methods here is `extract_features`, which uses Scikit-learn's `TfIdfVectorizer` to convert an iterable of documents into TF-IDF values. (TF-IDF, or term frequency - inverse document frequency, is a way to categorize each term in a document by its frequency of occurrence *within the document*, while reducing the importance of terms frequent *across all documents*). If `SpamCatcher` doesn't already have a `tfidf_vectorizer` attribute, it trains one on these documents.

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

The output of this function is a dataframe where each row is a document, the first column is the ham/spam label, and the remaining several thousand columns are the TF-IDF values for each term. We use this dataframe to then train a random forest classifier. We set this classifier to `self.model`, as well as save its accuracy and most informative features for easier retrieval later.

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

To actually train our model, we use a CSV stored in the `static/data/` directory. This location is hard-coded as a global variable, `DATA_PATH`, at the top of the script. We also use this directory to save a pickle file of our model once it's been trained. When we instantiate our class and run `set_model`, we'll load the model if it already exists, otherwise we'll train a new one.

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

The final "main" function of this class is one that actually predicts whether a text message is spam or not. We need to first convert the string to a TF-IDF vector. It's critical that this vector has the same features our model was trained on, so we use the same `TFIDFVectorizer` instance that was used to create our training set. This is one major advantage of object-oriented programming; we can easily refer to both this original vectorizer and our random forest classifier by making them attributes of `SpamCatcher`.

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

#### Flask
Our [Flask app](app.py) is fairly simple. We begin by loading the required libraries, instantiating `SpamCatcher`, and creating our application.

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

### The front-end
#### HTML
Our HTML is stored in the `templates` directory, as Flask expects. We start with a header to load in D3.js, Bootstrap CSS, and our custom CSS files. We also include a `<style>` tag to specify a footer class.

{% include header-html.html %}
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SpamCatch: Let's catch some spam</title>
    <script src="https://d3js.org/d3.v5.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="../static/css/reset.css">
    <link rel="stylesheet" href="../static/css/styles.css">
    <style>
            #footer {
                position: fixed;
                padding: 10px 10px 0px 10px;
                bottom: 0;
                width: 100%;
                height: 40px;
                font-size: 16px;
                text-align: center;
            }
    </style>
</head>
```

This simple styling gives us the black background with white text.

{% include header-html.html %}
```html
<body style="background-color: black; color: white">
```

This `<div>` is our background image. I found it easier to have a CSS class with the image as the background rather than inserting the image with `<img>` tags.

{% include header-html.html %}
```html
<div class="hero text-center"></div>
```

The CSS for this class, in [styles.css](static/css/styles.css):

{% include header-css.html %}
```css
.hero {
    position: relative;
    height: 240px;
    padding: 1px;
    margin-top: -2px;
    margin-left: -10px;
    background: black;
        background-attachment: scroll;
        /* image source: https://www.wsj.com/articles/getting-attacked-by-robotexts-heres-what-to-do-11566385200 */
        background-image: url("../images/spam.png");
        background-size: auto;
        background-size: cover;
}
```

After a header to get us pumped up, we have an input field to type in the spam message, with a placeholder to guide the user. Hitting enter (or even clicking outside the box) will trigger the JavaScript event handler (which we'll cover in a moment), but we also add a button for clarity.

{% include header-html.html %}
```html
<div class="text-center">
    <h1 style="color:white">Let's catch some spam.</h1>
<input id="text" size="100" placeholder="Type a text message here"
 style="background-color: black; color: white; border-color: black; font-size:16px">
 <button id="button" type="button" class="btn-danger" style="font-size:17px">Submit</button>
</div>
```

We then have two elements that are empty at loading but will be updated with the model output once a user submits a message.

{% include header-html.html %}
```html
<h1 id="spamProb" class="text-center spamProb"></h1>
<div id="decision" class="text-center" style="font-size: 20px"></div>
```

Finally, we have our footer with a link to the `/about` endpoint, as well as our JavaScript script that will make our page dynamic.

{% include header-html.html %}
```html
<div id="footer">
<a href="/about" style="color:orange">More info</a>
</div>

</body>

<script src="../static/js/script.js"></script>
</html>
```

#### JavaScript
We start by defining strings that we'll reference or modify later. `SPAM_API` is our classifier endpoint, while the following templates are the HTML we'll use for any probability returned by the endpoint. We use our custom `String.format` function to fill the `{0}` and `{1}` placeholders with inputted arguments; it's apparently taboo to modify built-in classes in JavaScript, but I was craving something analogous to Python's convenient string templating.

{% include header-javascript.html %}
```javascript
const SPAM_API = "/classify"
var spamProbTemplate = `Spam probability: <span style="color: {0}">{1}</span><span style="color:white">%</span>`;
var decisionTemplate = `<span style="color: {0}">{1}</span>`;
```

We then have our event handlers. The first function, `onSubmit`, gets the value of the input text field, logs it to the console, and passes it to `updateSpamProb`.

{% include header-javascript.html %}
```javascript
function onSubmit() {
    var text = d3.select("#text").property("value");
    console.log(text);
    updateSpamProb(text);
}
```

`updateSpamProb` then selects the (formerly empty) div whose ID is `spamProb`. It fills the URL with the text from the input field, then uses D3 to perform a `GET` request to our `classify` Flask endpoint. Our endpoint returns a probability of spam, which we convert to a HEX color with `prob2color`. We then format our `spamProbTemplate` with the color and spam probability (converted to a rounded percentage), and assign this to the div's HTML. We then use `updateDecision` to update the `decisionTemplate` with the corresponding message and color.

{% include header-javascript.html %}
```javascript
function updateSpamProb(value) {
    var div = d3.select("#spamProb");
    var url = `${SPAM_API}/${value}`;

    d3.json(url).then(prob => {
         var color = prob2color((1-prob));
         div.html(String.format(spamProbTemplate, color, Math.round(100*prob)));
         updateDecision(prob, color);
     });
}
```

Finally, we have the event listeners, which are what actually connect these JavaScript functions to our HTML page. When the user changes the text input field or clicks the button, we'll trigger `onSubmit`, which kicks off the whole process.

{% include header-javascript.html %}
```javascript
d3.select("#text").on("change", onSubmit);
d3.select("#button").on("click", onSubmit);
```

### Deployment
We can serve our app locally with `python app.py` and then navigating to `localhost:5000` (or whichever port your app ends up using), but the next level is being able to let anyone interact with the app. For this, we turn to Heroku. I found [this StackAbuse article](https://stackabuse.com/deploying-a-flask-application-to-heroku/) incredibly helpful. To summarize briefly:

1. Create a `Procfile` that's just the line `web: gunicorn app:app --preload --workers 1`.
  - This file tells Heroku to use `gunicorn` to serve our app, which is called `app` inside `app.py`, and to preload a worker before serving the app. Preloading causes Heroku's error logs to be much more informative.
2. Create a `requirements.txt` file with the necessary packages for your app to run. Make sure `Flask` and `gunicorn` are included.
3. Create a Heroku account and start a new application.
4. Link the GitHub repo for your app to your Heroku account, then manually deploy your app.
5. Repeat steps 1-4 a dozen times, puzzling over the error logs and making small changes. The final bug for me was needing to have `scikit-learn==0.21.3` in my requirements file, not `sklearn`.
6. Once you make it through, celebrate! You've deployed a web app!

## Conclusions
Ways to make it better:
* Looking for patterns in the URLs themselves. `www.google.com` is fine, but `u7x0apmw.com` isn't.
* Add features like number of letters that are capitalized, number of exclamation marks

## Footnotes
#### 1. [Strings to vectors](#strings-to-vectors)
Some would consider the word `cat` appearing 100 times in a document to be... *catastrophic.*
