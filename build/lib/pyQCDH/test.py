from pyQCDH.BedBimFam import BedBimFam, Bed
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


import os, sys
import statsmodels.api as sm
import numpy as np
os.chdir("/Users/kaiyin/Desktop/mmp")
trio = BedBimFam("mmp13")
bed = trio.bed.read_all()
phe = pandas.read_table("mmp13.phe", sep=" ", index_col=["FID", "IID"], usecols=["Sex", "Cage", "Page", "FID", "IID"])
phe.head()
dat = pandas.merge(phe, bed, how="inner", left_index=True, right_index=True)
dat
dir(dat.Page.dtype)
dat.Page.dtype.type
dat.Sex.dtype
dat
phe_n_cols = phe.shape[1]
phe_n_cols





geno = dat.drop(["Page", "Cage", "Sex"], axis=1)
pheno=dat[["Page", "Cage", "Sex"]]
g = Gwas(pheno=pheno, geno=geno, pheno_name="Page", covar_names=["Sex", "Cage"])
g.data.head()
g.geno.head()
g.pheno.head()
# %timeit gwas_res = g.run()
# gwas_res = g.run(model_method="ols")
# gwas_res.head()
fsp_res = g.run(model_method="fsp_ols")
fsp_res.head()
%timeit g.run(model_method="fsp_ols")



# from patsy import dmatrices, build_design_matrices
# from patsy import demo_data
# data = demo_data("x", "y", "a")
# data
# m = LM("y~a", data)



