//
// Created by Liao, Chang on 2020-09-07.
//

#include "subbasin.h"

namespace hexwatershed
{

  subbasin::subbasin()
  {
  }
  subbasin::~subbasin()
  {
  }

  int subbasin::calculate_subbasin_characteristics(float dLength_stream_conceptual)
  {
    int error_code = 1;
    calculate_subbasin_total_area();
    calculate_subbasin_drainage_density(dLength_stream_conceptual);
    return error_code;
  }

  int subbasin::calculate_subbasin_total_area()
  {
    int error_code = 1;
    float dArea_total = 0.0;
    std::vector<hexagon>::iterator iIterator;

    for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
    {
      if ((*iIterator).dArea < 0.0)
      {
        std::cout << "Something is wrong" << std::endl;
      }
      dArea_total = dArea_total + (*iIterator).dArea;
    }
    dArea = dArea_total;
    if (dArea < 0.0)
    {
      std::cout << "Something is wrong" << std::endl;
    }

    return error_code;
  }

  int subbasin::calculate_subbasin_drainage_density(float dLength_stream_conceptual)
  {
    int error_code = 1;
    dArea_2_stream_ratio = dArea / dLength_stream_conceptual;

    dLength_2_area_ratio = 1.0 / dArea_2_stream_ratio;
    dDrainage_density = dLength_2_area_ratio;

    return error_code;
  }
} // namespace hexwatershed