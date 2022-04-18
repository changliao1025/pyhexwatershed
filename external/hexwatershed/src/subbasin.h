//
// Created by Liao, Chang on 2020-09-07.
//

#pragma once
#include <iostream>
#include "hexagon.h"

using namespace std;
namespace hexwatershed
  {
      class subbasin
      {
      public:
          subbasin();

          ~subbasin();

          int iSubbasin; //each subbasin should have the same index with its segment
          long nCell;
          long lID_outlet; //the index of the subbasin outlet
          float dArea;
          float dSlope;
          float dSlope_mean;
          float dSlope_max;
          float dSlope_min;
          float dArea_2_stream_ratio; //the drainage density: https://en.wikipedia.org/wiki/Drainage_density
          float dLength_2_area_ratio; //the drainage density: https://en.wikipedia.org/wiki/Drainage_density
          float dDrainage_density;

          std::vector <hexagon> vCell;

          //function
          int calculate_subbasin_characteristics(float dLength_stream_conceptual);
          int calculate_subbasin_total_area();

          int calculate_subbasin_drainage_density(float dLength_stream_conceptual);
      };
  } // namespace hexwatershed
