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

#analyzeFromCenterPoints(patPath2, modeList = ['sup', 'pro'])
#saveCutPointsFile(patPath2)

pathList = [r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBD0033",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBG0026",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAF0056",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAJ0023",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAM0029",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAP0049",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAT0093",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBB0002",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBC0017"]


x = 8
analyzeFromCenterPoints(pathList[x], modeList = ['sup', 'pro'])
saveCutPointsFile(pathList[x])