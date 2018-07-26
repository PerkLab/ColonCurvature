from SplitSegments import *
from AllAnalysis import *
from ProcessCurvatureData import *
from GenerateResults import *

def doAllAfterCenterPointsCMD(patPath):
	
	
	
	patId = patPath[-8:]
	supCenterPointsPath = os.path.join(patPath, patId+ '_SupCenterPoints.fcsv')
	proCenterPointsPath = os.path.join(patPath, patId+ '_ProCenterPoints.fcsv')

	#CMD can run this:
	
	
	supCurvaturesPath = os.path.join(patPath, patId+ '_SupCurvatures.txt')
	proCurvaturesPath = os.path.join(patPath, patId+ '_ProCurvatures.txt')
	
	
	doAllProcessing(supCurvaturesPath,0,0,1,1.5)
	doAllProcessing(proCurvaturesPath,0,0,1,1.5)
	
	
	
	supDataPath = os.path.join(patPath, patId+ '_SupCurvaturesData.txt')
	proDataPath = os.path.join(patPath, patId+ '_ProCurvaturesData.txt')
	

	getStats(supDataPath)
	getStats(proDataPath)
	
	
	compareSupineProne(patPath)
	
	
	
patPath = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013"

doAllAfterCenterPointsCMD(patPath)
