import os

patPath = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013"

execfile(r"C:\Users\jlaframboise\Documents\ColonCurvature\AllAnalysis.py")

execfile(r"C:\Users\jlaframboise\Documents\ColonCurvature\SplitSegments.py")

patId = patPath[-8:]

supCenterPointsPath = os.path.join(patPath, patId+ '_SupCenterPoints.fcsv')
proCenterPointsPath = os.path.join(patPath, patId+ '_ProCenterPoints.fcsv')

#Slicer needs to run this:

#splitCenterPointsFileToFiles(supCenterPointsPath)
#splitCenterPointsFileToFiles(proCenterPointsPath)

analyzeFromCenterPoints(patPath, modeList = ['sup', 'pro'])
saveCutPointsFile(patPath)

	


