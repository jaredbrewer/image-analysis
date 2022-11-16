from ij import IJ, ImagePlus
from ij.plugin import ZProjector, RGBStackMerge, Concatenator
from ij.gui import GenericDialog, NonBlockingGenericDialog
import os, sys, random, re
from os import path

gui = GenericDialog("File Directory: ")
gui.addMessage("This script assumes (a) you have more than one channel, (b) this is a time lapse and (c) this has multiple stage positions.  If any of these are not true, this will not (currently) work for you. Let me know if you'd like to see more of that kind of functionality.")
gui.addDirectoryField("Individual Channels: ", "~/Documents")
gui.addCheckBox("Multiple Scenes?", True)
gui.addCheckbox("Multiple Time Points?", True)
gui.showDialog()

basedir = str(gui.getNextString())
multiscene = gui.getNextBoolean()
timelapse = gui.getNextBoolean()

outputdir = basedir + "/comps/"
if not path.isdir(outputdir):
	os.makedirs(outputdir)

inputs = os.listdir(basedir)
filenames = []
ext = []

for input in inputs:
	if "thumb" not in input and input.lower().endswith(".tif"):
		filenames.append(input)
		ext.append("." + input.rsplit(".", 1)[1])

ext = set(ext)

parts = []

for files in filenames:
	part = files.rsplit("_", 3)
	parts.append(part)

names = []
chans = []
scenes = []
times = []

for p in parts:
	names.append(p[0])
	chans.append(p[1])
	scenes.append(p[2].replace("s", "")))
	times.append(p[3].split(".")[0].replace("t", ""))

names = set(names)
chans = set(chans)
scenes = sorted(set(scenes))
times = sorted(set(times))

chan_pairs = ""
for chan in chans:
	chan_pairs += "C" + str(int(chans.index(chan) + 1)) + ": " + chan + "\n"

chan_list = ["C" + str(int(chans.index(chan) + 1)) for chan in chans]

gui = NonBlockingGenericDialog("Color Matcher")
gui.addMessage(chan_pairs)
gui.addChoice("Red: ", chan_list, "None")
gui.addChoice("Green: ", chan_list, "None")
gui.addChoice("Blue: ", chan_list, "None")
gui.addChoice("Grey: ", chan_list, "None")
gui.addChoice("Cyan: ", chan_list, "None")
gui.addChoice("Magenta: ", chan_list, "None")
gui.addChoice("Yellow: ", chan_list, "None")

gui.showDialog()

red_pick = str(gui.getNextChoice())
green_pick = str(gui.getNextChoice())
blue_pick = str(gui.getNextChoice())
grey_pick = str(gui.getNextChoice())
cyan_pick = str(gui.getNextChoice())
magenta_pick = str(gui.getNextChoice())
yellow_pick = str(gui.getNextChoice())

colors = [red_pick, green_pick, blue_pick, grey_pick, cyan_pick, magenta_pick, yellow_pick]

# color_picker = []
# for color in colors:
# 	if color != "None":
# 		color_picker.append(ImagePlus(combo_dict[color]))
# 	if color == "None"
# 		color_picker.append(None)

# from ij.gui import GenericDialog
# from ij import IJ, ImagePlus

#chans = ["A", "B", "C"]
#
#chan_pairs = ""
#for chan in chans:
#	chan_pairs += "C" + str(int(chans.index(chan) + 1)) + ": " + chan + "\n"

# combo_dict = {}
# colors = ["/Users/jared/Documents/Figure 1/fish2_GFP.tif", "None", "None", "None", "None", "None", "/Users/jared/Documents/Figure 1/fish3_GFP.tif"]
#
# color_picker = []
# for color in colors:
# 	if color != "None":
# 		color_picker.append(ImagePlus(color))
# 	if color == "None":
# 		color_picker.append(None)
#
# print(color_picker)

#print(chan_pairs)
#gui = GenericDialog("Colors")
#gui.addMessage(chan_pairs)
#gui.addChoice("Red", chans, None)
#
#gui.showDialog()
#
#chan_picker = gui.getNextChoice()
#print(chan_picker)


chans.remove("None")

for name in names:
	if multiscene:
		for scene in scenes:
			title = "_".join([name, scene])
			combo_dict = {}
			color_picker = []
			for chan in chans:
				stills = []
				if timelapse:
					for time in times:
						# Regenerate the name from defined parts -
						still = path.join(basedir, "_".join([name, chan, "s" + scene, "t" + time + ext]))
						stills.append(ImagePlus(still))
					combo_dict["C" + str(int(chans.index(chan) + 1))] = Concatenator.run(stills)
				else:
					still = path.join(basedir, "_".join([name, chan, "s" + scene + ext]))
					stills.append(ImagePlus(still))
			for color in colors:
				if color != "None":
					color_picker.append(ImagePlus(combo_dict[color]))
				if color == "None"
					color_picker.append(None)
			merge = RGBStackMerge.mergeChannels(color_picker, False)
			proj = ZProjector.run(merge, "max all")
			out = path.join(outputdir, title)
			del title
			IJ.saveAs(proj, "Tiff", out)
			rand = random.randint(1, 100)
			if rand > 85:
				IJ.run("Collect Garbage", "")
			else:
				pass
	else:
		title = name
		combo_dict = {}
		color_picker = []
		for chan in chans:
			stills = []
			if timelapse:
				for time in times:
						# Regenerate the name from defined parts -
					still = path.join(basedir, "_".join([name, chan, "s" + scene, "t" + time + ext]))
					stills.append(ImagePlus(still))
				combo_dict["C" + str(int(chans.index(chan) + 1))] = Concatenator.run(stills)
			else:
				still = path.join(basedir, "_".join([name, chan, "s" + scene + ext]))
				stills.append(ImagePlus(still))
		for color in colors:
			if color != "None":
				color_picker.append(ImagePlus(combo_dict[color]))
			if color == "None"
				color_picker.append(None)
		merge = RGBStackMerge.mergeChannels(color_picker, False)
		proj = ZProjector.run(merge, "max all")
		out = path.join(outputdir, title)
		del title
		IJ.saveAs(proj, "Tiff", out)
		rand = random.randint(1, 100)
		if rand > 85:
			IJ.run("Collect Garbage", "")
		else:
			pass

gui = GenericDialog("All Done!")
gui.showDialog()
