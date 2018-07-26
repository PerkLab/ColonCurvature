
import os


def doAllAfterCenterPointsSlicer(patPath):
	execfile(r"C:\Users\jlaframboise\Documents\ColonCurvature\AllAnalysis.py")
	execfile(r"C:\Users\jlaframboise\Documents\ColonCurvature\GenerateResults.py")
	execfile(r"C:\Users\jlaframboise\Documents\ColonCurvature\SplitSegments.py")
	execfile(r"C:\Users\jlaframboise\Documents\ColonCurvature\ProcessCurvatureData.py")
	patId = patpath[-8:]
	supCenterPointsPath = os.path.join(patPath, patId+ '_SupCenterPoints.fcsv')
	proCenterPointsPath = os.path.join(patPath, patId+ '_ProCenterPoints.fcsv')

	#Slicer needs to run this:
	
	splitCenterPointsFileToFiles(supCenterPointsPath)
	splitCenterPointsFileToFiles(proCenterPointsPath)
	
	analyzeFromSplitCenterPoints(patientPath, modeList = ['sup', 'pro'])
	
def doAllAfterCenterPointsCMD(patPath):
	from SplitSegments import *
	from AllAnalysis import *
	from ProcessCurvatureData import *
	from GenerateResults import *
	
	
	patId = patpath[-8:]
	supCenterPointsPath = os.path.join(patPath, patId+ '_SupCenterPoints.fcsv')
	proCenterPointsPath = os.path.join(patPath, patId+ '_ProCenterPoints.fcsv')

	#CMD can run this:
	
	supAcCenterPointsPath = os.path.join(patPath, patId+ '_SupAcCenterPoints.fcsv')
	supTcCenterPointsPath = os.path.join(patPath, patId+ '_SupTcCenterPoints.fcsv')
	supDcCenterPointsPath = os.path.join(patPath, patId+ '_SupDcCenterPoints.fcsv')
	proAcCenterPointsPath = os.path.join(patPath, patId+ '_ProAcCenterPoints.fcsv')
	proTcCenterPointsPath = os.path.join(patPath, patId+ '_ProTcCenterPoints.fcsv')
	proDcCenterPointsPath = os.path.join(patPath, patId+ '_ProDcCenterPoints.fcsv')
	
	
	doAllProcessing(supCenterPointsPath,0,0,1,1.5)
	doAllProcessing(proCenterPointsPath,0,0,1,1.5)
	
	doAllProcessing(supAcCenterPointsPath,0,0,1,1.5)
	doAllProcessing(proAcCenterPointsPath,0,0,1,1.5)
	doAllProcessing(supTcCenterPointsPath,0,0,1,1.5)
	doAllProcessing(proTcCenterPointsPath,0,0,1,1.5)
	doAllProcessing(supDcCenterPointsPath,0,0,1,1.5)
	doAllProcessing(proDcCenterPointsPath,0,0,1,1.5)
	
	
	supDataPath = os.path.join(patPath, patId+ '_SupCurvaturesData.txt')
	proDataPath = os.path.join(patPath, patId+ '_ProCurvaturesData.txt')
	
	supAcDataPath = os.path.join(patPath, patId+ '_SupAcCurvaturesData.txt')
	supTcDataPath = os.path.join(patPath, patId+ '_SupTcCurvaturesData.txt')
	supDcDataPath = os.path.join(patPath, patId+ '_SupDcCurvaturesData.txt')
	proAcDataPath = os.path.join(patPath, patId+ '_ProAcCurvaturesData.txt')
	proTcDataPath = os.path.join(patPath, patId+ '_ProTcCurvaturesData.txt')
	proDcDataPath = os.path.join(patPath, patId+ '_ProDcCurvaturesData.txt')

	getStats(supDataPath)
	getStats(proDataPath)
	
	getStats(supAcDataPath)
	getStats(proAcDataPath)
	getStats(supTcDataPath)
	getStats(proTcDataPath)
	getStats(supDcDataPath)
	getStats(proDcDataPath)
	
	compareSupineProne(patpath)
	
	
	
patPath = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013"

#doAllAfterCenterPointsSlicer(patPath)









