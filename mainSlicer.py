'''This file runs through slicer, and does the first portion of the work, as
slicer is needed for this. '''

import os

patPath = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013"
patPath2 = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0014"

execfile(r"C:\Users\jlaframboise\Documents\ColonCurvature\AllAnalysis.py")

execfile(r"C:\Users\jlaframboise\Documents\ColonCurvature\SplitSegments.py")

patId = patPath[-8:]

supCenterPointsPath = os.path.join(patPath2, patId+ '_SupCenterPoints.fcsv')
proCenterPointsPath = os.path.join(patPath2, patId+ '_ProCenterPoints.fcsv')

#Slicer needs to run this:

#splitCenterPointsFileToFiles(supCenterPointsPath)
#splitCenterPointsFileToFiles(proCenterPointsPath)

analyzeFromCenterPoints(patPath2, modeList = ['sup', 'pro'])
saveCutPointsFile(patPath2)

	


