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
    self.parent.title = "Prepare Colon Data"
    self.parent.categories = ["Colon Analysis"]
    self.parent.dependencies = ["Segmentations"]
    self.parent.contributors = ["Jacob Laframboise (Perk Lab)"]
    self.parent.helpText = """
This module will loop through a directory and convert all the segmentations to binary labelmaps
for the colon dataset. 
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
Jacob Laframboise was supported by the Queen's Summer Work Experience Program.
"""

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
    """This function will take in the path to a segmentation file,
    a nrrd volume file, and the desired output path for the binary labelmap.
    It will load the segmentation into slicer, find the segmentation id for
    the colon segment, and convert that segment into a binary labelmap.
    It will save it to the output path parameter. """
    success, segNode = slicer.util.loadSegmentation(segPath, returnNode=True)
    segmentation = segNode.GetSegmentation()
    segID = segmentation.GetSegmentIdBySegmentName('colon')
    segment = segmentation.GetSegment(segID)

    labelMapNode = slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(labelMapNode)

    success, referenceNode = slicer.util.loadVolume(volPath, returnNode=True)
    segToExport = vtk.vtkStringArray()
    segToExport.InsertNextValue(segID)
    slicer.modules.segmentations.logic().ExportSegmentsToLabelmapNode(segNode, segToExport, labelMapNode, referenceNode)
    slicer.util.saveNode(labelMapNode, binLabelOutPath)
    logging.info("Saved: " + binLabelOutPath)

  def convertAllSegmentationsInPatientFolder(self, folder):
    """This function will loop through a directory for files that start
    with PT and end with .seg.nrrd and contain the tag 'Seg'. This should
    isolate the segmentation files. Once it finds them it look for the
    volume file based on the patient id and position, and makes an
    output file based on the same conventions. This could be modified
    for a recursive implementation to find files in more complicated
    directories. """
    count = 0
    for item in os.listdir(folder):
      #logging.info(item)
      if item.endswith(".seg.nrrd") and item.startswith("PT") and "Seg" in item:
        logging.info(item.split('Seg')[0])
        segPath = os.path.join(folder, item)
        volPath = os.path.join(folder, item.split('Seg')[0].replace('Pro', 'Prone.nrrd').replace('Sup', 'Supine.nrrd'))
        binLabelOutPath = os.path.join(folder, item.split('Seg')[0]+"SegLabel.nrrd")
        logging.info("Creating: " + binLabelOutPath)
        self.convertSegmentation(segPath, volPath, binLabelOutPath)
        count+=1
        # clear scene to avoid memory problems with large datasets.
        slicer.mrmlScene.Clear(0)
    return count

  def convertDatasetToBinLabelMaps(self, directory):
    """This function will loop through a folder of patient folders and
    call convertAllSegmentationsInPatientFolder on each folder. This
    automates the conversion of segmentations to binary labelmaps for
    the whole dataset. """
    count = 0
    for item in os.listdir(directory):
      if os.path.isdir(os.path.join(directory, item)) and item.startswith("PT"):
        logging.info(item)
        count += self.convertAllSegmentationsInPatientFolder(os.path.join(directory, item))
    return count


  def run(self, directoryPath):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(directoryPath):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    logging.info(directoryPath)
    datasetSize = self.convertDatasetToBinLabelMaps(directoryPath)
    logging.info("The dataset has {} labelmap volumes.".format(datasetSize))

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
