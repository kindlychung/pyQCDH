from .BimFamReader import BimFamReader

class PlinkFile:
    def __init__(self, filename, ext, parent=None):
        """
        :type filename: str
        :type ext: str
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
    def __init__(self, filename):
        super().__init__(filename, ".bed")


class Bim(PlinkFile, BimFamReader):
    cols = ("CHR", "SNP", "GDIST", "BP", "A1", "A2")
    def __init__(self, filename):
        super().__init__(filename, ".bim")



class Fam(PlinkFile, BimFamReader):
    cols = ("FID", "IID", "PID", "MID", "SEX", "AFFECT")
    full_idx = tuple(range(len(cols)))
    def __init__(self, filename):
        super().__init__(filename, ".fam")




x = Bed("/Users/kaiyin/Desktop/mmp/mmp13.bed")
x = BedBimFam("/Users/kaiyin/Desktop/mmp/mmp13")
x.bed.ext
x.bim.filename

os.chdir("/Users/kaiyin/Desktop/mmp/")
import pandas
import pdb
trio = BedBimFam("/Users/kaiyin/Desktop/mmp/mmp13")
data = trio.fam.read(usecols=["IID", "FID"])
data = trio.fam.read()
data.head()
data = trio.bim.
