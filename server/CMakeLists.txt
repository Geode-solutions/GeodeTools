# Copyright (c) 2019 - 2022 Geode-solutions
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

cmake_minimum_required(VERSION 3.13)

#-------------------------------------------------------------------------------
# Project options
project(GeodeTools CXX)

set(PYTHON_VERSION 3 CACHE STRING "Python version to use")
set(VTK_PYTHON_VERSION "3")

message(STATUS "PYTHON_EXE = $ENV{PYTHON_EXE}")

include(ExternalProject)

set(VTK_PATH ${PROJECT_BINARY_DIR}/vtk)
set(VTK_INSTALL_PREFIX ${VTK_PATH}/install)
ExternalProject_Add(vtk
    PREFIX ${VTK_PATH}
    URL https://www.vtk.org/files/release/9.2/VTK-9.2.0.rc1.tar.gz
    URL_HASH SHA256=3d219ae624d0ce6d72bb9bdbf5895d0eaa875ff3115a61d3c300b257ea7c0f7e
    CMAKE_GENERATOR ${CMAKE_GENERATOR}
    CMAKE_GENERATOR_PLATFORM ${CMAKE_GENERATOR_PLATFORM}
    CMAKE_ARGS
        -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
        -DCMAKE_INSTALL_MESSAGE=LAZY
        -DCMAKE_BUILD_TYPE=Release
        -DCMAKE_INSTALL_PREFIX:PATH=${VTK_INSTALL_PREFIX}
    CMAKE_CACHE_ARGS
        -DVTK_INSTALL_SDK:BOOL=ON
        -DVTK_WRAP_PYTHON:BOOL=ON
        -DVTK_PYTHON_VERSION:STRING=3
        -DVTK_WHEEL_BUILD:BOOL=ON
        -DVTK_GROUP_ENABLE_Web:STRING=YES
        -DVTK_BUILD_TESTING:BOOL=OFF
        -DVTK_LEGACY_REMOVE:BOOL=ON
        -DPython3_FIND_STRATEGY:STRING=LOCATION
        -DPython3_EXECUTABLE:FILEPATH=$ENV{PYTHON_EXE}
)
