from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin.frame import RoiManager
from ij.process import AutoThresholder
from ij.plugin import ZProjector
from ij.gui import GenericDialog
import os, random, csv, sys
from os import path

def burden(directory, chan, min_threshold, ext, screen_threshold = "Otsu", proj_save = False, proj_show = False, imp_show = False, fish_channel = None, outline_threshold = "Triangle", brightfield = False, subset = None, man_psize = 100000):

# directory is a string with path to the files you wish to analyze.
# chan is an integer of the channel # with the bacteria.
# min_threshold is an integer of the minimum threshold value (empirically determined by checking a few images)
# ext is the file extension (".czi", ".lsm", ".tif" are some examples) as a string
# screen_threshold is the threshold algorithm to find the yolk as a string. I found that "Otsu dark" works well, but others may be better in other circumstances.
# proj_save is a boolean that determines whether or not to save the MIPs as you go.
# proj_show is a boolean to determine whether to show the MIPs as they are processed. A bit memory intensive, but valuable for sanity checking.
# imp_show is a boolean for whether or not to show the source image (not recommended except with small datasets)
# fish_channel is an integer for the channel containing something we could use as the basis for an outline of the fish.
# outline_threshold is a string with the thresholding algorithm to find the whole fish (you want something generous, but probably not MinError or similar).
# brightfield is a boolean telling whether or not the selected fish_channel is the brightfield channel. This can be useful and very convenient, but requires some additional processing to be useful.
# subset is to run the function over a subset of the total number of images. Provide an integer value less than the total number of images in the directory. If subset is selected, the projections will automatically show.
# man_psize is a manual particle size value for the "Analyze Particles..." function. Default has worked well for me, but can be changed if needed.

	filenames = os.listdir(str(directory))
	bfiles = []

	if not ext.startswith("."):
		# Rigid binding of extension per se.
		ext = "." + ext
	for files in filenames:
		if files.endswith(str(ext)):
			file = path.join(str(directory), files)
			bfiles.append(file)

	# Make sure all our measurements are set properly.
	IJ.run("Set Measurements...",
	"area mean min limit display redirect=None decimal=3")

	rm = RoiManager.getRoiManager()
	data = []


	if subset > len(bfiles):
		print("The subset is greater than the number of files - running on whole directory.")
		subset = None
	if subset:
		bfiles = bfiles[0:int(subset)]
		proj_show = True

	valid_thresholds = []
	for i in AutoThresholder.Method.values():
		valid_thresholds.append(str(i))

	if screen_threshold not in valid_thresholds:
		screen_threshold = "Otsu"
	if screen_threshold == "Try all":
		IJ.run(imp, "Auto Threshold", "method=[Try all]")
	if outline_threshold not in valid_thresholds:
		outline_threshold = "Triangle"
	if outline_threshold == "Try all":
		IJ.run(imp, "Auto Threshold", "method=[Try all]")

	if screen_threshold or outline_threshold == "Try all":
		sys.exit(0)

	for f in bfiles:

		imp = IJ.openImage(f)
		if imp_show:
			imp.show()
		proj = ZProjector.run(imp, "max all")
		if proj_show:
			proj.show()
		proj.setC(int(chan))
		IJ.setAutoThreshold(proj, str(screen_threshold))
		IJ.run(proj, "Analyze Particles...", "size="+man_psize+".00-Infinity clear include add slice")

		if rm.getCount() > 1: # This is the dumbest source of a downstream error I have ever encountered. rm.getCount is an attribute and rm.getCount() is a method = two different outcomes, but no evaluation error.
			rm.runCommand(proj, "Select All")
			rm.runCommand(proj, "Combine")
			rm.runCommand(proj, "Delete")
			rm.runCommand(proj, "Add")

		rm.select(proj, 0)

		IJ.run(proj, "Clear", "slice")
		IJ.run(proj, "Select None", "")
		IJ.run(proj, "Remove Overlay", "")
		rm.reset()

		# Build some logic for using the outline of the fish if provided. Brightfield images probably need even more work, but this will *probably* work for fluorescent channels.
		if fish_channel:
			proj.setC(int(fish_channel))
			if brightfield:
				IJ.run(proj, "Invert", "slice")
			IJ.setAutoThreshold(proj, outline_threshold)
			IJ.run(proj, "Analyze Particles...", "size="man_psize".00-Infinity clear include add slice")
			proj.setC(int(chan))
			ra = rm.getRoisAsArray()
			for r in ra:
				rm.addRoi(r)
			if rm.getCount() > 1:
				rm.runCommand(proj, "Select All")
				rm.runCommand(proj, "Combine")
				rm.runCommand(proj, "Delete")
				rm.runCommand(proj, "Add")
			rm.select(proj, 0)

		if not fish_channel:
			IJ.run(proj, "Select All", "")
		IJ.setRawThreshold(proj, int(min_threshold), 2**int(proj.getBitDepth()) - 1)
		IJ.run(proj, "Measure", "")
		rt = ResultsTable.getResultsTable()
		row = rt.getRowAsString(0).split("\t")
		headings = rt.getColumnHeadings().split("\t")
		data.append(row)

		if not imp_show:
			imp.close()
		if not proj_show:
			proj.close()

		if proj_save:
			out = path.join(directory, proj.getTitle())
			IJ.saveAs(proj, "Tiff", out)

		rand = random.randint(1, 100)
		if rand > 85:
			IJ.run("Collect Garbage", "")
		else:
			pass

	with open(path.join(directory, "burden.csv"), "w") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(headings)
		for datum in data:
			writer.writerow(datum)

	gui = GenericDialog("All Done! Output is located in " + directory)
	gui.showDialog()
