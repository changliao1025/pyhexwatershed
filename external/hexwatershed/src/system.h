/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * @file system.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief 
 * @version 0.1
 * @date 2019-08-02
 * 
 * @copyright Copyright (c) 2019
 * 
 */
#pragma once
//the global variables for all other modules
//c library
#include <limits.h>
#include <stdio.h>
#include <cstring>
//c++ library

#include <fstream>
#include <iostream>

#include <string>
//50==================================================
//cros-platform header
#ifdef _WIN32
//define something for Windows (32-bit and 64-bit, this part is common)
#include <direct.h>
#include <windows.h>
#ifdef _WIN64
//define something for Windows (64-bit only)
#else
//define something for Windows (32-bit only)
#endif
#elif __APPLE__
#include <sys/stat.h>
#include <TargetConditionals.h>
#if TARGET_IPHONE_SIMULATOR
// iOS Simulator
#elif TARGET_OS_IPHONE
// iOS device
#elif TARGET_OS_MAC
// Other kinds of Mac OS
#else
#error "Unknown Apple platform"
#endif
#elif __linux__
// linux
#include <sys/stat.h>
#include <sys/types.h>
#elif __unix__ // all unices not caught above
// Unix
#elif defined(_POSIX_VERSION)
// POSIX
#else
#error "Unknown compiler"
#endif

//50==================================================
#include "global.h"

//50==================================================
using namespace std;
//50==================================================
//functions
//50==================================================

//50==================================================
//test whether a file exists or not
//50==================================================
int file_test(std::string sFilename);

//50==================================================
//make directory ()
//50==================================================
int make_directory(std::string sDirectory);

//50==================================================
//check whether a directory exists or not
//50==================================================
int path_test(std::string sPath);

int run_command(std::string sCommand);

long get_file_size(std::string sFilename);
