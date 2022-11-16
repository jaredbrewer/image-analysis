from ij import IJ, ImagePlus, ImageStack
from ij.process import ImageProcessor
from mcib_plugins import Manager3D
import csv

imp = IJ.getImage()

def min_max(imp):

	width = imp.getWidth()
	height = imp.getHeight()
	title = imp.getTitle()
	depth = imp.getNSlices()

	impStack = imp.getImageStack()

	pix_vals = []

	for stack in range(1, depth):
		ip = impStack.getProcessor(stack)
	#	chans = ip.getNChannels()
		for x_coord in range(0, width):
			for y_coord in range(0, height):
				vpix = ip.getPixel(x_coord, y_coord)
				if vpix:
					pix_vals.append(vpix)

	maxp = max(pix_vals)
	minp = min(pix_vals)

	return [minp, maxp]

pixel_width = [num for num in range(0, imp.getWidth() - 1)]
pixel_height = [num for num in range(0, imp.getHeight() - 1)]
pixel_slice = [num for num in range(1, imp.getNSlices() + 1)]
pixel_values = [num for num in range(1, min_max(imp)[1])]

cells = []

impStack = imp.getImageStack()

for stack in pixel_slice:
	ip = impStack.getProcessor(stack)
	for y_coord in pixel_height:
		for x_coord in pixel_width:
			for pv in pixel_values:
				body = ip.getPixel(x_coord, y_coord)
				if int(body) == int(pv):
					pvs = [pv, [x_coord, y_coord, stack]]
					with open("/Users/jared/Downloads/analysis_for_Jared/pixels.csv", "a") as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow(pvs)

#with open("/Users/jared/Downloads/analysis_for_Jared/pixels.csv", "w") as csvfile:
#	writer = csv.writer(csvfile)
#	writer.writerows(cells)

#		if ip.getPixel(284, y_coord) > 0:
#			print(y_coord, stack)

#		for x_coord in pixel_width:
#			for pv in pixel_values:
#				if imp.getPixel(x_coord, y_coord) == int(pv):
#					pvs = [pv, [x_coord, y_coord, stack]]
#					print(pvs)
#					cells.append(pvs)
#
#print(cells[:5])



