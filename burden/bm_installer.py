from ij import IJ
import sys, os, shutil
from os import path
from ij.gui import GenericDialog, NonBlockingGenericDialog

if not path.isdir(sys.path[0]):
	os.mkdir(sys.path[0])

finder = path.join(path.dirname(path.realpath(__file__)), "burdenMeasurer.py")
func = path.join(path.dirname(path.realpath(__file__)), "burden.py")

if not os.path.exists(finder):
	print("This script and the burden measurement scripts need to be in the same folder!")
	sys.exit(0)
if not os.path.exists(func):
	print("This script and the burden measurement scripts need to be in the same folder!")
	sys.exit(0)

base = path.basename(func)
final_path = path.join(sys.path[0], base)

shutil.copyfile(func, final_path)
class_path = "$".join(final_path.rsplit(".", 1)) + ".class"

if path.exists(class_path):
	os.remove(class_path)

plugin_path = path.join(os.getcwd(), "plugins", "Burden")
if not path.isdir(plugin_path):
	os.mkdir(plugin_path)

plugin_put = path.join(plugin_path, "Measure_Burden.py")
shutil.copyfile(finder, plugin_put)

gui = NonBlockingGenericDialog("Quit?")
gui.addMessage("FIJI/ImageJ needs to quit to add menu items. Quit now?")
gui.setOKLabel("Quit now")
gui.setCancelLabel("Quit later")

gui.showDialog()

if gui.wasOKed():
	IJ.run("Quit")
elif gui.wasCanceled():
	pass
