import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import numpy as np




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




#
# CompareColonResults
#

class CompareColonResults(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "CompareColonResults" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Colon Analysis"]
    self.parent.dependencies = []
    self.parent.contributors = ["Jacob Laframboise (Perk Lab)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This module is part of the work done to comparatively analyze the curvature of patients colons.
This module takes in a list of quotations bound paths separated by spaces,
where each path is to the data folder of a patient with a supine and prone scan.
It creates a summary file which draws comparisons from all of them. 
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This extension was developed by Jacob Laframboise, Perk Lab.
This extension relies on the Extract Skeleton Module, the Markups to Model module,
and the Curve Maker Module.
""" # replace with organization, grant and thanks.

#
# CompareColonResultsWidget
#

class CompareColonResultsWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)


    #
    # a text input field for the input of patient's path. get path with self.displayText
    #
    self.pathListInputBox = qt.QLineEdit()
    parametersFormLayout.addRow("Patient Paths", self.pathListInputBox)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = True
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)

    # Add vertical spacer
    self.layout.addStretch(1)



  def cleanup(self):
    pass

  #def onSelect(self):
    #self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = CompareColonResultsLogic()
    logic.run(self.pathListInputBox.displayText)

#
# CompareColonResultsLogic
#

class CompareColonResultsLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """


  def makeAverageLists(self, patientPathList):
    '''A function to get the data from a patient's data path
    and get all average stats in both supine and prone positions. '''
    patientList = [Patient(x) for x in patientPathList]
    idList = [patient.patId for patient in patientList]

    textList = patientList[0].textLines

    allWholeDataList = []

    for x in range(len(patientList[0].wholeData)):
      supList = [patient.wholeData[x][0] for patient in patientList]
      proList = [patient.wholeData[x][1] for patient in patientList]
      supMean = np.mean(supList)
      proMean = np.mean(proList)
      # print((supMean, proMean))
      allWholeDataList.append((supMean, proMean))
      if 'Number of curves <' in textList[x + 1]:
        supDev = np.std(supList)
        proDev = np.std(proList)
        standardErrorSup = supDev / np.sqrt(len(supList))
        standardErrorPro = proDev / np.sqrt(len(proList))
        allWholeDataList.append((standardErrorSup, standardErrorPro))

    allAcDataList = []

    for x in range(len(patientList[0].acData)):
      supList = [patient.acData[x][0] for patient in patientList]
      proList = [patient.acData[x][1] for patient in patientList]
      supMean = np.mean(supList)
      proMean = np.mean(proList)
      allAcDataList.append((supMean, proMean))
      if 'Number of curves <' in textList[x + 1]:
        supDev = np.std(supList)
        proDev = np.std(proList)
        standardErrorSup = supDev / np.sqrt(len(supList))
        standardErrorPro = proDev / np.sqrt(len(proList))
        allAcDataList.append((standardErrorSup, standardErrorPro))

    allTcDataList = []

    for x in range(len(patientList[0].tcData)):
      supList = [patient.tcData[x][0] for patient in patientList]
      proList = [patient.tcData[x][1] for patient in patientList]
      supMean = np.mean(supList)
      proMean = np.mean(proList)
      allTcDataList.append((supMean, proMean))
      if 'Number of curves <' in textList[x + 1]:
        supDev = np.std(supList)
        proDev = np.std(proList)
        standardErrorSup = supDev / np.sqrt(len(supList))
        standardErrorPro = proDev / np.sqrt(len(proList))
        allTcDataList.append((standardErrorSup, standardErrorPro))

    allDcDataList = []

    for x in range(len(patientList[0].dcData)):
      supList = [patient.dcData[x][0] for patient in patientList]
      proList = [patient.dcData[x][1] for patient in patientList]
      supMean = np.mean(supList)
      proMean = np.mean(proList)
      allDcDataList.append((supMean, proMean))
      if 'Number of curves <' in textList[x + 1]:
        supDev = np.std(supList)
        proDev = np.std(proList)
        standardErrorSup = supDev / np.sqrt(len(supList))
        standardErrorPro = proDev / np.sqrt(len(proList))
        allDcDataList.append((standardErrorSup, standardErrorPro))

    for x, i in enumerate(textList):
      if 'Number of curves <' in i:
        textList.insert(x + 1, 'Stan Err Mean of Number of Curves ^')
    # for x in range(len(allWholeDataList)):
    # print(textList[x], end = ' ')
    # print(allWholeDataList[x], end = ' ')
    # print(allAcDataList[x], end = ' ')
    # print(allTcDataList[x], end = ' ')
    # print(allDcDataList[x])

    # for x in range(len(allWholeDataList)):
    # print('{}, {}'.format(textList[x+1], allWholeDataList[x]))
    # print(allWholeDataList)

    return textList, allWholeDataList, allAcDataList, allTcDataList, allDcDataList, idList

  def outputAverageListsToOnePrintReadyList(self, textLines, allWholeDataList, allAcDataList, allTcDataList, allDcDataList,
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

  def doFinalAverageComparison(self, patientPathList, outputPath):
    '''A function to call the above two functions on a series of patient data paths.
    This will ouput to one data file for a detailed comaprison of segments in both positions'''
    textLines, allWholeDataList, allAcDataList, allTcDataList, allDcDataList, idList = self.makeAverageLists(patientPathList)

    toPrintList = self.outputAverageListsToOnePrintReadyList(textLines, allWholeDataList, allAcDataList, allTcDataList,
                                                        allDcDataList, idList)

    addSpaceList = [4, 28, 33, 56, 62, 84]

    fOut = open(outputPath, 'w')
    for x, i in enumerate(toPrintList):
      if i.strip().split(',')[0] == 'Mean Curvature' and x > 0 or i.strip().split(',')[0] == 'Number of Curves':
        fOut.write('\n')
      fOut.write(i + '\n')
    fOut.close()



  def run(self, pathList):
    """
    Run the actual algorithm
    """


    logging.info('Processing started')

    self.pathList = pathList.split()
    self.pathList = [x[1:-1] for x in self.pathList]
    self.directory = self.pathList[0][:-9]
    self.outPath = os.path.join(self.directory, 'Summary.txt')

    self.doFinalAverageComparison(self.pathList, self.outPath)

    logging.info(self.outPath)




    logging.info('Processing completed')

    return True


class CompareColonResultsTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_CompareColonResults1()

  def test_CompareColonResults1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = CompareColonResultsLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
