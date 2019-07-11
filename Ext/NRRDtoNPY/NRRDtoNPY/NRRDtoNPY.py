import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import numpy as np

#
# NRRDtoNPY
#

class NRRDtoNPY(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "NRRD to NPY" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Colon Analysis"]
    self.parent.dependencies = []
    self.parent.contributors = ["Keiran Barr (Perk Lab)"]
    self.parent.helpText = """
This module was created as part of the Colon Analysis extension for slicer.
This module takes only an input directory, and searches for nrrd volumes in the directory.
When found, the files are imported to slicer, converted to a numpy array, and saved into a
new directory (npyOutput), each array titled according to the volume it was converted from.
The goal of this module is to automate the exporting of nrrd files to a supported format
for deep learning with keras
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was supported by the Queen's High School Internship in Computing
""" # replace with organization, grant and thanks.

#
# Widget
#

class NRRDtoNPYWidget(ScriptedLoadableModuleWidget):
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
    # input path box
    #
    self.pathInputBox = qt.QLineEdit()
    parametersFormLayout.addRow("Parent Directory Path", self.pathInputBox)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.pathInputBox.textChanged.connect(self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = len(self.pathInputBox.displayText)

  def onApplyButton(self):
    logic = NRRDtoNPYLogic()
    logic.run(self.pathInputBox.displayText)

#
# Logic
#

class NRRDtoNPYLogic(ScriptedLoadableModuleLogic):
    def run(self,rootPath):

      if rootPath.endswith('\\'):
        rootPath = rootPath[:-1]

      newDir = rootPath + '\\' + 'npyOutput'
      if not os.path.exists(newDir):
        os.makedirs(newDir)
      print('saving files to:' + newDir)



      #WORKING!!!
      pts = []
      nrrds = []
      segs = []

      for root, dirs, files in os.walk(rootPath):
        for dirname in dirs:
          #for this module, it is recommended that the data is organized into folders according to patient
          #for example:PTXX0000
          if dirname.startswith("PT"):
              pts.append(dirname)
        for filename in files:
          if filename.endswith(".nrrd"):
              if filename.endswith(".seg.nrrd"):
                segs.append(os.path.join(root,filename))
              else:
                pathToNrrd = os.path.join(root,filename)
                nrrds.append(pathToNrrd)
                #removes extension so getNode can read it
                nodeName = filename[:-5]
                #when using np.save, the text following the final backslash is the file name, hence the addition to the original newDir string
                newNewDir = newDir + '\\' + nodeName

                slicer.util.loadVolume(pathToNrrd)
                newlyLoaded = slicer.util.getNode(nodeName)
                arr = slicer.util.arrayFromVolume(newlyLoaded)
                np.save(newNewDir,arr)
                print('saved ' + filename)

      print('process completed')

      print('list of patients:')
      print(pts)
      print('(' + str(len(pts)) + ' patients\' folders searched)')

      print('list of saved volumes:')
      print(nrrds)
      print('(' + str(len(nrrds)) + ' nrrd volumes found and converted)')


class NRRDtoNPYTest(ScriptedLoadableModuleTest):
  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_NRRDtoNPY()

  def test_NRRDtoNPY(self):
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
    logic = NRRDtoNPYLogic()
    self.delayDisplay('Test passed!')