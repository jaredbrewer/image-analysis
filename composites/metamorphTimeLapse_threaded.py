from ij import IJ, ImagePlus
from ij.plugin import ZProjector, RGBStackMerge, Concatenator, Duplicator
from ij.gui import GenericDialog, NonBlockingGenericDialog
from ij.util import ThreadUtil
import os, sys, random, re
from os import path
from threading import Thread

gui = GenericDialog("Metamorph File Compiler")
gui.addMessage("Version 0.3a, 15 February 2023")
gui.addDirectoryField("Files Directory: ", "~/Documents")
gui.addCheckbox("Multiple Scenes?", True)
gui.addCheckbox("Multiple Time Points?", True)
gui.addCheckbox("Show Merged Image?", False)
gui.addCheckbox("Use Scenes Metadata from .nd File?", False)

gui.showDialog()

basedir = str(gui.getNextString())
multiscene = gui.getNextBoolean()
timelapse = gui.getNextBoolean()
opener = gui.getNextBoolean()
nder = gui.getNextBoolean()

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
for key, value in chan_dict.items():
	if key not in colors:
		del chan_dict[key]

chans = chan_dict

# I really have to break this entire script down to figure out how to best incorporate multithreading. The advantages are huge, if well managed, and disastrous if done poorly.

def metamorpher(names, chans, scenes, times, ext, colors, timelapse = True, multiscene = True, opener = False, nder = False):

	class ConciseResult(Thread):
		def run(self):
			self.result = self._target(*self._args, **self._kwargs)

	def clearmem():
		avail = (float(IJ.currentMemory())/float(IJ.maxMemory()))*100
		if avail > 85:
			IJ.run("Collect Garbage", "")
		else:
			pass

	def titler(nder, name, scene):
		if nder:
			if path.isfile(path.join(basedir, name + ".nd")):
				pos_dict = {}
				with open(path.join(basedir, name + ".nd"), "r") as nd_file:
					for line in nd_file.readlines():
						if line.startswith("\"Stage"):
							pos_dict[line.split(",")[0].strip("\"\n").replace("Stage", "")] = line.split(",")[1].strip("\"\n\r ")
				if str(scene) in pos_dict:
					scene_name = pos_dict.get(str(scene))
					title = "_".join([name, scene_name])
		else:
			title = "_".join([name, str(scene)])
		return title

	def stiller(timelapse, combo_dict, name, chan, times, key, scene = "scene"):

		def projector(time, still):
			imp = ImagePlus(still)
			if imp.getNSlices() > 1:
				proj = ZProjector.run(imp, "max")
				return proj
			else:
				return imp

		if timelapse:
			thread_dict = {}
			time_dict = {}
			for time in times:
				still = path.join(basedir, "_".join([name, chan, "s" + str(scene), "t" + str(time) + "".join(ext)]))
				if path.isfile(still):
					thread = ConciseResult(target = projector, args = (time, still))
					thread_dict[int(time)] = thread
			for thread in thread_dict.values():
				thread.start()
			for time, thread in thread_dict.items():
				thread.join()
				time_dict[int(time)] = thread.result
			if time_dict:
				stills = []
				for time, proj in sorted(time_dict.items()):
					stills.append(proj)
				cat = Concatenator.run(stills)
				return cat
		else:
			still = path.join(basedir, "_".join([name, chan, "s" + str(scene) + "".join(ext)]))
			if path.isfile(still):
				if still.getNSlices() > 1:
					thread = ConciseResult(target = projector, args = (time, still))
					thread.start()
					thread.join()
					still = thread.result
					cat = ImagePlus(still)
					return cat

	def merge_and_save(combo_dict, colors, title, outputdir, opener):
		color_picker = []
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

	# The central question here is how to best implement an intelligent threading model -- this seems compelling but may not be perfect and should be reevaluated pretty aggressively if we want to eek out the maximum performance.
	def threader(main_dict, name, chans, scenes, nder):
		for scene in scenes:
			thread_dict = {}
			combo_dict = {}
			title = titler(nder, name, scene)
			for key, chan in chans.items():
				thread = ConciseResult(target = stiller, args = (timelapse, combo_dict, name, chan, times, key, scene))
				thread_dict[key] = thread
			main_dict[title] = thread_dict
			# We now have a dictionary of dictionaries: A main dictionary with keys as scene titles and values containing a dictionary with channels and their associated unique threads.
		combos = {}
		for title, threads in main_dict.items():
			chan_dict = {}
			for channel, thread in threads.items():
				thread.start() # A quirk of the Jython threading model is that you need to start all of the threads before joining them for best performance.
			for channel, thread in threads.items():
				thread.join()
				chan_dict[channel] = thread.result
				 # This is why we needed a custom Thread class, to have it return a result that we could use.
				clearmem()
				# We need some sort of memory management model, but it is difficult to decide where to put it. Realistically, the best performance is going to be flying as close to the sun as possible with memory usage but backing off when needed. This threaded model is only going to be good on very high memory systems, otherwise the single-threaded version will probably outperform and be much more reliable.
			combos[title] = chan_dict
		for title, combo_dict in combos.items():
			merge_and_save(combo_dict, colors, title, outputdir, opener)

	for name in names:
		main_dict = {}
		if multiscene:
			threader(main_dict, name, chans, scenes, nder)
		else:
			# Threading does not seem overly beneficial in a single stage position time lapse -- you could in theory parallelize the channels but the real-world benefit seems pretty small.
			title = name
			combo_dict = {}
			for key, chan in chans.items():
				stiller(timelapse, combo_dict, name, chan, times, scene)
			if combo_dict:
				merge_and_save(combo_dict, colors, title, outputdir, opener)
		clearmem()

metamorpher(names, chans, scenes, times, ext, colors, timelapse, multiscene, opener, nder)

gui = GenericDialog("All Done!")
gui.showDialog()
