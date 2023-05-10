/**
 * @file system.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Provide interface to the hexagon vertex 
 * @version 0.1
 * @date 2019-08-02
 * @citation Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). 
 * Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 104702.
 * https://www.sciencedirect.com/science/article/pii/S1364815219308278
 * @github page https://github.com/changliao1025/hexwatershed
 * @copyright Copyright (c) 2019
 * 
 */
#pragma once

#include <string>
#include <cmath>
#include "../global.h"
#include "../geology.h"

using namespace std;
namespace jsonmodel
  {
      class vertex
      {
      public:
          vertex();
          ~vertex();

          long lVertexIndex; //reserved
          float dx; //3d sphere (unit: m)
          float dy; //3d (unit: m)
          float dz; // (unit: m)
          float dElevation; // (unit: m)
          float dLongitude_degree;
          float dLatitude_degree;
          
          float dLongitude_radian;
          float dLatitude_radian;

          bool operator==(const vertex &cVertex);
          
          int update_location();

          float calculate_slope( vertex pt );
          float calculate_distance( vertex pt );
      };
  } // namespace jsonmodel