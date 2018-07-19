def addDetails(inPath, outputPath):
	'''A function that takes the path of a text file and creates a new text file with the point number,
	and the percentage of how far the point is along the list. Easy to import to Excel'''
	inFile = open(inPath, 'r')
	data = inFile.readlines()
	outFile = open(outputPath, 'w')
	outFile.write(inPath[-26:] + "\n")
	for count, item in enumerate(data):
		if item != '' and item !="\n":
			outFile.write('{}, {}, {}'.format(count, count/(len(data)-2)*100, item))
	#outFile.write('***' + "\n")
	inFile.close()
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
combineDataFiles(allFilesList, outFilePath)

		
		

#The following 6 lines create more detailed data files for all the patients:
#idList = ['PTAF0056', 'PTAJ0023', 'PTAJ0095', 'PTAM0029', 'PTAP0049', 'PTAT0093', 'PTBB0002', 'PTBB0024', 'PTBC0016', 'PTBC0017', 'PTBD0033', 'PTBG0026', 'TEST0012']
#fileListPro = ["C:\\Users\\jlaframboise\\Documents\\ColonCurves_JL\CtVolumes\\" + id + "\\" + id + "_ProCurvatures.txt" for id in idList]
#fileListSup = ["C:\\Users\\jlaframboise\\Documents\\ColonCurves_JL\CtVolumes\\" + id + "\\" + id + "_SupCurvatures.txt" for id in idList]
#fileListLeftDown = ["C:\\Users\\jlaframboise\\Documents\\ColonCurves_JL\CtVolumes\\" + id + "\\" + id + "_LeftDownCurvatures.txt" for id in idList]
#addManyDetails(fileListPro)
#addManyDetails(fileListSup)
#addManyDetails(fileListLeftDown)
