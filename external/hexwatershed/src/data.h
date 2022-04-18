
/**
 * @file data.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief The header of data I/O component source code.
 * @version 0.1
 * @date 2017-01-25
 * @citation Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). 
 * Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 104702.
 * https://www.sciencedirect.com/science/article/pii/S1364815219308278
 * @github page https://github.com/changliao1025/hexwatershed
 * @copyright Copyright (c) 2019
 * 
 */
#pragma once

//50==================================================
//C header
//50==================================================
//C++ header
#include <algorithm>
#include <array>  //the small sized array
#include <fstream> //file stream
#include <iterator> //for vector and stream
#include <string> //c++ string
#include <vector> //vector
#include "system.h"
//50==================================================
using namespace std;
//50==================================================
class data
{
 public:
  data();
  ~data();
  //50==================================================
  //Traditional data IO
  //50==================================================
  static float * read_binary(std::string sFilename_in);
  static float ** read_binary(std::string sFilename_in,
                              long lColumn_in,
                              long lRow_in);
  static std::vector<float> read_binary_vector(std::string sFilename_in);
  static int write_binary_vector(std::string sFilename_in,
                                 vector <float> vData_in);
  //50==================================================
  //advanced data io using MPI
  //dataIO using PETSc
  //50==================================================
  //Mat Read_Binary(string filErtame,int m,int n);
  //50==================================================
};
