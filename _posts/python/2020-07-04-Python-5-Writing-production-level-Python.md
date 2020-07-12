---
layout: post
title: Python 5 - Writing production-level Python
author: matt_sosna
---

In this post, we'll be diving down into production-level code. Here's a snippit we'll work through.

```python
import logging
import pandas as pd
from typing import Optional, List

from ..services import DataLoader

N_SD_THRESH = 5


class Preprocessor:
    """
    | Functions for preprocessing data
    """
    def __init__(self, max_tries: int = MAX_TRIES):
        self.max_tries = MAX_TRIES
        self.dl = DataLoader()

    def remove_outliers(self,
                        df: pd.DataFrame,
                        cols: Optional[List[str]] = None,
                        n_sd_thresh: int = N_SD_THRESH) -> pd.DataFrame:
        """
        | Remove outliers from cols in df. If cols not specified,
        | all columns in df are processed.
        |
        | -------------------------------------------------------
        | Parameters
        | ----------
        |  df : pd.DataFrame
        |    Df with columns ['a', 'b', 'c']
        |
        |  cols : list or None
        |    Columns to check
        |
        |  n_sd_thresh : int
        |    Number of standard deviations from mean above/below
        |    which a value is excluded
        |
        |
        | Returns
        | -------
        |  pd.DataFrame
        |    Original df with outliers removed
        """
        bad_idx = []

        cols_to_check = cols if cols is not None else list(df)

        for col in cols_to_check:
            bad_idx.append(self._find_outliers(df[col], n_sd_thresh))

        df_filt = df[~df.index.isin(bad_idx)].reset_index(drop=True)

        if df_filt.empty:
            logging.error("df has no rows without outliers")
            return df

        return df_filt

    def _find_outliers(self,
                       s: pd.Series,
                       n_sd_thresh: int) -> np.ndarray:
        """
        | Identify indices where value is greater/lower than series
        | mean +/- a given number of standard deviations.
        |
        | ------------------------------------------------------------
        | Parameters
        | ----------
        |  s : pd.Series
        |    A series of values, e.g. a column in a df
        |
        |  n_sd_thresh : int
        |    Number of standard deviations above/below the mean beyond
        |    which an outlier is identified
        |
        |
        | Returns
        | -------
        |  np.ndarray
        |    Indices of s where outliers exist
        """
        upper_thresh = s.mean() + n_sd_thresh*s.std()
        lower_thresh = s.mean() - n_sd_thresh*s.std()
        return s[(s > upper_thresh) | (s < lower_thresh)].index.values
```
