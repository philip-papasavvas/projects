"""
Created on 30/06/19

Look at the stationarity of stock time series, carry out analysis on the log-returns of a stock.
Provide summary statistics on the data
Introduce tests (such as Augmented Dickey Fuller) to check stationarity of time series
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import utils_date

plt.style.use('seaborn')

pd.set_option('display.max_columns', 5)

wkdir = "C://Users//Philip//Documents//python//"
inputFolder = wkdir + "input/"
inputDir = wkdir + "input/"
outputFolder = wkdir + "output/"

# "example_data.csv", "example_data_na.csv" has NA rows
# df = pd.read_csv(inputDir + 'example_data.csv') #, parse_dates=True)
df = pd.read_csv(inputDir + "funds_stocks_2019.csv")
df = utils_date.char_to_date(df) #convert all dates to np datetime64
df.set_index('Date', inplace=True)

# deal with returns not time series of prices, as prices are non-stationary transform the time
# series so that it becomes stationary. If the non-stationary is a random walk with or without
# drift, it is transformed to a stationary process by differencing - it is now a stationary
# stochastic (random probability distribution) process if time series data also exhibits a
# deterministic trend, spurious results can be avoided by detrending if non-stationary time
# series are both stochastic and deterministic at the same time, differencing and detrending
# should be applied - differencing removes the trend in variance and detrending removes
# determinstic trend


def log_daily_returns(data):
    """Give log daily returns"""
    log_daily_return = data.apply(lambda x: np.log(x) - np.log(x.shift(1)))[1:]
    return log_daily_return

df_log_rets  = log_daily_returns(data= df)

# trim the dataframe to ignore columns with null values

def dropNullCols(data):
    origCols = list(data.columns)
    clean_df = data.dropna(axis=1)
    newCols = list(clean_df.columns)
    cutCols = [x for x in origCols if x not in newCols]

    print("The following columns have been dropped from the dataframe as they contain NaNs: \n {"
          "columns}".format(columns = cutCols))
    return clean_df

clean_df_log_rets = dropNullCols(df_log_rets)

# test the hypothesis that the returns are normally distibuted by looking at skewness and
# kurtosis under the normality assumption, s(x) and k(x) - 3 are distributed asymptotically as
# normal with zero mean and variances of 6/T and 24/T respectively. so in this case we have the (
# log) return series of the asset {r_1, ..., r_n}, and we want to test the skewness of the
# returns, so consider the null hyptothesis H_0: s(r) = 0 with the alternate hypthesis s(r) != 0.
# the t ratio statistic of the sample skewness is t = (s(hat)(r) / sqrt(6/T)) where you would
# reject null hypothesis at alpha sig level if |t| > z_(alpha/2) where z_(alpha/2) is the upper
# 100(alpha/2)th quantile of a standard normal distribution. or you could compute the p value of
# the test statistic t and reject H_0 iff p-value < alpha

# can also test the excess kurtosis of the return series using hypotheses H_0: k(r) - 3 = 0, versus alternate
# test statistic is then t = k(r) - 3 / sqrt(24/T)

# look at symmetry of return distribution

df_log_rets.dropna(axis=1, inplace=True)
