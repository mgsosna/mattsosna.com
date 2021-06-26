---
layout: post
title: A deep dive on ARIMA models
author: matt_sosna
---

Forecasting is a ubiquitous problem. What will weather be, what will stock price be, what will sales be next quarter.

Time series data = repeated measures over time.

There are assumptions in modeling time series. The biggest one is that the time series is **stationary** (at least over the period you're modeling and forecasting). This means that the parameters that can summarize the time series aren't changing over time; the mean isn't increasing, the variance isn't decreasing, etc. It doesn't matter what section of the time series you look at $-$ the underlying process generating that data is the same. If this _isn't_ true, you'll need to transform your data before you can model it, e.g. by differencing.



## AR(0): Gaussian white noise
Let's start with the simplest kind of forecasting model. In this model, there are no terms. Well, almost. There's just the _error_ term.

$$ y_t = \epsilon_t $$

$\epsilon_t$ is a random value drawn from a normal distribution with mean 0 and variance $\sigma^2$. Written mathematically, we would say:

$$ \epsilon_t \overset{iid}{\sim} \mathcal{N}(0, \sigma^2) $$

This kind of time series is called **Gaussian white noise.**<sup>[[1]](#1-ar0-gaussian-white-noise)</sup>

The important thing is that these values are completely independent. This means that the time series is a sequence of random numbers and **it cannot be predicted**. Your best bet at guessing the next value is to just guess the mean of the distribution the samples are drawn from, which here is zero.

<center>
<img src="{{  site.baseurl  }}/images/statistics/arima/white_noise.png" height="110%" width="110%">
</center>

A time series of random values we can't forecast is actually a useful tool to have. It's an important null hypothesis for our analyses $-$ is there a pattern in the data that's sufficiently strong to distinguish the series from white noise?

We also can have a constant $c$ so our time series isn't centered at zero, e.g. $y_t = \epsilon_t + c$.

## Autoregression (AR)
"Auto" means "self." In essence, you're fitting a regression to "yourself"; specifically, your past values. These previous values are called **lags.**

Here's a simple AR(1) model.

$$y_t = \alpha_1y_{t-1}+\epsilon_t$$

What this is saying that we predict the current time step, $y_t$, by adjusting the _previous_ time step $y_{t-1}$ by a multiplier $\alpha_1$. We then add an $\epsilon_t$ term to account for any changes in slope.

If $\alpha_1 = 1$, we can have a random walk.

<center>
<img src="{{  site.baseurl  }}/images/statistics/arima/random_walk.png" height="110%" width="110%">
</center>

Note that I extended the y-xis and generated 1000 instead of 100 points to better show how the path wanders.

If $0 < \alpha_1 < 1$, we have mean-reverting behavior.





Here's what an AR(2) model would look like. It's the same as above, just with another $\alpha_n y_{t-n}$ term.

$$y_t = \alpha_1y_{t-1} + \color{orange}{\alpha_2y_{t-2}} + \epsilon_t$$

This says that the value at our current time step $y_t$ is determined by the value at the previous time step multiplied by some number, the value two time steps ago multiplied by another number, and then our "shock term," which is just white noise.

And here's the general form for an AR(p) model, where $p$ is the number of lags.

$$y_t = \sum_{i=1}^{p} \alpha_ny_{t-n} + \epsilon_t$$

When we fit a model with an autoregressive component (be it AR, ARMA, ARIMA, etc.), we solve for the $\alpha$ coefficients such that the predicted and actual $y_t$ values are as similar as possible.

## Moving average (MA)
Here we regress the shock values against one another. Basically, we forecast the errors.

$$y_t = m_1\epsilon_{t-1} + \epsilon_t$$



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
#### 1. [AR(0): Gaussian white noise](#ar0-gaussian-white-noise)
We can use other distributions besides the Gaussian (normal) distribution to generate our random values. We could generate values with a uniform distribution, for example.
