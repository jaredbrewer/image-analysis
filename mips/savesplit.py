from ij import IJ, ImagePlus
from ij.io import DirectoryChooser, FileSaver
from ij.plugin import ChannelSplitter
from ij.gui import GenericDialog
import os, sys
from os import path

# Written in Python 2 - ImageJ does not (yet?) support Python 3 - really only impacts print statements

# inputdir = DirectoryChooser("Input ")
# outputdir = DirectoryChooser("Output ")

basedir = str("/Volumes/JB_SD2/THP1_032422/Lentivirus/Slide_2/NFATC2/ctrl")

inputdir = basedir
outputdir = basedir + "/Splits/"
if not path.isdir(outputdir):
	os.makedirs(outputdir)

filenames = os.listdir(inputdir)

czi_files = []

for files in filenames:
	if files.endswith(".czi"):
		file = os.path.join(inputdir, files)
		czi_files.append(file)
	
for f in czi_files:
	imp = IJ.openImage(f)
	imps = ChannelSplitter.split(imp)
	for i in imps:
		title = i.getTitle()
		out = path.join(outputdir, title)
		if "C4-" in title: 
			IJ.run(i, "Yellow", "")
			IJ.setMinAndMax(i, 0, 4095)
			IJ.saveAs(i, "Tiff", out)
			ImagePlus.close(i)
		if "C3-" in title:
			IJ.run(i, "Red", "")
			IJ.setMinAndMax(i, 0, 4095)
			IJ.saveAs(i, "Tiff", out)
			ImagePlus.close(i)
		if "C2-" in title:
			IJ.run(i, "Blue", "")
			IJ.setMinAndMax(i, 0, 4095)
			IJ.saveAs(i, "Tiff", out)
			ImagePlus.close(i)
		if "C1-" in title:
			ImagePlus.close(i)
			
gui = GenericDialog("All Done!")
gui.showDialog()