#####Centerpoints from file-------------------------------------------------------
	
	
def centerPointsFromFile(patPath, mode):
	print('Connected')
	
	#get patient id and make possible paths
	patId = patPath[-8:]
	supSegPath = patPath + "\\" + patId + "_SupSeg.seg.nrrd"
	proSegPath = patPath + "\\" + patId + "_ProSeg.seg.nrrd"
	leftDownSegPath = patPath + "\\" + patId + "_LeftDownSeg.seg.nrrd"
	logging.info(patId)
	
	
	if mode == 'sup':
		segName = patId+"_SupSeg"
		[success, segNode] = slicer.util.loadSegmentation(supSegPath, returnNode = True)
		logging.info("Loaded: "+supSegPath)
	elif mode == 'ld':
		segName = patId+"_LeftDownSeg"
		[success, segNode] = slicer.util.loadSegmentation(leftDownSegPath, returnNode = True)
		logging.info("Loaded: "+leftDownSegPath)
	else:
		segName = patId+"_ProSeg"
		[success, segNode] = slicer.util.loadSegmentation(proSegPath, returnNode = True)
		logging.info("Loaded: "+proSegPath)
	
	 
		
	#segNode = slicer.util.getNode(segName) #not used, returned when loaded
	bigSeg = segNode.GetSegmentation()
	colSeg = None
	notColSeg = None
	
	#select colon vs notColon segments
	for x in range(2):
		part = bigSeg.GetNthSegment(x)
		if len(part.GetName())<7:
			colSeg = part
		elif len(part.GetName())>6:
			notColSeg = part
	
	bigSeg.RemoveSegment(notColSeg)
	logging.info('Removed notColon')
	
	#export segment to labelmap
	inputVol = slicer.vtkMRMLLabelMapVolumeNode()
	slicer.mrmlScene.AddNode(inputVol)
	slicer.vtkSlicerSegmentationsModuleLogic.ExportAllSegmentsToLabelmapNode(segNode, inputVol)
	logging.info('Created Labelmap')
			
	#set the input volume
	pars = {}
	pars["InputImageFileName"] = inputVol.GetID()

	# create a markups fiducial node and name it, set it as the output
	fidsOut = slicer.vtkMRMLMarkupsFiducialNode()
	if mode == 'sup':
		fidsOut.SetName('PTBC0017_SupCenterPoints')
	elif mode == 'ld':
		fidsOut.SetName('PTBC0017_LeftDownCenterPoints')
	else:
		fidsOut.SetName('PTBC0017_ProCenterPoints')
		
	slicer.mrmlScene.AddNode(fidsOut)
	pars["OutputFiducialsFileName"] = fidsOut.GetID()
	
	pars['NumberOfPoints'] = 600
	
	# mkae last parameter, output volume. 
	imgOut = slicer.vtkMRMLLabelMapVolumeNode()
	imgOut.SetName('PTBC0017_Output') # TODO fix the hardcoded name
	slicer.mrmlScene.AddNode(imgOut)
	pars['OutputImageFileName'] = imgOut.GetID()
	logging.info('Created pars, running extract skeleton')

	#run the module with parameters
	cenLiner = slicer.modules.extractskeleton
	slicer.cli.runSync(cenLiner, None, pars)
	logging.info('Extracted Skeleton, saving.')
	
	#save as correct file name
	if mode == 'sup':
		savePath = patPath + "\\" + patId + "_SupCenterPoints.fcsv"
	elif mode == 'ld':
		savePath = patPath + "\\" + patId + "_LeftDownCenterPoints.fcsv"
	else:
		savePath = patPath + "\\" + patId + "_ProCenterPoints.fcsv"
	
	slicer.util.saveNode(fidsOut, savePath)
	logging.info('Saved to: '+savePath)
	
	return fidsOut



	
	
	
#####Curve from markups---------------------------------------

#function to return a curve model from fiducial list node
def doMarkupsToModel(markups):
	markupsToModelNode = slicer.vtkMRMLMarkupsToModelNode()
	markupsToModelNode.SetName('MyMarkupsToModelNode')
	slicer.mrmlScene.AddNode(markupsToModelNode)

	markupsToModelNode.SetAndObserveInputNodeID(markups.GetID())

	outputCurve = slicer.vtkMRMLModelNode()
	slicer.mrmlScene.AddNode(outputCurve)
	outputCurve.SetName(markups.GetName()[:-17]+'Curve')

	markupsToModelNode.SetAndObserveModelNodeID(outputCurve.GetID())
	markupsToModelNode.SetModelType(1)
	markupsToModelNode.SetModelType(1)
	markupsToModelNode.SetCurveType(3)
	markupsToModelNode.SetPolynomialFitType(1)
	markupsToModelNode.SetPolynomialOrder(2)
	markupsToModelNode.SetPolynomialSampleWidth(0.05)
	markupsToModelNode.SetTubeRadius(0)
	
	return outputCurve
	
	
#function to apply curve gen to file path, output to new file in same directory
def MarkupFileToModelFile(inPath):
	outPath = inPath[:-17]+'Curve.vtk'
	print(outPath)
	[success, markups] = slicer.util.loadMarkupsFiducialList(inPath, returnNode=True)
	slicer.util.saveNode(doMarkupsToModel(markups), outPath)
	


#Iterate through a list of patients in a directory and save supine and prone curves
'''
direc = "D:\ColonCurves_JL\CtVolumes\\"
idList = ['PTAF0056','PTAJ0023', 'PTAJ0095', 'PTAM0029', 'PTAP0049', 'PTAT0093', 'PTBB0002', 'PTBB0024', 'PTBC0016', 'PTBC0017', 'PTBD0033', 'PTBG0026' ]
#idList = ['PTAF0056']
for x in idList:
	slicer.mrmlScene.Clear(0)
	supPath = direc + x + "\\" + x + "_SupCenterPoints.fcsv"
	proPath = direc + x + "\\" + x + "_ProCenterPoints.fcsv"
	
	try:
		MarkupFileToModelFile(supPath)
	except:
		print('Failed supine curve! ' + supPath)
	try:
		MarkupFileToModelFile(proPath)
	except:
		print('Failed prone curve! ' + proPath)
'''







#####Curvature Modelling ------------------------------------------------

#a function to open a vtk curve in slicer, use curvemaker to find curvatures, and save them to text files
def CurveFileToCurvaturesFile(inPath):
	
	[success, n] = slicer.util.loadModel(inPath, returnNode = True)
	#print(n)
	#n = slicer.util.getFirstNodeByName(inPath[-17:])
	polyData = n.GetPolyData()
	import CurveMaker
	CurveMaker.CurveMakerLogic()
	curvatureArray = vtk.vtkDoubleArray()
	#print(polyData)
	avgCurve, minCurve, maxCurve = CurveMaker.CurveMakerLogic().computeCurvatures( polyData, curvatureArray )

	
	
	polyData.GetPointData().AddArray(curvatureArray)
	nd = n.GetDisplayNode()

	nd.SetActiveScalarName('Curvature')
	nd.SetScalarVisibility(1)
	

	curvatureList = [curvatureArray.GetTuple1(x) for x in range(curvatureArray.GetNumberOfTuples())]
	stringCurvatureList = [str(x) for x in curvatureList]
	#stringCurvatureList.append("\n")
	
	points = polyData.GetPoints()
	pointList = [points.GetPoint(x) for x in range(points.GetNumberOfPoints())]
	
	newLines = [stringCurvatureList[x] + ', ' + str(pointList[x][0]) + ', ' + str(pointList[x][1]) + ', ' + str(pointList[x][2]) + '\n' for x in range(len(pointList))]
	newLines.append("\n")
	
	outPath = inPath[:-9] + "Curvatures.txt"
	print(outPath)
	outFile = open(outPath, 'w')
	outFile.writelines(newLines)
	outFile.close()
	
	slicer.util.saveNode(n, inPath)
	
#process all the curve files
'''
direc = "D:\ColonCurves_JL\CtVolumes\\"
idList = ['PTAF0056','PTAJ0023', 'PTAJ0095', 'PTAM0029', 'PTAP0049', 'PTAT0093', 'PTBB0002', 'PTBB0024', 'PTBC0016', 'PTBC0017', 'PTBD0033', 'PTBG0026' ]
#idList = ['PTAF0056']
for x in idList:
	slicer.mrmlScene.Clear(0)
	supPath = direc + x + "\\" + x + "_SupCurve.vtk"
	proPath = direc + x + "\\" + x + "_ProCurve.vtk"
	
	try:
		CurveFileToCurvaturesFile(supPath)
	except:
		print('Failed supine curvatures! ' + supPath)
	try:
		CurveFileToCurvaturesFile(proPath)
	except:
		print('Failed prone curvatures! ' + proPath)

'''


####### run all processing:





def analyzePatient(patientPath, modeList = ['sup', 'pro']):
	'''A function to analyze a patients prone and suppine ct scan segmentations. It will use extract skeleton to get centerpoints, 
	it will use markups to model to get the curve model, and will use computeCurvatures() function from Curve Maker to get curvature data.
	One input is needed: patient's data folder, and all outputs are into files in that same folder. Will display errors in the console. '''
	
	doPro, doSup, doLeftDown = False, False, False
	
	if 'pro' in modeList:
		doPro = True
	if 'sup' in modeList:
		doSup = True
	if 'ld' in modeList:
		doLeftDown = True
	
	
	#try to get centerpoints from segmentations for supine and pro segmentations
	if doPro:
		try:
			centerPointsFromFile(patientPath, 'pro')
		except:
			print("Failed to extract prone centerpoints. " + patientPath)
			doPro = False
	if doSup:
		try:
			centerPointsFromFile(patientPath, 'sup')
		except:
			print("Failed to extract supine centerpoints. " + patientPath)
			doSup = False
	if doLeftDown:
		try:
			centerPointsFromFile(patientPath, 'ld')
		except:
			print("Failed to extract left down centerpoints. " + patientPath)
			doLeftDown = False


	cpSupPath = patientPath+ "\\" + patientPath[-8:] + "_SupCenterPoints.fcsv"
	cpProPath = patientPath+ "\\" + patientPath[-8:] + "_ProCenterPoints.fcsv"
	cpLeftDownPath = patientPath+ "\\" + patientPath[-8:] + "_LeftDownCenterPoints.fcsv"

	
	#try to generate curve model from centerpoints in both positions
	if doPro:
		try:
			MarkupFileToModelFile(cpProPath)
		except:
			print("Failed to get prone curve. " + patientPath)
			doPro = False
	if doSup:
		try:
			MarkupFileToModelFile(cpSupPath)
		except:
			print("Failed to get supine curve. " + patientPath)
			doSup = False
	if doLeftDown:
		try:
			MarkupFileToModelFile(cpLeftDownPath)
		except:
			print("Failed to get left down curve. " + patientPath)
			doLeftDown = False


	curveSupPath = patientPath+ "\\" + patientPath[-8:] + "_SupCurve.vtk"
	curveProPath = patientPath+ "\\" + patientPath[-8:] + "_ProCurve.vtk"
	curveLeftDownPath = patientPath+ "\\" + patientPath[-8:] + "_LeftDownCurve.vtk"


	#try to get the curvature data for both positions
	if doPro:
		try:
			CurveFileToCurvaturesFile(curveProPath)
		except:
			print("Failed to get prone curvatures. " + patientPath)
			doPro = False
	if doSup:
		try:
			CurveFileToCurvaturesFile(curveSupPath)
		except:
			print("Failed to get supine curvatures. " + patientPath)
			doSup = False
	if doLeftDown:
		try:
			CurveFileToCurvaturesFile(curveLeftDownPath)
		except:
			print("Failed to get left down curvatures. " + patientPath)
			doLeftDown = False
	
	
			
			
			
			
			
			
#direc = "C:\Users\jlaframboise\ColonCurves_JL\CtVolumes"
#patientIdList = ['PTAF0056','PTAJ0023', 'PTAJ0095', 'PTAM0029', 'PTAP0049', 'PTAT0093', 'PTBB0002', 'PTBB0024', 'PTBC0016', 'PTBC0017', 'PTBD0033', 'PTBG0026' ]		
#patientIdList = ['PTAJ0095', 'PTAM0029', 'PTAP0049', 'PTAT0093', 'PTBB0002', 'PTBB0024', 'PTBC0016', 'PTBC0017', 'PTBD0033', 'PTBG0026' ]		




#for x in patientIdList:
	#analyzePatient(direc + "\\" + x)
	
	

#do it
#analyzePatient("C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAP0049", ['pro'])



CurveFileToCurvaturesFile(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_LeftDownCurve.vtk")









