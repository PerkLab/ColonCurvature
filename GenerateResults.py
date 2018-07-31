'''A file which will hold the functions to process the data from the centerline analysis into more and more
relevant forms. '''

import statistics as stat
from operator import itemgetter
import os
import math


def getStats(dataInPath):
    '''A function that takes a created data file, and calculates certain statistics
    which it outputs to a results data file'''
    fIn = open(dataInPath, 'r')
    lines = fIn.readlines()
    fIn.close()
    dataOutPath = dataInPath[:-4] + 'Results.txt'
    title = lines[0].strip()
    curvatureValues = [float(x.strip().split(', ')[5]) for x in lines[1:]]
    maxMinTypes = [x.strip().split(', ')[7] for x in lines[1:]]
    maxDegrees = [float(x.strip().split(', ')[8]) for x in lines[1:]]
    maxDistances = [float(x.strip().split(', ')[9]) for x in lines[1:]]

    meanCuvature = stat.mean(curvatureValues)
    medianCurvature = stat.median(curvatureValues)
    # modeCurvature = stat.mode(curvatureValues)
    # print(curvatureValues)
    stanDevCurvature = stat.pstdev(curvatureValues)
    varianceCurvature = stat.pvariance(curvatureValues)
    totalCurvature = sum(curvatureValues)

    curveNumbers = []
    for x in range(len(maxMinTypes)):
        if maxMinTypes[x] == 'MAX' and maxDegrees[x] > 0:
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
        allCurveRatios.append(maxDegrees[x] / maxDistances[x])

        if maxDegrees[x] < 20:
            lessThan20Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x] / maxDistances[x]))
        elif maxDegrees[x] < 40:
            lessThan40Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x] / maxDistances[x]))
        elif maxDegrees[x] < 60:
            lessThan60Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x] / maxDistances[x]))
        elif maxDegrees[x] < 80:
            lessThan80Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x] / maxDistances[x]))
        elif maxDegrees[x] < 100:
            lessThan100Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x] / maxDistances[x]))
        elif maxDegrees[x] < 120:
            lessThan120Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x] / maxDistances[x]))
        elif maxDegrees[x] < 140:
            lessThan140Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x] / maxDistances[x]))
        elif maxDegrees[x] < 160:
            lessThan160Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x] / maxDistances[x]))
        elif maxDegrees[x] < 180:
            lessThan180Deg.append((maxDegrees[x], maxDistances[x], maxDegrees[x] / maxDistances[x]))

        allCurves.append((x, maxDegrees[x] / maxDistances[x], maxDegrees[x], maxDistances[x]))

    allCurves = sorted(allCurves, key=itemgetter(1))

    lessThan20DegDists = [str(x[1]) for x in sorted(lessThan20Deg, key=itemgetter(1))]
    lessThan40DegDists = [str(x[1]) for x in sorted(lessThan40Deg, key=itemgetter(1))]
    lessThan60DegDists = [str(x[1]) for x in sorted(lessThan60Deg, key=itemgetter(1))]
    lessThan80DegDists = [str(x[1]) for x in sorted(lessThan80Deg, key=itemgetter(1))]
    lessThan100DegDists = [str(x[1]) for x in sorted(lessThan100Deg, key=itemgetter(1))]
    lessThan120DegDists = [str(x[1]) for x in sorted(lessThan120Deg, key=itemgetter(1))]
    lessThan140DegDists = [str(x[1]) for x in sorted(lessThan140Deg, key=itemgetter(1))]
    lessThan160DegDists = [str(x[1]) for x in sorted(lessThan160Deg, key=itemgetter(1))]
    lessThan180DegDists = [str(x[1]) for x in sorted(lessThan180Deg, key=itemgetter(1))]

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
    # linesOut.append('Mode Curvature, {}'.format(modeCurvature))
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
    '''A function whihc takes the path to a patients data folder, and generates a file comparing the patients'
    supine and prone scans. '''
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

    for y in range(0, 5):
        outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1],
                                          proLines[y].strip().split(', ')[1]))

    outLines.append(supLines[5].strip())

    for y in range(6, 12):
        outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1],
                                          proLines[y].strip().split(', ')[1]))

    outLines.append(supLines[12].strip())

    for y in range(13, 38, 3):
        outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1],
                                          proLines[y].strip().split(', ')[1]))
        outLines.append(
            '{},{},{}'.format(supLines[y + 1].strip().split(', ')[0], supLines[y + 1].strip().split(', ')[1],
                              proLines[y + 1].strip().split(', ')[1]))

    outPath = os.path.join(patPath, patPath[-8:] + '_BothCurvaturesDataResults.txt')
    fOut = open(outPath, 'w')

    for x in outLines:
        fOut.write(x + '\n')

    fOut.close()


def getDataLines(supPath, proPath, patId, section):
    '''A function for use by other functions which will grab the statistics from a results file for comparison. '''
    supIn = open(supPath, 'r')
    supLines = supIn.readlines()
    supIn.close()
    proIn = open(proPath, 'r')
    proLines = proIn.readlines()
    proIn.close()

    outLines = []
    outLines.append('{} {},Supine,Prone'.format(patId, section))

    for y in range(0, 5):
        outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1],
                                          proLines[y].strip().split(', ')[1]))

    outLines.append(supLines[5].strip())

    for y in range(6, 12):
        outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1],
                                          proLines[y].strip().split(', ')[1]))

    outLines.append(supLines[12].strip())

    for y in range(13, 38, 3):
        outLines.append('{},{},{}'.format(supLines[y].strip().split(', ')[0], supLines[y].strip().split(', ')[1],
                                          proLines[y].strip().split(', ')[1]))
        outLines.append(
            '{},{},{}'.format(supLines[y + 1].strip().split(', ')[0], supLines[y + 1].strip().split(', ')[1],
                              proLines[y + 1].strip().split(', ')[1]))

    return outLines


def comparePatientResults(patPath):
    '''A function that will compare the supine and prone, Ac, Tc, Dc segments of the data. '''
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

    outPath = os.path.join(patPath, patPath[-8:] + '_PatientCurvatureComparison.txt')
    fOut = open(outPath, 'w')

    for x in outLinesAll:
        fOut.write(x + '\n')

    fOut.close()


class Patient():
    '''A class to hold raw data lines from the results file. For use in other functions, like comparing many patients below. '''

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
                7 * 2

        self.textLines = []
        for x in self.lines[0:32]:
            text = x.split(',')[0]
            if text != '' and text != '\n':
                self.textLines.append(text)

        self.acData = []
        for x in self.lines[33:65]:
            try:
                self.acData.append((float(x.split(',')[1]), float(x.split(',')[2])))
            except:
                7 * 2
                pass

        self.tcData = []
        for x in self.lines[66:98]:
            try:
                self.tcData.append((float(x.split(',')[1]), float(x.split(',')[2])))
            except:
                7 * 2
                pass

        self.dcData = []
        for x in self.lines[99:131]:
            try:
                self.dcData.append((float(x.split(',')[1]), float(x.split(',')[2])))
            except:
                7 * 2
                pass




def makeAverageLists(patientPathList):
    '''A function to get the data from a patient's data path
    and get all average stats in both supine and prone positions. '''
    patientList = [Patient(x) for x in patientPathList]
    idList = [patient.patId for patient in patientList]

    textList = patientList[0].textLines

    allWholeDataList = []

    for x in range(len(patientList[0].wholeData)):
        supList = [patient.wholeData[x][0] for patient in patientList]
        proList = [patient.wholeData[x][1] for patient in patientList]
        supMean = stat.mean(supList)
        proMean = stat.mean(proList)
        # print((supMean, proMean))
        allWholeDataList.append((supMean, proMean))
        if 'Number of curves <' in textList[x+1]:
            supDev = stat.stdev(supList)
            proDev = stat.stdev(proList)
            standardErrorSup = supDev/math.sqrt(len(supList))
            standardErrorPro = proDev / math.sqrt(len(proList))
            allWholeDataList.append((standardErrorSup, standardErrorPro))

    allAcDataList = []

    for x in range(len(patientList[0].acData)):
        supList = [patient.acData[x][0] for patient in patientList]
        proList = [patient.acData[x][1] for patient in patientList]
        supMean = stat.mean(supList)
        proMean = stat.mean(proList)
        allAcDataList.append((supMean, proMean))
        if 'Number of curves <' in textList[x+1]:
            supDev = stat.stdev(supList)
            proDev = stat.stdev(proList)
            standardErrorSup = supDev / math.sqrt(len(supList))
            standardErrorPro = proDev / math.sqrt(len(proList))
            allAcDataList.append((standardErrorSup, standardErrorPro))

    allTcDataList = []

    for x in range(len(patientList[0].tcData)):
        supList = [patient.tcData[x][0] for patient in patientList]
        proList = [patient.tcData[x][1] for patient in patientList]
        supMean = stat.mean(supList)
        proMean = stat.mean(proList)
        allTcDataList.append((supMean, proMean))
        if 'Number of curves <' in textList[x+1]:
            supDev = stat.stdev(supList)
            proDev = stat.stdev(proList)
            standardErrorSup = supDev / math.sqrt(len(supList))
            standardErrorPro = proDev / math.sqrt(len(proList))
            allTcDataList.append((standardErrorSup, standardErrorPro))

    allDcDataList = []

    for x in range(len(patientList[0].dcData)):
        supList = [patient.dcData[x][0] for patient in patientList]
        proList = [patient.dcData[x][1] for patient in patientList]
        supMean = stat.mean(supList)
        proMean = stat.mean(proList)
        allDcDataList.append((supMean, proMean))
        if 'Number of curves <' in textList[x+1]:
            supDev = stat.stdev(supList)
            proDev = stat.stdev(proList)
            standardErrorSup = supDev / math.sqrt(len(supList))
            standardErrorPro = proDev / math.sqrt(len(proList))
            allDcDataList.append((standardErrorSup, standardErrorPro))

    for x,i in enumerate(textList):
        if 'Number of curves <' in i:
            textList.insert(x+1, 'Stan Err Mean of Number of Curves ^')
    # for x in range(len(allWholeDataList)):
    # print(textList[x], end = ' ')
    # print(allWholeDataList[x], end = ' ')
    # print(allAcDataList[x], end = ' ')
    # print(allTcDataList[x], end = ' ')
    # print(allDcDataList[x])


    for x in range(len(allWholeDataList)):
        print('{}, {}'.format(textList[x+1], allWholeDataList[x]))
    #print(allWholeDataList)

    return textList, allWholeDataList, allAcDataList, allTcDataList, allDcDataList, idList




#pathList = [r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBD0033",
#r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\PTBG0026"]
#a,b,c,d,e,f = makeAverageLists(pathList)
#print(len(b))
#print(len(c))

def outputAverageListsToOnePrintReadyList(textLines, allWholeDataList, allAcDataList, allTcDataList, allDcDataList,
                                          idList):
    '''A function to combine a number of data types into one printable list. '''
    outLines = []
    outLines.append(','.join(idList))

    for x in range(len(allWholeDataList)):
        line = '{},{},{}'.format(textLines[x + 1], allWholeDataList[x][0], allWholeDataList[x][1])
        outLines.append(line)

    for x in range(len(allAcDataList)):
        line = '{},{},{}'.format(textLines[x + 1], allAcDataList[x][0], allAcDataList[x][1])
        outLines.append(line)

    for x in range(len(allTcDataList)):
        line = '{},{},{}'.format(textLines[x + 1], allTcDataList[x][0], allTcDataList[x][1])
        outLines.append(line)

    for x in range(len(allDcDataList)):
        line = '{},{},{}'.format(textLines[x + 1], allDcDataList[x][0], allDcDataList[x][1])
        outLines.append(line)

    return outLines


def doFinalAverageComparison(patientPathList, outputPath):
    '''A function to call the above two functions on a series of patient data paths.
    This will ouput to one data file for a detailed comaprison of segments in both positions'''
    textLines, allWholeDataList, allAcDataList, allTcDataList, allDcDataList, idList = makeAverageLists(patientPathList)

    toPrintList = outputAverageListsToOnePrintReadyList(textLines, allWholeDataList, allAcDataList, allTcDataList,
                                                        allDcDataList, idList)

    addSpaceList = [4, 28, 33, 56, 62, 84]

    fOut = open(outputPath, 'w')
    for x, i in enumerate(toPrintList):
        if i.strip().split(',')[0] == 'Mean Curvature' and x > 0 or i.strip().split(',')[0] == 'Number of Curves':
            fOut.write('\n')
        fOut.write(i + '\n')
    fOut.close()


def removeBlanksFromList(myList):
    '''A function ot remove any useless spaces or line breaks from a list'''
    newList = []
    for x, i in enumerate(myList):
        if i != '' and i != ' ' and i != '\n' and i != ' \n' and i != '\n':
            newList.append(i)
    return newList


class DetailedPatient():
    '''A class to hold all of the curvature data of a patient. '''

    def __init__(self, patientPath):
        self.path = patientPath
        self.patId = self.path[-8:]

        self.supAllPath = os.path.join(self.path, self.patId + '_SupCurvaturesDataResults.txt')
        fIn = open(self.supAllPath)
        self.supAllLines = fIn.readlines()
        fIn.close()
        self.supAllLines = removeBlanksFromList(self.supAllLines[43:])

        self.supAcPath = os.path.join(self.path, self.patId + '_SupCurvaturesAcDataResults.txt')
        fIn = open(self.supAcPath)
        self.supAcLines = fIn.readlines()
        fIn.close()
        self.supAcLines = removeBlanksFromList(self.supAcLines[43:])

        self.supTcPath = os.path.join(self.path, self.patId + '_SupCurvaturesTcDataResults.txt')
        fIn = open(self.supTcPath)
        self.supTcLines = fIn.readlines()
        fIn.close()
        self.supTcLines = removeBlanksFromList(self.supTcLines[43:])

        self.supDcPath = os.path.join(self.path, self.patId + '_SupCurvaturesDcDataResults.txt')
        fIn = open(self.supDcPath)
        self.supDcLines = fIn.readlines()
        fIn.close()
        self.supDcLines = removeBlanksFromList(self.supDcLines[43:])

        self.proAllPath = os.path.join(self.path, self.patId + '_ProCurvaturesDataResults.txt')
        fIn = open(self.proAllPath)
        self.proAllLines = fIn.readlines()
        fIn.close()
        self.proAllLines = removeBlanksFromList(self.proAllLines[43:])

        self.proAcPath = os.path.join(self.path, self.patId + '_ProCurvaturesAcDataResults.txt')
        fIn = open(self.proAcPath)
        self.proAcLines = fIn.readlines()
        fIn.close()
        self.proAcLines = removeBlanksFromList(self.proAcLines[43:])

        self.proTcPath = os.path.join(self.path, self.patId + '_ProCurvaturesTcDataResults.txt')
        fIn = open(self.proTcPath)
        self.proTcLines = fIn.readlines()
        fIn.close()
        self.proTcLines = removeBlanksFromList(self.proTcLines[43:])

        self.proDcPath = os.path.join(self.path, self.patId + '_ProCurvaturesDcDataResults.txt')
        fIn = open(self.proDcPath)
        self.proDcLines = fIn.readlines()
        fIn.close()
        self.proDcLines = removeBlanksFromList(self.proDcLines[43:])

        # print(float(self.proAllLines[0].strip().split(', ')[2]))
        self.proAllRatios, self.proAllDegs, self.proAllDistances = [float(line.strip().split(', ')[0]) for line in
                                                                    self.proAllLines], [
                                                                       float(line.strip().split(', ')[2]) for line in
                                                                       self.proAllLines], [
                                                                       float(line.strip().split(', ')[3]) for line in
                                                                       self.proAllLines]
        self.proAcRatios, self.proAcDegs, self.proAcDistances = [float(line.strip().split(', ')[0]) for line in
                                                                 self.proAcLines], [float(line.strip().split(', ')[2])
                                                                                    for line in self.proAcLines], [
                                                                    float(line.strip().split(', ')[3]) for line in
                                                                    self.proAcLines]
        self.proTcRatios, self.proTcDegs, self.proTcDistances = [float(line.strip().split(', ')[0]) for line in
                                                                 self.proTcLines], [float(line.strip().split(', ')[2])
                                                                                    for line in self.proTcLines], [
                                                                    float(line.strip().split(', ')[3]) for line in
                                                                    self.proTcLines]
        self.proDcRatios, self.proDcDegs, self.proDcDistances = [float(line.strip().split(', ')[0]) for line in
                                                                 self.proDcLines], [float(line.strip().split(', ')[2])
                                                                                    for line in self.proDcLines], [
                                                                    float(line.strip().split(', ')[3]) for line in
                                                                    self.proDcLines]

        self.supAllRatios, self.supAllDegs, self.supAllDistances = [float(line.strip().split(', ')[0]) for line in
                                                                    self.supAllLines], [
                                                                       float(line.strip().split(', ')[2]) for line in
                                                                       self.supAllLines], [
                                                                       float(line.strip().split(', ')[3]) for line in
                                                                       self.supAllLines]
        self.supAcRatios, self.supAcDegs, self.supAcDistances = [float(line.strip().split(', ')[0]) for line in
                                                                 self.supAcLines], [float(line.strip().split(', ')[2])
                                                                                    for line in self.supAcLines], [
                                                                    float(line.strip().split(', ')[3]) for line in
                                                                    self.supAcLines]
        self.supTcRatios, self.supTcDegs, self.supTcDistances = [float(line.strip().split(', ')[0]) for line in
                                                                 self.supTcLines], [float(line.strip().split(', ')[2])
                                                                                    for line in self.supTcLines], [
                                                                    float(line.strip().split(', ')[3]) for line in
                                                                    self.supTcLines]
        self.supDcRatios, self.supDcDegs, self.supDcDistances = [float(line.strip().split(', ')[0]) for line in
                                                                 self.supDcLines], [float(line.strip().split(', ')[2])
                                                                                    for line in self.supDcLines], [
                                                                    float(line.strip().split(', ')[3]) for line in
                                                                    self.supDcLines]

        self.curveCountSupAll = len(self.supAllLines)
        self.curveCountSupAc = len(self.supAcLines)
        self.curveCountSupTc = len(self.supTcLines)
        self.curveCountSupDc = len(self.supDcLines)

        self.curveCountProAll = len(self.proAllLines)
        self.curveCountProAc = len(self.proAcLines)
        self.curveCountProTc = len(self.proTcLines)
        self.curveCountProDc = len(self.proDcLines)

        self.bigSupAllCount = [1 if x > 60 else 0 for x in self.supAllDegs]
        self.bigSupAllCount = str(sum(self.bigSupAllCount))
        self.bigSupAcCount = [1 if x > 60 else 0 for x in self.supAcDegs]
        self.bigSupAcCount = str(sum(self.bigSupAcCount))
        self.bigSupTcCount = [1 if x > 60 else 0 for x in self.supTcDegs]
        self.bigSupTcCount = str(sum(self.bigSupTcCount))
        self.bigSupDcCount = [1 if x > 60 else 0 for x in self.supDcDegs]
        self.bigSupDcCount = str(sum(self.bigSupDcCount))

        self.bigProAllCount = [1 if x > 60 else 0 for x in self.proAllDegs]
        self.bigProAllCount = str(sum(self.bigProAllCount))
        self.bigProAcCount = [1 if x > 60 else 0 for x in self.proAcDegs]
        self.bigProAcCount = str(sum(self.bigProAcCount))
        self.bigProTcCount = [1 if x > 60 else 0 for x in self.proTcDegs]
        self.bigProTcCount = str(sum(self.bigProTcCount))
        self.bigProDcCount = [1 if x > 60 else 0 for x in self.proDcDegs]
        self.bigProDcCount = str(sum(self.bigProDcCount))

        self.supAllMeanDegrees = stat.mean(self.supAllDegs)
        self.supAcMeanDegrees = stat.mean(self.supAcDegs)
        self.supTcMeanDegrees = stat.mean(self.supTcDegs)
        self.supDcMeanDegrees = stat.mean(self.supDcDegs)
        self.proAllMeanDegrees = stat.mean(self.proAllDegs)
        self.proAcMeanDegrees = stat.mean(self.proAcDegs)
        self.proTcMeanDegrees = stat.mean(self.proTcDegs)
        self.proDcMeanDegrees = stat.mean(self.proDcDegs)


# d = DetailedPatient(r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013")

def arrangeDataForTTable(patientPathList, outPath):
    '''A fucntion to use the detailedPatient class to generate a text file with the
    ratio of degrees/distance for every curve, for all 8 sets of curves
    to be analyzed in a t-taple and the p value to be determined. '''
    detailedPatientList = [DetailedPatient(x) for x in patientPathList]
    allSupAllRatios = []
    allSupAcRatios = []
    allSupTcRatios = []
    allSupDcRatios = []

    allProAllRatios = []
    allProAcRatios = []
    allProTcRatios = []
    allProDcRatios = []

    for x in detailedPatientList:
        allSupAllRatios += [str(y) for y in x.supAllRatios]
        allSupAcRatios += [str(y) for y in x.supAcRatios]
        allSupTcRatios += [str(y) for y in x.supTcRatios]
        allSupDcRatios += [str(y) for y in x.supDcRatios]
        allProAllRatios += [str(y) for y in x.proAllRatios]
        allProAcRatios += [str(y) for y in x.proAcRatios]
        allProTcRatios += [str(y) for y in x.proTcRatios]
        allProDcRatios += [str(y) for y in x.proDcRatios]

    lines = [','.join(allSupAllRatios), ','.join(allSupAcRatios), ','.join(allSupTcRatios), ','.join(allSupDcRatios),
             ','.join(allProAllRatios), ','.join(allProAcRatios), ','.join(allProTcRatios), ','.join(allProDcRatios)]

    fOut = open(outPath, 'w')
    for x in lines:
        fOut.write(x + '\n')
    fOut.close()


def arrangeDataForTTableLarger60(patientPathList, outPath):
    '''A fucntion to use the detailedPatient class to generate a text file with degree change for
    all curves where the angle is greater than 60 degrees, for all 8 sections of curves.
    to be analyzed in a t taple and the p value to be determined. By chnaging just the 'x.supAllDegs'
    variable, you can change the stat that is analyzed. '''
    detailedPatientList = [DetailedPatient(x) for x in patientPathList]
    allSupAllRatios = []
    allSupAcRatios = []
    allSupTcRatios = []
    allSupDcRatios = []

    allProAllRatios = []
    allProAcRatios = []
    allProTcRatios = []
    allProDcRatios = []

    cutoff = 60
    for x in detailedPatientList:
        allSupAllRatios += [str(y) if y > cutoff else '' for y in x.supAllDegs]
        allSupAcRatios += [str(y) if y > cutoff else '' for y in x.supAcDegs]
        allSupTcRatios += [str(y) if y > cutoff else '' for y in x.supTcDegs]
        allSupDcRatios += [str(y) if y > cutoff else '' for y in x.supDcDegs]
        allProAllRatios += [str(y) if y > cutoff else '' for y in x.proAllDegs]
        allProAcRatios += [str(y) if y > cutoff else '' for y in x.proAcDegs]
        allProTcRatios += [str(y) if y > cutoff else '' for y in x.proTcDegs]
        allProDcRatios += [str(y) if y > cutoff else '' for y in x.proDcDegs]

    allSupAllRatios = removeBlanksFromList(allSupAllRatios)
    allSupAcRatios = removeBlanksFromList(allSupAcRatios)
    allSupTcRatios = removeBlanksFromList(allSupTcRatios)
    allSupDcRatios = removeBlanksFromList(allSupDcRatios)
    allProAllRatios = removeBlanksFromList(allProAllRatios)
    allProAcRatios = removeBlanksFromList(allProAcRatios)
    allProTcRatios = removeBlanksFromList(allProTcRatios)
    allProDcRatios = removeBlanksFromList(allProDcRatios)
    print(allSupAcRatios)

    lines = [','.join(allSupAllRatios), ','.join(allSupAcRatios), ','.join(allSupTcRatios), ','.join(allSupDcRatios),
             ','.join(allProAllRatios), ','.join(allProAcRatios), ','.join(allProTcRatios), ','.join(allProDcRatios)]

    fOut = open(outPath, 'w')
    for x in lines:
        fOut.write(x + '\n')
    fOut.close()


def arrangeSingleStatsForTTable(patientPathList, outPath):
    '''A fucntion to use the detailedPatient class to generate a text
    file with number of curves for all 8 sets of curves
    to be analyzed in a t taple and the p value to be determined. '''
    detailedPatientList = [DetailedPatient(x) for x in patientPathList]

    supAllCurveCounts = [str(x.curveCountSupAll) for x in detailedPatientList]
    supAcCurveCounts = [str(x.curveCountSupAc) for x in detailedPatientList]
    supTcCurveCounts = [str(x.curveCountSupTc) for x in detailedPatientList]
    supDcCurveCounts = [str(x.curveCountSupDc) for x in detailedPatientList]

    proAllCurveCounts = [str(x.curveCountProAll) for x in detailedPatientList]
    proAcCurveCounts = [str(x.curveCountProAc) for x in detailedPatientList]
    proTcCurveCounts = [str(x.curveCountProTc) for x in detailedPatientList]
    proDcCurveCounts = [str(x.curveCountProDc) for x in detailedPatientList]

    lines = [','.join(supAllCurveCounts), ','.join(supAcCurveCounts), ','.join(supTcCurveCounts),
             ','.join(supDcCurveCounts), ','.join(proAllCurveCounts), ','.join(proAcCurveCounts),
             ','.join(proTcCurveCounts), ','.join(proDcCurveCounts)]

    fOut = open(outPath, 'w')
    for x in lines:
        fOut.write(x + '\n')
    fOut.close()


def arrangeSingleMeanDegreesForTTable(patientPathList, outPath):
    '''A fucntion to use the detailedPatient class to generate a text
    file with number of curves for all 8 sets of curves
    to be analyzed in a t taple and the p value to be determined. '''
    detailedPatientList = [DetailedPatient(x) for x in patientPathList]

    supAllCurveCounts = [str(x.supAllMeanDegrees) for x in detailedPatientList]
    supAcCurveCounts = [str(x.supAcMeanDegrees) for x in detailedPatientList]
    supTcCurveCounts = [str(x.supTcMeanDegrees) for x in detailedPatientList]
    supDcCurveCounts = [str(x.supDcMeanDegrees) for x in detailedPatientList]

    proAllCurveCounts = [str(x.proAllMeanDegrees) for x in detailedPatientList]
    proAcCurveCounts = [str(x.proAcMeanDegrees) for x in detailedPatientList]
    proTcCurveCounts = [str(x.proTcMeanDegrees) for x in detailedPatientList]
    proDcCurveCounts = [str(x.proDcMeanDegrees) for x in detailedPatientList]

    lines = [','.join(supAllCurveCounts), ','.join(supAcCurveCounts), ','.join(supTcCurveCounts),
             ','.join(supDcCurveCounts), ','.join(proAllCurveCounts), ','.join(proAcCurveCounts),
             ','.join(proTcCurveCounts), ','.join(proDcCurveCounts)]

    fOut = open(outPath, 'w')
    for x in lines:
        fOut.write(x + '\n')
    fOut.close()


def arrangeSingleStatsForTTableLargerThan60(patientPathList, outPath):
    '''A fucntion to use the detailedPatient class to generate a text file with number
    of curves larger than 60 degrees for all 8 sets of curves
    to be analyzed in a t taple and the p value to be determined. '''
    detailedPatientList = [DetailedPatient(x) for x in patientPathList]

    supAllCurveCounts = [str(x.bigSupAllCount) for x in detailedPatientList]
    supAcCurveCounts = [str(x.bigSupAcCount) for x in detailedPatientList]
    supTcCurveCounts = [str(x.bigSupTcCount) for x in detailedPatientList]
    supDcCurveCounts = [str(x.bigSupDcCount) for x in detailedPatientList]

    proAllCurveCounts = [str(x.bigProAllCount) for x in detailedPatientList]
    proAcCurveCounts = [str(x.bigProAcCount) for x in detailedPatientList]
    proTcCurveCounts = [str(x.bigProTcCount) for x in detailedPatientList]
    proDcCurveCounts = [str(x.bigProDcCount) for x in detailedPatientList]

    lines = [','.join(supAllCurveCounts), ','.join(supAcCurveCounts), ','.join(supTcCurveCounts),
             ','.join(supDcCurveCounts), ','.join(proAllCurveCounts), ','.join(proAcCurveCounts),
             ','.join(proTcCurveCounts), ','.join(proDcCurveCounts)]

    fOut = open(outPath, 'w')
    for x in lines:
        fOut.write(x + '\n')
    fOut.close()

# patPathList = [r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0013",
# r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\TEST0014"]
# outPath = r"C:\Users\jlaframboise\Documents\ColonCurves_JL\CtVolumes\DegreesForTTable.txt"

# arrangeDataForTTable(patPathList, outPath)

# doFinalAverageComparison(patPathList, outPath)
