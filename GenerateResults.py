import statistics as stat

def getStats(dataInPath):
	fIn = open(inPath, 'r')
	lines = fIn.readlines()
	fIn.close()
	title = lines[0].strip()
	curvatureValues = [x.strip().split(', ')[5] for x in lines[1:]]
	maxMinTypes = [x.strip().split(', ')[7] for x in lines[1:]]
	maxDegrees= [x.strip().split(', ')[8] for x in lines[1:]]
	maxDistances= [x.strip().split(', ')[9] for x in lines[1:]]