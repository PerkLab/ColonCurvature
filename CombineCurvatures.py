masterCurvatures = open(r"C:\Users\jaker\Documents\ColonCurves_JL\CtVolumes\MasterCurvatures.txt", 'w')

fileList = [r"C:\Users\jaker\Documents\ColonCurves_JL\CtVolumes\PTAF0056_ProCurvatures.txt",
r"C:\Users\jaker\Documents\ColonCurves_JL\CtVolumes\PTAF0056_SupCurvatures.txt"]

for path in fileList:
	inFile = open(path, 'r')
	data = inFile.readlines()
	masterCurvatures.write(path[-22:] + "\n")
	for count, item in enumerate(data):
		if item != '' and item !="\n":
			masterCurvatures.write('{}, {}, {}'.format(count, count/(len(data)-2)*100, item))
	#masterCurvatures.write('***' + "\n")
	inFile.close()
	
masterCurvatures.close()
