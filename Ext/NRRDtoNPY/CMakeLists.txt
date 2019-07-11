cmake_minimum_required(VERSION 3.5)

project(NRRDtoNPY)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/NRRDtoNPY")
set(EXTENSION_CATEGORY "Colon Analysis")
set(EXTENSION_CONTRIBUTORS "Keiran Barr (Perk Lab)")
set(EXTENSION_DESCRIPTION "Convert nrrd volumes to npy arrays to prepare for deep learning applications")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/NRRDtoNPY.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/NRRDtoNPY/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(NRRDtoNPY)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
