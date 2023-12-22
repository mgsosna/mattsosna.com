---
layout: post
title: Visualizing clustering algorithms
author: matt_sosna
---

Let's build an app that makes it easy to visualize how clustering algorithms work.

We'll need to know Flask and some JavaScript.

Directory layout:

```
spamCatch
|   app.py
|   Procfile
|   requirements.txt
|   static/
|      css/
|         reset.css
|         styles.css
|      images/
|         Star-Cluster.jpg
|         ck-demo.png
|         ck-header.png
|         cluster_struggles.png
|         ds_circle.png
|      js/
|         constants.js
|         plot_functions.js
|         script.js
|      python/
|         __init__.py
|         cluster_labeler.py
|         data_generator.py
|   templates/
|       about.html
|       base.html
|       blobs.html
|       index.html
|       moons.html
|       rings.html
```
