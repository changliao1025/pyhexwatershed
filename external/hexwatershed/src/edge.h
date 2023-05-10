/**
 * @file edge.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Header file of the flowline class
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

#include <cmath>
#include <vector>
#include "json/vertex.h"

using namespace std;
using namespace jsonmodel;
namespace hexwatershed
{
    class edge {
     public:
      edge ();

      ~edge ();

      float dLength;

      vertex cVertex_start;
      vertex cVertex_end;

      int calculate_length ();

      int check_point_overlap (vertex pt);

      int check_overlap (vertex pt_start, vertex pt_end);

      int check_shared (edge ed);
    };
} // namespace hexwatershed
