def addPctCount(inPath, outputPath):
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
	
#addPctCount(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBD0033\PTBD0033_ProCurvatures.txt",r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBD0033\testing.txt")

def addManyPctCount(inPathList):
	for path in inPathList:
		try:
			outPath = path[:-4] + 'Data.txt'
			addPctCount(path, outPath)
			#print('In: {} \n Out: {}'.format(path, outPath))
		except:
			pass


		
#fileList = [r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBD0033\PTBD0033_ProCurvatures.txt",
#r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBD0033\PTBD0033_SupCurvatures.txt"]

idList = ['PTAF0056', 'PTAJ0023', 'PTAJ0095', 'PTAM0029', 'PTAP0049', 'PTAT0093', 'PTBB0002', 'PTBB0024', 'PTBC0016', 'PTBC0017', 'PTBD0033', 'PTBG0026', 'TEST0012']
#idList = idList[:2]

fileListPro = ["C:\\Users\\jlaframboise\\Documents\\ColonCurves_JL\CtVolumes\\" + id + "\\" + id + "_ProCurvatures.txt" for id in idList]
fileListSup = ["C:\\Users\\jlaframboise\\Documents\\ColonCurves_JL\CtVolumes\\" + id + "\\" + id + "_SupCurvatures.txt" for id in idList]
fileListLeftDown = ["C:\\Users\\jlaframboise\\Documents\\ColonCurves_JL\CtVolumes\\" + id + "\\" + id + "_LeftDownCurvatures.txt" for id in idList]

#print(fileList)

addManyPctCount(fileListPro)

addManyPctCount(fileListSup)

addManyPctCount(fileListLeftDown)
