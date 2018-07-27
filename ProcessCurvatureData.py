import statistics as stat
from operator import itemgetter
import numpy as np
import os

def addDetails(inPath, outputPath):
	'''A function that takes the path of a text file and creates a new text file with the point number,
	and the percentage of how far the point is along the list. Easy to import to Excel'''
	inFile = open(inPath, 'r')
	lines = inFile.readlines()
	inFile.close()
	lines = [x.strip().split(', ') for x in lines]
	outFile = open(outputPath, 'w')
	outFile.write(inPath[-26:] + "\n")
	for count, item in enumerate(lines):
		if item != '' and item !="\n" and item != ['']:
			outFile.write('{}, {}, {}, {}, {}, {}'.format(count, count/(len(lines)-2)*100, item[1], item[2], item[3], item[0]) + '\n')
	#outFile.write('***' + "\n")
	outFile.close()
	
#addDetails(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBD0033\PTBD0033_ProCurvatures.txt",r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBD0033\testing.txt")

def addManyDetails(inPathList):
	'''A function which appleis the addDetails function to a larger number fo files at once, with automated naming
	of output files. '''
	for path in inPathList:
		try:
			outPath = path[:-4] + 'Data.txt'
			addDetails(path, outPath)
			#print('In: {} \n Out: {}'.format(path, outPath))
		except:
			pass

def combineDataFiles(inFileList, outputPath):
	'''A function that takes detailed data files of curvaturee and combines them in an excel readable way. '''
	filesData = []
	for x in inFileList:
		try:
			f = open(x, 'r')
			lines = f.readlines()
			filesData.append(lines)
			f.close()
		except:
			7*2
			pass
	filesData.sort(key=len, reverse=True)
	
	outFile = open(outputPath, 'w')
	
	for x in range(len(filesData[0])): #this will be for every item in each list (going down the rows)
		toPrint = []
		for count, item in enumerate(filesData):
			try:
				toPrint.append(item[x])
			except: 
				7*2
				pass
		toPrint = [x.strip() for x in toPrint]
		toPrint = ', '.join(toPrint)
		outFile.write(toPrint + '\n')

def combinePatientDataFiles(patPath):
	'''A function that takes detailed data files of curvaturee and combines them in an excel readable way. '''
	supPath = patPath + '\\' + patPath[-8:] + '_SupCurvaturesData.txt'
	proPath = patPath + '\\' + patPath[-8:] + '_ProCurvaturesData.txt'
	leftDownPath = patPath + '\\' + patPath[-8:] + '_LeftDownCurvaturesData.txt'
	outPath = patPath + '\\' + patPath[-8:] + '_AllCurvaturesData.txt'
	
	combineDataFiles([supPath, proPath, leftDownPath], outPath)
	
def addDetailsStackMany(inFileList, outFilePath):
	'''A function that takes detailed data files of curvaturee and combines them in an excel readable way. '''
	outFile = open(outFilePath, 'w')
	for x in inFileList:
		detailedData = []
		try:
			inFile = open(x, 'r')
			data = [x.strip() + '\n' for x in inFile.readlines()]
			#name = x[-26:] + "\n"
			for count, item in enumerate(data):
				if item != '' and item !="\n":
					detailedDatum = '{}, {}, {}'.format(count, count/(len(data)-2)*100, item)
					detailedData.append(detailedDatum)
			inFile.close()
			for x in detailedData:
				outFile.write(x)
		except:
			7*2
			pass
	outFile.close()
	
def getSumCurvatures(curvaturesList, width):
	'''A function which takes a list, and it returns a new list of equal length, where each value corresponds
	to the same indexed value in the first list, plus the all the items 'width' positions up and down the list.'''
	sumList = []
	for x in range(len(curvaturesList)):
		subList = (curvaturesList[max(x-width, 0): min(x+width+1, len(curvaturesList))])
		subList = [float(y) for y in subList]
		sumList.append(sum(subList))
	return sumList


def findLocalMaximas(inList, minDist = 0, threshold = 0):
	'''A function to return a list of the local maximas of an input list. '''
	avgCurvature = stat.mean(inList)
	localMaximas = []
	for x in range(1, len(inList)-1):
		currentThreeList = inList[x-1:x+2]
		if currentThreeList[0]<currentThreeList[1] and currentThreeList[1] > currentThreeList[2] and currentThreeList[1]> avgCurvature*threshold:
			localMaximas.append((x+1, currentThreeList[1]))
	#reprocess localMaximas:
	'''reprocessing will iterate through the list and find clusters of max points,
	where there is achain of points with less than minDist between them, and this procedss replaces this
	chain with a single point, in the middle of where the chain was. '''
	newLocalMaximas = []
	closePointsList = []
	addedOne = False
	for x, i in enumerate(localMaximas[:-1]):
		if not addedOne:
			if len(closePointsList)==0:
				pass
			elif len(closePointsList)<2:
				newLocalMaximas.append(closePointsList[0])
				closePointsList = []
			elif len(closePointsList)>1:
				newLocalMaximas.append(closePointsList[len(closePointsList)//2])
				closePointsList = []
		addedOne = False
		if closePointsList == []:
			closePointsList = [i]
		if localMaximas[x+1][0] - i[0]< minDist:
			closePointsList.append(localMaximas[x+1])
			addedOne = True
	newLocalMaximas.append(localMaximas[-1])
	return newLocalMaximas
	
def findLocalMinimas(inList, minDist = 0, threshold = 0):
	'''A function to return a list of the local minimas of an input list. '''
	avgCurvature = stat.mean(inList)
	localMinimas = []
	for x in range(1, len(inList)-1):
		currentThreeList = inList[x-1:x+2]
		if currentThreeList[0]>currentThreeList[1] and currentThreeList[1] < currentThreeList[2] and currentThreeList[1] < avgCurvature/(threshold+0.001):
			localMinimas.append((x+1, currentThreeList[1]))
	#reprocess localMinimas:
	'''reprocessing will iterate through the list and find clusters of max points,
	where there is achain of points with less than minDist between them, and this procedss replaces this
	chain with a single point, in the middle of where the chain was. '''
	newLocalMinimas = []
	closePointsList = []
	addedOne = False
	for x, i in enumerate(localMinimas[:-1]):
		if not addedOne:
			if len(closePointsList)==0:
				pass
			elif len(closePointsList)<2:
				newLocalMinimas.append(closePointsList[0])
				closePointsList = []
			elif len(closePointsList)>1:
				newLocalMinimas.append(closePointsList[len(closePointsList)//2])
				closePointsList = []
		addedOne = False
		if closePointsList == []:
			closePointsList = [i]
		if localMinimas[x+1][0] - i[0]< minDist:
			closePointsList.append(localMinimas[x+1])
			addedOne = True
	newLocalMinimas.append(localMinimas[-1])
	return newLocalMinimas

	

	
def unCluster(minList, maxList, curvatures):
	'''A function which takes a list of maximum points, a list of minimum points, and it looks for
	clusters of maximuns uninterupted with minimums, or vice versa. It replaces those clusters with a single
	point at the center of where the cluster was. Essentially, a better version of the reprocessing section of the 
	in the find local maxima function. '''
	#print('In Whole Set: ' , curvatures)
	#print('In MIN: ' , minList)
	#print('In MAX: ' , maxList)
	newMinList = []
	newMaxList = []
	extremeList = []
	
	#make a sorted list of 3key tuples, where the last item identifies max/min
	for x in maxList:
		extremeList.append((x[0], x[1], 'MAX'))
	for x in minList:
		extremeList.append((x[0], x[1], 'MIN'))
	extremeList.sort(key = itemgetter(0))
	
	running = True
	count  = 0
	while running:
		if count>=len(extremeList):
			break
		subList = [extremeList[count]]
		#look ahead as far as possible
		for x in range(1, len(curvatures)):
			#print(extremeList[count+x][2])
			#print(extremeList[count][2])
			#if the xth item after the first item is the same type (max/min)
			if count+x < len(extremeList) and extremeList[count+x][2] == extremeList[count][2]:
				subList.append(extremeList[count+x])
			else: #if the next item is a different type (max/min)
				numberList = [int(z[0]) for z in subList]
				middleNumber = int(round(stat.mean(numberList)))
				
				middlePoint = (middleNumber, curvatures[middleNumber-1], extremeList[count][2])
				if middlePoint[2]=='MAX':
					newMaxList.append(middlePoint)
				else:
					newMinList.append(middlePoint)
				count += len(subList) - 1
				#print(subList)
				break
		count+=1
	
	#remove the third item in the tuples
	newMinList = [(i[0], i[1]) for i in newMinList]
	newMaxList = [(i[0], i[1]) for i in newMaxList]
	#print('Out MIN: ', newMinList)
	#print('Out MAX: ', newMaxList)
	return newMinList, newMaxList
	
	

def addSumCurvaturesToDataFile(inPath, width = 10):
	'''A fucntion to modify a detailed data file with curvatures, by adding a column 
	that contains the sum of curvatures in a given interval for every point '''
	fIn = open(inPath, 'r')
	lines = fIn.readlines()
	fIn.close()
	title = lines[0].strip()
	curvatureValues = [x.strip().split(', ')[5] for x in lines[1:]]
	sumCurvatureValues = getSumCurvatures(curvatureValues, width)
	newLines = [title] + [lines[x].strip() + ', '  + str(sumCurvatureValues[x-1]) for x in range(1, len(sumCurvatureValues)+1)]
	fOut = open(inPath, 'w')
	for line in newLines:
		fOut.write(line + '\n')
	fOut.close()
	
def addSumCurvatureMaxMinsToDataFile(inPath, minPointDist = 0, threshold = 1, minThresholdBoost = 1.5):
	'''A function to add a column to the data file whihc indicates if the point is at a max or a min. '''
	fIn = open(inPath, 'r')
	lines = fIn.readlines()
	fIn.close()
	fIn.close()
	title = lines[0].strip()
	sumCurvatureValues = [x.strip().split(', ')[6] for x in lines[1:]]
	sumCurvatureValues = [float(y) for y in sumCurvatureValues]
	locMaximas = findLocalMaximas(sumCurvatureValues, minPointDist, threshold)
	locMinimas = findLocalMinimas(sumCurvatureValues, minPointDist, threshold * minThresholdBoost) #The minimas are currently being held at a higher threshold so the maximas are unClustered more. 
	
	#print('Calling unCluster!')
	locMinimas, locMaximas = unCluster(locMinimas, locMaximas, sumCurvatureValues)
	
	#xVals = [x.strip().split(', ')[0] for x in lines[1:]]
	#xVals = [int(x) for x in xVals]
	locExtremesColumn = []
	for x in range(1, len(lines)):
		t = (x, sumCurvatureValues[x-1])
		if t in locMaximas:
			locExtremesColumn.append('MAX')
		elif t in locMinimas:
			locExtremesColumn.append('MIN')
		else:
			locExtremesColumn.append('0')
	newLines = [title] + [lines[x].strip() + ', '  + str(locExtremesColumn[x-1]) for x in range(1, len(locExtremesColumn)+1)]
	fOut = open(inPath, 'w')
	for line in newLines:
		fOut.write(line + '\n')
	fOut.close()
	
	
def unitVector(vec):
	return vec / np.linalg.norm(vec)

	
def angleBetween(v1,v2):
	v1U = unitVector(v1)
	v2U = unitVector(v2)
	return np.arccos(np.clip(np.dot(v1U, v2U), -1.0, 1.0))

def addDegreeChangesToFile1(inPath):
	'''A function to look at every max, and make a sublist of the mins on either side.
	it then takes the vector from min1 to max, and from max to min1, and compares them,
	to find the angle change of the curve over a distance of the vector min to min. '''
	fIn = open(inPath, 'r')
	lines = fIn.readlines()
	fIn.close()
	title = lines[0].strip()
	curvatureValues = [x.strip().split(', ')[5] for x in lines[1:]]
	numVals = [x.strip().split(', ')[0] for x in lines[1:]]
	maxMinTypes = [x.strip().split(', ')[7] for x in lines[1:]]
	coords = [(x.strip().split(', ')[2], x.strip().split(', ')[3], x.strip().split(', ')[4]) for x in lines[1:]]
	
	extremePoints = []
	maxPlaces = []
	for y in range(len(lines)-1):
		if maxMinTypes[y] == 'MAX' or maxMinTypes[y] == 'MIN':
			extremePoints.append((coords[y][0], coords[y][1], coords[y][2], maxMinTypes[y], numVals[y]))
			
	angleChangeList = []
	for x in range(1, len(extremePoints)-1):
		subList = [extremePoints[x-1], extremePoints[x], extremePoints[x+1]]
		
		if subList[1][3] =='MAX':
			vecPosList = [np.array([float(z[0]), float(z[1]), float(z[2])]) for z in subList]
			vecOne = vecPosList[1] - vecPosList[0]
			vecTwo = vecPosList[2] - vecPosList[1]
			vecThree = vecPosList[2] - vecPosList[0]
			angleChange = angleBetween(vecOne, vecTwo) * 180 / np.pi 
			straightDist = np.linalg.norm(vecThree)
			
			angleChangeList.append((subList[1][4], angleChange, straightDist))
	
	#print(angleChangeList)
	angleChangeValues = []
	straightDistValues = []
	numList = [int(x[0]) for x in angleChangeList]
	for i in range(len(lines)-1):
		if i in numList:
			for x in angleChangeList:
				if int(x[0]) == i:
					angleChangeValues.append(x[1])
					straightDistValues.append(x[2])
		else:
			angleChangeValues.append('0')
			straightDistValues.append('0')
			
	
			
	
	newLines = [title] + [lines[x].strip() + ', '  + str(angleChangeValues[x-1]) + ', '  + str(straightDistValues[x-1]) for x in range(1, len(angleChangeValues)+1)]
	fOut = open(inPath, 'w')
	for line in newLines:
		fOut.write(line + '\n')
	fOut.close()


	
def addDegreeChangesToFile(inPath):
	'''This function look at every max, and makes a sublist of itself, and the minimums on either side. 
	it then akes a tangent at each minimum, and compares the change in angle from one to the other,
	saying that the line curves that x degrees over the straight line distance from Min to Min. '''
	fIn = open(inPath, 'r')
	lines = fIn.readlines()
	fIn.close()
	title = lines[0].strip()
	curvatureValues = [x.strip().split(', ')[5] for x in lines[1:]]
	numVals = [x.strip().split(', ')[0] for x in lines[1:]]
	maxMinTypes = [x.strip().split(', ')[7] for x in lines[1:]]
	coords = [(x.strip().split(', ')[2], x.strip().split(', ')[3], x.strip().split(', ')[4]) for x in lines[1:]]
	
	extremePoints = []
	maxPlaces = []
	for y in range(len(lines)-1):
		if maxMinTypes[y] == 'MAX' or maxMinTypes[y] == 'MIN':
			extremePoints.append((coords[y][0], coords[y][1], coords[y][2], maxMinTypes[y], numVals[y]))
			
	angleChangeList = []
	for x in range(1, len(extremePoints)-1):
		subList = [extremePoints[x-1], extremePoints[x], extremePoints[x+1]]
		
		if subList[1][3] =='MAX':
			leftMinForwardPointNum = int(subList[0][4])+2
			rightMinBackwardPointNum = int(subList[2][4])-2
			leftMinForwardPointCoords = np.array([float(coords[leftMinForwardPointNum][0]), float(coords[leftMinForwardPointNum][1]), float(coords[leftMinForwardPointNum][2])])
			rightMinBackwardPointCoords = np.array([float(coords[rightMinBackwardPointNum][0]), float(coords[rightMinBackwardPointNum][1]), float(coords[rightMinBackwardPointNum][2])])
			
			vecPosList = [np.array([float(z[0]), float(z[1]), float(z[2])]) for z in subList]
			
			vecOne = leftMinForwardPointCoords - vecPosList[0]
			vecTwo = vecPosList[2] - rightMinBackwardPointCoords
			
			vecThree = vecPosList[2] - vecPosList[0]
			angleChange = angleBetween(vecOne, vecTwo) * 180 / np.pi 
			straightDist = np.linalg.norm(vecThree)
			
			angleChangeList.append((subList[1][4], angleChange, straightDist))
	
	#print(angleChangeList)
	angleChangeValues = []
	straightDistValues = []
	numList = [int(x[0]) for x in angleChangeList]
	for i in range(len(lines)-1):
		if i in numList:
			for x in angleChangeList:
				if int(x[0]) == i:
					angleChangeValues.append(x[1])
					straightDistValues.append(x[2])
		else:
			angleChangeValues.append('0')
			straightDistValues.append('0')
			
	
			
	
	newLines = [title] + [lines[x].strip() + ', '  + str(angleChangeValues[x-1]) + ', '  + str(straightDistValues[x-1]) for x in range(1, len(angleChangeValues)+1)]
	fOut = open(inPath, 'w')
	for line in newLines:
		fOut.write(line + '\n')
	fOut.close()
	
	
def splitDataFileToFiles(inDataPath, inCutPointsPath):
	'''A function to take a data file, and a file containing the coords of two fiducials
	representing the cut points, first being ascending and second being descending, 
	and create three new data files as the result of splitting the large data file at
	the two cut points. '''
	
	fIn = open(inDataPath, 'r')
	lines = fIn.readlines()
	fIn.close()
	title = lines[0].strip()
	lines2 = lines[1:]
	numVals = [x.strip().split(', ')[0] for x in lines[1:]]
	maxMinTypes = [x.strip().split(', ')[7] for x in lines[1:]]
	coords = [(x.strip().split(', ')[2], x.strip().split(', ')[3], x.strip().split(', ')[4]) for x in lines[1:]]
	
	fIn = open(inCutPointsPath, 'r')
	cutPointOne = fIn.readline().strip().split(',')
	cutPointTwo = fIn.readline().strip().split(',')
	fIn.close()
	
	outAcDataPath = inDataPath[:-8] + 'AcData.txt'
	outTcDataPath = inDataPath[:-8] + 'TcData.txt'
	outDcDataPath = inDataPath[:-8] + 'DcData.txt'
	
	
	cutPointOne = np.array([float(x) for x in cutPointOne])
	cutPointTwo = np.array([float(x) for x in cutPointTwo])
	
	
	minDist = 1000000
	closestPointNum=None
	for x in range(len(coords)):
		pos = np.array([float(coords[x][0]), float(coords[x][1]), float(coords[x][2])])
		
		cutPointToCenterPoint = np.subtract(pos, cutPointOne)
		dist = np.linalg.norm(cutPointToCenterPoint)
		if dist < minDist:
			closestPointNum = x
			minDist = dist
	closestPointNumToCutOne = closestPointNum
	
	minDist = 1000000
	closestPointNum=None
	for x in range(len(coords)):
		pos = np.array([float(coords[x][0]), float(coords[x][1]), float(coords[x][2])])
		
		cutPointToCenterPoint = np.subtract(pos, cutPointTwo)
		dist = np.linalg.norm(cutPointToCenterPoint)
		if dist < minDist:
			closestPointNum = x
			minDist = dist
	closestPointNumToCutTwo = closestPointNum
	
	ascendingLines = lines2[:closestPointNumToCutOne]
	transverseLines = lines2[closestPointNumToCutOne:closestPointNumToCutTwo]
	descendingLines = lines2[closestPointNumToCutTwo:]
	
	#REVERSE data file if it is backwards
	if not transverseLines:
		lines2 = lines2[::-1]
		numVals = [x.strip().split(', ')[0] for x in lines2[1:]]
		maxMinTypes = [x.strip().split(', ')[7] for x in lines2[1:]]
		coords = [(x.strip().split(', ')[2], x.strip().split(', ')[3], x.strip().split(', ')[4]) for x in lines2[1:]]
	
		minDist = 1000000
		closestPointNum=None
		for x in range(len(coords)):
			pos = np.array([float(coords[x][0]), float(coords[x][1]), float(coords[x][2])])
		
			cutPointToCenterPoint = np.subtract(pos, cutPointOne)
			dist = np.linalg.norm(cutPointToCenterPoint)
			if dist < minDist:
				closestPointNum = x
				minDist = dist
		closestPointNumToCutOne = closestPointNum
		
		minDist = 1000000
		closestPointNum=None
		for x in range(len(coords)):
			pos = np.array([float(coords[x][0]), float(coords[x][1]), float(coords[x][2])])
		
			cutPointToCenterPoint = np.subtract(pos, cutPointTwo)
			dist = np.linalg.norm(cutPointToCenterPoint)
			if dist < minDist:
				closestPointNum = x
				minDist = dist
		closestPointNumToCutTwo = closestPointNum
		
		ascendingLines = lines2[:closestPointNumToCutOne]
		transverseLines = lines2[closestPointNumToCutOne:closestPointNumToCutTwo]
		descendingLines = lines2[closestPointNumToCutTwo:]
	
	
	acOut = open(outAcDataPath, 'w')
	acOut.write(title +'\n')
	for line in ascendingLines:
		acOut.write(line)
	acOut.close()
	
	tcOut = open(outTcDataPath, 'w')
	tcOut.write(title +'\n')
	for line in transverseLines:
		tcOut.write(line)
	tcOut.close()
	
	dcOut = open(outDcDataPath, 'w')
	dcOut.write(title +'\n')
	for line in descendingLines:
		dcOut.write(line)
	dcOut.close()
	
	
	
def splitPatientDataFilesToFiles(patPath):
	'''A fucntion to call the split data set function for a patient's data files. '''
	supDataPath = os.path.join(patPath, patPath[-8:]+'_SupCurvaturesData.txt')
	proDataPath = os.path.join(patPath, patPath[-8:]+'_ProCurvaturesData.txt')
	
	supCutPath = os.path.join(patPath, patPath[-8:]+'_SupCutPoints.txt')
	proCutPath = os.path.join(patPath, patPath[-8:]+'_ProCutPoints.txt')
	
	splitDataFileToFiles(supDataPath, supCutPath)
	splitDataFileToFiles(proDataPath, proCutPath)
	
	

#splitDataFileToFiles(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013\TEST0013_SupCurvaturesData.txt", r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013\TEST0013_SupCutPoints.txt")
	
	
	
	
	

def doAllProcessing(inPath, sumSampleWidth = 0, minMaxPointDist = 0, threshold = 1, minThresholdBoost = 1.5):
	'''A function to do all post slicer processing and generate a data file with point number, point
	coords, point % of length, curvature, local curvature sum, max/min...'''
	outPath = inPath[:-4] + 'Data.txt'
	addDetails(inPath, outPath)
	addSumCurvaturesToDataFile(outPath, sumSampleWidth)
	addSumCurvatureMaxMinsToDataFile(outPath, minMaxPointDist, threshold, minThresholdBoost)
	addDegreeChangesToFile(outPath)
	

	
	
#doAllProcessing(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvatures.txt")
a = [0,1,0, 3, 4, 5, 3, 6, 7, 8, 7, 6, 7, 5, 9, 9, 9, 0, 1]

#addDetails(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvatures.txt", r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvaturesTest.txt")
pathOne = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvatures.txt"
pathTwo = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\Current\Curvatures.txt"
pathThree = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_ProCurvatures.txt"
pathLD = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_LeftDownCurvatures.txt"
#doAllProcessing(pathOne, 0, 0, 1, 1.5)

	
		
		

patList = [r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAT0093",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBB0002",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBB0024",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBC0016",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBC0017",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBD0033",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBG0026",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAF0056",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAJ0023",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAJ0095",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAM0029",
r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTAP0049"]

supFilesList = [x + '\\' + x[-8:] + '_SupCurvaturesData.txt' for x in patList]
proFilesList = [x + '\\' + x[-8:] + '_ProCurvaturesData.txt' for x in patList]
leftDownFilesList = [x + '\\' + x[-8:] + '_LeftDownCurvaturesData.txt' for x in patList]
outFilePath = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\AllData.txt"

allFilesList = supFilesList + proFilesList + leftDownFilesList


