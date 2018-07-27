from SplitSegments import *
from AllAnalysis import *
from ProcessCurvatureData import *
from GenerateResults import *

def doAllAfterCenterPointsCMD(patPath):
	'''The function that should be run through command prompt through python 3, will do all the worl
	after slicer's functionality is not needed. '''
	
	
	patId = patPath[-8:]
	supCenterPointsPath = os.path.join(patPath, patId+ '_SupCenterPoints.fcsv')
	proCenterPointsPath = os.path.join(patPath, patId+ '_ProCenterPoints.fcsv')

	#CMD can run this:
	
	
	supCurvaturesPath = os.path.join(patPath, patId+ '_SupCurvatures.txt')
	proCurvaturesPath = os.path.join(patPath, patId+ '_ProCurvatures.txt')
	
	
	doAllProcessing(supCurvaturesPath,0,0,1,1.5)
	doAllProcessing(proCurvaturesPath,0,0,1,1.5)
	
	splitPatientDataFilesToFiles(patPath)
	
	supDataPath = os.path.join(patPath, patId+ '_SupCurvaturesData.txt')
	proDataPath = os.path.join(patPath, patId+ '_ProCurvaturesData.txt')
	
	supAcDataPath = os.path.join(patPath, patId+ '_SupCurvaturesAcData.txt')
	proAcDataPath = os.path.join(patPath, patId+ '_ProCurvaturesAcData.txt')
	supTcDataPath = os.path.join(patPath, patId+ '_SupCurvaturesTcData.txt')
	proTcDataPath = os.path.join(patPath, patId+ '_ProCurvaturesTcData.txt')
	supDcDataPath = os.path.join(patPath, patId+ '_SupCurvaturesDcData.txt')
	proDcDataPath = os.path.join(patPath, patId+ '_ProCurvaturesDcData.txt')

	getStats(supDataPath)
	getStats(proDataPath)
	
	getStats(supAcDataPath)
	getStats(proAcDataPath)
	getStats(supTcDataPath)
	getStats(proTcDataPath)
	getStats(supDcDataPath)
	getStats(proDcDataPath)
	
	
	comparePatientResults(patPath)
	
	
	
patPath = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013"
patPath2 = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0014"


doAllAfterCenterPointsCMD(patPath2)

#splitPatientDataFilesToFiles(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013\TEST0013_SupCurvaturesData.txt", r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013\TEST0013_SupCutPoints.txt")

