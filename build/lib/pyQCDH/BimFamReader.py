# a mix-in class for reading bim and fam files
class BimFamReader:
    def read(self, **kwargs):
        # pdb.set_trace()
        #:type: list[str]
        cols_res = self.cols[:]
        if "usecols" in kwargs:
            # if usecols is a list of integers, use it as an index for colnames
            if isinstance(kwargs["usecols"][0], int):
                idx = [x for x in self.full_idx if x in kwargs["usecols"]]
                cols_res = [self.cols[x] for x in idx]
            # if usecols is a list of strings, then we need to calculate the index to be passed to read_csv
            if isinstance(kwargs["usecols"][0], str):
                idx = [self.cols.index(x) for x in kwargs["usecols"]]
                cols_res = [i for i in self.cols if i in kwargs["usecols"]]
                kwargs["usecols"] = idx
            else:
                raise ValueError("usecols must be a list of str or int")

        data = pandas.read_csv("mmp13.fam", delim_whitespace=True, header=None, **kwargs)
        data.columns = cols_res
        return data
