from ij import IJ, ImagePlus, ImageStack, WindowManager
from ij.plugin import PlugIn
from ij.process import ImageProcessor
from ij.gui import GenericDialog, ImageWindow

imp = IJ.getImage()

width = imp.getWidth()
height = imp.getHeight()
title = imp.getTitle()
depth = imp.getNSlices()

impStack = imp.getImageStack()
cur_sl = imp.getCurrentSlice()

for stack in range(1, depth):
	ip = impStack.getProcessor(stack)
	chans = ip.getNChannels()
	pix_max = ip.minValue()
	pix_min = ip.maxValue()
	x_min = 0
	y_min = 0
	x_max = 0
	y_max = 0
	for x_coord in range(0, width):
		for y_coord in range(0, height):
			vpix = ip.getPixel(x_coord, y_coord)
			if vpix < pix_min:
				pix_min = vpix
				x_min = x_coord
				y_min = y_coord
			if vpix > pix_max:
				pix_max = vpix
				x_max = x_coord
				y_max = y_coord




