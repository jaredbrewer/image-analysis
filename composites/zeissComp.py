from ij import IJ, ImagePlus
from ij.plugin import ZProjector, RGBStackMerge
from ij.gui import GenericDialog
import os, sys, random, re
from os import path

gui = GenericDialog("File Directory: ")
gui.addDirectoryField("Individual Channels: ", "~/Documents")
gui.showDialog()

basedir = str(gui.getNextString())
outputdir = basedir + "/comps/"
if not path.isdir(outputdir):
	os.makedirs(outputdir)

inputs = os.listdir(basedir)
filenames = []

for input in inputs:
	if input.startswith("MAX_"):
		filenames.append(input)

mips = []
names = []
chans = []

for files in filenames:
	file = os.path.join(basedir, files)
	mips.append(file)
	base = str(files.split("-", 1)[1])
	chan = str(files.split("-", 1)[0])
	chans.append(chan)
	names.append(base)

names = set(names)
chans = sorted(set(chans))
mip_dict = {}

for name in names:
	title = ""
	for mip in mips:
		for chan in chans:
			if mip.startswith(basedir + chan) and mip.endswith(name):
				mip_dict["C" + int(chans.index(chan) + 1)] = mip
				title = mip.replace(basedir + chan + "-", "")
	merge = RGBStackMerge.mergeChannels([ImagePlus(mip_dict['C3']), None, ImagePlus(mip_dict['C2']), None, None, None, ImagePlus(mip_dict['C1'])], False)
	out = path.join(outputdir, title)
	del title
	IJ.saveAs(merge, "Tiff", out)

gui = GenericDialog("All Done!")
gui.showDialog()
