//
// Created by Liao, Chang on 2020-09-07.
//

#pragma once
#include <iostream>
#include "hexagon.h"
#include "./json/JSONBase.h"
#include "./json/mesh.h"
#include "./json/cell.h"
#include "./json/basin.h"
#include "./json/multibasin.h"
using namespace std;
namespace hexwatershed
  {
      class subbasin
      {
      public:
          subbasin();

          ~subbasin();

          int iSubbasin; //each subbasin should have the same index with its segment
          int iSubbasinIndex;
          long nCell;
          long lCellID_outlet; //the index of the subbasin outlet
          float dArea;
          float dSlope;
          float dSlope_mean;
          float dSlope_max;
          float dSlope_min;
          float dArea_2_stream_ratio; //the drainage density: https://en.wikipedia.org/wiki/Drainage_density
          float dLength_2_area_ratio; //the drainage density: https://en.wikipedia.org/wiki/Drainage_density
          float dDistance_to_subbasin_outlet;
          float dDrainage_density;
          hexagon cCell_outlet; //the outlet of this subbasin, this cell is actually within the subbasin because it is shared by multiple subbasin
          std::vector <hexagon> vCell;
          

          //function
          int calculate_subbasin_characteristics(float dLength_stream_conceptual);
          int calculate_subbasin_total_area();
          int calculate_subbasin_slope();
          int calculate_subbasin_drainage_density(float dLength_stream_conceptual);
          int calculate_travel_distance();
          long subbasin_find_index_by_cellid(long lCellID_in);
      };
  } // namespace hexwatershed
