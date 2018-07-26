#Designed to be run throguh slicer, after you have a loaded segmentation and calculated centerlines. 
#this will check a list of fids, and cut the segmentations into 3 at two points. 
#Always place the fiducial on the ascending colon first. 

import numpy as np


def splitSegment(centerPointsNode, cutPointsNode):
	c1Pos = np.array([0,0,0])
	c2Pos = np.array([0,0,0])
	cutPointsNode.GetNthFiducialPosition(0, c1Pos)
	cutPointsNode.GetNthFiducialPosition(1, c2Pos)
	minDist = 1000000
	closestPointNum=None
	for x in range(centerPointsNode.GetNumberOfFiducials()):
		pos = np.zeros(3)
		centerPointsNode.GetNthFiducialPosition(x, pos)
		cutPointToCenterPoint = pos - c1Pos
		dist = np.linalg.norm(cutPointToCenterPoint)
		if dist < minDist:
			closestPointNum = x
			minDist = dist
	closestPointNumToCutOne = closestPointNum
	
	minDist = 1000000000000
	closestPointNum=None
	for x in range(centerPointsNode.GetNumberOfFiducials()):
		pos = np.zeros(3)
		centerPointsNode.GetNthFiducialPosition(x, pos)
		cutPointToCenterPoint = pos - c2Pos
		dist = np.linalg.norm(cutPointToCenterPoint)
		if dist < minDist:
			closestPointNum = x
			minDist = dist
	closestPointNumToCutTwo = closestPointNum
	
	
	ascendingCenterPoints = slicer.vtkMRMLMarkupsFiducialNode()
	for x in range(closestPointNumToCutOne):
		pos = np.zeros(3)
		centerPointsNode.GetNthFiducialPosition(x, pos)
		ascendingCenterPoints.AddFiducial(pos[0], pos[1], pos[2])
	slicer.mrmlScene.AddNode(ascendingCenterPoints)
	
	transverseCenterPoints = slicer.vtkMRMLMarkupsFiducialNode()
	for x in range(closestPointNumToCutOne, closestPointNumToCutTwo):
		pos = np.zeros(3)
		centerPointsNode.GetNthFiducialPosition(x, pos)
		transverseCenterPoints.AddFiducial(pos[0], pos[1], pos[2])
	slicer.mrmlScene.AddNode(transverseCenterPoints)
		
	descendingCenterPoints = slicer.vtkMRMLMarkupsFiducialNode()
	for x in range(closestPointNumToCutTwo, centerPointsNode.GetNumberOfFiducials()):
		pos = np.zeros(3)
		centerPointsNode.GetNthFiducialPosition(x, pos)
		descendingCenterPoints.AddFiducial(pos[0], pos[1], pos[2])
	slicer.mrmlScene.AddNode(descendingCenterPoints)

		
	return ascendingCenterPoints, transverseCenterPoints, descendingCenterPoints
	

def reversedFiducialNode(fidNode):
	fidCoords = []
	for x in range(fidNode.GetNumberOfFiducials()):
		pos = np.zeros(3)
		fidNode.GetNthFiducialPosition(x, pos)
		fidCoords.append(pos)
	newFids = slicer.vtkMRMLMarkupsFiducialNode()
	for x in fidCoords[::-1]:
		newFids.AddFiducial(x[0], x[1], x[2])
	return newFids
	
def splitSegmentCheckOrder(centerPointsNode, cutPointsNode):
	ac, tc, dc = splitSegment(centerPointsNode, cutPointsNode)
	if tc.GetNumberOfFiducials()==0:
		ac, tc, dc = splitSegment(reversedFiducialNode(centerPointsNode), cutPointsNode)
	return ac, tc, dc
	
def splitCenterPointsFileToFiles(cenPointsInPath):
	cutPointsInPath = cenPointsInPath[:-17]+'CutPoints.fcsv'
	
	AcOutPath = cenPointsInPath[:-17]+'AcCenterPoints.fcsv'
	TcOutPath = cenPointsInPath[:-17]+'TcCenterPoints.fcsv'
	DcOutPath = cenPointsInPath[:-17]+'DcCenterPoints.fcsv'
	

	#print(outPath)
	[success, centerPointsNode] = slicer.util.loadMarkupsFiducialList(cenPointsInPath, returnNode=True)
	[success, cutPointsNode] = slicer.util.loadMarkupsFiducialList(cutPointsInPath, returnNode=True)
	
	acNode, tcNode, dcNode = splitSegmentCheckOrder(centerPointsNode, cutPointsNode)
	
	slicer.util.saveNode(acNode, AcOutPath)
	slicer.util.saveNode(tcNode, TcOutPath)
	slicer.util.saveNode(dcNode, DcOutPath)
	
	
	
#splitCenterPointsFileToFiles(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCenterPoints.fcsv")
	
	
	
	
	
	
	
	
	