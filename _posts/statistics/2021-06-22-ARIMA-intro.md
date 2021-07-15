---
layout: post
title: A deep dive on ARIMA models
author: matt_sosna
---

Predicting the future has forever been a universal challenge, from decisions like whether to plant crops now or next week, marry someone or remain single, sell a stock or hold, or go to college or play music full time. We will never be able to perfectly predict the future<sup>[[1]](#1-intro)</sup>, but we can use tools from the statistical field of **forecasting** to better understand what lies ahead.

Forecasting involves **time series** data, or repeated measures over time. In data such as hourly temperature, daily electricity consumption, or annual global population estimates, we can look for patterns that collapse those hundreds or thousands of numbers down to a few defining characteristics. We can use time series analysis to quantify the rate at which the values are _trending_ upward or downward, measure how much one value is _correlated with the previous few_, decompose our data into its _underlying repeating cycles_, and more.

<img src="{{  site.baseurl  }}/images/statistics/arima/spy_500.png">
<span style="font-size: 12px"><i>S&P 500 daily prices over the last five years, an example of a highly-studied time series. Screenshot from Google Finance.</i></span>

To summarize a time series and predict its future, we need to model the relationship the values in the time series have with one another. Does today tend to be similar to yesterday? How about this time last week, or last year? How much do factors outside the time series play a role?

To answer these questions, we'll start with the most basic forecasting model and iterate towards a full autoregressive integrated moving average (ARIMA) model. We'll then take it a step further to include [_seasonal_](https://otexts.com/fpp2/seasonal-arima.html) and [_exogeneous_](https://www.statisticshowto.com/endogenous-variable/) variables, expanding into a [SARIMAX](https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html) model.

In other words, we'll build from this:

$$y_t = \epsilon_t$$

to this:

$$y_t =
\color{royalblue}{\sum_{n=1}^{p}\alpha_ny_{t-n}} +
\color{orangered}{\sum_{n=1}^{d}\omega_n(y_t-y_{t-n})} +
\color{darkorchid}{\sum_{n=1}^{q}m_n\epsilon_{t-n}} + \\
\color{green}{\sum_{n=1}^{r}\beta_nx_{tn}} +
\color{orange}{\sum_{n=1}^{P}\phi_ny_{t-sn}} +
\color{orange}{\sum_{n=1}^{D}\gamma_n(y_t-y_{t-sn})} +
\color{orange}{\sum_{n=1}^{Q}\theta_n\epsilon_{t-sn}} +
\epsilon_t $$

It looks complicated, but each of these pieces $-$ the <span style="color:royalblue; font-weight: bold">autoregressive</span>, <span style="color:orangered; font-weight: bold">integrated</span>, <span style="color:darkorchid; font-weight: bold">moving average</span>, <span style="color:green; font-weight: bold">exogeneous</span>, and <span style="color:orange; font-weight: bold">seasonal</span> components $-$ are just added together. We can easily tune up or down the complexity of our model by adding or removing terms.

Enough talk. Let's get started!

## Table of contents
* [**Getting started**](#getting-started)  
  - [Autocorrelation](#autocorrelation)
  - [Partial autocorrelation](#partial-autocorrelation)
  - [Stationarity](#stationarity)
* [**AR: Autoregression**](#ar-autoregression)
  - [AR(0): White noise](#ar0-white-noise)
  - [AR(1): Random walks and oscillations](#ar1-random-walks-and-oscillations)
* [**MA: Moving average**](#ma-moving-average)
* [**Additional components**](#additional-components)
  - [I: Integrated](#integrated)
  - [S: Seasonal](#seasonal)
  - [X: Exogeneous](#exogeneous)
* [**Comparing model fit**](#comparing-model-fit)


## Getting started
### Autocorrelation
Before we can start building any models, we need to cover a topic essential for describing time series: [**autocorrelation**](https://en.wikipedia.org/wiki/Autocorrelation). Autocorrelation means "self-correlation": it is the similarity of a time series' values with earlier values, or **lags**. If our time series was the values `[5, 10, 15]`, for example, our lag-1 autocorrelation would be the correlation of `[10, 15]` with `[5, 10]`.

We can visualize the correlation of the _present value_ with a _previous value $n$ lags ago_ with an autocorrelation plot. These plots are constructed by calculating the correlation of each value ($y_t$) with the value at the previous time step ($y_{t-1}$), two steps ago ($y_{t-2}$), three ($y_{t-3}$), and so on. The y-axis shows the strength of correlation at that lag, and we consider any value outside the shaded error interval to be a significant correlation.

The correlation at lag zero is always 1: $y_t$ better be perfectly correlated with $y_t$, or something's wrong. For the remaining lags, there are three typical patterns: 1) a lack of autocorrelation, 2) a gradual decay, and 3) a sharp drop. (Though in real-world data, you might get a mix of \#2 and \#3.)

<img src="{{  site.baseurl  }}/images/statistics/arima/autocorrelation.png">

Below we visualize the autocorrelation of [daily S&P 500 closing prices](https://finance.yahoo.com/quote/DX-Y.NYB/history?period1=1468195200&period2=1625961600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true) (left) and [daily maximum temperature at the Chicago Botanical Garden](https://www.ncdc.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND:USC00111497/detail) (right). The S&P 500 prices are so correlated that you have to look more than six months into the past to find uncorrelated values. The Chicago temperatures become uncorrelated faster, at about the two month mark, but then shoot out the other side and become _negatively correlated_ with temperatures from 4-7 months ago.

<img src="{{  site.baseurl  }}/images/statistics/arima/autocorr_examples.png">

### Partial autocorrelation
Autocorrelation plots are useful, but there can be substantial correlation "spillover" between lags. In the S&P 500 prices, for example, the lag-1 correlation is an astonishing 0.997 $-$ it's hard to get a good read on the following lags with the first lag indirectly affecting all downstream correlations.

This is where **partial autocorrelation** can be a useful measure. Partial autocorrelation is the correlation of $y_t$ and $y_{t-n}$, _controlling for the autocorrelation at earlier lags_. Rather than directly measure the correlation of $y_t$ and $y_{t-2}$, for example, we fit a linear regression of $y_t \sim \beta_0 + \beta_1y_{t-1}$, then find the correlation between $y_t$ and the _residuals_ of the regression. The residuals quantify the amount of variation in $y_t$ that cannot be explained by $y_{t-1}$, granting us an unbiased look at the relationship between $y_t$ and $y_{t-2}$.

Here's how the partial autocorrelation plots look for the S&P 500 prices and Chicago temperatures. Notice how the lag-1 autocorrelation remains highly significant, but the following lags dive off a cliff.

<img src="{{  site.baseurl  }}/images/statistics/arima/partial_autocorr_examples.png">

Autocorrelation and partial autocorrelation plots can be used to determine whether a simple AR or MA model (as opposed to full ARIMA model) is sufficient to describe your data<sup>[[2]](#2-partial-autocorrelation)</sup>, but you probably won't use them this way. In the fifty years since autocorrelation plots [were first introduced](https://archive.org/details/timeseriesanalys0000boxg), your laptop has likely become strong enough to perform a brute force scan to find the parameters for the ARIMA (or even SARIMAX) model that best describes your data, even if there are thousands of observations. These plots, then, are probably more useful as complementary ways of visualizing the temporal dependence of your data.

### Stationarity
As with any statistical model, there are assumptions that must be met when forecasting time series data. The biggest assumption is that the time series is **stationary.** In other words, we assume that **the parameters that describe the time series aren't changing over time.** To predict the future values of a time series, the data must have constant mean, variance, and autocorrelation.<sup>[[3]](#3-stationarity)</sup>

<img src="{{  site.baseurl  }}/images/statistics/arima/stationary.png">

This doesn't mean we can't forecast a time series unless it looks like a jumbled mess. Rather, we just have to _transform_ our time series of interest into one we can model. Some common transformations to deal with a changing mean or variance include [differencing](https://machinelearningmastery.com/remove-trends-seasonality-difference-transform-python/) (and then possibly differencing again), taking the logarithm or square root of the data, or taking the percent change. For changing autocorrelation, though, you may need to split your data into the different regimes.

We need to deal with these hassles because linear models tend to require that the samples be _independent_ and _identically likely to be drawn from the parent population_. This isn't the case with time series data, but many of the conveniences of independent random variables [also hold for stationary time series](https://stats.stackexchange.com/questions/19715/why-does-a-time-series-have-to-be-stationary)).
* Law of large numbers
* Central limit theorem

This means that the parameters that can summarize the time series aren't changing over time; the mean isn't increasing, the variance isn't decreasing, etc. It doesn't matter what section of the time series you look at $-$ the underlying process generating that data is the same. If this _isn't_ true, you'll need to transform your data before you can model it, e.g. by differencing.

ARMA = a nice model, but requires stationarity. ARIMA (differencing) is one way to achieve stationarity.



We'll generate the data using the incredibly handy `generate_arma_sample` function from the `statsmodels.tsa.arima_process` library in Python. We can pass in the coefficients for our autoregressive and moving average components, then see randomly generated data for such a process.


## AR: Autoregression
In a typical multivariate regression, you might model how features like _hours studied_ and _hours slept_ affect exam score. In an autoregressive model, you use _previous values of the target_ to predict _future values_. Rather than hours studied and slept, for example, you could use the student's two previous exam scores to predict their next score.

### AR(0): White noise
Let's start building out our ARIMA model. We'll start with the absolute simplest model, one with no terms. Well, almost. There's just the _error_ term.

$$ y_t = \epsilon_t $$

This kind of time series is called **white noise.** $\epsilon_t$ is a random value drawn from a normal distribution with mean 0 and variance $\sigma^2$.<sup>[[4]](#4-ar0-white-noise)</sup> Each value is drawn independently, meaning $\epsilon_t$ has no correlation with $\epsilon_{t-1}$, $\epsilon_{t+1}$, or any other $\epsilon_{t \pm n}$. Written mathematically, we would say:

$$ \epsilon_t \overset{iid}{\sim} \mathcal{N}(0, \sigma^2) $$

Because the $\epsilon_t$ values are completely independent, the time series described by the model $y_t = \epsilon_t$ is just a sequence of random numbers that **cannot be predicted**. Your best bet at guessing the next value is to just guess the mean of the distribution the samples are drawn from, which here is zero.

<center>
<img src="{{  site.baseurl  }}/images/statistics/arima/white_noise.png" height="110%" width="110%">
</center>

A time series of random values we can't forecast is actually a useful tool to have. It's an important null hypothesis for our analyses $-$ is there a pattern in the data that's sufficiently strong to distinguish the series from white noise?

We also can have a constant $c$ so our time series isn't centered at zero, e.g. $y_t = c + \epsilon_t$. When $c$ is zero, we just omit it for simplicity.

### AR(1): Random walks and oscillations
Let's start adding autoregressive terms to our model. The name indicates what we'll be doing $-$ "auto" means "self," so we'll be using the time series' _previous values_ as inputs to our model. These previous values are called **lags**.

In AR(1) model, we predict the current time step, $y_t$, by adjusting the _previous_ time step $y_{t-1}$ by a multiplier $\alpha_1$ and then adding white noise ($\epsilon_t$).

$$y_t = \alpha_1y_{t-1}+\epsilon_t$$

The value of $\alpha$ plays a defining role in what our time series looks like. If $\alpha_1 = 1$, we get a **random walk.**

<center>
<img src="{{  site.baseurl  }}/images/statistics/arima/random_walk.png" height="110%" width="110%">
</center>

If $0 < \alpha_1 < 1$, we have mean-reverting behavior. It's subtle, but you'll notice that the values are correlated with one another _and_ they tend to hover around zero. It's like less chaotic white noise. When $\alpha$ = 0, you get a white noise. When $\alpha$ = 1, you get a random walk.

<img src="{{  site.baseurl  }}/images/statistics/arima/mean_reversion.png">

We get really strange behavior if $\alpha_1$ is less than -1 or greater than 1. The magnitude of the time series values are constantly increasing, meaning they move exponentially further from the starting point. This causes the time series to not be stationary, meaning we can't model it anymore, so we usually [constrain our $\alpha_1$ parameter space](https://otexts.com/fpp2/AR.html) to -1 < $\alpha_1$ < 1 when performing [maximum likelihood estimation](https://towardsdatascience.com/probability-concepts-explained-maximum-likelihood-estimation-c7b4342fdbb1).


### AR(2): Smooth predictions


Here's what an AR(2) model would look like. It's the same as above, just with another $\alpha_n y_{t-n}$ term.

$$y_t = \alpha_1y_{t-1} + \color{orange}{\alpha_2y_{t-2}} + \epsilon_t$$

This says that the value at our current time step $y_t$ is determined by the value at the previous time step multiplied by some number, the value two time steps ago multiplied by another number, and then our "shock term," which is just white noise.

And here's the general form for an AR(p) model, where $p$ is the number of lags.

$$y_t = \sum_{n=1}^{p} \alpha_ny_{t-n} + \epsilon_t$$

When we fit a model with an autoregressive component (be it AR, ARMA, ARIMA, etc.), we solve for the $\alpha$ coefficients such that the predicted and actual $y_t$ values are as similar as possible.

## MA: Moving average
The second major component of an ARIMA model is the _moving average_ component. The $e_t$ term, previously just noise that we added to our forecast, now takes center stage. In an MA(1) model, our forecast for $y_t$ is the _previous_ white noise term with a multiplier, plus the _current_ white noise term.

$$y_t = m_1\epsilon_{t-1} + \epsilon_t$$

Here's what that would look like. Here we vary the value of $m_1$, the multiplier on the previous error value. I'm no forecasting expert, but I don't think there's an "ah-ha" waiting moment waiting for you when you look at these $-$ they should look fairly similar to a white noise plot.

<img src="{{  site.baseurl  }}/images/statistics/arima/ma1.png">

It's surprisingly hard to find a real-world example of a moving average process with no autoregressive component. What time series has no memory of its past behavior, but remembers its previous random noise? It took me days of searching before I found [this clear example](https://www.youtube.com/watch?v=voryLhxiPzE) by [YouTuber ritvikmath](https://www.youtube.com/channel/UCUcpVoi5KkJmnE3bvEhHR0Q).


You can imagine an MA model for a time series that doesn't care about its own history; it's just affected by external random factors that remember each other for a brief period.





MA model is a linear combination of past white noise with some multipliers, rather than past values of the time series itself.

MA models are strange. An MA model by itself (i.e. no AR component) is just modeling autocorrelation in the _errors_. Our $e_t$ term, previously just noise that we added to our time series forecasts, now takes center stage as we model the error.





Above,


It's hard to find a use case for using an MA model by itself. Generally, we use MA in conjunction with AR to account for different types of autocorrelation.



I wonder if the "indirect" effect of the errors on AR processes gets at the PACF sharp dropoff, while the "direct but restricted" gets at the sharp ACF dropoff in MA processes. Look into this...


Mean of an MA process is just zero, as it's the sum of white noise terms (which are sampled from a distribution centered at zero).

We build an MA model if the values are ACF drops sharply but the PACF trails off. (For AR: PACF drops sharply; ACF tails off.)


## SARIMAX
The main thing is the seasonal component.

{% include header-python.html %}
```python
import numpy as np
import pandas as pd
import pmdarima as pmd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

cycle_len = 25
train_start = -5*np.pi
train_end = 5*np.pi
step_size = 2*np.pi / cycle_len

x = np.arange(train_start, train_end, step_size)
y = np.sin(x) + np.random.normal(0, 0.05, len(x))

df = pd.DataFrame({'x': x, 'y': y})
```

We'll put our data into `pandas` so the index is automatically aligned when we plot our forecast later.

Now let's visualize it.

{% include header-python.html %}
```python
plt.figure(figsize=(15,5))
plt.plot(df['x'], df['y'])
plt.show()
```

Now let's build a model.

Scan for best parameters for $p$, $d$, $q$ (for the ARIMA part) and $P$, $D$, $Q$ and $S$ (for the seasonal part).

```python
results = pmd.auto_arima(df['y'],
                         start_p=0,  # initial guess for AR(p)
                         start_d=0,  # initial guess for I(d)
                         start_q=0,  # initial guess for MA(q)
                         max_p=2,    # max guess for AR(p)
                         max_d=2,    # max guess for I(d)
                         max_1=2,    # max guess for MA(q)
                         start_P=0,  # initial guess for seasonal AR(p)
                         start_D=0,  # initial guess for seasonal I(d)
                         start_Q=0,  # initial guess for seasonal MA(q)
                         trend='c',
                         information_criterion='aic',
                         trace=True,
                         error_action='ignore'
                         )
```


```python
mod = SARIMAX(df['y'],
              order=(0, 0, 0),
              seasonal_order=(1, 0, 0, cycle_len),
              trend='c')
```

## Conclusions
Why not just use an RNN? Well, it depends on the approach we want to take. If we're trying to generate the most accurate forecast without necessarily understanding how our model came to that conclusion, a deep learning model can be the way to go. But if we want to model the _underlying process that gave rise to that data_, we'll need to turn to statistics.


## Code to generate plots
#### White noise
```python
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_process import arma_generate_sample

# Set coefficients
ar_coefs = [1]
ma_coefs = [1]

# Plot data
plt.figure(figsize=(16,4.5))
for i, scale in enumerate([0.01, 0.1, 0.25]):

    y = arma_generate_sample(ar_coefs, ma_coefs, nsample=100,
                             scale=scale)

    plt.subplot(1, 3, i+1)
    plt.plot(y, label=f"$\sigma$ = {scale}")
    plt.ylim(-1, 1)
    plt.legend(fontsize=12, frameon=False, loc='upper left')

    if i == 1:
        plt.xlabel('Time (t)', fontsize=22)

plt.suptitle('White noise: $y_t = \epsilon_t$', fontsize=22)
plt.show()
```

#### Random walk
```python
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_process import arma_generate_sample

# Set coefficients
ar_coefs = [1, -1]  # Note: ar_coefs[1:] are negative of what you expect
ma_coefs = [1, 0]

# Plot data
plt.figure(figsize=(16,4.5))
for i, scale in enumerate([0.01, 0.03, 0.1]):

    # Generate data
    y = arma_generate_sample(ar_coefs, ma_coefs, nsample=1000,
                             scale=scale)

    plt.subplot(1, 3, i+1)
    plt.plot(y, label=f"$\sigma$ = {scale}")
    plt.ylim(-4, 4)
    plt.legend(fontsize=12, frameon=False, loc='upper left')

    if i == 1:
        plt.xlabel('Time (t)', fontsize=22)

plt.suptitle('Random walk: $y_t = y_{t-1} + \epsilon_t$', fontsize=22)
plt.show()
```

## Foonotes
#### 1. [Intro](#)
"We will never be able to perfectly predict the future" sounds obvious, but the reasoning behind it is actually fascinating. In the book [_Sapiens_](https://www.ynharari.com/book/sapiens-2/), Yuval Noah Harari talks about [two types of chaotic systems](https://www.goodreads.com/quotes/7426402-history-cannot-be-explained-deterministically-and-it-cannot-be-predicted). The first is chaos that doesn't react to predictions about it, such as the weather. Weather emerges via the nonlinear interactions of countless air molecules $-$ it's immensely difficult to predict but we can use stronger and stronger computer simulations to gradually improve our accuracy.

The second type of chaotic system, meanwhile, _does_ respond to predictions about it. History, politics, and markets are examples of this type of system. If we perfectly predict that the price of oil will be higher tomorrow than it is today, for example, the rush to buy oil will change its price both today and tomorrow, _causing the prediction to become inaccurate_.

As data scientists, we're used to thinking about our analyses as separate from the processes we're trying to understand. But in cases where our predictions actually influence the outcome, we have little hope to perfectly predict the future... unless perhaps we keep our guesses very quiet.

#### 2. [Partial autocorrelation](#partial-autocorrelation)
A sharp drop at lag $n$ in the autocorrelation plot indicates an **MA(n)** process, while a clear drop in the partial autocorrelation plot indicates an **AR(n)** process. However, unless your dataset is truly massive, you'll most likely end up doing a parameter scan to determine the parameters of a model that best describes your data. And if both autocorrelation plots trail off, you're looking at an ARMA or ARIMA process and will need to do a parameter scan anyway.

#### 3. [Stationarity](#stationarity)
I went down a long rabbit hole trying to understand what the assumption of stationarity really means. In the graphic of the stationary versus non-stationary processes, I use a noisy sine wave as the example of the stationary process. This dataset _does_ pass the [Augmented Dicky-Fuller test](https://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test), but if you extend the data out to 1000 samples, the ADF test no longer says the time series is stationary.

This is because the ADF in essence measures reversion to the mean $-$ a non-stationary process has no problem drifting away, and previous lags don't provide relevant information. The lagged values of a stationary process, meanwhile, _do_ provide relvant info in predicting the next values.

A sine wave, though, is a bit of an exception to all this because it's deterministic, not stochastic. If you know that a time series is a sine wave and where in the wave you are, you can perfectly predict all past and future values of the series. The concept of stationarity [doesn't apply to deterministic processes](https://stats.stackexchange.com/questions/172979/is-a-model-with-a-sine-wave-time-series-stationary), so perhaps an ADF test isn't the right approach. But what about when your series has sesonality but noise on top? It feels like we're extremely restricted in the sorts of time series we can model if they all need to meet this strict definition of stationarity... I like the mean/variance/autocorr one.


#### 4. [AR(0): White noise](#ar0-white-noise)
In our example, the $\epsilon_t$ values are sampled from a normal distribution, so this is **Gaussian white noise.** We could easily use another distribution to generate our values, though, such as a uniform distribution.
