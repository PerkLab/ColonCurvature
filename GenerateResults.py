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
	modeCurvature = stat.mode(curvatureValues)
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
	linesOut.append('Mode Curvature, {}'.format(modeCurvature))
	linesOut.append('Total Curvature, {}'.format(totalCurvature))
	linesOut.append('Standard Dev of Curvature, {}'.format(stanDevCurvature))
	linesOut.append('Variance of Curvature, {}'.format(varianceCurvature))
	linesOut.append('')
	
	
	linesOut.append('Number of Curves, {}'.format(len(allCurveDegrees)))
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
	#outLines.append('{},{},{}'.format('Mean Curvatures', supLines[0].strip().split(', ')[1], supLines[0].strip(', ').split()[1]))
	
	for y in range(0,6):
		outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1], proLines[y].strip().split(', ')[1]))
	
	outLines.append(supLines[6].strip())
	
	for y in range(7,12):
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
	
getStats(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvaturesData.txt")
getStats(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_ProCurvaturesData.txt")
	
compareSupineProne(r'C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012')
	
	
#getStats(r
	
	
	
	
	
	
	
	
	
	