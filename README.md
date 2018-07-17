# ColonCurvature
A set of tools to analyze the curvature of colon segmentations. 

The overall process:
1. Use the extract skeleton module in slicer (extension) to get a set of points along the
centerline of the colon. 
The code for automating just this step is contained in the file ExtractLineScript.py
This code can be run through a slicer instance by typing execfile(pathToScript) into the
slicer python interpreter. 

2. Use the Markups to Model module in slicer (extension) to fit a curve to the point. 
The code for automating this step is in the file CurveFromMarkups.ipynb
The code is a jupyter file, and can be run through a slicer instance accordingly. 

3. Use the computeCenterlines function from the Curve Maker module (extension) to
calculate the curvature at every point along the curve produced from step 2. 
The code for automating this process is CurvatureModelling.ipynb 
The code is a jupyter file, and can be run through slicer accordingly. 


However, as the above scripts were completed, a single script which integrated all of the above
functionality was written. The file AllAnalysis.py contains all of the functions described above, 
and has code to run through all of the steps analyzing a segmentation to a list of curvatures at points. 

IMPORTANT! The scripts that automate and string together the different functions depend upon the 
naming scheme and organization of your files. 

A walkthrough of the process:

To start, you have a project folder. 
Inside are several folders, each titled with an 8 digit patient ID such as PTAK0070.
Inside the patient folder PTAK0070 is between one, two, and three files.
There files are the segmentaions of the patients colon in suppine, prone, and or left down positions. 
There files are named as patID_ProSeg.seg.nrrd, for example PTAK0070_SupSeg.seg.nrrd.
In each segmentation, there is a segment labeled 'colon' and one labeled 'notColon'. 

Once you are set up, edit AllAnalysis.py in a text editor like Notepad++.
Inside you will find functions to:
-Get centerpoints of a colon seg from file,
-Fit a curve to markups 
-Get an output file containing a curve fit to a fiducial file
-Get a textfile with curvatures at every point for a curve file

You will also find commented code blocks which automate the processes of curve fitting 
and getting curvature at points for multipe patients. 

The last function in the file, analyzePatient(patientPath, modeList = ['sup', 'pro'])
is a function which takes the path to the patient file described above,
and a list containing the types of scans you are working with. Use 'sup' for supine, 'pro' for prone,
and 'ld' for left down. 

Once you have filled in the patient directory and the types of segmentations you want to process into
the analyzePatient function call at the bottom, save the file, and run the file in a slicer instance. 
You can run the file in a slicer instance with: execfile("scriptPath")
 


