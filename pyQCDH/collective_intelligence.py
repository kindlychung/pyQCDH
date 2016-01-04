from pandas import DataFrame, Series
import pandas as pd
import numpy as np

###############################################################
## recommendation system
###############################################################

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


pref = DataFrame(critics)


def topMatches(prefs, person):
    scores = prefs.corrwith(prefs.loc[:, person])
    return scores.drop(person)

toby_match = topMatches(pref, "Toby")

toby_recommend = pref.drop("Toby", axis=1)
toby_recommend = toby_recommend[pref.Toby.isnull()].T
toby_recommend


# In[53]:

toby_recommend = toby_recommend.ix[toby_match >= 0, :]
toby_match = toby_match[toby_match >= 0]
toby_recommend


# In[54]:

toby_match


# In[ ]:




# In[55]:

toby_recommend = toby_recommend.multiply(toby_match, axis=0)
toby_recommend


# In[56]:

weighted_sum = toby_recommend.sum(axis=0)
weighted_sum


# In[59]:

dummy = toby_recommend
dummy[dummy.notnull()] = 1
dummy


# In[60]:

dummy = dummy.multiply(toby_match, axis=0)
dummy


# In[61]:

total_weights = dummy.sum(0)
total_weights


# In[63]:

weight_score = weighted_sum / total_weights
weight_score


###############################################################
## blog words, clustering by closest distance #bloggermail
###############################################################

import os, re
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from urllib.request import urlopen
from bs4 import BeautifulSoup

chare = re.compile(r"[!-\.&]")
itemowners = {}
dropwords=['a','new','some','more','my','own','the','many','other','another']
for i in range(1, 51):
    c = urlopen('http://member.zebo.com/Main?event_key=USERSEARCH&wiowiw=wiw&keyword=car&page=%d' % (i))
    soup = BeautifulSoup(c.read())


os.chdir("/Users/kaiyin/Downloads/programming-collective-intelligence-code-master/chapter3")
blog_dat = pd.read_table("blogdata.txt", index_col="Blog")
blog_dat = blog_dat.astype(float)
all(blog_dat.notnull())
x = DataFrame(np.random.randn(99*706).reshape((99, 706)), index=blog_dat.index, columns=range(706))
pd.expanding_corr(blog_dat.iloc[:, :4], blog_dat.iloc[:, :4], pairwise=True)[-1, :, :]
pd.expanding_corr(blog_dat.iloc[:, :4], x.iloc[:, :4], pairwise=True)[-1, :, :]
blognames = list(blog_dat.index)


def corrpairs(df1, df2):
    """
    Pairwise correlation for columns of two data frames
    :param df1:
    :type df1:
    :param df2:
    :type df2:
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
    return df1.apply(lambda x: df2.corrwith(x))



import pdb
def kcluster(cols, k=4):
    """
    K Means clustering algorithm, applied to columns of a data frame.
    Using Pearson correlation as the distance function.
    :param rows:
    :type rows: pandas.core.frame.DataFrame
    :param k:
    :type k: int
    :return:
    :rtype: list[int]
    """
    cols = cols.astype(float)
    nrow, ncol = cols.shape
    nuclear0 = cols.iloc[:, :k]
    nuclear0.columns = range(k)
    nuclear0 += np.random.randn(np.prod(nuclear0.shape)).reshape(nuclear0.shape)

    correlations = corrpairs(cols, nuclear0)
    groups = correlations.idxmax(axis=0)
    nuclear1 = []
    for i in range(k):
        sub_cols = cols.loc[:, groups == i]
        sub_mean = sub_cols.mean(axis=1)
        nuclear1.append(sub_mean)
    nuclear1 = pd.concat(nuclear1, axis=1)

    while ((nuclear0 - nuclear1).abs() > 0.00001).any().any():
        # print(nuclear0)
        # print(nuclear1)
        # print((nuclear0 - nuclear1).abs())
        nuclear0 = nuclear1
        correlations = corrpairs(cols, nuclear0)
        groups = correlations.idxmax(axis=0)
        nuclear1 = []
        for i in range(k):
            sub_cols = cols.loc[:, groups == i]
            sub_mean = sub_cols.mean(axis=1)
            nuclear1.append(sub_mean)
        nuclear1 = pd.concat(nuclear1, axis=1)

    return groups

testdat = pd.read_csv("/tmp/test", header=None)
testdat.columns = list("abcde")
testdat
g = kcluster(blog_dat.T, 10)
g[g == g["Copyblogger"]]

