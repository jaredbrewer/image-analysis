[![DOI](https://zenodo.org/badge/521425912.svg)](https://zenodo.org/badge/latestdoi/521425912)

# Image Analysis Scripts in Jython for FIJI/ImageJ

This is a general purpose repository of Python language image analysis scripts for use in the Jython interpreter in FIJI/ImageJ. Where appropriate, I will also endeavor to included data analysis scripts in R. I will upload sets of things that will hopefully prove both user-friendly and generally useful to others. What is published here appears to work for my unique use-case, but may require some modifications or generalizations for other uses. Open to any pull requests with function extensions, enhancements, or optimizations.

## MIPS

These scripts are meant to be used to more rapidly generate maximum-intensity projections from Z-dimensional images. The __bulkMIPper.py__ file will take an input directory and perform maximum intensity projection on the entire directory of pattern-matched files. This will work best with a directory that only has the files of interest in it; however, bystander files are okay as long as they do not have the same file extension as the files of interest.

The __manMIPper.py__ is a convenience script that minimizes mouse clicks required to perform a maximum-intensity projection of custom top and bottom positions. Simply input the desired first and last slices and the macro will run and save the file in the original file directory. This is best if there are extraneous slices that reduce your final image quality or you would like to inspect the images prior to processing.

__fast_manMIPper.py__ is a lightweight implementation of __manMIPper.py__. Rather than requiring a library of open images, it opens them one at a time and queries user engagement prior to loading the subsequent image. This is great for low-memory settings. It also includes logic to check if the MIP already exists in the output folder and, if so, passes on to the next one. This may be the preferred method for most people, except in cases where image loading time is a greater bottleneck than memory itself.

__reSlicer.py__ is a Python translation of the built-in Slice Keeper and Slice Remover functions and can be called with sliceKeeper(imp, first, last, inc) and sliceRemover(imp, first, last, inc). The objective was to make these functions object-oriented and readily callable in a programmatic way. The hope is that this can simplify more precise logging by feeding first/last positions used to generate MIPs into a program that can then slice and save the Z positions used to generate the MIP while discarding less useful (out of focus, usually) data.

## Surface Plot

These scripts are built around the use of the [3D Surface Plot](https://github.com/fiji/Interactive_3D_Surface_Plot) plugin included in FIJI and ImageJ. Input was optimized for high-magnification images of individual cells. Both __autoIsolator.py__ and __manIsolator.py__ are meant to facilitate the pre-processing needed to input a set of images into the plugin. The objective is to use a generalist channel to create cellular outlines (something broadly present in the cytoplasm, for instance; in our instance, this was β-actin) and then use that as a mask for a more specific image you wish to interrogate (some more central or peripherally located protein). The mask is applied, the exterior of the mask is cleared, and the image is ready for input into the 3D Surface Plot plugin (which is not conducive to full automation if you need to manually find the maximum X dimension). The desired output from the 3D Surface Plot is a 2D plot of a cell along the longest X axis with Z in the Y direction (essentially a side-long or *horizon*tal view of the cell), smoothed to some consistent degree (we used 8.5, but any is acceptable with good rationale and consistent application), with axes removed and on a black background. This will allow for ready profiling in the downstream script (__surfacePlotMeasure.py__).

3D Surface Plot includes string parameters that allow for some automation; one could for instance place this script in a for loop to open all of the needed plots at once (depending on available memory and FIJI's handling of an arbitrary number of instances of 3D Surface Plot). However, the following code will open 3D Surface Plot with all the needed settings; use of the axes to guide the image into place and then turning them back off is extremely useful (switch drawAxes=0 to drawAxes=1).

```
from ij import IJ, ImagePlus

imp = IJ.getImage()
IJ.run(imp, "3D Surface Plot",
	'''plotType=1
	colorType=3
	drawAxes=0
	drawLines=0
	drawText=0
	grid=256
	drawLegend=0
	smooth=8.5
	backgroundColor=000000
	windowHeight=600
	windowWidth=720''')
```

__manSurfacePlotMeasure.py__ and __autoSurfacePlotMeasure.py__ take the 2D XZ images from 3D Surface Plot and captures all the bit-wise >0 points on the plot and saves them to a CSV file. It will do this for either an entire directory of images (perhaps best from __autoIsolator.py__) or individual images (__manIsolator.py__) and save the output to a .csv file. These .csv files can then be interpreted using the included __surface_plot_analsis.R__ script (although a Python interpretation is certainly possible).

surface_plot_analysis.R will take the directory of .csv files and process them to calculate area under the curve along the provided interval. This is useful for an application where you expect more central or distal distribution of a particular protein or other cellular feature. Other types of output and analysis are certainly possible from this data, although these have not yet been explored.

## Composites

One of the more click-intensive tasks in FIJI is the process of creating composite images from a set of individual color channels and these tools are meant as templates for implementing this logic in your own pipelines. They take folders of individual channels and then generate a LUT-keyed composite image from them. Some of the internal variables need to be edited in order to provide the results desired - for instance, the default merge is for 3 channels, but the function accepts up to 7 channels. I have, however, attempted to remove as much manual intervention as possible through string matching. One of the great things about ImageJ is the way it creates regularly patterned names for new files - the expected input for these scripts is the output of the "MIPS" scripts, but any set of channels will theoretically work with minor tweaking.
