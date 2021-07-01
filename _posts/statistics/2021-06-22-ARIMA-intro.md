---
layout: post
title: A deep dive on ARIMA models
author: matt_sosna
---

What does the future hold? Predicting the future, or **forecasting,** is a universal challenge. Will tomorrow be sunny or rainy? Will my AAPL stock price increase or crash? What will my company's sales be next quarter? In each of these cases, we can use _historical patterns_ to predict the future (with varying accuracy).

Forecasting involves **time series** data, or repeated measures over time.



We'll cover the three components of ARIMA before expanding to _seasonality_ and _exogeneous_ variables, creating a full SARIMAX model.

We'll generate the data using the incredibly handy `generate_arma_sample` function from the `statsmodels.tsa.arima_process` library in Python. We can pass in the coefficients for our autoregressive and moving average components, then see randomly generated data for such a process.

## Table of contents
* [Getting started](#getting-started)
  - [Assumptions](#assumptions)
  - [Autocorrelation](#autocorrelation)
* [**AR:** Autoregression](#ar-autoregression)
  - [AR(0): White noise](#ar0-white-noise)
  - [AR(1): Random walks and oscillations](#ar1-random-walks-and-oscillations)
* [**MA:** Moving average](#ma-moving-average)
* [Additional components](#additional-components)
  - [**I:** Integrated](#integrated)
  - [**S:** Seasonal](#seasonal)
  - [**X:** Exogeneous](#exogeneous)
* [Comparing model fit](#comparing-model-fit)


## Getting started
As with any statistical model, there are assumptions that must be met when modeling time series data. The biggest one is that the time series is **stationary**. 

This means that the parameters that can summarize the time series aren't changing over time; the mean isn't increasing, the variance isn't decreasing, etc. It doesn't matter what section of the time series you look at $-$ the underlying process generating that data is the same. If this _isn't_ true, you'll need to transform your data before you can model it, e.g. by differencing.

## AR: Autoregression
In a typical multivariate regression, you might model how features like _hours studied_ and _hours slept_ affect exam score. In an autoregressive model, you use _previous values of the target_ to predict _future values_. Rather than hours studied and slept, for example, you could use the student's two previous exam scores to predict their next score.

### AR(0): White noise
Let's start with the simplest kind of forecasting model. In this model, there are no terms. Well, almost. There's just the _error_ term.

$$ y_t = \epsilon_t $$

This kind of time series is called **white noise.**<sup>[[1]](#1-ar0-white-noise)</sup> $\epsilon_t$ is a random value drawn from a normal distribution with mean 0 and variance $\sigma^2$. Each value is drawn independently, meaning $\epsilon_t$ has no correlation with $\epsilon_{t-1}$ or $\epsilon_{t+1}$. Written mathematically, we would say:

$$ \epsilon_t \overset{iid}{\sim} \mathcal{N}(0, \sigma^2) $$


The important thing is that these values are completely independent. This means that the time series is a sequence of random numbers and **it cannot be predicted**. Your best bet at guessing the next value is to just guess the mean of the distribution the samples are drawn from, which here is zero.

<center>
<img src="{{  site.baseurl  }}/images/statistics/arima/white_noise.png" height="110%" width="110%">
</center>

A time series of random values we can't forecast is actually a useful tool to have. It's an important null hypothesis for our analyses $-$ is there a pattern in the data that's sufficiently strong to distinguish the series from white noise?

We also can have a constant $c$ so our time series isn't centered at zero, e.g. $y_t = \epsilon_t + c$.

### AR(1): Random walks and oscillations
"Auto" means "self." In essence, you're fitting a regression to "yourself"; specifically, your past values. These previous values are called **lags.**

Here's a simple AR(1) model.

$$y_t = \alpha_1y_{t-1}+\epsilon_t$$

What this is saying that we predict the current time step, $y_t$, by adjusting the _previous_ time step $y_{t-1}$ by a multiplier $\alpha_1$. We then add an $\epsilon_t$ term to account for any changes in slope.

If $\alpha_1 = 1$, we can have a random walk.

<center>
<img src="{{  site.baseurl  }}/images/statistics/arima/random_walk.png" height="110%" width="110%">
</center>

Note that I extended the y-xis and generated 1000 instead of 100 points to better show how the path wanders.

If $0 < \alpha_1 < 1$, we have mean-reverting behavior. It's subtle, but you'll notice that the values are correlated with one another _and_ they tend to hover around zero. It's like less chaotic white noise. When $\alpha$ = 0, you get a white noise. When $\alpha$ = 1, you get a random walk.

<img src="{{  site.baseurl  }}/images/statistics/arima/mean_reversion.png">

We get really strange behavior if $\alpha_1$ is less than -1 or greater than 1. The magnitude of the time series values are constantly increasing, meaning they move exponentially further from the starting point. This causes the time series to not be stationary, meaning we can't model it anymore, so we usually [constrain our $\alpha_1$ parameter space](https://otexts.com/fpp2/AR.html) to -1 < $\alpha_1$ < 1 when performing [maximum likelihood estimation](https://towardsdatascience.com/probability-concepts-explained-maximum-likelihood-estimation-c7b4342fdbb1).


### AR(2): Smooth predictions


Here's what an AR(2) model would look like. It's the same as above, just with another $\alpha_n y_{t-n}$ term.

$$y_t = \alpha_1y_{t-1} + \color{orange}{\alpha_2y_{t-2}} + \epsilon_t$$

This says that the value at our current time step $y_t$ is determined by the value at the previous time step multiplied by some number, the value two time steps ago multiplied by another number, and then our "shock term," which is just white noise.

And here's the general form for an AR(p) model, where $p$ is the number of lags.

$$y_t = \sum_{i=1}^{p} \alpha_ny_{t-n} + \epsilon_t$$

When we fit a model with an autoregressive component (be it AR, ARMA, ARIMA, etc.), we solve for the $\alpha$ coefficients such that the predicted and actual $y_t$ values are as similar as possible.

## MA: Moving average
MA models are strange. An MA model by itself (i.e. no AR component) is just modeling autocorrelation in the _errors_. Our $e_t$ term, previously just noise that we added to our time series forecasts, now takes center stage as we model the error.



$$y_t = m_1\epsilon_{t-1} + \epsilon_t$$

Above,


It's hard to find a use case for using an MA model by itself. Generally, we use MA in conjunction with AR to account for different types of autocorrelation.






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
#### 1. [AR(0): White noise](#ar0-gaussian-white-noise)
In our example, the $\epsilon_t$ values are sampled from a normal distribution, so this is **Gaussian white noise.** We could easily use another distribution to generate our values, though, such as a uniform distribution.
