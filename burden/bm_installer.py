import sys, os, shutil
from os import path
from ij.gui import GenericDialog

print(sys.path)

if not path.isdir(sys.path[0]):
	os.mkdir(sys.path[0])

gui = GenericDialog("Macro Location: ")
gui.addFileField("Macro Path", "~/Documents")
gui.showDialog()

macro = str(gui.getNextString()) # File path to where the macro was downloaded.
base = path.basename(macro)

final_path = path.join(sys.path[0], base)

shutil.copyfile(macro, final_path)
class_path = "$".join(final_path.rsplit(".", 1)) + ".class"

if path.exists(class_path):
	os.remove(class_path)
