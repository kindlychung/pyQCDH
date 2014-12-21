import os
import weakref



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


