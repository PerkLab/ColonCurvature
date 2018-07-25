import statistics as stat

def getStats(dataInPath):
	fIn = open(inPath, 'r')
	lines = fIn.readlines()
	fIn.close()
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
	
	for x in curveNumbers:
		allCurveDegrees.append(maxDegrees[x])
		allCurveDistances.append(maxDistances[x])
		allCurveRatios.append(maxDegrees[x]/maxDistances[x])
		
		if maxDegrees[x]<20:
			lessThan20Deg.append(maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x])
		elif maxDegrees[x]<40:
			lessThan40Deg.append(maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x])
		elif maxDegrees[x]<60:
			lessThan60Deg.append(maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x])
		elif maxDegrees[x]<80:
			lessThan80Deg.append(maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x])
		elif maxDegrees[x]<100:
			lessThan100Deg.append(maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x])
		elif maxDegrees[x]<120:
			lessThan120Deg.append(maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x])
		elif maxDegrees[x]<140:
			lessThan140Deg.append(maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x])
		elif maxDegrees[x]<160:
			lessThan160Deg.append(maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x])
		elif maxDegrees[x]<180:
			lessThan180Deg.append(maxDegrees[x], maxDistances[x], maxDegrees[x]/maxDistances[x])
		
	
	