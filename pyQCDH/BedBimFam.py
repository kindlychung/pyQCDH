import pdb
import os, sys
import math
import weakref
import itertools
import pandas
import numpy
from .BimFamReader import BimFamReader
from .ByteDict import byte_dict


class BedBimFam:
    def __init__(self, stem):
        """
        :type filename: str
        :type self: BedBimFam
        """
        self._stem = os.path.abspath(stem)
        self._dir, tmp = os.path.split(self.stem)
        bed_file, bim_file, fam_file = map(lambda ext: self.stem + ext, (ext  for ext in (".bed", ".bim", ".fam")))
        self.bed = Bed(bed_file)
        self.bim = Bim(bim_file)
        self.fam = Fam(fam_file)
        # I didn't put parent=self in the above 3 lines, because this is a circular reference and needs weakref
        self.bed.parent = weakref.proxy(self)
        self.bim.parent = weakref.proxy(self)
        self.fam.parent = weakref.proxy(self)
        self._n_individuals = None
        self._n_snps = None
        self._bytes_per_snp = None
        self._n_individuals_apparent = None
        self._validate_file_size()
        #:type: list[str]
        self.snp = self.bim.snp["SNP"].tolist() # a list of SNP names
        self.snp_idx_dict = dict(zip(self.snp, range(len(self.snp))))


    @property
    def stem(self):
        """
        Common stem of bed/bim/fam filepaths
        :return:
        :rtype:
        """
        return self._stem

    @property
    def dir(self):
        """
        Directory of bed/bim/fam file
        :return:
        :rtype:
        """
        return self._dir

    @property
    def n_individuals(self):
        """
        Calculate number of individuals, from line number of fam file
        :return:
        :rtype:
        """
        if self._n_individuals is None:
            self._n_individuals = self.fam.count_lines()
        return self._n_individuals

    @property
    def n_snps(self):
        """
        Calculate number of SNPs, from line numbers of bim file
        :return:
        :rtype:
        """
        if self._n_snps is None:
            self._n_snps = self.bim.count_lines()
        return self._n_snps

    @property
    def bytes_per_snp(self):
        """
        Calculate the number of bytes per SNP (2 bits for each, hence 1/4 byte)
        :return:
        :rtype:
        """
        if self._bytes_per_snp is None:
            self._bytes_per_snp = math.ceil(self.n_individuals / 4)
        return self._bytes_per_snp

    @property
    def n_individuals_apparent(self):
        if self._n_individuals_apparent is None:
            self._n_individuals_apparent = self._bytes_per_snp * 4
        return self._n_individuals_apparent

    def _validate_file_size(self):
        """
        Validate the size of .bed file. It should be equal to n_snps * bytes_per_snp - 3
        :return:
        :rtype:
        """
        bed_size = os.path.getsize(self.bed.filename)
        expected_size = self.bytes_per_snp * self.n_snps + 3
        if bed_size != expected_size:
            raise ValueError("Size of %s does not match that of bim and fam file:"
                             "\nExpected %d bytes, got %d bytes"
                             "\nDetail:"
                             "\nNumber of SNPs: %d"
                             "\nNumber of obs:  %d"
                             "\nBytes per SNP:  %d"
                             % (self.bed.filename, expected_size, bed_size, self.n_snps, self.n_individuals, self.bytes_per_snp))


class PlinkFile:
    def __init__(self, filename, ext, parent=None):
        """
        A class for managing plink files (bed, bim, fam).
        :param filename:
        :type filename: str
        :param ext:
        :type ext: str
        :param parent:
        :type parent: BedBimFam
        :return:
        :rtype:
        """
        self._filename = os.path.abspath(filename)
        self._ext = ext
        self.stem = None
        self._validate()
        self.parent = parent

    def _validate(self):
        self.stem, real_ext = os.path.splitext(self.filename)
        if real_ext != self.ext:
            raise ValueError("Wrong extension, expected %s and get %s" % (self.ext, real_ext))
        if not os.path.isfile(self.filename):
            raise ValueError("%s is not a file" % self.filename)


    @property
    def filename(self):
        return self._filename

    @property
    def ext(self):
        return self._ext


class Bed(PlinkFile):
    """
    A class for managing bed file, should have a BedBimFam instance as a parent.
    """
    def __init__(self, filename, parent=None):
        super().__init__(filename, ".bed", parent)
        self._validate()

    def _validate(self):
        """
        Validate that the file conforms to plink format.
        First two bits must be b"l\x1b", the third bit b"\x01" indicates SNP-major.
        This package does not support individual-major format.
        :return:
        :rtype:
        """
        with open(self.filename, "rb") as fh:
            magic_bits = fh.read(2)
            if magic_bits != b'l\x1b':
                raise ValueError("%s is not a valide plink bed file" % self.filename)
            major_bit = fh.read(1)
            if major_bit != b'\x01':
                raise ValueError("%s is not in SNP-major" % self.filename)

            return None

    def read_cols(self, idx):
        """
        Read columns by an index of integers. Index is an iterable of ints, 0-based, like in C.
        :param idx:
        :type idx: list[int]
        :return:
        :rtype: pandas.core.frame.DataFrame
        """
        idx.sort()
        with open(self.filename, "rb") as fh:
            def read_one_col_raw(i):
                # seek to beginning of file
                fh.seek(0)
                # seek 3 format bytes, then seek to the ith SNP
                fh.seek(3 + self.parent.bytes_per_snp * i)
                return fh.read(self.parent.bytes_per_snp)
            res = b"".join(read_one_col_raw(i) for i in idx)
            res = self._bytes_to_data(res)
            res.columns = [self.parent.snp[i] for i in idx]
            return res


    def _bytes_to_data(self, bytes_str):
        """
        Convert raw bytes read from bed file into genotype data frame.
        :param bytes_str:
        :type bytes_str: bytes
        :return:
        :rtype: pandas.core.frame.DataFrame
        """
        geno_data= (byte_dict[x] for x in bytes_str)
        # flatten the list
        geno_data = list(itertools.chain.from_iterable(geno_data))
        # convert it into a numpy array and reshape it into right dimensions
        geno_data = numpy.array(geno_data)
        geno_data = geno_data.reshape((self.parent.n_individuals_apparent, -1), order="F")
        geno_data = pandas.DataFrame(geno_data[0:self.parent.n_individuals, ], index=[self.parent.fam.fidiid.FID, self.parent.fam.fidiid.IID])
        geno_data = geno_data.replace(-9, numpy.nan)
        # fill all NAs with column mean
        return geno_data.apply(lambda x: numpy.where(x.isnull(), x.mean(), x))

    def read_all(self):
        """
        Read the whole bed file into a pandas data frame.
        :return:
        :rtype: pandas.core.frame.DataFrame
        """
        with open(self.filename, "rb") as fh:
            fh.seek(3)
            all_bytes = fh.read(self.parent.bytes_per_snp * self.parent.n_snps)
            all_bytes =  self._bytes_to_data(all_bytes)
            all_bytes.columns = self.parent.snp
            return all_bytes

    def read_snps(self, snp_list, warning=False):
        """
        Read selected SNPs into a pandas data frame.
        :type snp_list: list[str]
        :return:
        :rtype: pandas.core.frame.DataFrame
        """
        # get the indices of SNPs in the list
        # idx = [i for i in range(len(self.parent.snp)) if self.parent.snp[i] in snp_list]
        idx = [self.parent.snp_idx_dict[snp] for snp in snp_list]
        # check if all SNPs in the list can be found in plink files
        if warning:
            snp_found = [self.parent.snp[i] for i in idx]
            snp_missing = [snp for snp in snp_list if snp not in snp_found]
            if snp_missing:
                sys.stderr.write("Warning: the following SNPs cannot be found: \n" + str(snp_missing))
        # DRY: make use of self.read_cols
        return self.read_cols(idx)



class Bim(PlinkFile, BimFamReader):
    """
    A class for managing bim file, should have a BedBimFam instance as a parent.
    """
    cols = ("CHR", "SNP", "GDIST", "BP", "A1", "A2")
    full_idx = tuple(range(len(cols)))
    def __init__(self, filename, parent=None):
        PlinkFile.__init__(self, filename, ".bim", parent)
        BimFamReader.__init__(self)
        #:type: pandas.core.frame.DataFrame
        self._snp = None # SNP names

    @property
    def snp(self):
        """
        Returns a data frame of SNP names. Try to as lazy as possible,
        if SNP has already been read before, use existing SNP data frame,
        otherwise, if self._data has been read before, then extract the
        SNP column out of it.
        To actually read the SNP column from the bim file is the last resort.
        """
        if self._snp is None:
            if self._data is not None:
                self._snp = self.data["SNP"]
            else:
                self._snp = self.read(usecols=["SNP"])
        return self._snp


class Fam(PlinkFile, BimFamReader):
    """
    A class for managing fam file, should have a BedBimFam instance as a parent.
    """
    cols = ("FID", "IID", "PID", "MID", "SEX", "AFFECT")
    full_idx = tuple(range(len(cols)))
    def __init__(self, filename, parent=None):
        PlinkFile.__init__(self, filename, ".fam", parent)
        BimFamReader.__init__(self)
        #:type: pandas.core.frame.DataFrame
        self._fidiid = None # family and individual id, lazily evaluated

    @property
    def fidiid(self):
        """
        Returns a data frame of two columns, FID and IID
        :return:
        :rtype:
        """
        if self._fidiid is None:
            if self._data is not None:
                self._fidiid = self.data[["FID", "IID"]]
            else:
                self._fidiid = self.read(usecols=["FID", "IID"])
        return self._fidiid



