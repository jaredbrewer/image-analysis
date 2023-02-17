from ij import IJ, ImagePlus, ImageStack, WindowManager
from ij.plugin import ZProjector, RGBStackMerge, ChannelSplitter
from ij.gui import NonBlockingGenericDialog, GenericDialog
from ij.process import ImageProcessor
from ij.measure import Calibration
from ij.io import DirectoryChooser, FileSaver
import os, sys, random, re
from os import path

gui = GenericDialog("File Directory: ")
gui.addDirectoryField("Raw Image Location", "~/Documents")
gui.addChoice("File Extension: ", [".czi", ".lif", ".lsm", ".tif", ".tiff", "Other"], ".tif")
gui.addStringField("Custom File Extension: ", "")
gui.addMessage("NB: The final composite images will always be saved")
gui.addMessage("This also assumes that the channels are all the same for all images!")
gui.addCheckbox("Save Splits?", True)
gui.addCheckbox("Manually Select Slices for Each Image?", False)
gui.addCheckbox("Save Z-Projections?", True)
gui.showDialog()

basedir = str(gui.getNextString())

outputdir = path.join(basedir, "comps")
if not path.isdir(outputdir):
	os.makedirs(outputdir)

ext = str(gui.getNextChoice())
cusext = str(gui.getNextString())

extension = ""

if ext != "Other":
	extension = ext.lower()
elif ext == "Other":
	extension = cusext.lower()

splitsaver = gui.getNextBoolean()

if splitsaver:
	splitdir = path.join(basedir, "splits")
	if not path.isdir(splitdir):
		os.makedirs(splitdir)

manmip = gui.getNextBoolean()

projsaver = gui.getNextBoolean()

if projsaver:
	projdir = path.join(basedir, "projs")
	if not path.isdir(projdir):
		os.makedirs(projdir)

inputs = os.listdir(basedir)
images = []

for input in inputs:
	if input.lower().endswith(extension) and not input.startswith(".") and not input.startswith("_"):
		file = path.join(basedir, input)
		images.append(file)

if len(images) > 0:
	sample = images[0]
	sample = IJ.openImage(sample)
	chan_list = ["C" + str(i + 1) for i in range(sample.getNChannels())] # I love list comprehensions
	chan_list.append("None")

	gui = NonBlockingGenericDialog("Set Channel LUTs")

	gui = NonBlockingGenericDialog("Color Matcher")
	gui.addChoice("Red: ", chan_list, "None")
	gui.addChoice("Green: ", chan_list, "None")
	gui.addChoice("Blue: ", chan_list, "None")
	gui.addChoice("Grey: ", chan_list, "None")
	gui.addChoice("Cyan: ", chan_list, "None")
	gui.addChoice("Magenta: ", chan_list, "None")
	gui.addChoice("Yellow: ", chan_list, "None")

	gui.showDialog()

	if gui.wasCanceled():
		IJ.error("Dialog cancelled!")
		exit()

	red_pick = str(gui.getNextChoice() + "-")
	green_pick = str(gui.getNextChoice() + "-")
	blue_pick = str(gui.getNextChoice() + "-")
	grey_pick = str(gui.getNextChoice() + "-")
	cyan_pick = str(gui.getNextChoice() + "-")
	magenta_pick = str(gui.getNextChoice() + "-")
	yellow_pick = str(gui.getNextChoice() + "-")

	color_list = [red_pick, green_pick, blue_pick, grey_pick, cyan_pick, magenta_pick, yellow_pick]

	colors = {red_pick: "Red", green_pick: "Green", blue_pick: "Blue", grey_pick: "Grays", cyan_pick: "Cyan", magenta_pick: "Magenta", yellow_pick: "Yellow"}
	del colors["None-"]
else:
	IJ.error("Empty Directory?")
	exit()

for image in images:
	raw = IJ.openImage(image)
	splits = ChannelSplitter.split(raw)
	bit_depth = raw.getBitDepth()
	mips = []
	combo_dict = {}
	for split in splits:
		if splitsaver:
			title = split.getTitle()
			out = path.join(splitdir, title)
			for key, value in colors.items():
				if title.startswith(key):
					IJ.run(split, value, "")
					IJ.setMinAndMax(split, 0, 2**int(bit_depth))
					IJ.saveAs(split, "Tiff", out)
					ImagePlus.close(split)
		title = split.getTitle()
		for key, value in colors.items():
			if title.startswith(key):
				if manmip:
					mips = [mip.lower() for mip in os.listdir(projdir)]
					mip_title = str("MAX_" + path.basename(title).lower())
					if mip_title.replace(extension, ".tif") not in mips:
						split.show()
						gui = NonBlockingGenericDialog("MIP Ranges")
						gui.addNumericField("First Slice: ", 0, 0)
						gui.addNumericField("Last Slice: ", 0, 0)
						gui.showDialog()

						bot = gui.getNextNumber()
						top = gui.getNextNumber()

						if bot is 0 and top is 0:
							bot = 1
							top = int(split.getImageStackSize())
						if int(bot) > int(top):
							IJ.error("Bottom is greater than top, invalid combination.")
							exit()
						if int(top) > int(split.getImageStackSize()):
							IJ.error("Top is greater than the dimensions of the image - try again")
							exit()
						if int(bot) < 1:
							IJ.error("Out of range - bottom number must be greater than or equal to 1")
							exit()

						proj = ZProjector.run(split, "max", int(bot), int(top))
						combo_dict[key] = proj

				if not manmip:
					proj = ZProjector.run(split, "max all")
					combo_dict[key] = proj

	if projsaver:
		for chan, proj in combo_dict.items():
			title = proj.getTitle()
			out = path.join(projdir, title)
			IJ.saveAs(proj, "Tiff", out)

	color_picker = []
	for color in color_list:
		if color != "None-":
			color_picker.append(combo_dict[color])
		elif color == "None-":
			color_picker.append(None)

	merge = RGBStackMerge.mergeChannels(color_picker, False)
	title = "composite_" + raw.getTitle()
	out = path.join(outputdir, title)
	del title
	IJ.saveAs(merge, "Tiff", out)
