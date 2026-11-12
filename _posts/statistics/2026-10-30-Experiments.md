---
layout: post
title: Experimentation under pressure
author: matt_sosna
tags: statistics
---

_**Disclaimer:** The scenarios, metrics, and examples presented in this post are entirely fictionalized and for illustrative purposes only. They do not represent real-world data, internal operations, or specific policies of any past or current employer. All views, analyses, and opinions in this article are solely mine._

It's Monday morning and your phone buzzes as you're sipping your morning coffee. "Have you seen the hacked accounts dashboard?" your coworker at Big Social Media Company messages you. "I think we have a problem."

You log in and see a critical alert: the number of users reporting their accounts were hacked just breached guardrail and is growing rapidly.

<img src="{{  site.baseurl  }}/images/statistics/experiments/volume.png">

Your mind starts racing. Could the metric calculation have a bug? Daylight Savings Time was over the weekend, but this metric is hourly, not daily, so the extra hour shouldn't affect the values.

The spike implies an attack by bad actors bulk-compromising users' accounts. But when you look more closely you see that prevalence started inching upwards days ago, around Saturday. Could there have been a bad code change that bad actors discovered? Or are the upward trend and the spike unrelated?



### Extra
**Permutation tests**, from the famous ["There is only one test"](https://allendowney.blogspot.com/2011/05/there-is-only-one-test.html) article.

Indeed, [most of your ideas will fail](https://medium.com/@atticusli/why-most-of-your-ideas-will-fail-90723698fa04), even when proposed by experts.



# Code
### 1. [Intro](#)
{% include header-python.html %}
```python
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

np.random.seed(4)

# Set up ~1 week of hourly data, ending on Monday
n = 160
end_time = datetime(2026, 11, 2, 8, 0, 0)  # A Monday anchor date
start_time = end_time - timedelta(hours=n - 1)
t = [start_time + timedelta(hours=i) for i in range(n)]

# Create white noise base
y = np.random.normal(2, 0.02, n)

# Split the rising trend section in two
rising_index = 105
attack_index = 152

# First phase of the rise
y[rising_index:attack_index] += np.linspace(0, 0.22, attack_index - rising_index)

# Second phase of the rise
y[attack_index:] += np.linspace(0.45, 0.7, n - attack_index)

# Define a visual band width for the shaded region
band_width = 0.1
y_lower = y - band_width
y_upper = y + band_width

plt.figure(figsize=(9, 4.5))

# 1. Plot the main trend line on top
plt.plot(t, y, color="royalblue", lw=1.5, label="Prevalence")

# 2. Add the shaded confidence interval band
plt.fill_between(
    t,
    y_lower,
    y_upper,
    color="royalblue",
    alpha=0.2,
    label="Conf. Interval",
)

# Horizontal threshold line
threshold_value = 2.65
plt.axhline(
    y=threshold_value, color="orange", linestyle="--", label="Guardrail"
)

# --- X-AXIS DATE FORMATTING & STYLING ---
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
# \n creates a newline between the day of the week and the date
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%a\n%m/%d"))
plt.xticks(fontsize=14)
# ----------------------------------------

plt.ylabel("Hacked Account Prevalence", fontsize=16)
plt.tick_params(axis="y", which="both", left=False, labelleft=False)
plt.legend(loc="center left", fontsize=14)
plt.grid(True, alpha=0.3, axis="both")

plt.xlim([datetime(2026, 10, 26, 15, 0, 0), datetime(2026, 11, 2, 9, 0)])
plt.tight_layout()
plt.savefig("prevalence.png", dpi=300)
plt.show()
```
