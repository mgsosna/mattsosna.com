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

To answer these questions, we'll start with a basic forecasting model and iterate towards a full autoregressive moving average (ARMA) model. We'll then take it a step further to include [_integrated_](https://www.investopedia.com/terms/a/autoregressive-integrated-moving-average-arima.asp), [_seasonal_](https://otexts.com/fpp2/seasonal-arima.html), and [_exogeneous_](https://www.statisticshowto.com/endogenous-variable/) components, expanding into a [SARIMAX](https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html) model.

In other words, we'll build from this:

$$y_t = c + \epsilon_t$$

to this:

$$\color{orangered}{d_t} = c +
\color{royalblue}{\sum_{n=1}^{p}\alpha_nd_{t-n}} +
\color{darkorchid}{\sum_{n=1}^{q}\theta_n\epsilon_{t-n}} + \\
\color{green}{\sum_{n=1}^{r}\beta_nx_{n_t}} +
\color{orange}{\sum_{n=1}^{P}\phi_nd_{t-sn}} +
\color{orange}{\sum_{n=1}^{Q}\eta_n\epsilon_{t-sn}} +
\epsilon_t $$

It looks complicated, but each of these pieces $-$ the <span style="color:royalblue; font-weight: bold">autoregressive</span>, <span style="color:darkorchid; font-weight: bold">moving average</span>, <span style="color:green; font-weight: bold">exogeneous</span>, and <span style="color:orange; font-weight: bold">seasonal</span> components $-$ are just added together. We can easily tune up or down the complexity of our model by adding or removing terms, and switching between raw and <span style="color:orangered; font-weight: bold">differenced</span> data, to create ARMA, SARIMA, ARX, etc. models.

Once we've built a model, we'll be able to predict the future of a time series like this. But perhaps more importantly, we'll understand the underlying patterns that give rise to our time series.

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
* [**Putting it together**](#putting-it-together)
  - [ARMA: Autoregressive moving average](#arma-autoregressive-moving-average)
  - [ARIMA: Autoregressive integrated moving average](#arima-autoregressive-integrated-moving-average)
* [**Additional components**](#additional-components)
  - [S: Seasonality](#seasonal)
  - [X: Exogeneous variables](#exogeneous-variables)
* [**Time series in Python**](#time-series-in-python)
  - [Fitting models](#fitting-models)
  - [Comparing model fit](#comparing-model-fit)
  - [Why not deep learning?](#why-not-deep-learning)

## Getting started
### Autocorrelation
Before we can start building any models, we need to cover a topic essential for describing time series: [**autocorrelation**](https://en.wikipedia.org/wiki/Autocorrelation). Autocorrelation means "self-correlation": it is the similarity of a time series' values with earlier values, or **lags**. If our time series was the values `[5, 10, 15]`, for example, our lag-1 autocorrelation would be the correlation of `[10, 15]` with `[5, 10]`.

We can visualize the correlation of the _present value_ with a _previous value $n$ lags ago_ with an **autocorrelation plot.** These plots are constructed by calculating the correlation of each value ($y_t$) with the value at the previous time step ($y_{t-1}$), two steps ago ($y_{t-2}$), three ($y_{t-3}$), and so on. The y-axis shows the strength of correlation at lag $n$, and we consider any value outside the shaded error interval to be a significant correlation.

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

So when $\alpha_1$ = 0, we get white noise, and when $\alpha_1$ = 1, we get a random walk. When $0 < \alpha_1 < 1$, our time series exhibits [**mean reversion**](https://www.investopedia.com/terms/m/meanreversion.asp). It's subtle, but you'll notice that the values are correlated with one another _and_ they tend to hover around zero, like less chaotic white noise. A real-world example of this process is large changes in stock prices: sudden shifts [tend to be followed by mean reversion](https://decodingmarkets.com/mean-reversion-trading-strategy/).

<img src="{{  site.baseurl  }}/images/statistics/arima/mean_reversion.png">

When fitting an AR model, statistics packages typically [constrain the $\alpha$ parameter space](https://otexts.com/fpp2/AR.html) to $-1 \leq \alpha \leq 1$ when performing [maximum likelihood estimation](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation). Unless you're modeling exponential growth or sharp oscillations, the time series described by these models are probably not what you're looking for.

<img src="{{  site.baseurl  }}/images/statistics/arima/bad_arr.png">

### AR(p): Higher-order terms
Adding more lags to our model is just a matter of adding $\alpha_n y_{t-n}$ terms. Here's what an AR(2) model looks like, with the additional term highlighted in blue.

$$y_t = c + \alpha_1y_{t-1} + \color{royalblue}{\mathbf{\alpha_2y_{t-2}}} + \epsilon_t$$

This says that the value at our current time step $y_t$ is determined by our constant $c$, plus the value at the previous time step $y_{t-1}$ multiplied by some number $\alpha_1$, plus the value two time steps ago $y_{t-2}$ multiplied by another number $\alpha_2$, plus a white noise value $\epsilon_t$. To fit this type of model, we now estimate values for both $\alpha_1$ and $\alpha_2$.

As we add more lags to our model, or we start including moving average, exogeneous, or seasonal terms, it will become useful to rewrite our autoregressive terms as a summation. (Statisticians also use [backshift notation](https://otexts.com/fpp2/backshift.html), but we'll stick with summations to avoid that learning curve.) Here's the general form for an AR(p) model, where $p$ is the number of lags.

$$y_t = c + \sum_{n=1}^{p} \alpha_ny_{t-n} + \epsilon_t$$

The above equation simply says "our current value $y_t$ equals our constant $c$, plus every lag $y_{t-n}$ multiplied by its coefficient $\alpha_n$, plus $\epsilon_t$." We can use the same equation regardless of whether $p$ is 1 or 100... though if your model has 100 lags, you might want to look into including the next term we'll describe: the moving average.

## MA: Moving average
The second major component of an ARIMA model is the **moving average** component. This component is _not_ a rolling average, but rather _the lags in the white noise_.

The $\epsilon_t$ term, previously some forgettable noise we add to our forecast, now takes center stage. In an MA(1) model, our forecast for $y_t$ is our constant plut the _previous_ white noise term $\epsilon_{t-1}$ with a multiplier $\theta_1$, plus the _current_ white noise term $\epsilon_t$.

$$y_t = c + \theta_1\epsilon_{t-1} + \epsilon_t$$

As before, we can concisely describe an MA(q) model with this summation:

$$y_t = c + \sum_{n=1}^{q}\theta_n\epsilon_{t-n} + \epsilon_t$$

Here's are three MA(1) time series that vary in the value of $\theta_1$, the multiplier on $\epsilon_{t-1}$. Don't feel bad if you don't experience an "ah-ha" moment looking at these; they should look fairly similar to white noise.

<img src="{{  site.baseurl  }}/images/statistics/arima/ma1.png">

Moving average processes are a lot less intuitive than autoregression $-$ what time series has no memory of its past behavior, but remembers it previous random noise? Yet a surprising number of [real-world time series _are_ moving average processes](https://stats.stackexchange.com/questions/45026/real-life-examples-of-moving-average-processes), from misalignment of store goods and sales, battery purchases in response to natural disasters, and low-pass filters such as the treble knobs on car stereos.

Here's a silly but helpful [misalignment example](https://www.youtube.com/watch?v=voryLhxiPzE) from [YouTuber ritvikmath](https://www.youtube.com/channel/UCUcpVoi5KkJmnE3bvEhHR0Q). Imagine a recurring party where you're assigned to provide one cupcake per guest. $y_t$ is the correct number of cupcakes to bring. You're expecting roughly 10 people, so you start by bringing 10 cupcakes ($c=10$). When you arrive, you note how many cupcakes you over- or under-supplied ($\epsilon_t$).

For the following meeting, you bring 10 cupcakes _adjusted by that difference from the previous meeting_ (now $\epsilon_{t-1}$) multiplied by some factor ($\theta_1$). You want to bring the negative of the number of cupcakes you were off by last time, so you set $\theta_1=-1$. If you were two short last time ($\epsilon_{t-1}=-2$), for example, you'd bring two extra.

The number of guests who show up is essentially random, but **the guests remember the number of cupcakes at the previous meeting** $-$ if there were too many, more guests will show up, and if there were too few, then fewer guests will come.

We can therefore model the correct number of cupcakes at each meeting like below. The blue terms are the number of cupcakes you bring to the meeting, and the orange is the difference between the number we bring and the number of people who show up.

$$y_t = \color{royalblue}{10 - \epsilon_{t-1}} + \color{orange}{\epsilon_t}$$

The thing to note here is that **this time series doesn't care about its own history** (the correct number of cupcakes); it is only affected by **external random noise that is remembered for a brief period** (the difference between the number of cupcakes and the number of party attendees). This is therefore a moving average process.

<img src="{{  site.baseurl  }}/images/statistics/arima/cupcakes.jpg">
<span style="font-size: 12px"><i>Photo by <a href="https://unsplash.com/@brookelark">Brooke Lark</a> on <a href="https://unsplash.com">Unsplash</a></i></span>

## Putting it together
Having covered AR and MA processes, we have all we need to build ARMA and ARIMA models. As you'll see, these more complex models simply consist of AR and MA components added together.

### ARMA: Autoregressive moving average
While many time series can be boiled down to a pure autoregressive or pure moving average process, you often need to combine AR and MA components to successfully describe your data. These **ARMA** processes can be modeled with the following equation:

$$y_t = c + \sum_{n=1}^{p}\alpha_ny_{t-n} + \sum_{n=1}^{q}\theta_n\epsilon_{t-n} + \epsilon_t$$

The ARMA equation simply states that the value at the current time step is a constant plus the sum of the autoregressive lags and their multipliers, plus the sum of the moving average lags and their multipliers, plus some white noise. This equation is the basis for a wide range of applications, from [modeling wind speed](https://www.koreascience.or.kr/article/JAKO201315463253802.pdf), [forecasting financial returns](https://link.springer.com/article/10.1007/s00180-014-0543-9), and even [filtering images](https://projecteuclid.org/journals/brazilian-journal-of-probability-and-statistics/volume-23/issue-2/Spatial-ARMA-models-and-its-applications-to-image-filtering/10.1214/08-BJPS019.full).

Below are four ARMA(1,1) time series. As with the MA(1) plot above, it's difficult to look at any of the time series below and intuit the parameter values, or even that they're ARMA processes rather than AR or MA alone. We're at the point where our time series have become too complex to intuit the type of model or its parameters from eyeballing the raw data.

<img src="{{  site.baseurl  }}/images/statistics/arima/arma.png">

But that's ok. Moving forward, we'll start using [**AIC**](https://en.wikipedia.org/wiki/Akaike_information_criterion) to determine which model best describes our data, whether that's an AR, MA, or ARMA model, as well as the optimal number of lags for each component. We'll cover this process at the end of this post, but in the meantime let's cover the remaining pieces of the SARIMAX model.

### ARIMA: Autoregressive integrated moving average
We've arrived at the namesake of this blog post: the ARIMA model. Despite the buildup, we'll actually see that an ARIMA model is just an ARMA model, with a preprocessing step handled by the model rather than the user.

Let's start with the equation for an ARIMA(1,1,0) model.

$$\color{red}{y_t - y_{t-1}} = c + \alpha_1(\color{red}{y_{t-1} - y_{t-2}}) + \epsilon_t$$

We've gone from modeling $y_t$ to modeling the _change_ between $y_t$ and $y_{t-1}$. As such, our autoregressive term, previously $\alpha_1y_{t-1}$, is now $\alpha_1(y_{t-1}-y_{t-2})$.

In other words, an ARIMA model is simply an ARMA model on the _differenced_ time series. That's it! If we replace $y_t$ with $d_t$, representing our differenced data, then we simply have the ARMA equation again.

$$\color{red}{d_t} = c + \sum_{n=1}^{p}\alpha_n\color{red}{d_{t-n}} + \sum_{n=1}^{q}\theta_n\epsilon_{t-n} + \epsilon_t$$

We could perform the differencing ourselves and then fit the model, but it gets cumbersome if $d$ is greater than 1, and we would then need to transform our values back to get the original units (on top of undoing any log, square root, etc. transformations to make the time series stationary).

But to prove I'm not making this up, here's a demonstration of how the model coefficients in an ARIMA(1,1,1) model on the _raw_ data and ARMA(1,1) model on the _differenced_ data are equal.

{% include header-python.html %}
```python
# Using statsmodels v0.12.2
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import arma_generate_sample

# Set coefficients
ar_coefs = [1, -1]
ma_coefs = [1, 0.5]

# Generate data
y1 = arma_generate_sample(ar_coefs, ma_coefs, nsample=2500, scale=0.01)
y2 = np.diff(y1)

# Fit models
mod1 = ARIMA(y1, order=(1, 1, 1)).fit()  # ARIMA on original
mod2 = ARIMA(y2, order=(1, 0, 1)).fit()  # ARMA on differenced

# AR coefficients are same
print(mod1.polynomial_ar.round(3) == mod2.polynomial_ar.round(3))
# array([True, True])

# MA coefficients are same
print(mod1.polynomial_ma.round(3) == mod2.polynomial_ma.round(3))
# array([True, True])
```

Above, we first use the `arma_generate_sample` function to simulate data for an ARMA process with specified $\alpha$ and $\theta$ parameters. We then use the `ARIMA` function to fit an ARIMA model on the raw data and an ARMA data on the differenced data. Finally, we compare the two models' estimated parameters and show that they're equal.

## Additional components
With the AR, MA, and I components under our belt, we're equipped to analyze and forecast a wide range of time series. But there are two additional components that will truly take our forecasting to the next level: **seasonality** and **exogeneous variables.** Let's briefly cover those before going over some code and then closing out this post.










### S: Seasonality
As alluded to in the name, seasonality refers to _repeating patterns with a fixed frequency_ in the data: patterns that repeat every day, every two weeks, every four months, etc. Movie theater ticket sales tend to be correlated with the sales from a week earlier, for example, while [housing sales](https://otexts.com/fpp2/tspatterns.html) and temperature tend to be correlated with the values from the previous year.

We can readily control for seasonality by adding an additional set of parameters to our model. Below is a SARIMA model, with the seasonal component highlighted in orange.

$$y_t = c + \\
\sum_{n=1}^{p}\alpha_ny_{t-n} +
\sum_{n=1}^{d}\omega_n(y_t-y_{t-n}) +
\sum_{n=1}^{q}\theta_n\epsilon_{t-n} + \\
\color{orange}{\sum_{n=1}^{P}\phi_ny_{t-sn}} +
\color{orange}{\sum_{n=1}^{D}\gamma_n(y_t-y_{t-sn})} +
\color{orange}{\sum_{n=1}^{Q}\eta_n\epsilon_{t-sn}} + \\
\epsilon_t $$

Notice how the seasonal and non-seasonal components look suspiciously similar. This is because we actually fit a _separate_ set of autoregressive, integrated, and moving average components on data differenced by some number of lags $s$, the frequency of our seasonality. For a model of daily e-commerce profits with strong weekly seasonality, for example, we'd set $s$ = 7.

A perfect sine wave with a wavelength of 10 could be modeled with a SARMA(0,0)(1,0)[10] model like below.<sup>[[5]](#5-s-seasonality)</sup>

$$y_t = c + \phi_1y_{t-10} + \epsilon_t$$

But for real-world time series, even highly seasonal data is likely still better modeled with a non-seasonal component or two: the seasonal component may capture _long-term trends_ while the non-seasonal components adjust our predictions for _shorter-term variation_. We could accomplish this with a basic SARMA(1,0)(1,0)[7] model, for example, which contains both seasonal and non-seasonal autoregressive terms.

$$y_t = c + \alpha_1y_{t-1} + \phi_1y_{t-7} + \epsilon_t$$

This model says that the current value $y_t$ is a function of a constant $c$ plus the previous value $y_{t-1}$ multiplied by a coefficient $\alpha_1$, plus the value seven lags ago $y_{t-7}$ multiplied by a coefficient $\phi_1$, plus white noise $\epsilon_t$.

### X: Exogeneous variables
All the components we've described so far are features from our time series itself. Our final component, **exogeneous variables,** bucks this trend by considering the effect of _external data_ on our time series.

This shouldn't sound too intimidating $-$ **exogeneous variables are simply the features in any non-time series model you've built up to this point.** In a model of student test scores, for example, a standard linear regression would have features like the _number of hours studied_ and _number of hours slept_. An ARIMAX model, meanwhile, would also include **_endogeneous_** features such as the student's previous $n$ exam scores and previous white noise terms.  

Here's what our full SARIMAX equation looks like. The exogeneous term is highlighted in green.

$$y_t = c +
\sum_{n=1}^{p}\alpha_ny_{t-n} +
\sum_{n=1}^{d}\omega_n(y_t-y_{t-n}) +
\sum_{n=1}^{q}\theta_n\epsilon_{t-n} + \\
\color{green}{\sum_{n=1}^{r}\beta_nx_{n_t}} + \\
\sum_{n=1}^{P}\phi_ny_{t-sn} +
\sum_{n=1}^{D}\gamma_n(y_t-y_{t-sn}) +
\sum_{n=1}^{Q}\eta_n\epsilon_{t-sn} +
\epsilon_t $$

Some examples of exogeneous variables in ARIMAX models include the effects of the [price of oil on the U.S. exchange rate](https://www.mathworks.com/help/econ/arima-model-including-exogenous-regressors.html), [outdoor temperature on electricity demand](https://www.mdpi.com/1996-1073/7/5/2938), and [economic indicators on disability insurance claims](https://www.soa.org/globalassets/assets/files/research/projects/research-2013-arima-arimax-ben-appl-rates.pdf).

Note that the effects of exogeneous factors are already _indirectly_ included in our time series' history. Even if we don't include a term for the price of oil in our model of the U.S. exchange rate, for example, oil's effects will be reflected in the exchange rate's autoregressive or moving average components. Any real-world time series is a result of dozens or hundreds of exogeneous influences, so why bother with exogeneous terms at all?

While external effects are indirectly represented within the endogeneous terms in our model, it is still much more powerful to directly measure those influences. Our forecasts will respond much more quickly to nudges from the external factor, for example, rather than needing to wait for it to be reflected in the lags.

## Time series in Python
So far, we've covered the theory and math behind [autoregressive](#ar-autoregression), [moving average](#ma-moving-average), [integrated](#arima-integrated-moving-average), [seasonal](#s-seasonality), and [exogeneous](#x-exogeneous-variables) components of time series models. With a little effort we could probably fill out the equation for a SARIMAX model and generate a prediction by hand. But how do we find the parameter values for the model?

To do this, we'll use Python's `statsmodels` library. We'll first fit a model where we know ahead of time what our model order should be. In the following section, we'll then show how to use the `pmdarima` library to scan through potential model orders and find the best match for your data.

### Fitting models
Let's say we're a data scientist at some e-commerce company and we want to forecast our sales for the following few weeks. We have a CSV of the last year of daily sales, as well as each day's spending on advertising. We know we want our model to have a non-seasonal ARIMA(1,1,1) component, a seasonal AR(1) component with a period of 7 days, and an exogeneous variable of advertising spend.

In other words, we know we want a SARIMAX(1,1,1)(1,0,0)[7] model. Here's how we would fit such a model in Python.

{% include header-python.html %}
```python
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Load data
df = pd.read_csv("data.csv")

# Specify model
mod = SARIMAX(endog=df['sales'],
              exog=df['ad_spend'],
              order=(1, 1, 1),
              seasonal_order=(1, 0, 0, 7),
              trend='c')

# Fit model
results = mod.fit()

# Inspect model
results.summary()

# Generate predictions
results.predict(7)   # In-sample predictions
results.forecast(7)  # Out-of-sample forecast
```

That's it! We specify our model with `SARIMAX`, then fit it with the `.fit` method (which must be saved to a separate variable). We can then get a [scikit-learn](https://scikit-learn.org/stable/) style model summary with the `summary` method. The `predict` method lets us compare our model [in-sample predictions](https://stats.stackexchange.com/questions/260899/what-is-difference-between-in-sample-and-out-of-sample-forecasts) to the actual values, while the `forecast` method generates a prediction of the future `n` steps.

### Comparing model fit
This is all great, but what if we don't know ahead of time what our model order should be? For simple AR or MA models, we can look at the [partial autocorrelation](#partial-autocorrelation) or [autocorrelation plots](#autocorrelation), respectively. But for more complex models, we'll need to perform **model comparison.**

We typically perform model comparisons with AIC, a measure of how well our model fits the data, with a penalty for more complex models. The penalty is a way to safeguard against overfitting $-$ yes, model accuracy inevitably increases as we add more terms, but is the improvement enough to justify adding another term?

To identify the optimal model, we can perform a parameter scan on different model orders, then choose the model with the lowest AIC. (If we're particularly concerned about overfitting, we can use the stricter [BIC](https://en.wikipedia.org/wiki/Bayesian_information_criterion) instead.)

Rather than needing to write a bunch of `for` loops ourselves, we can rely on the `auto_arima` function from the [pmdarima](https://pypi.org/project/pmdarima/) library to do the heavy lifting. All we need to do is pass in our initial order estimates for the AR, I, and MA components, as well as the highest order in each category that we want to consider. For a seasonal model, we also need to pass in the frequency of our seasonality, as well as the estimates for the seasonal AR, I, and MA components.

Here's how we would identify the optimal SARIMA model on our S&P 500 daily closing prices from the start of this post.

```python
import pandas as pd
import pmdarima as pmd

df = pd.read_csv("spy.csv")

results = pmd.auto_arima(df['Close'],
                         start_p=0,  # initial guess for AR(p)
                         start_d=0,  # initial guess for I(d)
                         start_q=0,  # initial guess for MA(q)
                         max_p=2,    # max guess for AR(p)
                         max_d=2,    # max guess for I(d)
                         max_1=2,    # max guess for MA(q)
                         m=7,        # seasonal order
                         start_P=0,  # initial guess for seasonal AR(P)
                         start_D=0,  # initial guess for seasonal I(D)
                         start_Q=0,  # initial guess for seasonal MA(Q)
                         trend='c',
                         information_criterion='aic',
                         trace=True,
                         error_action='ignore'
                         )

# Performing stepwise search to minimize aic
# ARIMA(0,1,0)(0,0,0)[7] intercept   : AIC=6671.069, Time=0.03 sec
# ARIMA(1,1,0)(1,0,0)[7] intercept   : AIC=6595.106, Time=0.30 sec
# ARIMA(0,1,1)(0,0,1)[7] intercept   : AIC=6602.479, Time=0.38 sec
# ARIMA(0,1,0)(0,0,0)[7]             : AIC=6671.069, Time=0.03 sec
# ARIMA(1,1,0)(0,0,0)[7] intercept   : AIC=6626.321, Time=0.10 sec
# ARIMA(1,1,0)(2,0,0)[7] intercept   : AIC=6596.194, Time=0.60 sec
# ARIMA(1,1,0)(1,0,1)[7] intercept   : AIC=6595.849, Time=0.53 sec
# ARIMA(1,1,0)(0,0,1)[7] intercept   : AIC=6597.437, Time=0.31 sec
# ARIMA(1,1,0)(2,0,1)[7] intercept   : AIC=inf, Time=2.65 sec
# ARIMA(0,1,0)(1,0,0)[7] intercept   : AIC=6619.748, Time=0.15 sec
# ARIMA(2,1,0)(1,0,0)[7] intercept   : AIC=6588.194, Time=0.39 sec
# ARIMA(2,1,0)(0,0,0)[7] intercept   : AIC=6614.206, Time=0.11 sec
# ARIMA(2,1,0)(2,0,0)[7] intercept   : AIC=6589.336, Time=0.79 sec
# ARIMA(2,1,0)(1,0,1)[7] intercept   : AIC=6588.839, Time=0.68 sec
# ARIMA(2,1,0)(0,0,1)[7] intercept   : AIC=6590.019, Time=0.31 sec
# ARIMA(2,1,0)(2,0,1)[7] intercept   : AIC=inf, Time=3.14 sec
# ARIMA(2,1,1)(1,0,0)[7] intercept   : AIC=6589.040, Time=0.57 sec
# ARIMA(1,1,1)(1,0,0)[7] intercept   : AIC=6592.657, Time=0.47 sec
# ARIMA(2,1,0)(1,0,0)[7]             : AIC=6588.194, Time=0.40 sec
#
# Best model:  ARIMA(2,1,0)(1,0,0)[7] intercept
# Total fit time: 11.975 seconds
```

The code above says that a SARIMA(2,1,0)(1,0,0)[7] model best fits the last five years of S&P 500 data... with some important caveats! Before you gamble your life savings on the forecasts from this model, we should keep in mind that despite a convenient parameter scan, we still have a lot of accuracy we can squeeze out of modeling this data.

For one, we didn't pre-process the data in any way, such as scanning for outliers or interpolating any gaps. Similarly, we didn't examine whether any transformations would make the data easier to forecast. Finally, the frequency of our seasonality, 7, came somewhat out of thin air $-$ there could be a seasonality such as monthly, quarterly, or yearly that significantly improves our model performance.

### Why not deep learning?
There's one issue we haven't covered and is essential to this post. Classical statistics is great, but in the era of machine learning, is ARIMA a relic from the past? When open-source libraries like [Facebook's Prophet](https://facebook.github.io/prophet/) and [LinkedIn's Greykite](https://engineering.linkedin.com/blog/2021/greykite--a-flexible--intuitive--and-fast-forecasting-library) generate forecasts far more accurate than our carefully-polished ARIMA model, why even bother?

The answer comes from an important distinction between statistics and machine learning.

Why not just use an RNN? Well, it depends on the approach we want to take. If we're trying to generate the most accurate forecast without necessarily understanding how our model came to that conclusion, a deep learning model can be the way to go. But if we want to model the _underlying process that gave rise to that data_, we'll need to turn to statistics.



## Conclusions
In this post, we did a lot...




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

#### 4. [AR(0): White noise](#ar0-white-noise)
In our example, the $\epsilon_t$ values are sampled from a normal distribution, so this is **Gaussian white noise.** [We could easily use another distribution](https://ionides.github.io/531w20/03/notes03.pdf) to generate our values, though, such as a uniform, binary, or sinusoidal distribution.

#### 5. [S: Seasonality](#s-seasonality)
After much digging through Stack Exchange debates, it seems like we may have violated some critical forecasting assumptions by modeling a sine wave (even though it works as a great example of a seasonal process!). The issue is that sine waves are **deterministic:** if you know that a time series is a sine wave and where in the wave you are, you can perfectly predict all past and future values of the series. The concept of stationarity, and building ARIMA models in general, [only applies to **stochastic** processes](https://stats.stackexchange.com/questions/172979/is-a-model-with-a-sine-wave-time-series-stationary).
