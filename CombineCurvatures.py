import itertools


fileList = [r"C:\Users\jaker\Documents\ColonCurves_JL\CtVolumes\AllCurvatureTextFiles\PTAF0056_SupCurvatures.txt",
r"C:\Users\jaker\Documents\ColonCurves_JL\CtVolumes\AllCurvatureTextFiles\PTAF0056_ProCurvatures.txt"]

def combineData(fileList, outputPath):

	masterCurvatures = open(outputPath, 'w')
	for path in fileList:
		inFile = open(path, 'r')
		data = inFile.readlines()
		masterCurvatures.write(path[-26:] + "\n")
		for count, item in enumerate(data):
			if item != '' and item !="\n":
				masterCurvatures.write('{}, {}, {}'.format(count, count/(len(data)-2)*100, item))
		#masterCurvatures.write('***' + "\n")
		inFile.close()
		
	masterCurvatures.close()

	
def combineManyData(pathList, outputPath):
	masterCurvatures = open(outputPath, 'w')
	data = []
	maxLength = 0
	for file in pathList:
		inFile = open(file, 'r')
		lines = inFile.readlines()
		maxLength = max(maxLength, len(lines))
		data.append(lines)
		inFile.close()
	swappedList = [list(x) for x in itertools.zip_longest(fillvalue = '-')]
	
	for rowNum in range(len(swappedList[0])):
		for columnNum in range(len(swappedList[0])-1):
			line = ','.join(swappedList[rowNum])
			masterCurvatures.write(line)
	masterCurvatures.close()
	
def combineManyData(pathList, outputPath):
	masterCurvatures = open(outputPath, 'w')
	maxLen = 0
	listList = []
	for x in pathList:
		file = open(x, 'r')
		lines = file.readlines()
		maxLen = max(maxLen, len(lines))
		listList.append(lines)
		file.close()
		
	newListList = []
	currentList = listList[0]
	while len(currentList)<maxLen:
		currentList.append('*')
	newListList.append(currentList)
	
	for x in range(1, len(listList)):
		currentList = listList[x]
		while len(currentList)<maxLen:
			currentList.append('*')
		newListList.append(currentList)
	
	lastList = [','.join(x) for x in newListList]
	
	for y in lastList:
		masterCurvatures.write(y)
	
def combineData2(pathList, outputPath):
	masterCurvatures = open(outputPath, 'w')
	file1 = open(pathList[0], 'r')
	file2 = open(pathList[1], 'r')
	lines1 = file1.readlines()
	lines2 = file2.readlines()
	
	maxLength = min(len(lines1), len(lines2))
	
	for x in range(maxLength):
		masterCurvatures.write('{}, {}, {}'.format(x, x/(len(lines1))*100, lines1[x].strip())    +   ', {}, {}, {}'.format(x, x/(len(lines2))*100, lines2[x]))
		

	
combineData(fileList, r"C:\Users\jaker\Documents\ColonCurves_JL\CtVolumes\MasterCurvatures.txt")

