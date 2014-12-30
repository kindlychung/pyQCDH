s1 = Series([7.3, -2.5, 3.4, 1.5], index=[(1,2), (2,3), (3,4), (4,5)])
s1
s2 = Series([-2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])

string_data = Series(['aardvark', 'artichoke', np.nan, 'avocado'])
string_data
string_data.isnull()
string_data.dropna()

# 3 ways of doing pairwise correlation between two data frames
# using pandas/python

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
df2 = DataFrame([list("aabbb"), list("12123")]).T
df1 = DataFrame(np.random.randn(15).reshape(5,3), index=[df2.ix[:, 0], df2.ix[:, 1]], columns=list("def"))
df3 = DataFrame(np.random.randn(20).reshape(5,4), index=[df2.ix[:, 0], df2.ix[:, 1]], columns=list("ghij"))
type(df3)

def pairwise_corr(df1, df2):
    """
    Pairwise correlation between columns of two data frames
    :param df1:
    :type df1: pandas.core.frame.DataFrame
    :param df2:
    :type df2: pandas.core.frame.DataFrame
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
    res = []
    for i in range(df2.shape[1]):
        res.append(df1.corrwith(df2.ix[:, i]))
    res = pd.concat(res, axis=1)
    res.columns = df2.columns
    return res

pairwise_corr(df1, df3)
df1.corrwith(df3.h)


def corr_df3(obj):
    """
    :param obj:
    :type obj: pandas.core.frame.DataFrame
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
    return df3.corrwith(obj)
df1.apply(corr_df3)
df1.apply(lambda x: df3.corrwith(x))
df3.apply(lambda x: df1.corrwith(x))

df3.index
df3
df3.ix["b", ].ix[1:, ]
df3.ix["a":"b",].ix[1:, ]
df3.unstack().unstack()

frame = DataFrame(np.arange(12).reshape((4, 3)),
                  index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                  columns=[['Ohio', 'Ohio', 'Colorado'],
                           ['Green', 'Red', 'Green']])
frame
frame.index.names = ['key1', 'key2']
frame.columns.names = ['state', 'color']
frame
frame.swaplevel("key1", "key2")
frame
frame.sortlevel(0)
frame
frame.sum(level="key1")

frame = DataFrame(np.arange(12).reshape((4, 3)),
                  index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                  columns=[['Ohio', 'Ohio', 'Colorado'],
                           ['Green', 'Red', 'Green']])
frame.index.names = ['key1', 'key2']
frame.columns.names = ['state', 'color']
frame.sum(level="color", axis=1)
frame.sum(level="state", axis=1)

ser = Series(np.arange(3.), index=list("abc"))
ser
ser[-1]
ser.iget_value(2)

import pandas.io.data as web
pdata = pd.Panel(
    dict((stk, web.get_data_google(stk, "1/1/2012", "12/30/2014"))
         for stk in ["AAPL", "GOOG", "MSFT", "DELL"]))
pdata
pdata = pdata.swapaxes("items", "minor")
pdata
pdata.ix[:, "12/3/2012", :]

import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
nsample = 100
x = np.linspace(0, 10, 100)
x
X = np.column_stack((x, x**2))
X
X = sm.add_constant(X)
y = np.dot(X, beta)











