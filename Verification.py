import math
#m = slicer.vtkMRMLMarkupsFiducialNode()
#slicer.mrmlScene.AddNode(m)
#m.AddFiducial(-10, -40, 1111)

def addFiducialsOnCurvatureMaximums(inPath):
		'''A function to take the path of the curvatures data file, and generate slicer fiducials on the model to verify'''
		fIn = open(inPath, 'r')
		lines = fIn.readlines()
		fIn.close()
		xVals = []
		yVals = []
		zVals = []

		for x in range(1, len(lines)):
			if lines[x].strip().split(', ')[7] == 'MAX':
				xVals.append(lines[x].strip().split(', ')[2])
				yVals.append(lines[x].strip().split(', ')[3])
				zVals.append(lines[x].strip().split(', ')[4])
		m = slicer.vtkMRMLMarkupsFiducialNode()
		slicer.mrmlScene.AddNode(m)
		
		for i in range(len(xVals)):
			m.AddFiducial(float(xVals[i]), float(yVals[i]), float(zVals[i]))
			

#addFiducialsOnCurvatureMaximums(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvaturesCopyData.txt")


def generateCurve():
	coords = []
	
	for x in range(300):
		coords.append((100,x/2,math.sin(x)*8))
	
	markups = slicer.vtkMRMLMarkupsFiducialNode()
	slicer.mrmlScene.AddNode(markups)
	for i in coords:
		markups.AddFiducial(i[0], i[1], i[2])

generateCurve()