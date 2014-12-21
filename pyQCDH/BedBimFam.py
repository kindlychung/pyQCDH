import os
from .BimFamReader import BimFamReader


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
        self.bed.parent = self
        self.bim.parent = self
        self.fam.parent = self

    @property
    def stem(self):
        return self._stem

    @property
    def dir(self):
        return self._dir


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




