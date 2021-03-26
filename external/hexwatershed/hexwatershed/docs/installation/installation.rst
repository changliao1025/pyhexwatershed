############
Installation
############


********
Overview
********

This document provides the instruction to build the HexWatershed model.

************
Requirements
************

It is possible to build the HexWatershed on Linux/Mac/Windows as long as your system has the following libraries:

* cmake 3.1.0 and above
* GCC 5.2.0 and above
* GDAL 2.3.1

=====
CMake
=====

cmake is the tool used to generate the makefile.

cmake can be installed through a package manager. If you are on a Linux HPC, you administration should have already installed in most cases.

If you are on a Mac computer, cmake can be installed through Homebrew (https://brew.sh/).

===
GCC
===

GCC is the compiler used to compile the source code.

Similar to cmake, you can install GCC on linux or Mac.

==========================================
GDAL
==========================================

HexWatershed relies on GDAL C++ API (https://gdal.org/) to operate on Shapefile and other spatial datasets.
In this version, I only tested GDAL version 2.3.1.

In this instruction, I only use a Linux machine as an example. For other platforms, you need to change several files:

- CMakeLists.txt
- cmake.sh (Optional)
- make.sh (Optional)

There are several outdated CMakeLists.txt files in this directory for different platforms such as Mac OS, you can use it as a template. I use two bash scripts to simplify the process of setting environmental variables. For your own platform and application, you may use different approach.

Figures are provided for illustration when needed.

***********
Instruction 
***********

- In the terminal, create a folder for this project
- Clone the repository into the folder with::

    git clone git@github.com:pnnl/hexwatershed.git
 
- Create a folder outside the hexwatershed repository::
 
    mkdir CMake
 
- Go into the CMake folder and copy the CMakeLists.txt file from the repository into the CMake folder::
 
    cp ./installation/figure/CMakeLists.txt  ./
    cp ./installation/figure/cmake.sh  ./
    cp ./installation/figure/make.sh  ./
 
You should also change the permission of the bash files::
 
    chmod 755 cmake.sh
    chmod 755 make.sh
 
- Open the CMakeLists.txt file and edit the path of gdal based on your system with your preferred editor.

The highlight rectangle is where you can change the gdal library.



- Run the cmake bash script to load modules and run the cmake command::
 
    ./cmake.sh
 


This script should generates some results as follow:

- Run the make bash file::
 
    ./make.sh




This script should generates some results as follow:



- By now, your build should be successful if you receive no errors. And you will see the binary file in the CMake folder and another one within the repository as well.



Congratulations, you have successfully built the HexWatershed model!

Now you can test the model with the example following this instruction: https://github.com/pnnl/hexwatershed/tree/master/example
