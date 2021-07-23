---
layout: post
title: A deep dive on ARIMA models
author: matt_sosna
---

Predicting the future has forever been a universal challenge, from decisions like whether to plant crops now or next week, marry someone or remain single, sell a stock or hold, or go to college or play music full time. We will never be able to perfectly predict the future<sup>[[1]](#1-intro)</sup>, but we can use tools from the statistical field of **forecasting** to better understand what lies ahead.

Forecasting involves **time series** data, or repeated measures over time. In data such as hourly temperature, daily electricity consumption, or annual global population estimates, we can look for patterns that collapse those hundreds or thousands of numbers down to a few defining characteristics. We can use time series analysis to quantify the rate at which the values are _trending_ upward or downward, measure how much one value is _correlated with the previous few_, decompose our data into its _underlying repeating cycles_, and more.

<img src="{{  site.baseurl  }}/images/statistics/arima/spy_500.png">
<span style="font-size: 12px"><i>S&P 500 daily prices over the last five years, an example of a highly-studied time series. Screenshot from Google Finance.</i></span>

To summarize a time series and predict its future, we need to model the relationship the values in the time series have with one another. Does today tend to be similar to yesterday, a week ago, or last year? How much do factors outside the time series, such as noise or _other_ time series, play a role?

To answer these questions, we'll start with the most basic forecasting model and iterate towards a full autoregressive integrated moving average (ARIMA) model. We'll then take it a step further to include [_seasonal_](https://otexts.com/fpp2/seasonal-arima.html) and [_exogeneous_](https://www.statisticshowto.com/endogenous-variable/) variables, expanding into a [SARIMAX](https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html) model.

In other words, we'll build from this:

$$y_t = c + \epsilon_t$$

to this:

$$y_t = c +
\color{royalblue}{\sum_{n=1}^{p}\alpha_ny_{t-n}} +
\color{orangered}{\sum_{n=1}^{d}\omega_n(y_t-y_{t-n})} +
\color{darkorchid}{\sum_{n=1}^{q}\theta_n\epsilon_{t-n}} + \\
\color{green}{\sum_{n=1}^{r}\beta_nx_{tn}} +
\color{orange}{\sum_{n=1}^{P}\phi_ny_{t-sn}} +
\color{orange}{\sum_{n=1}^{D}\gamma_n(y_t-y_{t-sn})} +
\color{orange}{\sum_{n=1}^{Q}\eta_n\epsilon_{t-sn}} +
\epsilon_t $$

It looks complicated, but each of these pieces $-$ the <span style="color:royalblue; font-weight: bold">autoregressive</span>, <span style="color:orangered; font-weight: bold">integrated</span>, <span style="color:darkorchid; font-weight: bold">moving average</span>, <span style="color:green; font-weight: bold">exogeneous</span>, and <span style="color:orange; font-weight: bold">seasonal</span> components $-$ are just added together. We can easily tune up or down the complexity of our model by adding or removing terms.

Once we've built a model, we'll be able to predict the future of a time series like this.

<img src="{{  site.baseurl  }}/images/statistics/arima/example_forecast.png">

## Table of contents
* [**Getting started**](#getting-started)  
  - [Autocorrelation](#autocorrelation)
  - [Partial autocorrelation](#partial-autocorrelation)
  - [Stationarity](#stationarity)
* [**AR: Autoregression**](#ar-autoregression)
  - [AR(0): White noise](#ar0-white-noise)
  - [AR(1): Random walks and oscillations](#ar1-random-walks-and-oscillations)
  - [AR(p): Higher-order terms](#arp-higher-order-terms)
* [**MA: Moving average**](#ma-moving-average)
* [**ARMA: Autoregressive moving average**](#arma-autoregressive-moving-average)
* [**Additional components**](#additional-components)
  - [I: Integrated](#integrated)
  - [S: Seasonal](#seasonal)
  - [X: Exogeneous](#exogeneous)
* [**Comparing model fit**](#comparing-model-fit)


## Getting started
### Autocorrelation
Before we can start building any models, we need to cover a topic essential for describing time series: [**autocorrelation**](https://en.wikipedia.org/wiki/Autocorrelation). Autocorrelation means "self-correlation": it is the similarity of a time series' values with earlier values, or **lags**. If our time series was the values `[5, 10, 15]`, for example, our lag-1 autocorrelation would be the correlation of `[10, 15]` with `[5, 10]`.

We can visualize the correlation of the _present value_ with a _previous value $n$ lags ago_ with an **autocorrelation plot.** These plots are constructed by calculating the correlation of each value ($y_t$) with the value at the previous time step ($y_{t-1}$), two steps ago ($y_{t-2}$), three ($y_{t-3}$), and so on. The y-axis shows the strength of correlation at that lag, and we consider any value outside the shaded error interval to be a significant correlation.

The correlation at lag zero is always 1: $y_t$ better be perfectly correlated with $y_t$, or something's wrong. For the remaining lags, there are three typical patterns: 1) a lack of autocorrelation, 2) a gradual decay, and 3) a sharp drop. (Though in real-world data, you might get a mix of \#2 and \#3.)

<img src="{{  site.baseurl  }}/images/statistics/arima/autocorrelation.png">

Below we visualize the autocorrelation of [daily S&P 500 closing prices](https://finance.yahoo.com/quote/SPY/history?p=SPY) (left) and [daily maximum temperature at the Chicago Botanical Garden](https://www.ncdc.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND:USC00111497/detail) (right). The S&P 500 prices are so correlated that you have to look more than three months into the past to find uncorrelated values. The Chicago temperatures become uncorrelated faster, at about the two month mark, but then shoot out the other side and become _negatively correlated_ with temperatures from 4-7 months ago.

<img src="{{  site.baseurl  }}/images/statistics/arima/autocorr_examples.png">

### Partial autocorrelation
Autocorrelation plots are useful, but there can be substantial correlation "spillover" between lags. In the S&P 500 prices, for example, the lag-1 correlation is an astonishing 0.994 $-$ it's hard to get a good read on the following lags with the first lag indirectly affecting all downstream correlations.

This is where [**partial autocorrelation**](https://online.stat.psu.edu/stat510/lesson/2/2.2) can be a useful measure. Partial autocorrelation is the correlation of $y_t$ and $y_{t-n}$, _controlling for the autocorrelation at earlier lags_.

Let's say we want to measure the lag-2 autocorrelation without the lag-1 spillover. Rather than directly measure the correlation of $y_t$ and $y_{t-2}$, we'd fit a linear regression of $y_t \sim \beta_0 + \beta_1y_{t-1}$, then find the correlation between $y_t$ and the _residuals_ of the regression. The residuals quantify the amount of variation in $y_t$ that cannot be explained by $y_{t-1}$, granting us an unbiased look at the relationship between $y_t$ and $y_{t-2}$.

Here's how the partial autocorrelation plots look for the S&P 500 prices and Chicago temperatures. Notice how the lag-1 autocorrelation remains highly significant, but the following lags dive off a cliff.

<img src="{{  site.baseurl  }}/images/statistics/arima/partial_autocorr_examples.png">

Autocorrelation and partial autocorrelation plots can be used to determine whether a simple AR or MA model (as opposed to full ARIMA model) is sufficient to describe your data<sup>[[2]](#2-partial-autocorrelation)</sup>, but you probably won't use them this way. In the fifty years since autocorrelation plots [were first introduced](https://archive.org/details/timeseriesanalys0000boxg), your laptop has likely become strong enough to perform a brute force scan to find the parameters for the ARIMA (or even SARIMAX) model that best describes your data, even if there are thousands of observations. These plots, then, are probably more useful as complementary ways of visualizing the temporal dependence of your data.

### Stationarity
As with any statistical model, there are assumptions that must be met when forecasting time series data. The biggest assumption is that the time series is **stationary.** In other words, we assume that **the parameters that describe the time series aren't changing over time.** No matter where on the time series you look, you should see the same mean, variance, and autocorrelation.<sup>[[3]](#3-stationarity)</sup>

<img src="{{  site.baseurl  }}/images/statistics/arima/stationary.png">

This doesn't mean we can only forecast time series that look like the green jumbled mess above. While most real-world time series aren't stationary, we can _transform_ a time series into one that is stationary, generate forecasts on the stationary data, then _un-transform_ the forecast to get the real-world values. Some common transformations include [differencing](https://machinelearningmastery.com/remove-trends-seasonality-difference-transform-python/) (and then possibly differencing again), taking the logarithm or square root of the data, or taking the percent change.

Transformations are necessary because linear models require that the data they model be _independent_ and _identically likely to be drawn from the parent population_. This isn't the case with time series data $-$ any autocorrelation at all immediately violates the independence assumption. But many of the conveniences of independent random variables $-$ such as the [law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers) and the [central limit theorem](https://sphweb.bumc.bu.edu/otlt/mph-modules/bs/bs704_probability/BS704_Probability12.html) $-$ [also hold for stationary time series](https://stats.stackexchange.com/questions/19715/why-does-a-time-series-have-to-be-stationary). Making a time series stationary is therefore a critical step in being able to model our data.

## AR: Autoregression
With some basics behind us, let's start building towards our ARIMA model. We'll start with the **AR**, or **autoregressive** component, then later add in the moving average and integrated pieces.

### AR(0): White noise
The simplest model we can build is one with no terms. Well, almost. There's just a _constant_ and an _error_ term.

$$ y_t = c + \epsilon_t $$

This kind of time series is called **white noise.** $\epsilon_t$ is a random value drawn from a normal distribution with mean 0 and variance $\sigma^2$.<sup>[[4]](#4-ar0-white-noise)</sup> Each value is drawn independently, meaning $\epsilon_t$ has no correlation with $\epsilon_{t-1}$, $\epsilon_{t+1}$, or any other $\epsilon_{t \pm n}$. Written mathematically, we would say:

$$ \epsilon_t \overset{iid}{\sim} \mathcal{N}(0, \sigma^2) $$

Because all $\epsilon_t$ values are independent, the time series described by the model $y_t = \epsilon_t$ is just a sequence of random numbers that **cannot be predicted**. Your best guess for the next value is the mean of the distribution the samples are drawn from, which is zero.

Below are three white noise time series drawn from normal distributions with increasing standard deviation. $c$ is zero and is therefore omitted from the equation. (A positive or negative $c$ would cause the series to trend upwards or downwards, respectively.)

<center>
<img src="{{  site.baseurl  }}/images/statistics/arima/white_noise.png" height="110%" width="110%">
</center>

**A time series of random values we can't forecast is actually a useful tool to have.** It's an important null hypothesis for our analyses $-$ is there a pattern in the data that's sufficiently strong to distinguish the series from white noise? Our eyes love finding patterns $-$ even when none actually exist $-$ so a white noise comparison can protect against false positives.

White noise is also useful for determining whether our model is capturing all the [**signal**](https://conceptually.org/concepts/signal-and-noise) it can get from our time series. If the deviations of our forecasts from actual values _isn't_ white noise, [your model is overlooking a pattern](https://machinelearningmastery.com/white-noise-time-series-python/) that it could use to generate more accurate predictions.

### AR(1): Random walks and oscillations
Let's start adding autoregressive terms to our model. These terms will be lagged values of our time series, multiplied by coefficients that best translate those previous values into our current value.

In an AR(1) model, we predict the current time step, $y_t$, by taking our constant $c$, adding the _previous_ time step $y_{t-1}$ adjusted by a multiplier $\alpha_1$, and then adding white noise, $\epsilon_t$.

$$y_t = c + \alpha_1y_{t-1} + \epsilon_t$$

The value of $\alpha_1$ plays a defining role in what our time series looks like. If $\alpha_1 = 1$, we get a [**random walk**](https://www.sciencedirect.com/science/article/pii/S0370157317302946). Unlike white noise, our time series is free to wander away from its origin. Random walks are an incredibly useful model for stochastic processes across many applications, such as modeling [the movement of particles through a fluid](https://en.wikipedia.org/wiki/Brownian_motion), the [search path of a foraging animal](https://www.quantamagazine.org/random-search-wired-into-animals-may-help-them-hunt-20200611/), or [changes in stock prices](https://www.investopedia.com/terms/r/randomwalktheory.asp).

<center>
<img src="{{  site.baseurl  }}/images/statistics/arima/random_walk.png" height="110%" width="110%">
</center>

So when $\alpha_1$ = 0, we get white noise, and when $\alpha_1$ = 1, we get a random walk. When $0 < \alpha_1 < 1$, our time series exhibits [**mean reversion**](https://www.investopedia.com/terms/m/meanreversion.asp). It's subtle, but you'll notice that the values are correlated with one another _and_ they tend to hover around zero, like less chaotic white noise. Large changes in stock prices [tend to be followed by mean reversion](https://decodingmarkets.com/mean-reversion-trading-strategy/).

<img src="{{  site.baseurl  }}/images/statistics/arima/mean_reversion.png">

When fitting an AR model, we [constrain the $\alpha$ parameter space](https://otexts.com/fpp2/AR.html) to $-1 \leq \alpha \leq 1$. Unless you're modeling exponential growth or sharp oscillations, the time series described by these models are probably not what you're looking for.

<img src="{{  site.baseurl  }}/images/statistics/arima/bad_arr.png">

### AR(p): Higher-order terms
Adding more lags to our model is just a matter of adding $\alpha_n y_{t-n}$ terms. Here's what an AR(2) model looks like, with the additional term highlighted in blue.

$$y_t = c + \alpha_1y_{t-1} + \color{royalblue}{\mathbf{\alpha_2y_{t-2}}} + \epsilon_t$$

This says that the value at our current time step $y_t$ is determined by our constant $c$, plus the value at the previous time step $y_{t-1}$ multiplied by some number $\alpha_1$, plus the value two time steps ago $y_{t-2}$ multiplied by another number $\alpha_2$, plus a white noise value $\epsilon_t$. To fit this type of model, we now estimate values for both $\alpha_1$ and $\alpha_2$.

As we add more lags to our model, or we start including moving average, exogeneous, or seasonal terms, it will become useful to rewrite our autoregressive terms as a summation. (Statisticians also use [backshift notation](https://otexts.com/fpp2/backshift.html), but we'll stick with summations to avoid that learning curve.) Here's the general form for an AR(p) model, where $p$ is the number of lags.

$$y_t = c + \sum_{n=1}^{p} \alpha_ny_{t-n} + \epsilon_t$$

The above equation simply says "our current value equals our constant, plus every lag $y_{t-n}$ multiplied by its coefficient $\alpha_n$, plus $\epsilon_t$." We can use the same equation regardless of whether $p$ is 1 or 100... though if your model has 100 lags, you might want to look into including the next term we'll describe: the moving average.

## MA: Moving average
The second major component of an ARIMA model is the **moving average** component. This component is _not_ a rolling average, but rather _the lags in the white noise_.

The $\epsilon_t$ term, previously some forgettable noise we add to our forecast, now takes center stage. In an MA(1) model, our forecast for $y_t$ is our constant plut the _previous_ white noise term $\epsilon_{t-1}$ with a multiplier $\theta_1$, plus the _current_ white noise term $\epsilon_t$.

$$y_t = c + \theta_1\epsilon_{t-1} + \epsilon_t$$

As before, we can concisely describe an MA(q) model with this summation:

$$y_t = c + \sum_{n=1}^{q}\theta_n\epsilon_{t-n} + \epsilon_t$$

Here's are three MA(1) time series that vary in the value of $\theta_1$, the multiplier on $\epsilon_{t-1}$. Don't feel bad if you don't experience an "ah-ha" moment looking at these; they should look fairly similar to white noise.

<img src="{{  site.baseurl  }}/images/statistics/arima/ma1.png">

Moving average processes are a lot less intuitive than autoregression $-$ what time series has no memory of its past behavior, but remembers it previous random noise? Yet a surprising number of [real-world time series _are_ moving average processes](https://stats.stackexchange.com/questions/45026/real-life-examples-of-moving-average-processes), from mis-alignment of store goods and sales, battery purchases in response to (unpredicted) natural disasters, and low-pass filters such as the treble knobs on car stereos.

Here's a silly but helpful ["mis-alignment" example]([this clear example](https://www.youtube.com/watch?v=voryLhxiPzE)) from [YouTuber ritvikmath](https://www.youtube.com/channel/UCUcpVoi5KkJmnE3bvEhHR0Q). Imagine a recurring party where you're assigned to provide one cupcake per guest. The number of guests follows a white noise process and cannot be predicted ahead of time. With no idea how many people to expect, you start by bringing 10 cupcakes ($c=10$). When you arrive, you note how many cupcakes you over- or under-supplied ($\epsilon_t$). $y_t$ is the number of leftover cupcakes, and it's possible to be negative.

For the following meeting, you bring 10 cupcakes _adjusted by that difference from the previous meeting_ (now $\epsilon_{t-1}$) multiplied by some factor ($\theta_1$). You want to bring the negative of the number of cupcakes you were off by last time, so we set $\theta_1=-1$. If you were two short last time ($\epsilon_{t-1}=-2$), for example, you'd bring two extra.

We can therefore model the number of leftover cupcakes at each meeting like below. The blue terms are the number of cupcakes you bring to the meeting, and the orange is the number of people who show up.

$$y_t = \color{royalblue}{10 - \epsilon_{t-1}} + \color{orange}{\epsilon_t}$$

The thing to note here is that **this time series doesn't care about its own history;** it is only affected by external random noise that is remembered for a brief period. This is therefore a moving average process.

## Beyond the fundamentals
Having covered AR and MA processes, we have all we need to build ARMA and ARIMA models. As you'll see, these more complex models simply consist of AR and MA components added together.

### ARMA: Autoregressive moving average
Outside a textbook, you're unlikely to find a time series that's a pure autoregressive or pure moving average process. Real-world time series, rather, are much more likely to be comprised of both AR and MA components. These **ARMA** processes can be modeled with the following equation:

$$y_t = c + \sum_{n=1}^{p}\alpha_ny_{t-n} + \sum_{n=1}^{q}\theta_n\epsilon_{t-n}$$

ARMA models cover a wide range of topics... etc. etc.



Below are four ARMA(1,1) time series. As with the MA(1) plot above, it's difficult to look at any of the time series below and intuit the parameter values, or even that they're ARMA processes. We're at the point where our time series have become too complex to be able to get much out of inspecting the raw values.

<img src="{{  site.baseurl  }}/images/statistics/arima/arma.png">

But that's ok. Moving forward, we'll start using [**AIC**](https://en.wikipedia.org/wiki/Akaike_information_criterion) to determine which model to use and [**maximum likelihood estimation**](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation) to set the model parameters. At the end of this post, we'll walk through the Python code to do so. In the meantime, let's finish covering the remaining pieces of our SARIMAX model.

### ARIMA: Autoregressive integrated moving average
An ARIMA model is simply an ARMA model on the _differenced_ time series. We could perform the differencing ourselves and then fit the model, but.

```python
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import arma_generate_sample

ar_coefs = [1, -1]
ma_coefs = [1, 0.5]

y1 = arma_generate_sample(ar_coefs, ma_coefs, nsample=1500)
y2 = np.diff(y1)

mod1 = ARIMA(y1, order=(1, 1, 1)).fit()  # ARIMA on original
mod2 = ARIMA(y2, order=(1, 0, 1)).fit()  # ARMA on differenced

# AR coefficients are identical
print(mod1.polynomial_ar.round(4) == mod2.polynomial_ar.round(4))
# True

# MA coefficients are identical
print(mod1.polynomial_ma.round(4) == mod2.polynomial_ma.round(4))
# True
```



To do so, we'll use the `auto_arima` function from the [pmdarima](https://pypi.org/project/pmdarima/) library. Here's the code for identifying what the AR and MA orders should be for an ARMA model on the last five years of S&P 500 closing prices.

{% include header-python.html %}
```python
import pandas as pd
import pmdarima as pmd

df = pd.read_csv("spy.csv")

results = pmd.auto_arima(df['Close'],
                         d=0,        # restrict to ARMA, not ARIMA
                         start_p=0,  # initial guess for AR(p)
                         start_q=0,  # initial guess for MA(q)
                         max_p=2,    # max guess for AR(p)
                         max_q=2,    # max guess for MA(q)
                         trend='c',
                         information_criterion='aic',
                         trace=True,
                         error_action='ignore'
                         )

# Performing stepwise search to minimize aic
#  ARIMA(0,0,0)(0,0,0)[0] intercept   : AIC=13722.091, Time=0.03 sec
#  ARIMA(1,0,0)(0,0,0)[0] intercept   : AIC=inf, Time=0.10 sec
#  ARIMA(0,0,1)(0,0,0)[0] intercept   : AIC=12044.936, Time=0.20 sec
#  ARIMA(0,0,0)(0,0,0)[0]             : AIC=13722.091, Time=0.03 sec
#  ARIMA(1,0,1)(0,0,0)[0] intercept   : AIC=6654.430, Time=0.71 sec
#  ARIMA(2,0,1)(0,0,0)[0] intercept   : AIC=6680.479, Time=0.75 sec
#  ARIMA(1,0,2)(0,0,0)[0] intercept   : AIC=6627.935, Time=0.96 sec
#  ARIMA(0,0,2)(0,0,0)[0] intercept   : AIC=10841.632, Time=0.58 sec
#  ARIMA(2,0,2)(0,0,0)[0] intercept   : AIC=6637.467, Time=1.03 sec
#  ARIMA(1,0,2)(0,0,0)[0]             : AIC=6627.935, Time=0.96 sec
#
# Best model:  ARIMA(1,0,2)(0,0,0)[0] intercept
# Total fit time: 5.356 seconds
```

The code above says that an ARMA(1,2) model best fits


## Additional components
We've built an ARMA model. This gets us pretty far in modeling time series. But now we can add additional components to handle additional cases.

### S: Seasonal
Seasonality is important to model. There are its own autoregressive, integrated, and moving average components.

### Exogeneous
It's no strange idea to think of incorporating external features to help predict a target $-$ you can't build a predictive model without doing exactly this. Time series forecasting is no different.


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

Interested in learning more? Check out [Facebook's Prophet](https://facebook.github.io/prophet/) and [LinkedIn's Greykite](https://engineering.linkedin.com/blog/2021/greykite--a-flexible--intuitive--and-fast-forecasting-library) packages.


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
In our example, the $\epsilon_t$ values are sampled from a normal distribution, so this is **Gaussian white noise.** [We could easily use another distribution](https://ionides.github.io/531w20/03/notes03.pdf) to generate our values, though, such as a uniform, binary, or sinusoidal distribution.
