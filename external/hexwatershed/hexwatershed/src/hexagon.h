/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * @file hexagon.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief The header file the hexagon class.
 * @version 0.1
 * @date 2019-08-02
 * 
 * @copyright Copyright (c) 2019
 * 
 */
#pragma once

#include <string>
#include <vector>
#include <array>

using namespace std;
namespace hexwatershed
  {

      struct ptVertex
      {
          double dX; //map projection
          double dY; //map projection
      };
      class hexagon
      {
      public:
          hexagon();

          ~hexagon();

          long lGlobalID;
          long lID;
          int iFlag_active;
          int iFlag_watershed;
          int iFlag_stream;
          int iFlag_first_reach;
          int iFlag_last_reach;
          int iFlag_headwater;
          int iFlag_neighbor;

          int iSegment;
          int iSegment_order;
          int iSubbasin;
          int iFlag_confluence;
          int nNeighbor;
          int nUpslope;
          int iSegment_downstream;

          int nPtVertex; //the vertex number from polygon
          //std::string sMeta;
          long lIndex_downslope;
          long lAccumulation;
            
          double dSlope;
          double dLength_edge;
          double dX; //map projection
          double dY; //map projection
          double dLatitude;
          double dLongitude;
          double dElevation;
          double dArea;
          double dTwi;
          //std::array<long, 6> aNeighbor;
          std::vector<long> vNeighbor;
          std::vector<long> vUpslope;
          std::vector<ptVertex> vPtVertex;

      };

  }

