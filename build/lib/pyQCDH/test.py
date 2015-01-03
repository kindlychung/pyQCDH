from pyQCDH.BedBimFam import BedBimFam, Bed
from pyQCDH.Gwas import Gwas
import scipy
import os
import pandas
import numpy as np
import pdb

# os.chdir("/Users/kaiyin/Desktop/mmp/")
# trio = BedBimFam("/Users/kaiyin/Desktop/mmp/mmp13")
# data = trio.fam.read(usecols=["IID", "FID"])
# print(data.head())
# data = trio.fam.read()
# print(data.head())
# data = trio.bim.read()
# print(data.head())
# data = trio.bim.read(usecols=["SNP", "CHR", "GDIST"])
# print(data.head())
# trio.bim.count_lines()
# trio.fam.count_lines()
# trio.n_snps
# trio.n_individuals

os.chdir("/Users/kaiyin/Desktop/testbed")
trio = BedBimFam("test")

###################################
## test reading bim files
###################################
# trio.bim.count_lines()
# x = trio.bim.read(usecols="all")
# x = trio.bim.read(usecols=["SNP"])
# print(x.head())

###################################
## test reading fam files
###################################
# x = trio.fam.read(usecols=["FID", "IID", "PID"])

##################################
# test reading bed files
##################################
x = trio.bed.read_all()
print(x)
x = trio.bed.read_cols([0, 1, 2])
print(x)
x = trio.bed.read_snps(["snp1", "snp2"])
print(x)
x.corr(x)
x.corr()

# ###################################
# ## test join data frames
# ###################################
# df1 = pandas.DataFrame(np.random.randn(10, 2))
# df1
# df2 = pandas.DataFrame(np.random.randn(10, 4))
# df2
# df = pandas.concat([df1, df2], axis=1)
# df


## test gwas
import os, sys
import statsmodels.api as sm
import numpy as np
os.chdir("/Users/kaiyin/Desktop/mmp")
trio = BedBimFam("mmp13")
bed = trio.bed.read_all()
phe = pandas.read_table("mmp13.phe", sep=" ", index_col=["FID", "IID"], usecols=["Sex", "Cage", "Page", "FID", "IID"])
dat = pandas.merge(phe, bed, how="inner", left_index=True, right_index=True)
geno = dat.drop(["Page", "Cage", "Sex"], axis=1)
pheno=dat[["Page", "Cage", "Sex"]]
g = Gwas(pheno=pheno, geno=geno, pheno_name="Page", covar_names=["Sex", "Cage"])
g.data.head()
g.geno.head()
g.pheno.head()
# %timeit gwas_res = g.run()
gwas_res = g.run(model_method="ols")
gwas_res.head()
fsp_res = g.run(model_method="fsp_ols")
fsp_res.head()
contrast_data = pandas.merge(gwas_res, fsp_res, how="inner", left_index=True, right_index=True)
contrast_data.head()

import ggplot
ggplot.ggplot(ggplot.aes("coef_x", "coef_y"), data=contrast_data) + ggplot.geom_point()
ggplot.ggplot(ggplot.aes("P_x", "P_y"), data=contrast_data) + ggplot.geom_point()
n = 1000000
simudat = pandas.DataFrame({"x":range(n), "y":-np.log10(np.random.uniform(size=n))})
simudat.head()
ggplot.ggplot(ggplot.aes("x", "y"), data=simudat) + ggplot.geom_point()
import matplotlib.pyplot as plt
import numpy as np
plt.pcolor()


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time, os
os.chdir("/tmp")
bedtw = pd.read_pickle("bed_twinsuk_big.pickle")
bednl = pd.read_pickle("bed_NLAUUK_big.pickle")

def conccur(ser1, ser2):
    # pdb.set_trace()
    ser1 = np.where(ser1 == -9, np.nan, ser1)
    ser2 = np.where(ser2 == -9, np.nan, ser2)
    diff = np.abs(ser1 - ser2)
    diff = diff[~np.isnan(diff)]
    return np.sum(diff) / diff.shape[0]

def conccur_df(df, ser):
    return df.apply(lambda x: conccur(x, ser), axis=0)

start = time.time()
# con_mat = bedtw.apply(lambda x: conccur_df(bednl, x), axis=0)
con_mat = bedtw.apply(lambda x: conccur_df(bednl.iloc[:, :3], x), axis=0)
print(time.time() - start)
con_mat.head()


def get_row_info(row):
    row.sort()
    smallest = row[:3]
    return pd.Series(list(smallest.index)+list(smallest), index=["match1", "match2", "match3", "conc1", "conc2", "conc3"])

indiv_map = con_mat.apply(get_row_info, axis=1)
indiv_map.conc1.plot(kind="hist")
indiv_map.conc2.plot(kind="hist")


plt.show()

row1 = con_mat.iloc[1, :]
row1
row1.sort()
smallest = row1[:3]

row1 = row1[row1 < .5]
row1.plot(kind="hist")
plt.show()

con_mat.head()
con_mat.min(axis=1)
dat = pd.DataFrame({"x":[1,1,2,2,2,2], "y":[3,4,3,3,4,4]})
dat.x.value_counts()
dat.pivot("x", "y")
dat.index
dat


fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
plt.plot(np.random.randn(50).cumsum(), "k--")
ax1.hist(np.random.randn(100), bins=20, color="k", alpha=0.3)
ax2.scatter(np.arange(30), np.arange(30) + 3 * np.random.randn(30))
plt.show()
close()









# from patsy import dmatrices, build_design_matrices
# from patsy import demo_data
# data = demo_data("x", "y", "a")
# data
# m = LM("y~a", data)


import os
import IPython.nbformat.current as nbf
py_file = "/tmp/x.py"
fn, ext = os.path.splitext(py_file)
ipy_file = fn + ".ipynb"
nb = nbf.read(open(py_file, 'r'), 'py')
nbf.write(nb, open(ipy_file, 'w'), 'ipynb')

