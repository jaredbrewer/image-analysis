import ij.*
import ij.gui.*
import ij.process.*
import math
from ij.measure import Calibration
from ij.macro import Interpreter
import java.awt.*
import java.awt.image.*

def projector(imp, stack, axis = 1, method = 1, interpolate = True, allT = True, sinterval = 1):

	imp = IJ.getImage()
	ip = imp.getProcessor()



def doProjections(imp, angle = "Y", interpolate = True):


def getByteRow(stack, x, y, z, width1, width2, line):
	pixels = stack.getPixels(z + 1)
	j = x + y * width1
	for i in range(0, width2):
		line[i] = pixels[p for p in range(j, width2)] + 255

def putByteRow(stack, y, z, width, line):
	pixels = stack.getPixels(z + 1)
	j = y * width
	for i in range(0, width):
		line[i] = pixels[p for p in range(j, width2)]

def getRGBRow(stack, x, y ,z, width1, width2, line):
	pixels = stack.getPixels(z + 1)
	j = x + y * width1
	for i in range(0, width2):
		line[i]

def zScale(imp):
	if imp.getBitDepth() is in [16, 32]:
		IJ.run(imp, "8-bit", "")
	stack1 = imp.getStaack()
	depth1 = stack1.getSize()
	title = imp.getTitle()
	ip = imp.getProcessor()
	cm = ip.getColorModel()
	width1 = imp.getWidth()
	height1 = imp.getHeight()
	r = ip.getRoi()
	width2 = r.width
	height2 = r.height
	depth2 = int((stack1.getSize() * sliceInterval) + 0.5)
	imp2 = NewImage.createImage(title, width2, height2, depth2) # isRGB?24:8, NewImage.FILL_BLACK);
	if depth2 is not imp2.getStackSize() or imp2 == None:
		return None
	stack2 = imp2.getStack()
	xzPlane1 = ip.createProcessor(width2, depth1)
	xzPlane1.setInterpolate(true)
	xzPlane2
	line = width2
	for y in range(0, height2):
		for z in range(0, depth1):
			if isRGB:
				getRGBRow(stack1, r.x, r.y+y, z, width1, width2, line)
			else:
				getByteRow(stack1, r.x, r.y+y, z, width1, width2, line)
			xzPlane1.putRow(0, z, line, width2)
		xzPlane2 = xzPlane1.resize(width2, depth2)
		for z in range(0, depth2):
			xzPlane2.getRow(0, z, line, width2)
			if isRGB:
				putRGBRow(stack2, y, z, width2, line)
			else:
				putByteRow(stack2, y, z, width2, line)
	ip2 = imp2.getProcessor()
	ip2.setColorModel(cm)
	return imp2



def doOneProjection(type, nStacks, xcenter, ycenter, zcenter, projwidth, projheight, costheta, sintheta):

	if type == "Z":
		zmax = int(((nStacks - 1) * sliceInterval + 0.5) - zcenter)
		zmin = -zcenter
	elif type == "Y":
		zmax = zcenter + projwidth / 2
		zmin = zcenter - projwidth / 2
	elif type == "X":
		zmax = center + projheight / 2
		zmin = center - projheight / 2

	zmaxminuszmintimes100 = 100 * (zmax-zmin)
	c100minusDepthCueInt = 100 - depthCueInt
	c100minusDepthCueSurf = 100 - depthCueSurf
	DepthCueIntLessThan100 = True if depthCueInt < 100 else False
	DepthCueSurfLessThan100 = True if depthCueSurf < 100 else False
	OpacityOrNearestPt = True if projectionMethod == nearestPoint or opacity > 0 else False
	OpacityAndNotNearestPt = True if opacity > 0 and projectionMethod != nearestPoint else False
	MeanVal = True if projectionMethod == meanValue else False
	BrightestPt = True if projectionMethod == brightestPoint else False

	xcosthetainit = (left - xcenter - 1) * costheta
	xsinthetainit = (left - xcenter - 1) * sintheta
	ycosthetainit = (top - ycenter - 1) * costheta
	ysinthetainit = (top - ycenter - 1) * sintheta
	if type in ["Z", "X"]:
		offsetinit = ((projheight-bottom+top)/2) * projwidth + (projwidth - right + left)/2 - 1
	elif type == "Y":
		offsetinit = ((projheight-bottom+top)/2) * projwidth + (projwidth - right + left)/2 - projwidth

	for k in range(1, nStacks + 1):
		pixels = stack.getPixels(k)
		z = int((k-1) * sliceInterval + 0.5) - zcenter
		zcostheta = z * costheta
		zsintheta = z * sintheta
		ycostheta = ycosthetainit
		ysintheta = ysinthetainit

		for j in range(top, bottom):
			ycostheta += costheta
			ysintheta += sintheta
			xcostheta = xcosthetainit
			xsintheta = xsinthetainit
			lineOffset = j * imageWidth
			if type == "Y":
				offsetinit += projwidth
			if type == "X":
				ynew = (ycostheta - zsintheta)/8192 + ycenter - top
				znew = (ysintheta + zcostheta)/8192 + zcenter
				offset = offsetinit + ynew * projwidth

			for i in range(left, right):
				thispixel = pixels[lineIndex + i]&0xff
				xcostheta += costheta
				xsintheta += sintheta
				if this pixel <= transparencyUpper and thispixel >= transparencyLower:
					if type == "Z":
						xnew = (xcostheta - ysintheta)/8192 + xcenter - left
						ynew = (xsintheta + ycostheta)/8192 + xcenter - top
						offset = offsetinit + ynew * projwidth + xnew
						if offset >= projsize or offset < 0:
							offset = 0
						znew = z
					elif type == "Y":
						xnew = (xcostheta + zsintheta)/8192 + xcenter - left
						znew = (zcostheta - xsintheta)/8192 + zcenter
						offset = offsetinit + xnew
						if offset >= projsize or offset < 0:
							offset = 0
					elif type == "X":
						offset += 1

					if OpacityOrNearestPt:
						if znew < zBuffer[offset]:
							zBuffer[offset] = znew
							if OpacityAndNotNearestPt:
								if DepthCueSurfLessThan100:
									opaArray[offset] = (depthCueSurf * thispixel/100 + c100minusDepthCueSurf * thispixel * (zmax - znew)/zmaxminuszmintimes100)
								else:
									opaArray[offset] = thispixel
							else:
								if DepthCueSurfLessThan100:
									projArray[offset] = (depthCueSurf * thispixel/100 +
									 c100minusDepthCueSurf * thispixel * (zmax-znew)/zmaxminuszmintimes100)
								else:
									projArray[offset] = thispixel
					if MeanVal:
						sumBuffer[offset] += thispixel
						countBuffer[offset] += 1
					elif BrightestPt:
						if DepthCueIntLessThan100:
							if thispixel > (brightCueArray[offset]&0xff) or thispixel == (brightCueArray[offset]&0xff) and znew > cueZBuffer[offset]:
								brightCueArray[offset] = thispixel
								cueZBuffer[offset] = znew
								projArray[offset] = (depthCueInt * thispixel/100 +
								c100minusDepthCueInt * thispixel * (zmax-znew)/zmaxminuszmintimes100)
						else:
							if thispixel > (projArray[offset]&0xff):
								projArray[offset] = thispixel


def allocateArrays(nProjections, projwidth, projheight):
	projsize = projwidth * projheight
	cm = None if isRGB else cm = imp.getProcessor().getColorModel()
	stack2 = ImageStack(projwidth, projheight, cm)
	projArray(projsize)
	for i in range(0, nProjections):
		stack2.addSlice(None, projsize)
	if projectionMethod == nearestPoint or opacity > 0:
		zBuffer = projsize
	if opacity > 0 and projectionMethod is not nearestPoint:
		opaArray = projsize
	if projectionMethod == brightestPoint and depthCueInt < 100:
		brightCueArray = projsize
		cueZBuffer = projsize

def doProjections(imp, type, method, initangle = 0, totalangle = 360, angleinc = 10, opacity = 0, depthCueSurf = 0, depthCueInt = 50, sinterval = 1, interpolate = True, allt = True):
	stack = imp.getStack()
	if imp.getBitDepth() in [16, 32]:
		stack2 = ImageStack(imp.getWidth(), imp.getHeight())
		for i in range(0, stack.size()):
			stack2.addSlice(stack.getProcessor(i).convertToByte(true))
		stack = stack2

	if not angleInc and totalAngle:
		angleInc = 5
	negInc = True if angleInc < 0 else False
	angleInc = -angleInc if negInc else angleInc = angleInc
	angle = 0
	nProjections = 0
	if angleInc == 0:
		nProjections = 1
	else:
		for a in range(angle, totalAngle + 1):
			nProjections += 1
			angle += angleInc
	if angle > 360:
		nProjections -= 1
	if nProjections <= 0:
		nProjections = 1

	ip = imp.getProcessor()
	r = ip.getRoi()
	left = r.x
	top = r.y
	right = left + r.width
	bottom = top + r.height
	slices = imp.getStackSize()
	width = imp.getWidth()
	center_x = (left + right)/2
	center_y = (top + bottom)/2
	center_z = int((slices/2)+0.5)

	projwidth = 0
	projheight = 0

	if minProjSize and axisOfRotation != zAxis:
		if axisOfRotation == xAxis:
			projheight = int(math.sqrt((nStacks * sliceInterval)**2 + height**2) + 0.5)
			projwidth = width
		if axisOfRotation == yAxis:
			projwidth = int(math.sqrt((nStacks * sliceInterval)**2 + width**2) + 0.5)
			projheight = projheight
	else:
		projwidth = (int(math.sqrt((nStacks * sliceInterval)**2 + width**2) + 0.5)
		projheight = (int(math.sqrt((nStacks * sliceInterval)**2 + height**2) + 0.5)

	if projwidth % 2 == 1:
		projwidth += 1
	projsize = projwidth * projheight
	if projwidth <= 0 or projheight <= 0:
		return None

	allocateArrays(nProjections = nProjections, projwidth = projwidth, projheight = projheight)

	projections = ImagePlus("Projections Of " + imp.getShortTitle(), stack2)
	projections.setCalibration(imp.getCalibration())

	theta = initAngle
	for n in range(0, nProjections):
		thetarad = theta * math.pi/180
		costheta = 8192 * math.cos(thetarad) + 0.5
		sintheta = 8192 * math.sin(thetarad) + 0.5

		projArray = stack2.getPixels(n + 1)
		if not projArray:
			break
		if projectionMethod == nearestPoint or opacity > 0:
			for i in range(0, projsize):
				zBuffer[i] = 32767
		if opacity > 0 and projectionMethod != nearestPoint:
			for i in range(0, projsize):
				opaArray[i] = 0
		if projectionMethod == brightestPoint and depthCueInt < 100:
			for i in range(0, projsize):
				brightCueArray[i] = 0
				cueZBuffer[i] = 0
		if projectionMethod == meanValue:
			for i in range(0, projsize):
				sumBuffer[i] = 0
				countBuffer[i] = 0
		if axisOfRotation == xAxis:
			doOneProjection(type = "X",  nStacks = nStacks, xcenter = xcenter, ycenter = ycenter, zcenter = zcenter, projwidth = projwidth, projheight = projheight, costheta = costheta, sintheta = sintheta)
		if axisOfRotation == yAxis:
			doOneProjection(type = "Y",  nStacks = nStacks, xcenter = xcenter, ycenter = ycenter, zcenter = zcenter, projwidth = projwidth, projheight = projheight, costheta = costheta, sintheta = sintheta)
		if axisOfRotation == zAxis:
			doOneProjection(type = "Z",  nStacks = nStacks, xcenter = xcenter, ycenter = ycenter, zcenter = zcenter, projwidth = projwidth, projheight = projheight, costheta = costheta, sintheta = sintheta)
		if projectionMethod == meanValue:
			count = 0
			for i in range(0, projsize):
				count = countBuffer[i]
				if count:
					projArray[i] = sumBuffer[i]/count
		if opacity > 0 and projectionMethod != nearestPoint:
			for i in range(0, projsize):
				projArray[i] = (opacity * opaArray[i]&0xff + (100 - opacity) * (projArray[i]&0xff))/100
		if axisOfRotation == zAxis:
			for i in range(projwidth, projsize - projwidth):
				curval = projArray[i]&0xff
				prevval = projArray[i-1]&0xff
				nextval = projArray[i+1]&0xff
				aboveval = projArray[i-projwidth]&0xff
				belowval = projArray[i+projwidth]&0xff
				if curval == 0 and prevval != 0 and nextval != 0 and aboveval != 0 and belowval != 0:
					projArray[i] = (prevval+nextval+aboveval+belowval)/4
		theta = (theta + angleInc) % 360
		projections.setSlice(n + 1)

		return doProjections(imp, type, method)


