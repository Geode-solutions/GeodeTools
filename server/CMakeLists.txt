# Copyright (c) 2019 - 2020 Geode-solutions
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

cmake_minimum_required(VERSION 3.11)

#-------------------------------------------------------------------------------
# Project options
project(GeodeTools CXX)

set(PYTHON_VERSION 3 CACHE STRING "Python version to use")
message(STATUS "Using Python 3")
set(VTK_PYTHON_VERSION "3")
if(DEFINED ENV{Python3_ROOT_DIR})
    message(STATUS "Using Python_ROOT_DIR = $ENV{Python3_ROOT_DIR}")
    set(EXTRA_VTK_OPTIONS 
        -DPython3_FIND_STRATEGY:STRING=LOCATION
        -DPython3_ROOT_DIR:PATH=$ENV{Python3_ROOT_DIR}
    )
else()
    if(PYTHON_EXECUTABLE)
        message(STATUS "Using PYTHON_EXECUTABLE = ${PYTHON_EXECUTABLE}")
        set(EXTRA_VTK_OPTIONS -DPython3_EXECUTABLE:STRING=${PYTHON_EXECUTABLE})
    endif()
    if(PYTHON_LIBRARY)
        message(STATUS "Using PYTHON_LIBRARY = ${PYTHON_LIBRARY}")
        set(EXTRA_VTK_OPTIONS -DPython3_LIBRARY:STRING=${PYTHON_LIBRARY} ${EXTRA_VTK_OPTIONS})
    endif()
    if(PYTHON_INCLUDE_DIR)
        message(STATUS "Using PYTHON_INCLUDE_DIR = ${PYTHON_INCLUDE_DIR}")
        set(EXTRA_VTK_OPTIONS -DPython3_INCLUDE_DIR:STRING=${PYTHON_INCLUDE_DIR} ${EXTRA_VTK_OPTIONS})
    endif()
endif()


include(ExternalProject)

set(VTK_PATH ${PROJECT_BINARY_DIR}/vtk)
set(VTK_INSTALL_PREFIX ${VTK_PATH}/install)
string(REPLACE "/MDd" "/MD" NEW_FLAGS ${CMAKE_CXX_FLAGS_DEBUG})
ExternalProject_Add(vtk
    PREFIX ${VTK_PATH}
    URL https://www.vtk.org/files/release/9.0/VTK-9.0.1.tar.gz
    URL_MD5 b3ba14d616c3b23583c42cffb585deac
    CMAKE_GENERATOR ${CMAKE_GENERATOR}
    CMAKE_GENERATOR_PLATFORM ${CMAKE_GENERATOR_PLATFORM}
    CMAKE_ARGS
        -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
        -DCMAKE_INSTALL_MESSAGE=LAZY
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
    CMAKE_CACHE_ARGS
        -DCMAKE_C_FLAGS_DEBUG:INTERNAL=${NEW_FLAGS}
        -DCMAKE_CXX_FLAGS_DEBUG:INTERNAL=${NEW_FLAGS}
        -DVTK_WRAP_PYTHON:BOOL=ON
        -DVTK_PYTHON_VERSION:STRING=${VTK_PYTHON_VERSION}
        -DVTK_GROUP_ENABLE_Web:STRING=YES
        -DVTK_BUILD_TESTING:BOOL=OFF
        -DVTK_LEGACY_REMOVE:BOOL=ON
        -DCMAKE_INSTALL_PREFIX:PATH=${VTK_INSTALL_PREFIX}
        ${EXTRA_VTK_OPTIONS}
)
