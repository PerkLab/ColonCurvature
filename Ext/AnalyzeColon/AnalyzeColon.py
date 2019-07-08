from __future__ import division
import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import numpy as np
from operator import itemgetter



#
# AnalyzeColon
#

class AnalyzeColon(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Analyze Colon"
    self.parent.categories = ["Colon Analysis"]
    self.parent.dependencies = ["MarkupsToModel", "CurveMaker", "ExtractSkeleton"]
    self.parent.contributors = ["Jacob Laframboise (Perk Lab)"]
    self.parent.helpText = """
This module is part of the work done to comparatively analyze the curvature of patients colons.
This module will take in the nodes for a segmentation of a colon,
a fiducial node containing a cut point at the ascending and descending colon,
an output volume, a box to past the patients data folder path into, 
and a box to type the tag 'Sup' or 'Pro' into to identify the tpe of scan.
It will generate a set of points along the curve (with Extract Skeleton),
Fit a curve to the points (with Markups to Model),
Find the curvature at every point (with Curve Maker),
And analyze the data to generate statistics.  
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This work was supported in part by Queen's Highschool Internship in Computing.
Jacob Laframboise was supported by the Queen's Summer Work Experience Program. 
""" # replace with organization, grant and thanks.

#
# AnalyzeColonWidget
#

class AnalyzeColonWidget(ScriptedLoadableModuleWidget):
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
    # input segmentation selector
    #
    self.inputSegmentationSelector = slicer.qMRMLNodeComboBox()
    self.inputSegmentationSelector.nodeTypes = ["vtkMRMLSegmentationNode"]
    self.inputSegmentationSelector.selectNodeUponCreation = True
    self.inputSegmentationSelector.addEnabled = False
    self.inputSegmentationSelector.removeEnabled = False
    self.inputSegmentationSelector.noneEnabled = False
    self.inputSegmentationSelector.showHidden = False
    self.inputSegmentationSelector.showChildNodeTypes = False
    self.inputSegmentationSelector.setMRMLScene(slicer.mrmlScene)
    self.inputSegmentationSelector.setToolTip("Pick the input to the algorithm.")
    parametersFormLayout.addRow("Input Segmentation: ", self.inputSegmentationSelector)


    #
    # input cut point selector
    #
    self.cutPointSelector = slicer.qMRMLNodeComboBox()
    self.cutPointSelector.nodeTypes = ['vtkMRMLMarkupsFiducialNode']
    self.cutPointSelector.selectNodeUponCreation = True
    self.cutPointSelector.addEnabled = False
    self.cutPointSelector.removeEnabled = False
    self.cutPointSelector.noneEnabled = False
    self.cutPointSelector.showHidden = False
    self.cutPointSelector.showChildNodeTypes = False
    self.cutPointSelector.setMRMLScene(slicer.mrmlScene)
    self.cutPointSelector.setToolTip("Pick the cut points for the algorithm.")
    parametersFormLayout.addRow("Input Cut Points: ", self.cutPointSelector)

    #
    # a text input field for the input of patient's path. get path with self.displayText
    #
    self.pathInputBox = qt.QLineEdit()
    parametersFormLayout.addRow("Patient Path", self.pathInputBox)

    self.tagInputBox = qt.QLineEdit()
    parametersFormLayout.addRow("Scan type (Sup, Pro): ", self.tagInputBox)


    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSegmentationSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.cutPointSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.pathInputBox.textChanged.connect(self.onSelect)
    self.tagInputBox.textChanged.connect(self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    logging.debug("onSelect called. ")
    self.applyButton.enabled = self.inputSegmentationSelector.currentNode() and self.cutPointSelector.currentNode() and len(self.pathInputBox.displayText) > 0 and len(self.tagInputBox.displayText) == 3

  def onApplyButton(self):
    logic = AnalyzeColonLogic()
    logic.run(self.inputSegmentationSelector.currentNode(), self.cutPointSelector.currentNode(), self.pathInputBox.displayText, self.tagInputBox.displayText)

#
# AnalyzeColonLogic
#

class AnalyzeColonLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  # -------------- tool functions ---------------------------

  def findLocalMaximas(self, inList, minDist=0, threshold=0):
    '''A function to return a list of the local maximas of an input list. '''
    avgCurvature = np.mean(inList)

    # create a list of local maximas, provided each maxima is > avg curvature
    localMaximas = []
    for x in range(1, len(inList) - 1):
      currentThreeList = inList[x - 1:x + 2]
      # ex. in [1,2,1], 2 is a max. In [2.333, 2, 1], 2 is not a max
      if currentThreeList[0] < currentThreeList[1] and currentThreeList[1] > currentThreeList[2] and currentThreeList[
        1] > avgCurvature * threshold:
        localMaximas.append((x + 1, currentThreeList[1]))


    # reprocess localMaximas:
    '''reprocessing will iterate through the list and find clusters of max points,
    where there is a chain of points with less than minDist between them, and this process replaces this
    chain with a single point, in the middle of where the chain was. '''
    newLocalMaximas = []
    closePointsList = []
    addedOne = False
    for x, i in enumerate(localMaximas[:-1]):

      if not addedOne:

        if len(closePointsList) == 0:
          pass

        # if there are no maximas close by, add the current max to the new list
        elif len(closePointsList) < 2:
          newLocalMaximas.append(closePointsList[0])
          closePointsList = []

        # if the close points list has multiple maximums, only return the middle point
        elif len(closePointsList) > 1:
          newLocalMaximas.append(closePointsList[len(closePointsList) // 2])
          closePointsList = []

      addedOne = False

      if closePointsList == []:
        closePointsList = [i]

      if localMaximas[x + 1][0] - i[0] < minDist:
        closePointsList.append(localMaximas[x + 1])
        addedOne = True

    newLocalMaximas.append(localMaximas[-1])

    return newLocalMaximas

  def findLocalMinimas(self, inList, minDist=0, threshold=0):
    '''A function to return a list of the local minimas of an input list. '''
    avgCurvature = np.mean(inList)
    localMinimas = []
    for x in range(1, len(inList) - 1):
      currentThreeList = inList[x - 1:x + 2]
      if currentThreeList[0] > currentThreeList[1] and currentThreeList[1] < currentThreeList[2] and currentThreeList[
        1] < avgCurvature / (threshold + 0.001):
        localMinimas.append((x + 1, currentThreeList[1]))
    # reprocess localMinimas:
    '''reprocessing will iterate through the list and find clusters of max points,
    where there is achain of points with less than minDist between them, and this procedss replaces this
    chain with a single point, in the middle of where the chain was. '''
    newLocalMinimas = []
    closePointsList = []
    addedOne = False
    for x, i in enumerate(localMinimas[:-1]):
      if not addedOne:
        if len(closePointsList) == 0:
          pass
        elif len(closePointsList) < 2:
          newLocalMinimas.append(closePointsList[0])
          closePointsList = []
        elif len(closePointsList) > 1:
          newLocalMinimas.append(closePointsList[len(closePointsList) // 2])
          closePointsList = []
      addedOne = False
      if closePointsList == []:
        closePointsList = [i]
      if localMinimas[x + 1][0] - i[0] < minDist:
        closePointsList.append(localMinimas[x + 1])
        addedOne = True
    newLocalMinimas.append(localMinimas[-1])
    return newLocalMinimas

  def unCluster(self, minList, maxList, curvatures):
    '''A function which takes a list of maximum points, a list of minimum points, and it looks for
    clusters of maximuns uninterupted with minimums, or vice versa. It replaces those clusters with a single
    point at the center of where the cluster was. Essentially, a better version of the reprocessing section of the
    in the find local maxima function. '''

    newMinList = []
    newMaxList = []
    extremeList = []

    # make a sorted list of 3 key tuples, where the last item identifies max/min
    for x in maxList:
      extremeList.append((x[0], x[1], 'MAX'))
    for x in minList:
      extremeList.append((x[0], x[1], 'MIN'))
    extremeList.sort(key=itemgetter(0))

    running = True
    count = 0
    while running:
      # break if all points were checked
      if count >= len(extremeList):
        break
      subList = [extremeList[count]]
      # look ahead as far as possible
      for x in range(1, len(curvatures)):

        # if the xth item after the first item is the same type (max/min)
        if count + x < len(extremeList) and extremeList[count + x][2] == extremeList[count][2]:
          subList.append(extremeList[count + x])

        else:  # if the next item is a different type (max/min)

          # get the mean point number of the neighboring max/mins
          numberList = [int(z[0]) for z in subList]
          middleNumber = int(round(np.mean(numberList)))

          # set the middle point at the middlemost extreme point
          middlePoint = (middleNumber, curvatures[middleNumber - 1], extremeList[count][2])

          # add new extreme value to new list of points
          if middlePoint[2] == 'MAX':
            newMaxList.append(middlePoint)
          else:
            newMinList.append(middlePoint)
          count += len(subList) - 1

          break
      count += 1

    # remove the third item (min, max id) in the tuples
    newMinList = [(i[0], i[1]) for i in newMinList]
    newMaxList = [(i[0], i[1]) for i in newMaxList]

    return newMinList, newMaxList

  def unitVector(self, vec):
    '''A function to return the unit vector in the direction of a numpy paramter vector. '''
    return vec / np.linalg.norm(vec)

  def angleBetween(self, v1, v2):
    '''A function to return the angle between two input numpy vectors'''
    v1U = self.unitVector(v1)
    v2U = self.unitVector(v2)
    return np.arccos(np.clip(np.dot(v1U, v2U), -1.0, 1.0))

  def addFiducialsOnCurvatureMaximums(self, inPath):
    '''A function to take the path of the curvatures data file, and generate slicer fiducials on the model to verify'''
    fIn = open(inPath, 'r')
    lines = fIn.readlines()
    fIn.close()
    # lists to hold coordinates
    xVals = []
    yVals = []
    zVals = []

    # for every maximum in the file, add the coords
    for x in range(1, len(lines)):
      if lines[x].strip().split(', ')[7] == 'MAX':
        xVals.append(lines[x].strip().split(', ')[2])
        yVals.append(lines[x].strip().split(', ')[3])
        zVals.append(lines[x].strip().split(', ')[4])

    # create a node to hold fiducials
    m = slicer.vtkMRMLMarkupsFiducialNode()
    m.SetName(self.maximumPointsName)
    slicer.mrmlScene.AddNode(m)
    slicer.util.saveNode(m, self.maximumPointsPath)

    # add a fiducial at each coordinate location
    for i in range(len(xVals)):
      m.AddFiducial(float(xVals[i]), float(yVals[i]), float(zVals[i]))

  def addFiducialsOnCurvatureMinimums(self, inPath):
    '''A function to take the path of the curvatures data file, and generate slicer fiducials
    on the model's extreme values to verify'''
    fIn = open(inPath, 'r')
    lines = fIn.readlines()
    fIn.close()

    # lists to hold coordinates
    xVals = []
    yVals = []
    zVals = []

    # for every maximum in the file, add the coords
    for x in range(1, len(lines)):
      if lines[x].strip().split(', ')[7] == 'MIN':
        xVals.append(lines[x].strip().split(', ')[2])
        yVals.append(lines[x].strip().split(', ')[3])
        zVals.append(lines[x].strip().split(', ')[4])

    # create a node to hold fiducials
    m = slicer.vtkMRMLMarkupsFiducialNode()
    m.SetName(self.minimumPointsName)
    slicer.mrmlScene.AddNode(m)
    slicer.util.saveNode(m, self.minimumPointsPath)

    # add a fiducial at each coordinate location
    for i in range(len(xVals)):
      m.AddFiducial(float(xVals[i]), float(yVals[i]), float(zVals[i]))

  # ------------------- process functions -------------------------------------

  def convertSegmentationToBinaryLabelmap(self, segNode):
    '''A function to take in a node which stores a segmentation, and output the
    segmentation as a binary labelmap node. '''
    segmentation = segNode.GetSegmentation()

    # here the segments that are not the colon segment are removed to leave
    # just the colon segment to be converted into a binary labelmap
    for x in range(segmentation.GetNumberOfSegments()-1, -1, -1):
      segment = segmentation.GetNthSegment(x)
      if segment.GetName().lower() != 'colon':
        segmentation.RemoveSegment(segment)
    if (segmentation.GetNthSegment(0) is None) or segmentation.GetNthSegment(0).GetName() != 'colon':
      logging.debug("Error, no colon segment found in segmentation node. ")


    # make the bin label map node
    colonBinLabelMapNode = slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(colonBinLabelMapNode)

    # export the segmentation node to the binary label map node
    slicer.vtkSlicerSegmentationsModuleLogic.ExportAllSegmentsToLabelmapNode(segNode, colonBinLabelMapNode)
    logging.info('Removed non colon, created binary labelmap.')
    return colonBinLabelMapNode


  def genCenterPoints(self, binLabelMapNode):
    '''A function to use the Extract Skeleton module to generate a set
    of center points along the centerline of the colon. They will be saved
    to file. '''

    # a parameters dict that will be passed to the extract skeleton module.
    pars = {}
    pars["InputImageFileName"] = binLabelMapNode.GetID()

    # create a markups fiducial node and name it, set it as the output
    fidsOut = slicer.vtkMRMLMarkupsFiducialNode()
    fidsOut.SetName('{}_{}CenterPoints'.format(self.patId, self.mode))
    slicer.mrmlScene.AddNode(fidsOut)
    pars["OutputFiducialsFileName"] = fidsOut.GetID()

    pars['NumberOfPoints'] = 600

    imgOut = slicer.vtkMRMLLabelMapVolumeNode()
    imgOut.SetName('{}_{}OutputImg'.format(self.patId, self.mode))
    slicer.mrmlScene.AddNode(imgOut)
    pars['OutputImageFileName'] = imgOut.GetID()
    logging.info('Created pars, running extract skeleton')

    # run the module with parameters
    extractor = slicer.modules.extractskeleton
    slicer.cli.runSync(extractor, None, pars)
    logging.info('Extracted Skeleton.')
    return fidsOut

  def fitCurve(self, fidsNode):
    '''A function to return a curve model from a fiducial list node
    with specific parameters for this project. '''

    logging.info('Fitting curve to center points...')

    # create the logic node
    markupsToModelNode = slicer.vtkMRMLMarkupsToModelNode()
    markupsToModelNode.SetName('MyMarkupsToModelNode')
    slicer.mrmlScene.AddNode(markupsToModelNode)

    # link the input
    markupsToModelNode.SetAndObserveInputNodeID(fidsNode.GetID())

    # make the output node
    outputCurveNode = slicer.vtkMRMLModelNode()
    slicer.mrmlScene.AddNode(outputCurveNode)
    outputCurveNode.SetName(self.curveName)

    # Link the ouput and update the curve with parameters below
    markupsToModelNode.SetAndObserveModelNodeID(outputCurveNode.GetID())
    markupsToModelNode.SetModelType(1)
    markupsToModelNode.SetModelType(1)
    markupsToModelNode.SetCurveType(3)
    markupsToModelNode.SetPolynomialFitType(1)
    markupsToModelNode.SetPolynomialOrder(2)
    markupsToModelNode.SetPolynomialSampleWidth(0.05)
    markupsToModelNode.SetTubeRadius(0)

    logging.info('Fitted curve to center points. ')

    return outputCurveNode


  def makeCurvaturesFile(self, curveNode):
    '''A function to use Curve Maker to calculate the curvature at every point,
    and to write that curvature to a text data file. '''

    logging.info("Computing and writing curvatures...")

    # get the point data from the model
    polyData = curveNode.GetPolyData()

    # initiate curve maker logic
    import CurveMaker
    CurveMaker.CurveMakerLogic()
    # an array to hold the resulting curvatures
    curvatureArray = vtk.vtkDoubleArray()

    # run the computeCurvatures function, and get the stats that are returned
    avgCurve, minCurve, maxCurve = CurveMaker.CurveMakerLogic().computeCurvatures(polyData, curvatureArray)

    # add the curvature data as a scalar to the curve model
    polyData.GetPointData().AddArray(curvatureArray)
    curveDisplayNode = curveNode.GetDisplayNode()

    # activate this scalar in its dispay node
    curveDisplayNode.SetActiveScalarName('Curvature')
    curveDisplayNode.SetScalarVisibility(1)

    # get the curvature values from the array
    curvatureList = [curvatureArray.GetTuple1(x) for x in range(curvatureArray.GetNumberOfTuples())]
    stringCurvatureList = [str(x) for x in curvatureList]

    points = polyData.GetPoints()
    pointList = [points.GetPoint(x) for x in range(points.GetNumberOfPoints())]

    # prepare the data to be outputed to a text file
    newLines = [stringCurvatureList[x] + ', ' + str(pointList[x][0]) + ', ' + str(pointList[x][1]) + ', ' + str(
      pointList[x][2]) + '\n' for x in range(len(pointList))]
    newLines.append("\n")

    # write the lines of data to a text file
    outPath = self.curvaturesPath
    print(outPath)
    outFile = open(outPath, 'w')
    outFile.writelines(newLines)
    outFile.close()

    logging.info("Saved curvatures.")

  def makeCutPointsFile(self, fidsNode):
    '''A function that takes the fiducial node containing cut points,
    and it saves a text file with the coordinate data there for later use. '''

    outPath = self.cutPointsPath
    fOut = open(outPath, 'w')

    # for both points:
    for x in range(2):
      pos = np.zeros(3)
      fidsNode.GetNthFiducialPosition(x, pos)
      fOut.write('{},{},{}\n'.format(pos[0], pos[1], pos[2]))

    fOut.close()

  def addDetails(self, inPath, outPath):
    '''A function that takes the path of a text file and creates a new text file with the point number,
        and the percentage of how far the point is along the list. Easy to import to Excel'''

    inFile = open(inPath, 'r')
    lines = inFile.readlines()
    inFile.close()

    lines = [x.strip().split(', ') for x in lines]

    outFile = open(outPath, 'w')
    outFile.write(inPath[-26:] + "\n")

    for count, item in enumerate(lines):
        if item != '' and item != "\n" and item != ['']:
            # (pointNum, % of length, x, y, z, curvature)
            outFile.write(
                '{}, {}, {}, {}, {}, {}'.format(count,  100 * count / (len(lines) - 2), item[1], item[2], item[3],
                                                item[0]) + '\n') # it was count / (len(lines) - 2) * 100
    outFile.close()

  def getSumCurvatures(self, curvaturesList, width):
    '''A function which takes a list, and it returns a new list of equal length, where each value corresponds
    to the same indexed value in the first list, plus the all the items 'width' positions up and down the list.'''

    sumList = []
    for x in range(len(curvaturesList)):
      subList = (curvaturesList[max(x - width, 0): min(x + width + 1, len(curvaturesList))])
      subList = [float(y) for y in subList]
      sumList.append(sum(subList))
    return sumList

  def addSumCurvaturesToDataFile(self, inPath, width=10):
      '''A fucntion to modify a detailed data file with curvatures, by adding a column
      that contains the sum of curvatures in a given interval for every point.
      It applies the getSumCurvatures function. '''

      fIn = open(inPath, 'r')
      lines = fIn.readlines()
      fIn.close()
      title = lines[0].strip()

      # read the values
      curvatureValues = [x.strip().split(', ')[5] for x in lines[1:]]

      # calculate the summed values
      sumCurvatureValues = self.getSumCurvatures(curvatureValues, width)
      newLines = [title] + [lines[x].strip() + ', ' + str(sumCurvatureValues[x - 1]) for x in
                            range(1, len(sumCurvatureValues) + 1)]
      # write all the data back to file
      fOut = open(inPath, 'w')
      for line in newLines:
          fOut.write(line + '\n')
      fOut.close()

  def addSumCurvatureMaxMinsToDataFile(self, inPath, minPointDist=0, threshold=1, minThresholdBoost=1.5):
    '''A function to add a column to the data file which indicates if the point is at a max or a min. '''
    fIn = open(inPath, 'r')
    lines = fIn.readlines()
    fIn.close()
    title = lines[0].strip()

    # get the curvature values
    sumCurvatureValues = [x.strip().split(', ')[6] for x in lines[1:]]
    sumCurvatureValues = [float(y) for y in sumCurvatureValues]

    # find local minimas and maximas
    locMaximas = self.findLocalMaximas(sumCurvatureValues, minPointDist, threshold)
    locMinimas = self.findLocalMinimas(sumCurvatureValues, minPointDist,
                                  threshold * minThresholdBoost)  # The minimas are currently being held at a higher threshold so the maximas are unClustered more.

    # remove clustered max/mins
    locMinimas, locMaximas = self.unCluster(locMinimas, locMaximas, sumCurvatureValues)

    # add the max or mins to the list of lines to be written to file
    locExtremesColumn = []
    # for every line, if its curvature and point number is in the max list or min list,
    # add the correct label to the extreme column, else add 0
    for x in range(1, len(lines)):
      t = (x, sumCurvatureValues[x - 1])
      if t in locMaximas:
        locExtremesColumn.append('MAX')
      elif t in locMinimas:
        locExtremesColumn.append('MIN')
      else:
        locExtremesColumn.append('0')
    newLines = [title] + [lines[x].strip() + ', ' + str(locExtremesColumn[x - 1]) for x in
                          range(1, len(locExtremesColumn) + 1)]

    # write the columns to file, with the new max/min column
    fOut = open(inPath, 'w')
    for line in newLines:
      fOut.write(line + '\n')
    fOut.close()


  def addDegreeChangesToFile(self, inPath):
    '''This function look at every max, and makes a sublist of itself, and the minimums on either side.
    it then akes a tangent at each minimum, and compares the change in angle from one to the other,
    saying that the line curves that x degrees over the straight line distance from Min to Min. '''
    fIn = open(inPath, 'r')
    lines = fIn.readlines()
    fIn.close()
    title = lines[0].strip()
    curvatureValues = [x.strip().split(', ')[5] for x in lines[1:]]
    numVals = [x.strip().split(', ')[0] for x in lines[1:]]
    maxMinTypes = [x.strip().split(', ')[7] for x in lines[1:]]
    coords = [(x.strip().split(', ')[2], x.strip().split(', ')[3], x.strip().split(', ')[4]) for x in lines[1:]]

    extremePoints = []
    maxPlaces = []
    for y in range(len(lines) - 1):
      if maxMinTypes[y] == 'MAX' or maxMinTypes[y] == 'MIN':
        extremePoints.append((coords[y][0], coords[y][1], coords[y][2], maxMinTypes[y], numVals[y]))

    angleChangeList = []
    for x in range(1, len(extremePoints) - 1):
      subList = [extremePoints[x - 1], extremePoints[x], extremePoints[x + 1]]

      if subList[1][3] == 'MAX':
        leftMinForwardPointNum = int(subList[0][4]) + 2
        rightMinBackwardPointNum = int(subList[2][4]) - 2
        leftMinForwardPointCoords = np.array(
          [float(coords[leftMinForwardPointNum][0]), float(coords[leftMinForwardPointNum][1]),
          float(coords[leftMinForwardPointNum][2])])
        rightMinBackwardPointCoords = np.array(
          [float(coords[rightMinBackwardPointNum][0]), float(coords[rightMinBackwardPointNum][1]),
          float(coords[rightMinBackwardPointNum][2])])

        vecPosList = [np.array([float(z[0]), float(z[1]), float(z[2])]) for z in subList]

        vecOne = leftMinForwardPointCoords - vecPosList[0]
        vecTwo = vecPosList[2] - rightMinBackwardPointCoords

        vecThree = vecPosList[2] - vecPosList[0]
        angleChange = self.angleBetween(vecOne, vecTwo) * 180 / np.pi
        straightDist = np.linalg.norm(vecThree)

        angleChangeList.append((subList[1][4], angleChange, straightDist))

    # print(angleChangeList)
    angleChangeValues = []
    straightDistValues = []
    numList = [int(x[0]) for x in angleChangeList]

    for i in range(len(lines) - 1):
      if i in numList:
        for x in angleChangeList:
          if int(x[0]) == i:
            angleChangeValues.append(x[1])
            straightDistValues.append(x[2])
      else:
        angleChangeValues.append('0')
        straightDistValues.append('0')

    newLines = [title] + [
      lines[x].strip() + ', ' + str(angleChangeValues[x - 1]) + ', ' + str(straightDistValues[x - 1]) for x in
      range(1, len(angleChangeValues) + 1)]
    fOut = open(inPath, 'w')
    for line in newLines:
      fOut.write(line + '\n')
    fOut.close()

  def splitDataFileToFiles(self, inDataPath, inCutPointsPath):
    '''A function to take a data file, and a file containing the coords of two fiducials
    representing the cut points, first being ascending and second being descending,
    and create three new data files as the result of splitting the large data file at
    the two cut points. '''

    fIn = open(inDataPath, 'r')
    lines = fIn.readlines()
    fIn.close()
    title = lines[0].strip()
    lines2 = lines[1:]
    numVals = [x.strip().split(', ')[0] for x in lines[1:]]
    maxMinTypes = [x.strip().split(', ')[7] for x in lines[1:]]
    coords = [(x.strip().split(', ')[2], x.strip().split(', ')[3], x.strip().split(', ')[4]) for x in lines[1:]]

    fIn = open(inCutPointsPath, 'r')
    cutPointOne = fIn.readline().strip().split(',')
    cutPointTwo = fIn.readline().strip().split(',')
    fIn.close()

    outAcDataPath = inDataPath[:-8] + 'AcData.txt'
    outTcDataPath = inDataPath[:-8] + 'TcData.txt'
    outDcDataPath = inDataPath[:-8] + 'DcData.txt'

    cutPointOne = np.array([float(x) for x in cutPointOne])
    cutPointTwo = np.array([float(x) for x in cutPointTwo])

    minDist = 1000000
    closestPointNum = None
    for x in range(len(coords)):
      pos = np.array([float(coords[x][0]), float(coords[x][1]), float(coords[x][2])])

      cutPointToCenterPoint = np.subtract(pos, cutPointOne)
      dist = np.linalg.norm(cutPointToCenterPoint)
      if dist < minDist:
        closestPointNum = x
        minDist = dist
    closestPointNumToCutOne = closestPointNum

    minDist = 1000000
    closestPointNum = None
    for x in range(len(coords)):
      pos = np.array([float(coords[x][0]), float(coords[x][1]), float(coords[x][2])])

      cutPointToCenterPoint = np.subtract(pos, cutPointTwo)
      dist = np.linalg.norm(cutPointToCenterPoint)
      if dist < minDist:
        closestPointNum = x
        minDist = dist
    closestPointNumToCutTwo = closestPointNum

    ascendingLines = lines2[:closestPointNumToCutOne]
    transverseLines = lines2[closestPointNumToCutOne:closestPointNumToCutTwo]
    descendingLines = lines2[closestPointNumToCutTwo:]

    # REVERSE data file if it is backwards
    if not transverseLines:
      lines2 = lines2[::-1]
      numVals = [x.strip().split(', ')[0] for x in lines2[1:]]
      maxMinTypes = [x.strip().split(', ')[7] for x in lines2[1:]]
      coords = [(x.strip().split(', ')[2], x.strip().split(', ')[3], x.strip().split(', ')[4]) for x in lines2[1:]]

      minDist = 1000000
      closestPointNum = None
      for x in range(len(coords)):
        pos = np.array([float(coords[x][0]), float(coords[x][1]), float(coords[x][2])])

        cutPointToCenterPoint = np.subtract(pos, cutPointOne)
        dist = np.linalg.norm(cutPointToCenterPoint)
        if dist < minDist:
          closestPointNum = x
          minDist = dist
      closestPointNumToCutOne = closestPointNum

      minDist = 1000000
      closestPointNum = None
      for x in range(len(coords)):
        pos = np.array([float(coords[x][0]), float(coords[x][1]), float(coords[x][2])])

        cutPointToCenterPoint = np.subtract(pos, cutPointTwo)
        dist = np.linalg.norm(cutPointToCenterPoint)
        if dist < minDist:
          closestPointNum = x
          minDist = dist
      closestPointNumToCutTwo = closestPointNum

      ascendingLines = lines2[:closestPointNumToCutOne]
      transverseLines = lines2[closestPointNumToCutOne:closestPointNumToCutTwo]
      descendingLines = lines2[closestPointNumToCutTwo:]

    acOut = open(outAcDataPath, 'w')
    acOut.write(title + '\n')
    for line in ascendingLines:
      acOut.write(line)
    acOut.close()

    tcOut = open(outTcDataPath, 'w')
    tcOut.write(title + '\n')
    for line in transverseLines:
      tcOut.write(line)
    tcOut.close()

    dcOut = open(outDcDataPath, 'w')
    dcOut.write(title + '\n')
    for line in descendingLines:
      dcOut.write(line)
    dcOut.close()

  def getStats(self, dataInPath):
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

    meanCuvature = np.mean(curvatureValues)
    medianCurvature = np.median(curvatureValues)
    stanDevCurvature = np.std(curvatureValues)
    varianceCurvature = np.var(curvatureValues)
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
      lessThan20DegAvgDist = np.mean([float(x[1]) for x in lessThan20Deg])
    else:
      lessThan20DegAvgDist = 0

    if lessThan40Deg:
      lessThan40DegAvgDist = np.mean([float(x[1]) for x in lessThan40Deg])
    else:
      lessThan40DegAvgDist = 0

    if lessThan60Deg:
      lessThan60DegAvgDist = np.mean([float(x[1]) for x in lessThan60Deg])
    else:
      lessThan60DegAvgDist = 0

    if lessThan80Deg:
      lessThan80DegAvgDist = np.mean([float(x[1]) for x in lessThan80Deg])
    else:
      lessThan80DegAvgDist = 0

    if lessThan100Deg:
      lessThan100DegAvgDist = np.mean([float(x[1]) for x in lessThan100Deg])
    else:
      lessThan100DegAvgDist = 0

    if lessThan120Deg:
      lessThan120DegAvgDist = np.mean([float(x[1]) for x in lessThan120Deg])
    else:
      lessThan120DegAvgDist = 0

    if lessThan140Deg:
      lessThan140DegAvgDist = np.mean([float(x[1]) for x in lessThan140Deg])
    else:
      lessThan140DegAvgDist = 0

    if lessThan160Deg:
      lessThan160DegAvgDist = np.mean([float(x[1]) for x in lessThan160Deg])
    else:
      lessThan160DegAvgDist = 0

    if lessThan180Deg:
      lessThan180DegAvgDist = np.mean([float(x[1]) for x in lessThan180Deg])
    else:
      lessThan180DegAvgDist = 0

    meanCurveDegrees = np.mean(allCurveDegrees)
    meanCurveDistance = np.mean(allCurveDistances)
    medianCurveDegrees = np.median(allCurveDegrees)
    medianCurveDistance = np.median(allCurveDistances)

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


  def isValidInputOutputData(self, inputSegNode, inputCutPointsNode, outputPathText, inputTagText):
    """Validates if the output is not the same as input
    """
    if not inputSegNode:
      logging.debug('isValidInputOutputData failed: no input segmentation node defined.')
      return False
    if not inputSegNode.GetClassName() =='vtkMRMLSegmentationNode':
      logging.debug('isValidInputOutputData failed: input segmentation node is the wrong type.')
    if not inputCutPointsNode:
      logging.debug('isValidInputOutputData failed: no input cut points markups node defined.')
      return False
    if not inputCutPointsNode.GetClassName() =='vtkMRMLMarkupsFiducialNode':
      logging.debug('isValidInputOutputData failed: input cut points node is the wrong type.')
      return False
    if inputSegNode.GetID()==inputCutPointsNode.GetID():
      logging.debug('isValidInputOutputData failed: your input nodes are the same.')
      return False
    if inputTagText != 'Pro' and inputTagText != 'Sup':
      logging.debug('isValidInputOutputData failed: the patient tag is incorrect. Must be \'Sup\' or \'Pro\'')
      return False
    return True

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    slicer.util.delayDisplay('Take screenshot: '+description+'.\nResult is available in the Annotations module.', 3000)

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qimage = ctk.ctkWidgetsUtils.grabWidget(widget)
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, 1, imageData)

  def run(self, inputSegmentation, inputCutPoints, pathText, tagType):
    """
    Run the actual algorithm
    """

    # if the input is not valid, do not run and tell the user
    if not self.isValidInputOutputData(inputSegmentation, inputCutPoints, pathText, tagType):
      slicer.util.errorDisplay('The input and output data is not correct. Please fix and try again. ')
      return False

    logging.info('Processing started')

    # get the path and key words to name and find files
    self.patientFolder = pathText
    self.patId = self.patientFolder[-8:]
    self.mode = tagType

    # use the directory path and keyword to name each type of file that will need to be created
    # paths will be used to write to file, names will be used to name nodes in scene
    self.cutPointsPath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'CutPoints.txt')
    self.curvaturesPath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'Curvatures.txt')
    self.curvaturesDataPath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'CurvaturesData.txt')
    self.curvaturesAcDataPath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'CurvaturesAcData.txt')
    self.curvaturesTcDataPath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'CurvaturesTcData.txt')
    self.curvaturesDcDataPath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'CurvaturesDcData.txt')
    self.centerPointsPath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'CenterPoints.fcsv')
    self.curveName = self.patId + '_' + self.mode + 'Curve'
    self.curvePath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'Curve.vtk')
    self.maximumPointsPath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'MaxPoints.fcsv')
    self.minimumPointsPath = os.path.join(self.patientFolder, self.patId + '_' + self.mode + 'MinPoints.fcsv')
    self.maximumPointsName = self.patId + '_' + self.mode + 'MaxPoints'
    self.minimumPointsName = self.patId + '_' + self.mode + 'MinPoints'


    #generate an output volume


    # convert the segmentation to a binary labelmap
    self.binLabelMapNode = self.convertSegmentationToBinaryLabelmap(inputSegmentation)

    # get the centerpoints through the binary label map via Extract Skeleton
    self.centerPointsNode = self.genCenterPoints(self.binLabelMapNode)
    # save the centerpoints to file
    slicer.util.saveNode(self.centerPointsNode, self.centerPointsPath)

    # use Markups to Model to fit a curve to the centerpoints
    self.curveNode = self.fitCurve(self.centerPointsNode)

    # use Curve Maker to get all point curvatures and save them to a text file
    self.makeCurvaturesFile(self.curveNode)
    # save the curve model to file
    slicer.util.saveNode(self.curveNode, self.curvePath)
    self.makeCutPointsFile(inputCutPoints)

    # takes the curvatures file and adds various columns to the curvature data files
    self.addDetails(self.curvaturesPath, self.curvaturesDataPath)
    self.addSumCurvaturesToDataFile(self.curvaturesDataPath, 0) # TODO fix hardcode
    self.addSumCurvatureMaxMinsToDataFile(self.curvaturesDataPath, 0, 1, 1.5)
    self.addDegreeChangesToFile(self.curvaturesDataPath)

    # split the main data file to data files corresponding to individual segments.
    self.splitDataFileToFiles(self.curvaturesDataPath, self.cutPointsPath)

    # retrieve key stats from data files
    self.getStats(self.curvaturesDataPath)
    self.getStats(self.curvaturesAcDataPath)
    self.getStats(self.curvaturesTcDataPath)
    self.getStats(self.curvaturesDcDataPath)

    # add the fiducials on the computed max/mins to the scene
    self.addFiducialsOnCurvatureMaximums(self.curvaturesDataPath)
    self.addFiducialsOnCurvatureMinimums(self.curvaturesDataPath)


    logging.info('Processing completed')

    return True


class AnalyzeColonTest(ScriptedLoadableModuleTest):
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
    self.test_AnalyzeColon1()

  def test_AnalyzeColon1(self):
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
    logic = AnalyzeColonLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
