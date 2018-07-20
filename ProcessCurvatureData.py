import statistics as stat



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
	for path in inPathList:
		try:
			outPath = path[:-4] + 'Data.txt'
			addDetails(path, outPath)
			#print('In: {} \n Out: {}'.format(path, outPath))
		except:
			pass

def combineDataFiles(inFileList, outputPath):
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
	supPath = patPath + '\\' + patPath[-8:] + '_SupCurvaturesData.txt'
	proPath = patPath + '\\' + patPath[-8:] + '_ProCurvaturesData.txt'
	leftDownPath = patPath + '\\' + patPath[-8:] + '_LeftDownCurvaturesData.txt'
	outPath = patPath + '\\' + patPath[-8:] + '_AllCurvaturesData.txt'
	
	combineDataFiles([supPath, proPath, leftDownPath], outPath)
	
def addDetailsStackMany(inFileList, outFilePath):
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

def findLocalMaximas(inList, minDist = 11):
	'''A function to return a list of the local maximas of an input list. '''
	avgCurvature = stat.mean(inList)
	localMaximas = []
	for x in range(1, len(inList)-1):
		currentThreeList = inList[x-1:x+2]
		if currentThreeList[0]<currentThreeList[1] and currentThreeList[1] > currentThreeList[2] and currentThreeList[1]> avgCurvature:
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
	return newLocalMaximas

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
	
def addSumCurvatureMaximumsToDataFile(inPath):
	fIn = open(inPath, 'r')
	lines = fIn.readlines()
	fIn.close()
	title = lines[0].strip()
	sumCurvatureValues = [x.strip().split(', ')[6] for x in lines[1:]]
	sumCurvatureValues = [float(y) for y in sumCurvatureValues]
	locMaximas = findLocalMaximas(sumCurvatureValues)
	#xVals = [x.strip().split(', ')[0] for x in lines[1:]]
	#xVals = [int(x) for x in xVals]
	locMaximasColumn = []
	for x in range(1, len(lines)):
		t = (x, sumCurvatureValues[x-1])
		if t in locMaximas:
			locMaximasColumn.append('MAX')
		else:
			locMaximasColumn.append('0')
	newLines = [title] + [lines[x].strip() + ', '  + str(locMaximasColumn[x-1]) for x in range(1, len(locMaximasColumn)+1)]
	fOut = open(inPath, 'w')
	for line in newLines:
		fOut.write(line + '\n')
	fOut.close()
	
	

def doAllProcessing(inPath, sumSampleWidth = 300):
	outPath = inPath[:-4] + 'Data.txt'
	addDetails(inPath, outPath)
	addSumCurvaturesToDataFile(outPath, sumSampleWidth)
	addSumCurvatureMaximumsToDataFile(outPath)

	
	
#doAllProcessing(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvatures.txt")
a = [0,1,0, 3, 4, 5, 3, 6, 7, 8, 7, 6, 7, 5, 9, 9, 9, 0, 1]

#addDetails(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvatures.txt", r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvaturesTest.txt")
doAllProcessing(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvaturesCopy.txt", 0)

#addDetails(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvatures.txt", r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvaturesData.txt")

#addSumCurvatureMaximumsToDataFile(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0012\TEST0012_SupCurvaturesData.txt")
	
#The following 5 lines of code will create a combined data file for each patient with all their scans. 
#idList = ['PTAF0056', 'PTAJ0023', 'PTAJ0095', 'PTAM0029', 'PTAP0049', 'PTAT0093', 'PTBB0002', 'PTBB0024', 'PTBC0016', 'PTBC0017', 'PTBD0033', 'PTBG0026', 'TEST0012']
#directory = r'C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\\' 
#for id in idList:
	#patPath = directory + id
	#combinePatientDataFiles(patPath)
		
		

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

#print(allFilesList)
#combineDataFiles(allFilesList, outFilePath)



#addDetailsStackMany(supFilesList, r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\AllSupDataStacked.txt")
		

#The following 6 lines create more detailed data files for all the patients:
#idList = ['PTAF0056', 'PTAJ0023', 'PTAJ0095', 'PTAM0029', 'PTAP0049', 'PTAT0093', 'PTBB0002', 'PTBB0024', 'PTBC0016', 'PTBC0017', 'PTBD0033', 'PTBG0026', 'TEST0012']
#fileListPro = ["C:\\Users\\jlaframboise\\Documents\\ColonCurves_JL\CtVolumes\\" + id + "\\" + id + "_ProCurvatures.txt" for id in idList]
#fileListSup = ["C:\\Users\\jlaframboise\\Documents\\ColonCurves_JL\CtVolumes\\" + id + "\\" + id + "_SupCurvatures.txt" for id in idList]
#fileListLeftDown = ["C:\\Users\\jlaframboise\\Documents\\ColonCurves_JL\CtVolumes\\" + id + "\\" + id + "_LeftDownCurvatures.txt" for id in idList]
#addManyDetails(fileListPro)
#addManyDetails(fileListSup)
#addManyDetails(fileListLeftDown)
