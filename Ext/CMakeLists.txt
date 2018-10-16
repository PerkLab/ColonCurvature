cmake_minimum_required(VERSION 3.5)

project(ColonCurvature)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/ColonCurvature")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Jacob Laframboise (Laboratory for Percutaneous Surgery)")
set(EXTENSION_DESCRIPTION "This extension contains functionality to analyze curvature of colons, and compare them. ")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/ColonCurvature.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/ColonCurvature/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(AnalyzeColon)
add_subdirectory(PatientComparison)
add_subdirectory(CompareColonResults)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
