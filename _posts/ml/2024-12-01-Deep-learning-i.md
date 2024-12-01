---
layout: post
title: Deep Learning: I
author: matt_sosna
tags: machine_learning
---

**Questions to answer**
* Why not classical statistics?
* Why not machine learning?

Deep learning is ideal for when you have a massive feature space. You're trying to understand text, for example: the English language has [~470,000 words](https://www.merriam-webster.com/help/faq-how-many-english-words), and training a classical linear regression or random forest classifier just won't cut it. (Not even trying to generate text, just understand what the text is saying.)

Do we need fancier and fancier statistics? It turns out that _chaining together_ networks of extremely simple decisioning rules is the way to handle these challenges. The way we chain together the networks allows us to handle images (e.g., convolutional neural networks), text and time series (e.g., recurrent neural networks), and more.

# Starting with Sigmoids
What is the simplest decision? Binary: yes or no. This is how neurons in the animal brain work: they get stimulated up to a certain threshold and then fire if the threshold is exceeded. The input space is collapsed from a continuous value to a boolean: _fire_ or _do nothing_.

Artificial neurons are similar. (This is where I need to pull out the DL books.) ReLU, etc.
