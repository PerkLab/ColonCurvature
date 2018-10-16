import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# PatientComparison
#

class PatientComparison(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "PatientComparison" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Colon Analysis"]
    self.parent.dependencies = []
    self.parent.contributors = ["Jacob Laframboise (Perk Lab)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This module is part of the work done to comparatively analyze the curvature of patients colons.
This module will take in the path to the patients data folder, 
and will make a comparison file of all the important stats between supine and prone scans. 
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This extension was developed by Jacob Laframboise, Perk Lab.
This extension relies on the Extract Skeleton Module, the Markups to Model module,
and the Curve Maker Module.
""" # replace with organization, grant and thanks.

#
# PatientComparisonWidget
#

class PatientComparisonWidget(ScriptedLoadableModuleWidget):
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
    self.textInputBox = qt.QLineEdit()
    parametersFormLayout.addRow("Patient Path", self.textInputBox)


    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = True

  def onApplyButton(self):
    logic = PatientComparisonLogic()

    logic.run(self.textInputBox.displayText)

#
# PatientComparisonLogic
#

class PatientComparisonLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def getDataLines(self, supPath, proPath, patId, section):
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


  def comparePatientResults(self, patPath):
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

    outLinesMain = self.getDataLines(supPath, proPath, patId, 'All')
    outLinesAc = self.getDataLines(supAcPath, proAcPath, patId, 'AC')
    outLinesTc = self.getDataLines(supTcPath, proTcPath, patId, 'TC')
    outLinesDc = self.getDataLines(supDcPath, proDcPath, patId, 'DC')

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



  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """


    return True


  def run(self, patFolderPath):
    """
    Run the actual algorithm
    """

    logging.info('Processing started')

    self.patientFolder = patFolderPath
    self.patId = self.patientFolder[-8:]

    self.comparePatientResults(self.patientFolder)

    logging.info('Processing completed')

    return True


class PatientComparisonTest(ScriptedLoadableModuleTest):
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
    self.test_PatientComparison1()

  def test_PatientComparison1(self):
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
    logic = PatientComparisonLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
