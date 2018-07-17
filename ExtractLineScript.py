def getLine(inputVol):
	print('Connected')

	pars = {}
	#inName = "PTBC0017_SupSeg-label"
	#inNode = slicer.util.getNode(inName)
	#pars["InputImageFileName"] = inNode.GetID()
	pars["InputImageFileName"] = inputVol.GetID()

	fidsOut = slicer.vtkMRMLMarkupsFiducialNode()
	fidsOut.SetName('PTBC0017_SupCenterPoints')
	slicer.mrmlScene.AddNode(fidsOut)
	pars["OutputFiducialsFileName"] = fidsOut.GetID()
	
	pars['NumberOfPoints'] = 600
	
	imgOut = slicer.vtkMRMLLabelMapVolumeNode()
	imgOut.SetName('PTBC0017_Output')
	slicer.mrmlScene.AddNode(imgOut)
	pars['OutputImageFileName'] = imgOut.GetID()
	#print(pars)

	cenLiner = slicer.modules.extractskeleton
	return (slicer.cli.runSync(cenLiner, None, pars))
	
	
	
	
def getCenterPoints(inputVol):
	print('Connected')

	pars = {}
	#inName = "PTBC0017_SupSeg-label"
	#inNode = slicer.util.getNode(inName)
	#pars["InputImageFileName"] = inNode.GetID()
	pars["InputImageFileName"] = inputVol.GetID()

	fidsOut = slicer.vtkMRMLMarkupsFiducialNode()
	fidsOut.SetName('PTBC0017_SupCenterPoints')
	slicer.mrmlScene.AddNode(fidsOut)
	pars["OutputFiducialsFileName"] = fidsOut.GetID()
	
	pars['NumberOfPoints'] = 600
	
	imgOut = slicer.vtkMRMLLabelMapVolumeNode()
	imgOut.SetName('PTBC0017_Output')
	slicer.mrmlScene.AddNode(imgOut)
	pars['OutputImageFileName'] = imgOut.GetID()
	#print(pars)

	cenLiner = slicer.modules.extractskeleton
	slicer.cli.runSync(cenLiner, None, pars)
	return fidsOut
	
	
def centerPointsFromFile(patPath, mode):
	print('Connected')
	patId = patPath[-8:]
	supSegPath = patPath + "\\" + patId + "_SupSeg.seg.nrrd"
	proSegPath = patPath + "\\" + patId + "_ProSeg.seg.nrrd"
	leftDownSegPath = patPath + "\\" + patId + "_LeftDownSeg.seg.nrrd"
	logging.info(patId)
	
	if mode == 'sup':
		segName = patId+"_SupSeg"
		slicer.util.loadSegmentation(supSegPath)
		logging.info("Loaded: "+supSegPath)
	elif mode == 'ld':
		segName = patId+"_LeftDownSeg"
		slicer.util.loadSegmentation(leftDownSegPath)
		logging.info("Loaded: "+leftDownSegPath)
	else:
		segName = patId+"_ProSeg"
		slicer.util.loadSegmentation(proSegPath)
		logging.info("Loaded: "+proSegPath)
	
	 
		
	segNode = slicer.util.getNode(segName)
	bigSeg = segNode.GetSegmentation()
	colSeg = None
	notColSeg = None
	
	for x in range(2):
		part = bigSeg.GetNthSegment(x)
		if len(part.GetName())<7:
			colSeg = part
		elif len(part.GetName())>6:
			notColSeg = part
	
	bigSeg.RemoveSegment(notColSeg)
	logging.info('Removed notColon')
	
	inputVol = slicer.vtkMRMLLabelMapVolumeNode()
	slicer.mrmlScene.AddNode(inputVol)
	slicer.vtkSlicerSegmentationsModuleLogic.ExportAllSegmentsToLabelmapNode(segNode, inputVol)
	logging.info('Created Labelmap')
			
	pars = {}
	pars["InputImageFileName"] = inputVol.GetID()

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
	
	imgOut = slicer.vtkMRMLLabelMapVolumeNode()
	imgOut.SetName('PTBC0017_Output')
	slicer.mrmlScene.AddNode(imgOut)
	pars['OutputImageFileName'] = imgOut.GetID()
	logging.info('Created pars, running extract skeleton')

	cenLiner = slicer.modules.extractskeleton
	slicer.cli.runSync(cenLiner, None, pars)
	logging.info('Extracted Skeleton, saving.')
	if mode == 'sup':
		savePath = patPath + "\\" + patId + "_SupCenterPoints.fcsv"
	if mode == 'ld':
		savePath = patPath + "\\" + patId + "_LeftDownCenterPoints.fcsv"
	else:
		savePath = patPath + "\\" + patId + "_ProCenterPoints.fcsv"
	
	slicer.util.saveNode(fidsOut, savePath)
	logging.info('Saved to: '+savePath)
	
	return fidsOut
	
	
	
'''
patIds = ['PTAF0056', 'PTAJ0023', 'PTAJ0095',  
		'PTAM0029', 'PTAP0049', 'PTAT0093', 
		'PTBB0002', 'PTBB0024', 'PTBC0016']

patIds = ['PTAJ0095', 'PTAM0029', 'PTBB0002', 'PTBC0016']

directory = "D:\ColonCurves_JL\CtVolumes\\"

for patient in patIds:
	path = directory + patient
	
	try:
		centerPointsFromFile(path, 'sup')
		logging.info('---------------------------------------------------------------Successful supine points for: ' + patient)
	except:
		logging.info('---------------------------------------------------------------Failed supine points for: ' + patient)
	try:
		centerPointsFromFile(path, 'pro')
		logging.info('---------------------------------------------------------------Successful prone points for: ' + patient)
	except:
		logging.info('---------------------------------------------------------------Failed prone points for: ' + patient)
		
	slicer.mrmlScene.Clear(0)
	
	
'''
	
	
	