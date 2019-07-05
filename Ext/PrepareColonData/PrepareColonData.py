import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# PrepareColonData
#

class PrepareColonData(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "PrepareColonData" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Jacob Laframboise (Perk Lab)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It performs a simple thresholding on the input volume and optionally captures a screenshot.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# PrepareColonDataWidget
#

class PrepareColonDataWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer)
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/PrepareColonData.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # connections
    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.ui.directoryButton.directoryChanged.connect(self.onSelect)
    self.ui.labelmapCheckbox.stateChanged.connect(self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.ui.applyButton.enabled = self.ui.labelmapCheckbox.checked

  def onApplyButton(self):
    logic = PrepareColonDataLogic()
    logic.run(self.ui.directoryButton.directory)

#
# PrepareColonDataLogic
#

class PrepareColonDataLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """


  def isValidInputOutputData(self, directoryPath):
    """Validates if the output is not the same as input
    """
    return True

  def convertSegmentation(self, segPath, volPath, binLabelOutPath):
    success, segNode = slicer.util.loadSegmentation(r"C:\Users\jlaframboise\Desktop\TEST0012\TEST0012_ProSeg.seg.nrrd", returnNode=True)
    segmentation = segNode.GetSegmentation()
    segID = segmentation.GetSegmentIdBySegmentName('colon')
    segment = segmentation.GetSegment(segID)

    labelMapNode = slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(labelMapNode)

    success, referenceNode = slicer.util.loadVolume(r"C:\Users\jlaframboise\Desktop\TEST0012\TEST0012_Prone.nrrd", returnNode=True)
    segToExport = vtk.vtkStringArray()
    segToExport.InsertNextValue(segID)
    slicer.modules.segmentations.logic().ExportSegmentsToLabelmapNode(segNode, segToExport, labelMapNode, referenceNode)
    slicer.util.saveNode(labelMapNode, r"C:\Users\jlaframboise\Desktop\TEST0012\TEST0012_ProSegLabel.nrrd")


  def run(self, directoryPath):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(directoryPath):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    logging.info(directoryPath)
    self.convertSegmentation('cat', 'dog', 'banana')

    logging.info('Processing completed')

    return True


class PrepareColonDataTest(ScriptedLoadableModuleTest):
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
    self.test_PrepareColonData1()

  def test_PrepareColonData1(self):
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
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767',
      checksums='SHA256:12d17fba4f2e1f1a843f0757366f28c3f3e1a8bb38836f0de2a32bb1cd476560')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = PrepareColonDataLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
