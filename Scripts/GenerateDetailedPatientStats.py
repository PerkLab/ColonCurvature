# This file is to generate a deatiled text file which can be easily imported into
# Excel to look at each patient on a single line. It takes a text file in this
# format and adds the individual curves for each patient.



import os


class Patient():
    def __init__(self, path):
        self.patPath = path
        self.patId = self.patPath[-8:]
        self.proCurves = self.loadPatientData('Pro')
        self.supCurves = self.loadPatientData('Sup')

    def loadPatientData(self, tag):
        filePath = os.path.join(self.patPath, self.patId+'_{}CurvaturesDataResults.txt'.format(tag))
        f = open(filePath, 'r')
        lines = [line.strip() for line in f.readlines()]
        f.close()
        start = 0
        for lineNum in range(len(lines)):
            if 'Sorted' in lines[lineNum]:
                start = lineNum+1
        lines = lines[start:]
        lines = [','.join(x.split(', ')[2:]) for x in lines]
        return lines


def createDetailedPatientStats(byPatientFilePath):
    directory = os.path.dirname(byPatientFilePath)
    f = open(byPatientFilePath, 'r')
    lines = [x.strip() for x in f.readlines()]
    f.close()
    lines[0] = lines[0] + ',Pro individual curves ->' + ',Deg,Dist'*50 + ',Sup individual curves ->' + ',Deg,Dist'*50
    for i in range(1, len(lines)):
        patId = lines[i][:8]
        patPath = os.path.join(directory, patId)

        p = Patient(patPath)
        numProCurves = len(p.proCurves)-1
        assert numProCurves<50
        numSupCurves = len(p.supCurves) - 1
        assert numSupCurves < 50
        lines[i] = lines[i] + ',,' + ','.join(p.proCurves[1:]) + ',,'*(50-numProCurves) + ',,' + ','.join(p.supCurves[1:])
    f2 = open(os.path.join(directory, 'CompleteDataByPatient.txt'), 'w')
    for line in lines:
        f2.write(line+'\n')
    f2.close()
createDetailedPatientStats(r"D:\OneDrive - Queen's University\Perk\ColonWork\FullDataset\AllDataByPatient-Oct6th2019.txt")
