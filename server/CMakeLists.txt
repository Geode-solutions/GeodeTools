# Copyright (c) 2019 - 2021 Geode-solutions
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

cmake_minimum_required(VERSION 3.18)

#-------------------------------------------------------------------------------
# Project options
project(GeodeTools CXX)

set(PYTHON_VERSION 3 CACHE STRING "Python version to use")
message(STATUS "Using Python 3")
set(VTK_PYTHON_VERSION "3")
if(DEFINED ENV{Python3_ROOT_DIR})
    message(STATUS "Using Python3_ROOT_DIR = $ENV{Python3_ROOT_DIR}")
    set(PYTHON_ROOT 
        -DPython3_ROOT_DIR:PATH=$ENV{Python3_ROOT_DIR}
    )
endif()

if(DEFINED ENV{Python3_EXECUTABLE})
    message(STATUS "Using Python3_EXECUTABLE = $ENV{Python3_EXECUTABLE}")
    set(PYTHON_EXE 
        -DPython3_EXECUTABLE:FILEPATH=$ENV{Python3_EXECUTABLE}
    )
endif()

message(STATUS "PYTHON_ROOT = ${PYTHON_ROOT}")
message(STATUS "PYTHON_EXE = ${PYTHON_EXE}")

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
        -DCMAKE_PREFIX_PATH=$ENV{Python3_ROOT_DIR}
    CMAKE_CACHE_ARGS
        -DCMAKE_C_FLAGS_DEBUG:INTERNAL=${NEW_FLAGS}
        -DCMAKE_CXX_FLAGS_DEBUG:INTERNAL=${NEW_FLAGS}
        -DVTK_WRAP_PYTHON:BOOL=ON
        -DPYTHON_VERSION:STRING=${PYTHON_VERSION}
        -DVTK_PYTHON_VERSION:STRING=${VTK_PYTHON_VERSION}
        -DVTK_GROUP_ENABLE_Web:STRING=YES
        -DVTK_BUILD_TESTING:BOOL=OFF
        -DVTK_LEGACY_REMOVE:BOOL=ON
        -DCMAKE_INSTALL_PREFIX:PATH=${VTK_INSTALL_PREFIX}
        -DPython3_FIND_STRATEGY:STRING=LOCATION
        ${PYTHON_ROOT}
        ${PYTHON_EXE}
)
