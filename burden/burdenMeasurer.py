from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin.frame import RoiManager
from ij.plugin import ZProjector
from ij.gui import GenericDialog
import os, random, csv
from os import path

def burden(directory, chan, min_meas_thres, ext = ".czi", screen_thres = "Otsu dark"):

	filenames = os.listdir(str(directory))
	bfiles = []

	if not ext.startswith("."):
		ext = "." + ext
	for files in filenames:
		if files.endswith(str(ext)):
			file = path.join(str(directory), files)
			bfiles.append(file)

	IJ.run("Set Measurements...",
	"area mean min limit display redirect=None decimal=3")

	rm = RoiManager.getRoiManager()
	data = []

	for f in bfiles:

		imp = IJ.openImage(f)
		proj = ZProjector.run(imp, "max all")
		proj.setC(int(chan))
		IJ.setAutoThreshold(proj, str(screen_thres))
		IJ.run(proj, "Analyze Particles...", "size=100000.00-Infinity clear include add slice")

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

		IJ.run(proj, "Select All", "")
		IJ.setRawThreshold(proj, int(min_meas_thres), 2**int(proj.getBitDepth()) - 1)
		IJ.run(proj, "Measure", "")
		rt = ResultsTable.getResultsTable()
		row = rt.getRowAsString(0).split("\t")
		headings = rt.getColumnHeadings().split("\t")
		data.append(row)

		imp.close()
		proj.close()

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
