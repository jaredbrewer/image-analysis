from ij import IJ, ImagePlus
from ij.plugin import ZProjector, RGBStackMerge, Concatenator, Duplicator, HyperStackConverter
from ij.gui import GenericDialog, NonBlockingGenericDialog
import os, sys, random, re
from os import path

<<<<<<< HEAD
gui = GenericDialog("Metamorph File Compiler")
gui.addMessage("Version 0.1a, 17 November 2022")
gui.addDirectoryField("Files Directory: ", "~/Documents")
gui.addCheckbox("Multiple Scenes?", True)
gui.addCheckbox("Multiple Time Points?", True)
gui.addCheckbox("Show Merged Image?", False)
gui.addCheckbox("Use Metadata from .nd File?", False)
=======
gui = GenericDialog("File Directory: ")
gui.addMessage("This script assumes: \n (a) you have more than one channel, \n (b) this is a time lapse and \n (c) this has multiple stage positions.  \n If any of these are not true, this will not (currently) work for you. \n Let me know if you'd like to see more of that kind of functionality.")
gui.addDirectoryField("Individual Channels: ", "~/Documents")
gui.addCheckbox("Multiple Scenes?", True)
gui.addCheckbox("Multiple Time Points?", True)
>>>>>>> 5a0826858ff2ad1ef736f2782cb48258a0a7df2f
gui.showDialog()

basedir = str(gui.getNextString())
multiscene = gui.getNextBoolean()
timelapse = gui.getNextBoolean()
<<<<<<< HEAD
opener = gui.getNextBoolean()
nder = gui.getNextBoolean()
=======
>>>>>>> 5a0826858ff2ad1ef736f2782cb48258a0a7df2f

outputdir = path.join(basedir, "comps")
if not path.isdir(outputdir):
	os.makedirs(outputdir)

inputs = os.listdir(basedir)
filenames = []
ext = []

for input in inputs:
	if "thumb" not in input and input.lower().endswith(".tif") and not input.startswith(".") and not input.startswith("_"):
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

chan_dict = {}
chan_pairs = ""
for chan in chans:
	chan_dict["C" + str(int(chans.index(chan) + 1))] = chan
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
for key, value in chan_dict.items():
	if key not in colors:
		del chan_dict[key]

<<<<<<< HEAD
chans = chan_dict

print(names)
print(chans)
print(scenes)
print(times)
print(ext)
print(colors)
print(timelapse)
print(multiscene)
print(opener)
print(nder)

def metamorpher(names, chans, scenes, times, ext, colors, timelapse = True, multiscene = True, opener = False, nder = False):

	def titler(nder, name, scene):
		if nder:
			if path.isfile(path.join(basedir, name + ".nd")):
				pos_dict = {}
				with open(path.join(basedir, name + ".nd"), "r") as nd_file:
					for line in nd_file.readlines():
						if line.startswith("\"Stage"):
							pos_dict[line.split(",")[0].strip("\"\n").replace("Stage", "")] = line.split(",")[1].strip("\"\n\r ")
				scene_name = pos_dict.get(str(scene))
				if scene_name:
					title = "_".join([name, scene_name])
		else:
			title = "_".join([name, str(scene)])
		return title

	def merge_and_save(combo_dict, colors, title, outputdir, opener):
		color_picker = []
=======
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
>>>>>>> 5a0826858ff2ad1ef736f2782cb48258a0a7df2f
		for color in colors:
			if color != "None":
				color_picker.append(combo_dict[color])
			elif color == "None":
				color_picker.append(None)
		merge = RGBStackMerge.mergeChannels(color_picker, False)
		if opener:
			merge.show()
		out = path.join(outputdir, title)
		del title
		IJ.saveAs(merge, "Tiff", out)
		rand = random.randint(1, 100)
		if rand > 85:
			IJ.run("Collect Garbage", "")
		else:
			pass

<<<<<<< HEAD
	for name in names:
		if timelapse and multiscene:
			for scene in scenes:
				title = titler(nder, name, scene)
				print(title)
				combo_dict = {}
				for key, chan in chans.items():
					stills = []
					for time in times:
						still = path.join(basedir, "_".join([name, chan, "s" + str(scene), "t" + str(time) + "".join(ext)]))
						if path.isfile(still):
							still = ImagePlus(still)
							if still.getNSlices() > 1:
								still = ZProjector.run(still, "max")
								stills.append(still)
							else:
								stills.append(still)
					if stills:
						if timelapse:
							combo_dict[key] = Concatenator.run(stills)
						else:
							combo_dict[key] = ImagePlus(still)
				if combo_dict:
					merge_and_save(combo_dict, colors, title, outputdir, opener)
		elif timelapse:
			title = name
			combo_dict = {}
			for key, chan in chans.items():
				stills = []
				for time in times:
					still = path.join(basedir, "_".join([name, chan, "t" + str(time) + "".join(ext)]))
					if path.isfile(still):
						still = ImagePlus(still)
						num_stacks.append(still.getNSlices())
						stills.append(still)
				if stills:
					if timelapse:
						combo_dict[key] = Concatenator.run(stills)
					else:
						combo_dict[key] = ImagePlus(still)
			if combo_dict:
				merge_and_save(combo_dict, colors, title, outputdir, opener)	
		elif multiscene:
			# If you have a multiple scene, non-timelapse image (I'm not sure how or why it would have been set up like that?), there are definitely better options out there, but this should work?
			for scene in scenes:
				title = titler(nder, name, scene)
				combo_dict = {}
				for key, chan in chans.items():
					stills = []
					still = path.join(basedir, "_".join([name, chan, "s" + str(scene) + "".join(ext)]))
					if path.isfile(still):
						still = ImagePlus(still)
						if still.getNSlices() > 1:
							still = ZProjector.run(still, "max")
							stills.append(still)
						else:
							stills.append(still)
					if stills:
						if timelapse:
							combo_dict[key] = Concatenator.run(stills)
						else:
							combo_dict[key] = ImagePlus(still)
				if combo_dict:
					merge_and_save(combo_dict, colors, title, outputdir, opener)
		else:
			title = name
			combo_dict = {}
			num_stacks = []
			for key, chan in chans.items():
				stills = []
				still = path.join(basedir, "_".join([name, chan + "".join(ext)]))
				if path.isfile(still):
					still = ImagePlus(still)
					if still.getNSlices() > 1:
						still = ZProjector.run(still, "max")
						stills.append(still)
					else:
						stills.append(still)
				if stills:
					if timelapse:
						combo_dict[key] = Concatenator.run(stills)
					else:
						combo_dict[key] = ImagePlus(still)
			if combo_dict:
				merge_and_save(combo_dict, colors, title, outputdir, opener)

metamorpher(names, chans, scenes, times, ext, colors, timelapse, multiscene, opener, nder)
=======
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
	
>>>>>>> 5a0826858ff2ad1ef736f2782cb48258a0a7df2f

gui = GenericDialog("All Done!")
gui.showDialog()

<<<<<<< HEAD
#def merge_and_save(combo_dict = combo_dict, colors = colors, title = title, outputdir = outputdir):
#	if combo_dict:
#		color_picker = []
#		for color in colors:
#			if color != "None":
#				color_picker.append(combo_dict[color])
#			elif color == "None":
#				color_picker.append(None)
#		merge = RGBStackMerge.mergeChannels(color_picker, False)
#		proj = ZProjector.run(merge, "max all")
#		out = path.join(outputdir, title)
#		del title
#		IJ.saveAs(proj, "Tiff", out)
#		rand = random.randint(1, 100)
#		if rand > 85:
#			IJ.run("Collect Garbage", "")
#		else:
#			pass
#
#def tl_logic(still, name, chan, scene, time, ext, timelapse = True, multiscene = True):
#
#	def checker(chan, still):
#		if path.isfile(still):
#			still = ImagePlus(still)
#			num_stacks.append(still.getNSlices())
#			stills.append(still)
##			combo_dict["C" + str(int(chans.index(chan) + 1))] = ImagePlus(still)
#			
#	def stiller(stills, num_stacks, timelapse):
#		if stills:
#			max_stacks = max(num_stacks)
#			for still in stills:
#				if still.getNSlices() < max_stacks:
#					bt = still.getTitle()
#					bd = str(still.getBitDepth()) + "-bit black"
#					blank = IJ.createImage(bt, bd,
#						still.getWidth(), 
#						still.getHeight(), 
#						still.getNChannels(), 
#						max_stacks,
#						still.getNFrames())
#					for i in range(0, still.getNSlices() + 1):
#						still.setSlice(i)
#						still.copy()
#						blank.setSlice(i)
#						blank.paste()
#					imp2 = blank.duplicate()
#					stills[stills.index(still)] = imp2
#			if timelapse:
#				combo_dict["C" + str(int(chans.index(chan) + 1))] = Concatenator.run(stills)
#			else:
#				combo_dict["C" + str(int(chans.index(chan) + 1))] = ImagePlus(still)
#		
#	if timelapse and multiscene:
#		for time in times:
#			still = path.join(basedir, "_".join([name, chan, "s" + str(scene), "t" + str(time) + "".join(ext)]))
#			checker(chan, still)
#			if stills:
#				max_stacks = max(num_stacks)
#				for still in stills:
#					if still.getNSlices() < max_stacks:
#						bt = still.getTitle()
#						bd = str(still.getBitDepth()) + "-bit black"
#						blank = IJ.createImage(bt, bd,
#							still.getWidth(), 
#							still.getHeight(), 
#							still.getNChannels(), 
#							max_stacks,
#							still.getNFrames())
#						for i in range(0, still.getNSlices() + 1):
#							still.setSlice(i)
#							still.copy()
#							blank.setSlice(i)
#							blank.paste()
#						imp2 = blank.duplicate()
#						stills[stills.index(still)] = imp2
#				combo_dict["C" + str(int(chans.index(chan) + 1))] = Concatenator.run(stills)
#	elif timelapse:
#		for time in times:
#			still = path.join(basedir, "_".join([name, chan, "t" + str(time) + "".join(ext)]))
#			checker(chan, still)
#	elif multiscene:
#		still = path.join(basedir, "_".join([name, chan, "s" + str(scene) + "".join(ext)]))
#		checker(chan, still)
#	else:
#		still = path.join(basedir, "_".join([name, chan + "".join(ext)]))
#		checker(chan, still)

 
#def stiller(stills, num_stacks, timelapse):
#	max_stacks = max(num_stacks)
#	for still in stills:
#		if still.getNSlices() < max_stacks:
#			bt = still.getTitle()
#			bd = str(still.getBitDepth()) + "-bit black"
#			blank = IJ.createImage(bt, bd,
#				still.getWidth(), 
#				still.getHeight(), 
#				still.getNChannels(), 
#				max_stacks,
#				still.getNFrames())
#			for i in range(0, still.getNSlices() + 1):
#				still.setSlice(i)
#				still.copy()
#				blank.setSlice(i)
#				blank.paste()
#			imp2 = blank.duplicate()
#			stills[stills.index(still)] = imp2
#	if timelapse:
#		combo_dict["C" + str(int(chans.index(chan) + 1))] = Concatenator.run(stills)
#	else:
#		combo_dict["C" + str(int(chans.index(chan) + 1))] = ImagePlus(still)

#for name in names:
#	if multiscene:
#		for scene in scenes:
#			combo_dict = {}
#			num_stacks = []
#			for chan in chans:
#				title = "_".join([name, str(scene)])
#				stills = []
#				if timelapse:
#					for time in times:
#						# Regenerate the name from defined parts -
#						still = path.join(basedir, "_".join([name, chan, "s" + str(scene), "t" + str(time) + "".join(ext)]))
#						if path.isfile(still):
#							still = ImagePlus(still)
#							num_stacks.append(still.getNSlices())
#							stills.append(still)
#					if stills:
#						max_stacks = max(num_stacks)
#						for still in stills:
#							if still.getNSlices() < max_stacks:
#								bt = still.getTitle()
#								bd = str(still.getBitDepth()) + "-bit black"
#								blank = IJ.createImage(bt, bd,
#									still.getWidth(), 
#									still.getHeight(), 
#									still.getNChannels(), 
#									max_stacks,
#									still.getNFrames())
#								for i in range(0, still.getNSlices() + 1):
#									still.setSlice(i)
#									still.copy()
#									blank.setSlice(i)
#									blank.paste()
#								imp2 = blank.duplicate()
#								stills[stills.index(still)] = imp2
#						combo_dict["C" + str(int(chans.index(chan) + 1))] = Concatenator.run(stills)
#			merge_and_save(combo_dict, colors, title, outputdir)
#		else:
#			title = name
#			combo_dict = {}
#			color_picker = []
#			stills = []
#			if timelapse:
#				for time in times:
#					# Regenerate the name from defined parts -
#					still = path.join(basedir, "_".join([name, chan, "t" + str(time) + "".join(ext)]))
#					if path.isfile(still):
#						stills.append(ImagePlus(still))
#				if stills:
#					combo_dict["C" + str(int(chans.index(chan) + 1))] = Concatenator.run(stills)
#			else:
#				still = path.join(basedir, "_".join([name, chan + "".join(ext)]))
#				if path.isfile(still):
#					combo_dict["C" + str(int(chans.index(chan) + 1))] = ImagePlus(still)
#			merge_and_save(combo_dict, colors, title, outputdir)

#	def nd_titler(nder, name, scene, title):
#		if nder:
#			if path.isfile(path.join(basedir, name + ".nd")):
#				pos_dict = {}
#				with open(path.join(basedir, name + ".nd"), "r") as nd_file:
#					for line in nd_file.readlines():
#						if line.startswith("\"Stage"):
#							pos_dict[line.split(",")[0].strip("\"\n").replace("Stage", "")] = line.split(",")[1].strip("\"\n\r ")
#				scene_name = pos_dict.get(str(scene))
#				if scene_name:
#					title += "_".join([name, scene_name])
#		else:
#			title += "_".join([name, str(scene)])

#				title = ""
#				nd_titler(nder, name, scene, title)
#				if nder:
#					if path.isfile(path.join(basedir, name + ".nd")):
#						pos_dict = {}
#						with open(path.join(basedir, name + ".nd"), "r") as nd_file:
#							for line in nd_file.readlines():
#								if line.startswith("\"Stage"):
#									pos_dict[line.split(",")[0].strip("\"\n").replace("Stage", "")] = line.split(",")[1].strip("\"\n\r ")
#						scene_name = pos_dict.get(str(scene))
#						if scene_name:
#							title = "_".join([name, scene_name])
#							print(title)
#				else:
#				if nder:
#					if path.isfile(path.join(basedir, name + ".nd")):
#						pos_dict = {}
#						with open(path.join(basedir, name + ".nd"), "r") as nd_file:
#							for line in nd_file.readlines():
#								if line.startswith("\"Stage"):
#									pos_dict[line.split(",")[0].strip("\"\n").replace("Stage", "")] = line.split(",")[1].strip("\"\n\r ")
#						if str(scene) in pos_dict:
#							scene_name = pos_dict[str(scene)]
#							title = "_".join([name, scene_name])
#							print(title)
#					else:
#						title = "_".join([name, str(scene)])
#				else:
#					title = "_".join([name, str(scene)])
	
=======
>>>>>>> 5a0826858ff2ad1ef736f2782cb48258a0a7df2f
