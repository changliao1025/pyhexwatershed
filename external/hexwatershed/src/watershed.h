/**
 * @file watershed.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief This class provide interface to watershed characteristics, 
 * @version 0.1
 * @date 2019-08-02
 *  @citation Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). 
 * Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 104702.
 * https://www.sciencedirect.com/science/article/pii/S1364815219308278
 * @github page https://github.com/changliao1025/hexwatershed
 * @copyright Copyright (c) 2019
 * 
 */
#pragma once
#include <cmath>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <vector>
#include "conversion.h"
#include "hexagon.h"
#include "segment.h"
#include "subbasin.h"

using namespace std;

namespace hexwatershed
  {
      //some improvements are needed in next development
      class watershed
      {
      public:
          watershed();

          ~watershed();

          float dArea;
          float dSlope;
          float dSlope_mean;
          float dSlope_max;
          float dSlope_min;
          long nCell;
          long nSegment;
          long nSubbasin;
   
          long lCellID_outlet; //the mesh ID of the outlet

          float dArea_2_stream_ratio; //the drainage density: https://en.wikipedia.org/wiki/Drainage_density
          float dLength_2_area_ratio; //the drainage density: https://en.wikipedia.org/wiki/Drainage_density
          float dDrainage_density;
          float dLongest_length_stream; //the length of longest stream segment
          float dLength_stream_conceptual; //total stream length

          std::vector <hexagon> vCell;
          std::vector <segment> vSegment;
          std::vector <subbasin> vSubbasin;

          //function

          int watershed_build_stream_topology();

          int watershed_define_stream_order();

          //the watershed characteristics for comparison
          int calculate_watershed_characteristics();

          int calculate_watershed_drainage_area();

          int calculate_watershed_total_stream_length();

          int calculate_watershed_longest_stream_length();

          int calculate_watershed_drainage_density();

          int calculate_watershed_average_slope();

          int calculate_topographic_wetness_index();

          int save_watershed_characteristics(std::string sFilename_in);
      };
  }


