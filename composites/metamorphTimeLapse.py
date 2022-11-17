from ij import IJ, ImagePlus
from ij.plugin import ZProjector, RGBStackMerge, Concatenator, Duplicator, HyperStackConverter
from ij.gui import GenericDialog, NonBlockingGenericDialog
import os, sys, random, re
from os import path

gui = GenericDialog("File Directory: ")
gui.addMessage("This script assumes: \n (a) you have more than one channel, \n (b) this is a time lapse and \n (c) this has multiple stage positions.  \n If any of these are not true, this will not (currently) work for you. \n Let me know if you'd like to see more of that kind of functionality.")
gui.addDirectoryField("Individual Channels: ", "~/Documents")
gui.addCheckbox("Multiple Scenes?", True)
gui.addCheckbox("Multiple Time Points?", True)
gui.showDialog()

basedir = str(gui.getNextString())
multiscene = gui.getNextBoolean()
timelapse = gui.getNextBoolean()

outputdir = path.join(basedir, "comps")
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
	if multiscene and timelapse:
		chans.append(p[1])
		scenes.append(int(p[2].replace("s", "")))
		times.append(int(p[3].split(".")[0].replace("t", "")))
	elif multiscene:
		chans.append(p[1])
		scenes.append(int(p[2].split(".")[0].replace("s", "")))
	elif timelapse:
		chans.append(p[1])
		times.append(int(p[2].split(".")[0].replace("t", "")))
	else:
		chans.append(p[1]).split(".")[0]
	
names = list(set(names))
chans = list(set(chans))
scenes = list(sorted(set(scenes)))
times = list(sorted(set(times)))

chan_pairs = ""
for chan in chans:
	chan_pairs += "C" + str(int(chans.index(chan) + 1)) + ": " + chan + "\n"

chan_list = ["C" + str(int(chans.index(chan) + 1)) for chan in chans]
chan_list.append("None")

#for name in names:
gui = NonBlockingGenericDialog("Color Matcher")
#	gui.addMessage("Image Set: " + name)
gui.addMessage(chan_pairs)
#	gui.addCheckbox("Do this set?", True)
gui.addChoice("Red: ", chan_list, "None")
gui.addChoice("Green: ", chan_list, "None")
gui.addChoice("Blue: ", chan_list, "None")
gui.addChoice("Grey: ", chan_list, "None")
gui.addChoice("Cyan: ", chan_list, "None")
gui.addChoice("Magenta: ", chan_list, "None")
gui.addChoice("Yellow: ", chan_list, "None")

gui.showDialog()
#	do_set = gui.getNextBoolean()
#	if not do_set:
#		names.remove(name)

red_pick = str(gui.getNextChoice())
green_pick = str(gui.getNextChoice())
blue_pick = str(gui.getNextChoice())
grey_pick = str(gui.getNextChoice())
cyan_pick = str(gui.getNextChoice())
magenta_pick = str(gui.getNextChoice())
yellow_pick = str(gui.getNextChoice())

colors = [red_pick, green_pick, blue_pick, grey_pick, cyan_pick, magenta_pick, yellow_pick]

if path.isdir(outputdir):
	print(outputdir)
print(names)
print(chans)
print(scenes)
print(times)
print(chan_list)
print(colors)

def merge_and_save():
	if combo_dict:
		for color in colors:
			if color != "None":
				color_picker.append(combo_dict[color])
			elif color == "None":
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

def tl_logic():

	def checker():
		if path.isfile(still):
			combo_dict["C" + str(int(chans.index(chan) + 1))] = ImagePlus(still)
			
	if timelapse and multiscene:
		for time in times:
			still = path.join(basedir, "_".join([name, chan, "s" + str(scene), "t" + str(time) + "".join(ext)]))
			checker()
	elif timelapse:
		for time in times:
			still = path.join(basedir, "_".join([name, chan, "t" + str(time) + "".join(ext)]))
			checker()
	elif multiscene:
		still = path.join(basedir, "_".join([name, chan, "s" + str(scene) + "".join(ext)]))
		checker()
	else:
		still = path.join(basedir, "_".join([name, chan + "".join(ext)]))
		checker()

for name in names:
	if multiscene:
		for scene in scenes:
			color_picker = []
			combo_dict = {}
			num_stacks = []
			for chan in chans:
				title = "_".join([name, str(scene)])
				stills = []
				if timelapse:
					for time in times:
						# Regenerate the name from defined parts -
						still = path.join(basedir, "_".join([name, chan, "s" + str(scene), "t" + str(time) + "".join(ext)]))
						if path.isfile(still):
							still = ImagePlus(still)
							num_stacks.append(still.getNSlices())
							stills.append(still)
					if stills:
						max_stacks = max(num_stacks)
						for still in stills:
							if still.getNSlices() < max_stacks:
								bt = still.getTitle()
								bd = str(still.getBitDepth()) + "-bit black"
								blank = IJ.createImage(bt, bd,
									still.getWidth(), 
									still.getHeight(), 
									still.getNChannels(), 
									max_stacks,
									still.getNFrames())
								for i in range(0, still.getNSlices() + 1):
									still.setSlice(i)
									still.copy()
									blank.setSlice(i)
									blank.paste()
								imp2 = blank.duplicate()
								stills[stills.index(still)] = imp2
						combo_dict["C" + str(int(chans.index(chan) + 1))] = Concatenator.run(stills)
			if combo_dict:
				print(combo_dict)
				for color in colors:
					if color != "None":
						color_picker.append(combo_dict[color])
					elif color == "None":
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
			stills = []
			if timelapse:
				for time in times:
					# Regenerate the name from defined parts -
					still = path.join(basedir, "_".join([name, chan, "t" + str(time) + "".join(ext)]))
					if path.isfile(still):
						stills.append(ImagePlus(still))
				if stills:
					combo_dict["C" + str(int(chans.index(chan) + 1))] = Concatenator.run(stills)
			else:
				still = path.join(basedir, "_".join([name, chan + "".join(ext)]))
				if path.isfile(still):
					combo_dict["C" + str(int(chans.index(chan) + 1))] = ImagePlus(still)
			if combo_dict:
				for color in colors:
					if color != "None":
						color_picker.append(combo_dict[color])
					if color == "None":
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

