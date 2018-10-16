'''This file will hold functions that will allow one to check the success of colon centerline analysis. 
It has functions to add fiducials to the maximums of a curve from the data file to a slicer instance, 
and do the saem for minimums. 
It also has functions to generate test curves to validate the process. '''

import math


def addFiducialsOnCurvatureMaximums(inPath):
    '''A function to take the path of the curvatures data file, and generate slicer fiducials on the model to verify'''
    fIn = open(inPath, 'r')
    lines = fIn.readlines()
    fIn.close()
    xVals = []
    yVals = []
    zVals = []

    for x in range(1, len(lines)):
        if lines[x].strip().split(', ')[7] == 'MAX':
            xVals.append(lines[x].strip().split(', ')[2])
            yVals.append(lines[x].strip().split(', ')[3])
            zVals.append(lines[x].strip().split(', ')[4])
    m = slicer.vtkMRMLMarkupsFiducialNode()
    m.SetName('Maxs')
    slicer.mrmlScene.AddNode(m)

    for i in range(len(xVals)):
        m.AddFiducial(float(xVals[i]), float(yVals[i]), float(zVals[i]))


def addFiducialsOnCurvatureMinimums(inPath):
    '''A function to take the path of the curvatures data file, and generate slicer fiducials
    on the model's extreme values to verify'''
    fIn = open(inPath, 'r')
    lines = fIn.readlines()
    fIn.close()
    xVals = []
    yVals = []
    zVals = []

    for x in range(1, len(lines)):
        if lines[x].strip().split(', ')[7] == 'MIN':
            xVals.append(lines[x].strip().split(', ')[2])
            yVals.append(lines[x].strip().split(', ')[3])
            zVals.append(lines[x].strip().split(', ')[4])
    m = slicer.vtkMRMLMarkupsFiducialNode()
    m.SetName('Mins')
    slicer.mrmlScene.AddNode(m)

    for i in range(len(xVals)):
        m.AddFiducial(float(xVals[i]), float(yVals[i]), float(zVals[i]))


def generateQuadraticCurve():
    '''A function to generate a known curve for analysis. '''
    coords = []

    for x in range(-100, 100):
        coords.append((100, x, (x / 5) ** 2))

    markups = slicer.vtkMRMLMarkupsFiducialNode()
    slicer.mrmlScene.AddNode(markups)
    for i in coords:
        markups.AddFiducial(i[0], i[1], i[2])


def generate2DQuadraticCurve():
    '''A function to generate a known curve for analysis. '''
    coords = []

    for x in range(-100, 100):
        coords.append((((x + 50) / 5) ** 2, ((x - 50) / 5) ** 2, (x / 5) ** 2))

    markups = slicer.vtkMRMLMarkupsFiducialNode()
    slicer.mrmlScene.AddNode(markups)
    for i in coords:
        markups.AddFiducial(i[0], i[1], i[2])


def generateCubicCurve():
    '''A function to generate a known curve for analysis. '''
    coords = []

    for x in range(-200, 200):
        coords.append((100, x, (x / 20) ** 3))

    markups = slicer.vtkMRMLMarkupsFiducialNode()
    slicer.mrmlScene.AddNode(markups)
    for i in coords:
        markups.AddFiducial(i[0], i[1], i[2])


def generateSinCurve():
    '''A function to generate a known curve for analysis. '''
    coords = []

    for x in range(-50, 50):
        res = 2
        x2 = x / res

        exp = 20
        coords.append((100, x2 * exp, exp * math.sin(x2)))

    markups = slicer.vtkMRMLMarkupsFiducialNode()
    slicer.mrmlScene.AddNode(markups)
    for i in coords:
        markups.AddFiducial(i[0], i[1], i[2])


def genCurve():
    '''A function to generate a known curve for analysis. '''
    coords = []

    for x in range(-40, 40):
        res = 2
        x2 = x / res

        exp = 10
        coords.append((x2 ** 2, x2 * exp, exp * math.sin(x2)))

    markups = slicer.vtkMRMLMarkupsFiducialNode()
    slicer.mrmlScene.AddNode(markups)
    for i in coords:
        markups.AddFiducial(i[0], i[1], i[2])


#genCurve()


dataPath = r"C:\Users\jaker\OneDrive - Queen's University\ColonCurves_JL\CtVolumes\PTCI0052\PTCI0052_SupCurvaturesData.txt"
addFiducialsOnCurvatureMaximums(dataPath)
addFiducialsOnCurvatureMinimums(dataPath)
