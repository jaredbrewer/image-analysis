from ij import IJ, ImagePlus
from ij.measure import ResultsTable
from ij.plugin.frame import RoiManager
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

IJ.run("Set Measurements...",
		"area mean min limit display redirect=None decimal=3")

rm = RoiManager.getRoiManager()
data = []

for f in bfiles:
	imp = IJ.openImage(f)
	proj = ZProjector.run(imp, "max all")
	proj.setC(2)
	IJ.setAutoThreshold(proj, "Otsu dark")
	IJ.run(proj, "Analyze Particles...", "size=100000.00-Infinity clear include add slice")

	if rm.getCount() > 1:
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
	IJ.setRawThreshold(proj, 170, 4095)
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

with open(path.join(basedir, "1dpi_burden.csv"), "w") as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(headings)
	for datum in data:
		writer.writerow(datum)
