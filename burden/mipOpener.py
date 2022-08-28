from ij import IJ, ImagePlus
from ij.plugin import ZProjector
import os, random, csv
from os import path

basedir = "/Volumes/JB_SD1/JB324/1dpi"
filenames = os.listdir(basedir)
bfiles = []
for files in filenames:
	if files.endswith(".czi"):
		file = path.join(basedir, files)
		bfiles.append(file)

for f in files:
	imp = IJ.openImage(f)
	proj = ZProjector.run(imp, "max all")
	proj.setC(2)

	imp.close()
	proj.show()

	rand = random.randint(1, 100)
	if rand > 85:
		IJ.run("Collect Garbage", "")
	else:
		pass

