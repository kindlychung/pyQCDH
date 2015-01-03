import pandas, scipy
import numpy as np
import statsmodels.api as sm

class Gwas:
    def __init__(self, pheno, geno, pheno_name, covar_names):
        """
        :param pheno: Phenotype data frame, which contains both phenotypes and covariates
        :type pheno: pandas.core.frame.DataFrame
        :param geno: Genotype data frame
        :type geno: pandas.core.frame.DataFrame
        :param pheno_name: Name of phenotype, should correspond the a column name of phenotype data frame
        :type pheno_name: str
        :param geno_names: Name(s) of covariates, should correspond the column name(s) of phenotype data frame
        :type geno_names: list[str]
        :param method: Method of model building
        :type method: str
        :return: A data frame of statistics
        :rtype: pandas.core.frame.DataFrame
        """
        # fsp_ols: fast semiparallel linear regression
        self.model_methods = {"ols": self.ols, "fsp_ols": self.fsp_ols}
        self.pheno_name = [pheno_name]
        self.covar_names = covar_names
        self.data = pandas.concat([pheno[self.pheno_name + self.covar_names], geno], axis=1, join="inner")
        self.pheno = self.data[pheno_name]
        self.covar = self.data[covar_names]
        self.geno = self.data.drop(self.pheno_name + self.covar_names, axis=1)

    def _ols(self, series):
        """
        Ordinary Least Squares
        :param series:
        :type series:
        :return:
        :rtype:
        """
        x = sm.add_constant(pandas.concat([series, self.covar], axis=1))
        model = sm.OLS(self.pheno, x)
        res = model.fit()
        return pandas.Series([res.pvalues[1], res.params[1]], index=["P", "coef"])

    def ols(self):
        return self.geno.apply(self._ols).T

    def fsp_ols(self):
        self.covar1 = sm.add_constant(self.covar)
        # this k is different from Karolina's paper, it's one more
        n,k = self.covar1.shape
        u1 = np.dot(self.covar1.T, self.pheno)
        xinvx = np.dot(self.covar1.T, self.covar1)
        u2 = np.linalg.solve(xinvx, u1)
        ytr = self.pheno - np.dot(self.covar1, u2)
        u3 = np.dot(self.covar1.T, self.geno)
        u4 = np.linalg.solve(xinvx, u3)
        Str = self.geno - np.dot(self.covar1, u4)
        Str2 = np.sum(Str**2, 0)
        b = np.dot(ytr.T, Str) / Str2
        sig =  ((ytr**2).sum() - b**2 * Str2) / (n-k-1)
        err = np.sqrt(sig * (1/Str2))
        p = scipy.stats.norm.sf(np.abs(b/err))
        return pandas.DataFrame({"P":p, "coef":b})



    def run(self, model_method):
        """
        Run GWAS
        :param model_method: Modeling method name
        :type model_method: str
        :return: A data frame of P values and coefficients
        :rtype: pandas.core.frame.DataFrame
        """
        return self.model_methods[model_method]()

