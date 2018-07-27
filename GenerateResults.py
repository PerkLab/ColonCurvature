import statistics as stat
from operator import itemgetter
import os


def getStats(dataInPath):
	fIn = open(dataInPath, 'r')
	lines = fIn.readlines()
	fIn.close()
	dataOutPath = dataInPath[:-4] + 'Results.txt'
	title = lines[0].strip()
	curvatureValues = [float(x.strip().split(', ')[5]) for x in lines[1:]]
	maxMinTypes = [x.strip().split(', ')[7] for x in lines[1:]]
	maxDegrees= [float(x.strip().split(', ')[8]) for x in lines[1:]]
	maxDistances= [float(x.strip().split(', ')[9]) for x in lines[1:]]
	
	meanCuvature = stat.mean(curvatureValues)
	medianCurvature = stat.median(curvatureValues)
	#modeCurvature = stat.mode(curvatureValues)
	#print(curvatureValues)
	stanDevCurvature = stat.pstdev(curvatureValues)
	varianceCurvature = stat.pvariance(curvatureValues)
	totalCurvature = sum(curvatureValues)
	
	curveNumbers = []
	for x in range(len(maxMinTypes)):
		if maxMinTypes[x] == 'MAX' and maxDegrees[x]>0:
			curveNumbers.append(x)
	
	allCurveDegrees = []
	allCurveDistances = []
	allCurveRatios = []
	
	lessThan20Deg = []
	lessThan40Deg = []
	lessThan60Deg = []
	lessThan80Deg = []
	lessThan100Deg = []
	lessThan120Deg = []
	lessThan140Deg = []
	lessThan160Deg = []
	lessThan180Deg = []
	
	allCurves = []
	
	for x in curveNumbers:
		allCurveDegrees.append(maxDegrees[x])
		allCurveDistances.append(maxDistances[x])
		allCurveRatios.append(maxDegrees[x]/maxDistances[x])
		
		if maxDegrees[x]<20:
			lessThan20Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x]))
		elif maxDegrees[x]<40:
			lessThan40Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x]))
		elif maxDegrees[x]<60:
			lessThan60Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x]))
		elif maxDegrees[x]<80:
			lessThan80Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x]))
		elif maxDegrees[x]<100:
			lessThan100Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x]))
		elif maxDegrees[x]<120:
			lessThan120Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x]))
		elif maxDegrees[x]<140:
			lessThan140Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x]))
		elif maxDegrees[x]<160:
			lessThan160Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x]))
		elif maxDegrees[x]<180:
			lessThan180Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x]))
			
		allCurves.append((x, maxDegrees[x]/maxDistances[x], maxDegrees[x], maxDistances[x]))
	
	allCurves = sorted(allCurves, key = itemgetter(1))
	
	
	lessThan20DegDists = [str(x[1]) for x in sorted(lessThan20Deg, key = itemgetter(1))]
	lessThan40DegDists = [str(x[1]) for x in sorted(lessThan40Deg, key = itemgetter(1))]
	lessThan60DegDists = [str(x[1]) for x in sorted(lessThan60Deg, key = itemgetter(1))]
	lessThan80DegDists = [str(x[1]) for x in sorted(lessThan80Deg, key = itemgetter(1))]
	lessThan100DegDists = [str(x[1]) for x in sorted(lessThan100Deg, key = itemgetter(1))]
	lessThan120DegDists = [str(x[1]) for x in sorted(lessThan120Deg, key = itemgetter(1))]
	lessThan140DegDists = [str(x[1]) for x in sorted(lessThan140Deg, key = itemgetter(1))]
	lessThan160DegDists = [str(x[1]) for x in sorted(lessThan160Deg, key = itemgetter(1))]
	lessThan180DegDists = [str(x[1]) for x in sorted(lessThan180Deg, key = itemgetter(1))]
	
	if lessThan20Deg:
		lessThan20DegAvgDist = stat.mean([float(x[1]) for x in lessThan20Deg])
	else:
		lessThan20DegAvgDist = 0
		
	if lessThan40Deg:
		lessThan40DegAvgDist = stat.mean([float(x[1]) for x in lessThan40Deg])
	else:
		lessThan40DegAvgDist = 0
		
	if lessThan60Deg:
		lessThan60DegAvgDist = stat.mean([float(x[1]) for x in lessThan60Deg])
	else:
		lessThan60DegAvgDist = 0
		
	if lessThan80Deg:
		lessThan80DegAvgDist = stat.mean([float(x[1]) for x in lessThan80Deg])
	else:
		lessThan80DegAvgDist = 0
		
	if lessThan100Deg:
		lessThan100DegAvgDist = stat.mean([float(x[1]) for x in lessThan100Deg])
	else:
		lessThan100DegAvgDist = 0
		
	if lessThan120Deg:
		lessThan120DegAvgDist = stat.mean([float(x[1]) for x in lessThan120Deg])
	else:
		lessThan120DegAvgDist = 0
		
	if lessThan140Deg:
		lessThan140DegAvgDist = stat.mean([float(x[1]) for x in lessThan140Deg])
	else:
		lessThan140DegAvgDist = 0
		
	if lessThan160Deg:
		lessThan160DegAvgDist = stat.mean([float(x[1]) for x in lessThan160Deg]) 
	else:
		lessThan160DegAvgDist = 0
		
	if lessThan180Deg:
		lessThan180DegAvgDist = stat.mean([float(x[1]) for x in lessThan180Deg])
	else:
		lessThan180DegAvgDist = 0

	
	meanCurveDegrees = stat.mean(allCurveDegrees)
	meanCurveDistance = stat.mean(allCurveDistances)
	medianCurveDegrees = stat.median(allCurveDegrees)
	medianCurveDistance = stat.median(allCurveDistances)
	
	
	linesOut = []
	linesOut.append('Mean Curvature, {}'.format(meanCuvature))
	linesOut.append('Median Curvature, {}'.format(medianCurvature))
	#linesOut.append('Mode Curvature, {}'.format(modeCurvature))
	linesOut.append('Total Curvature, {}'.format(totalCurvature))
	linesOut.append('Standard Dev of Curvature, {}'.format(stanDevCurvature))
	linesOut.append('Variance of Curvature, {}'.format(varianceCurvature))
	linesOut.append('')
	
	linesOut.append('Number of Curves, {}'.format(len(allCurveDegrees)))
	linesOut.append('Number of Points, {}'.format(len(curvatureValues)))
	linesOut.append('Mean Degrees of Curve, {}'.format(meanCurveDegrees))
	linesOut.append('Median Degrees of Curve, {}'.format(medianCurveDegrees))
	linesOut.append('Mean Distance of Curve, {}'.format(meanCurveDistance))
	linesOut.append('Median Distance of Curve, {}'.format(medianCurveDistance))
	linesOut.append('')
	
	
	linesOut.append('Number of curves < 20deg, {}'.format(len(lessThan20Deg)))
	linesOut.append('Mean Distance of Curves ^, {}'.format(str(lessThan20DegAvgDist)))
	linesOut.append('Curve Distances, {}'.format(' '.join(lessThan20DegDists)))
	
	linesOut.append('Number of curves < 40deg, {}'.format(len(lessThan40Deg)))
	linesOut.append('Mean Distance of Curves ^, {}'.format(str(lessThan40DegAvgDist)))
	linesOut.append('Curve Distances, {}'.format(' '.join(lessThan40DegDists)))
	
	linesOut.append('Number of curves < 60deg, {}'.format(len(lessThan60Deg)))
	linesOut.append('Mean Distance of Curves ^, {}'.format(str(lessThan60DegAvgDist)))
	linesOut.append('Curve Distances, {}'.format(' '.join(lessThan60DegDists)))
	
	linesOut.append('Number of curves < 80deg, {}'.format(len(lessThan80Deg)))
	linesOut.append('Mean Distance of Curves ^, {}'.format(str(lessThan80DegAvgDist)))
	linesOut.append('Curve Distances, {}'.format(' '.join(lessThan80DegDists)))
	
	linesOut.append('Number of curves < 100deg, {}'.format(len(lessThan100Deg)))
	linesOut.append('Mean Distance of Curves ^, {}'.format(str(lessThan100DegAvgDist)))
	linesOut.append('Curve Distances, {}'.format(' '.join(lessThan100DegDists)))
	
	linesOut.append('Number of curves < 120deg, {}'.format(len(lessThan120Deg)))
	linesOut.append('Mean Distance of Curves ^, {}'.format(str(lessThan120DegAvgDist)))
	linesOut.append('Curve Distances, {}'.format(' '.join(lessThan120DegDists)))
	
	linesOut.append('Number of curves < 140deg, {}'.format(len(lessThan140Deg)))
	linesOut.append('Mean Distance of Curves ^, {}'.format(str(lessThan140DegAvgDist)))
	linesOut.append('Curve Distances, {}'.format(' '.join(lessThan140DegDists)))
	
	linesOut.append('Number of curves < 160deg, {}'.format(len(lessThan160Deg)))
	linesOut.append('Mean Distance of Curves ^, {}'.format(str(lessThan160DegAvgDist)))
	linesOut.append('Curve Distances, {}'.format(' '.join(lessThan160DegDists)))
	
	linesOut.append('Number of curves < 180deg, {}'.format(len(lessThan180Deg)))
	linesOut.append('Mean Distance of Curves ^, {}'.format(str(lessThan180DegAvgDist)))
	linesOut.append('Curve Distances, {}'.format(' '.join(lessThan180DegDists)))
	linesOut.append('')
	
	
	linesOut.append('All Curves Sorted by Degrees/Distance,')
	linesOut.append('{}, {}, {}, {}'.format('Deg/Dist', 'Num', 'Deg', 'Dist'))
	for curve in allCurves:
		linesOut.append('{}, {}, {}, {}'.format(curve[1], curve[0], curve[2], curve[3]))
	
	
	
	
	
	
	
	
	
	fOut = open(dataOutPath, 'w')
	for line in linesOut:
		fOut.write(line)
		fOut.write('\n')
	
	
	fOut.close()
	
	
def compareSupineProne(patPath):
	patId = patPath[-8:]
	supPath = os.path.join(patPath, patId + '_SupCurvaturesDataResults.txt')
	proPath = os.path.join(patPath, patId + '_ProCurvaturesDataResults.txt')
	supIn = open(supPath, 'r')
	supLines = supIn.readlines()
	supIn.close()
	proIn = open(proPath, 'r')
	proLines = proIn.readlines()
	proIn.close()
	
	outLines = []
	outLines.append('{},Supine,Prone'.format(patId))
	
	for y in range(0,5):
		outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1], proLines[y].strip().split(', ')[1]))
	
	outLines.append(supLines[5].strip())
	
	for y in range(6,12):
		outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1], proLines[y].strip().split(', ')[1]))
	
	outLines.append(supLines[12].strip())

	for y in range(13, 38, 3):
		outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1], proLines[y].strip().split(', ')[1]))
		outLines.append('{},{},{}'.format(supLines[y+1].strip().split(', ')[0], supLines[y+1].strip().split(', ')[1], proLines[y+1].strip().split(', ')[1]))
	
	
	outPath = os.path.join(patPath, patPath[-8:]+'_BothCurvaturesDataResults.txt')
	fOut = open(outPath, 'w')
	
	for x in outLines:
		fOut.write(x+'\n')
	
	
	fOut.close()
	

def getDataLines(supPath, proPath, patId, section):
	supIn = open(supPath, 'r')
	supLines = supIn.readlines()
	supIn.close()
	proIn = open(proPath, 'r')
	proLines = proIn.readlines()
	proIn.close()
	
	outLines = []
	outLines.append('{} {},Supine,Prone'.format(patId, section))
	
	for y in range(0,5):
		outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1], proLines[y].strip().split(', ')[1]))
	
	outLines.append(supLines[5].strip())
	
	for y in range(6,12):
		outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1], proLines[y].strip().split(', ')[1]))
	
	outLines.append(supLines[12].strip())

	for y in range(13, 38, 3):
		outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1], proLines[y].strip().split(', ')[1]))
		outLines.append('{},{},{}'.format(supLines[y+1].strip().split(', ')[0], supLines[y+1].strip().split(', ')[1], proLines[y+1].strip().split(', ')[1]))
	
	return outLines
	
	
def comparePatientResults(patPath):

	patId = patPath[-8:]
	supPath = os.path.join(patPath, patId + '_SupCurvaturesDataResults.txt')
	proPath = os.path.join(patPath, patId + '_ProCurvaturesDataResults.txt')
	
	supAcPath = os.path.join(patPath, patId + '_SupCurvaturesAcDataResults.txt')
	proAcPath = os.path.join(patPath, patId + '_ProCurvaturesAcDataResults.txt')
	supTcPath = os.path.join(patPath, patId + '_SupCurvaturesTcDataResults.txt')
	proTcPath = os.path.join(patPath, patId + '_ProCurvaturesTcDataResults.txt')
	supDcPath = os.path.join(patPath, patId + '_SupCurvaturesDcDataResults.txt')
	proDcPath = os.path.join(patPath, patId + '_ProCurvaturesDcDataResults.txt')
	
	outLinesMain = getDataLines(supPath, proPath, patId, 'All')
	outLinesAc = getDataLines(supAcPath, proAcPath, patId, 'AC')
	outLinesTc = getDataLines(supTcPath, proTcPath, patId, 'TC')
	outLinesDc = getDataLines(supDcPath, proDcPath, patId, 'DC')
	
	outLinesMain.append('')
	outLinesAc.append('')
	outLinesTc.append('')
	outLinesDc.append('')
	
	outLinesAll = outLinesMain + outLinesAc + outLinesTc + outLinesDc
	
	
	outPath = os.path.join(patPath, patPath[-8:]+'_PatientCurvatureComparison.txt')
	fOut = open(outPath, 'w')
	
	for x in outLinesAll:
		fOut.write(x+'\n')
	
	
	fOut.close()
	
	
	
class Patient():
	def __init__(self, path):
		self.patPath = path
		self.patId = self.patPath[-8:]
		self.completeDataFilePath = os.path.join(self.patPath, self.patId + '_PatientCurvatureComparison.txt')
		self.loadData()
		
	def loadData(self):
		fIn = open(self.completeDataFilePath, 'r')
		self.lines = [x.strip() for x in fIn.readlines()]
		fIn.close()
		
		self.wholeData = []
		for x in self.lines[0:32]:
			try:
				self.wholeData.append((float(x.split(',')[1]), float(x.split(',')[2])))
			except:
				7*2
				
		self.textLines = []
		for x in self.lines[0:32]:
			text = x.split(',')[0] 
			if text!='' and text != '\n':
				self.textLines.append(text)
		
		
		self.acData = []
		for x in self.lines[33:65]:
			try:
				self.acData.append((float(x.split(',')[1]), float(x.split(',')[2])))
			except:
				7*2
				pass
				
		self.tcData = []
		for x in self.lines[66:98]:
			try:
				self.tcData.append((float(x.split(',')[1]), float(x.split(',')[2])))
			except:
				7*2
				pass
		
		self.dcData = []
		for x in self.lines[99:131]:
			try:
				self.dcData.append((float(x.split(',')[1]), float(x.split(',')[2])))
			except:
				7*2
				pass
				
	
	
	
#p = Patient(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013")



def makeAverageLists(patientPathList):
	patientList = [Patient(x) for x in patientPathList]
	idList = [patient.patId for patient in patientList]
	
	textList = patientList[0].textLines
	
	allWholeDataList = []
	
	for x in range(len(patientList[0].wholeData)):
		supList = [patient.wholeData[x][0] for patient in patientList]
		proList = [patient.wholeData[x][1] for patient in patientList]
		supMean = stat.mean(supList)
		proMean = stat.mean(proList)
		#print((supMean, proMean))
		allWholeDataList.append((supMean, proMean))
	
	allAcDataList = []
	
	for x in range(len(patientList[0].acData)):
		supList = [patient.acData[x][0] for patient in patientList]
		proList = [patient.acData[x][1] for patient in patientList]
		supMean = stat.mean(supList)
		proMean = stat.mean(proList)
		allAcDataList.append((supMean, proMean))
	
	allTcDataList = []
	
	for x in range(len(patientList[0].tcData)):
		supList = [patient.tcData[x][0] for patient in patientList]
		proList = [patient.tcData[x][1] for patient in patientList]
		supMean = stat.mean(supList)
		proMean = stat.mean(proList)
		allTcDataList.append((supMean, proMean))
	
	allDcDataList = []
	
	for x in range(len(patientList[0].dcData)):
		supList = [patient.dcData[x][0] for patient in patientList]
		proList = [patient.dcData[x][1] for patient in patientList]
		supMean = stat.mean(supList)
		proMean = stat.mean(proList)
		allDcDataList.append((supMean, proMean))
	
	#for x in range(len(allWholeDataList)):
		#print(textList[x], end = ' ')
		#print(allWholeDataList[x], end = ' ')
		#print(allAcDataList[x], end = ' ')
		#print(allTcDataList[x], end = ' ')
		#print(allDcDataList[x])
	
	
	return textList, allWholeDataList, allAcDataList, allTcDataList, allDcDataList, idList
	
	
	
def outputAverageListsToOnePrintReadyList(textLines, allWholeDataList, allAcDataList, allTcDataList, allDcDataList, idList):
	outLines = []
	outLines.append(','.join(idList))
	
	
	for x in range(len(allWholeDataList)):
		line = '{},{},{}'.format(textLines[x+1], allWholeDataList[x][0], allWholeDataList[x][1])
		outLines.append(line)
		
	for x in range(len(allAcDataList)):
		line = '{},{},{}'.format(textLines[x+1], allAcDataList[x][0], allAcDataList[x][1])
		outLines.append(line)
	
	for x in range(len(allTcDataList)):
		line = '{},{},{}'.format(textLines[x+1], allTcDataList[x][0], allTcDataList[x][1])
		outLines.append(line)
	
	for x in range(len(allDcDataList)):
		line = '{},{},{}'.format(textLines[x+1], allDcDataList[x][0], allDcDataList[x][1])
		outLines.append(line)
	
	return outLines
	
	
def doFinalAverageComparison(patientPathList, outputPath):
	textLines, allWholeDataList, allAcDataList, allTcDataList, allDcDataList, idList = makeAverageLists(patientPathList)
	
	toPrintList = outputAverageListsToOnePrintReadyList(textLines, allWholeDataList, allAcDataList, allTcDataList, allDcDataList, idList)
	
	addSpaceList = [4, 28, 33, 56, 62, 84]
	
	fOut = open(outputPath, 'w')
	for x, i in enumerate(toPrintList):
		if i.strip().split(',')[0] == 'Mean Curvature' and x>0 or i.strip().split(',')[0] == 'Number of Curves':
			fOut.write('\n')
		fOut.write(i+'\n')
	fOut.close()
	

#patPathList = [r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013",
#r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0014"]
#outPath = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\SampleOfpatients.txt"
#doFinalAverageComparison(patPathList, outPath)
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	