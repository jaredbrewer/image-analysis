# Image Analysis Scripts in Jython for FIJI/ImageJ

This is a general purpose repository of Python language image analysis scripts for use in the Jython interpreter in FIJI/ImageJ. I will upload sets of things that will hopefully prove both user-friendly and generally useful to others. What is published here appears to work for my unique use-case, but may require some modifications or generalizations for other uses. Open to any pull requests with function extensions, enhancements, or optimizations.

## MIPS

These scripts are meant to be used to more rapidly generate maximum-intensity projections from Z-dimensional images. The bulkMIPper.py file will take an input directory and perform maximum intensity projection on the entire directory of pattern-matched files. This will work best with a directory that only has the files of interest in it; however, bystander files are okay as long as they do not have the same file extension as the files of interest. 

The manMIPper.py is a convenience script that minimizes mouse clicks required to perform a maximum-intensity projection of custom top and bottom positions. Simply input the desired first and last slices and the macro will run and save the file in the original file directory. This is best if there are extraneous slices that reduce your final image quality or you would like to inspect the images prior to processing. 

## Surface Plot

These scripts are built around the use of the [3D Surface Plot](https://github.com/fiji/Interactive_3D_Surface_Plot) plugin included in FIJI and ImageJ. Input was optimized for high-magnification images of individual cells. Both autoIsolator.py and manIsolator.py are meant to facilitate the pre-processing needed to input a set of images into the plugin. The objective is to use a generalist channel to create cellular outlines (something broadly present in the cytoplasm, for instance) and then use that as a mask for a more specific image you wish to interrogate. The mask is applied, the exterior of the mask is cleared, and the image is ready for input into the 3D Surface Plot plugin (which is not conducive to automation). The desired output from the 3D Surface Plot is a 2D plot of a cell along the longest X axis with Z in the Y direction (essentially a side-long view of the cell), smoothed to some consistent degree, with axes removed and on a black background. This will allow for ready profiling in the downstream script (surfacePlotMeasure.py).

manSurfacePlotMeasure.py and autoSurfacePlotMeasure.py take the 2D XZ images from 3D Surface Plot and captures all the bit-wise >0 points on the plot and saves them to a CSV file. It will do this for either an entire directory of images (perhaps best from autoIsolator.py) or individual images (manIsolator.py) and save the output to a .csv file. These .csv files can then be interpreted using the included surface_plot_analsis.R script (although a Python interpretation is certainly possible). 

surface_plot_analysis.R will take the directory of .csv files and process them to calculate area under the curve along the provided interval. This is useful for an application where you expect more central or distal distribution of a particular protein or other cellular feature. Other types of output and analysis are certainly possible from this data, although these have not yet been explored.

## Composites
