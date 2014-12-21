from pyQCDH.BedBimFam import BedBimFam
from imp import reload
import os

x = BedBimFam("/Users/kaiyin/Desktop/mmp/mmp13")
print(x.bed.ext)
print(x.bim.filename)

os.chdir("/Users/kaiyin/Desktop/mmp/")
trio = BedBimFam("/Users/kaiyin/Desktop/mmp/mmp13")
data = trio.fam.read(usecols=["IID", "FID"])
print(data.head())
data = trio.fam.read()
print(data.head())
data = trio.bim.read()
print(data.head())
data = trio.bim.read(usecols=["SNP", "CHR", "GDIST"])
print(data.head())
