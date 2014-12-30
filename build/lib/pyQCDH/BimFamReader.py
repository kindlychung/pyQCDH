import pandas


def count_lines(filename):
    """
    Count the number of lines in a file.
    :param filename:
    :type filename:  str
    :return:
    :rtype: int
    """
    n = 0
    with open(filename, "rb") as fh:
        for line in fh:
            n += 1
    return n


# a mix-in class for reading bim and fam files
class BimFamReader:
    def __init__(self, *args, **kwargs):
        """
        The cols and full_idx field must exist in the other class that uses this one as a mix-in.
        :return:
        :rtype:
        """
        #:type: pandas.core.frame.DataFrame
        self._data = None # family and individual id, lazily evaluated

    @property
    def data(self):
        if not self._data:
            self._data = self.read(usecols="all")
        return self._data

    def read(self, **kwargs):
        """
        Read bim or fam file. All the **kwargs are passed to pandas.read_csv,
        the usecols option is given special care, you can pass an numbered index list,
        or a list of column names that you wish to select.
        When usecols is set to "all", all columns are read.
        :param kwargs:
        :type kwargs:
        :return:
        :rtype: pandas.core.frame.DataFrame
        """
        # pdb.set_trace()
        #:type: list[str]
        cols_res = self.cols[:]
        if "usecols" in kwargs:
            # read all if usecols is set to "all"
            if kwargs["usecols"] == "all":
                kwargs["usecols"] = self.full_idx
            # if usecols is a list of integers, use it as an index for colnames
            elif isinstance(kwargs["usecols"][0], int):
                idx = [x for x in self.full_idx if x in kwargs["usecols"]]
                cols_res = [self.cols[x] for x in idx]
            # if usecols is a list of strings, then we need to calculate the index to be passed to read_csv
            elif isinstance(kwargs["usecols"][0], str):
                idx = [self.cols.index(x) for x in kwargs["usecols"]]
                cols_res = [i for i in self.cols if i in kwargs["usecols"]]
                kwargs["usecols"] = idx
            else:
                raise ValueError("usecols must be a list of str or int or None")

        data = pandas.read_csv(self.filename, delim_whitespace=True, header=None, **kwargs)
        data.columns = cols_res
        return data

    def count_lines(self):
        """
        Count the number of lines in the bim or fam file.
        :return:
        :rtype: int
        """
        return count_lines(self.filename)
