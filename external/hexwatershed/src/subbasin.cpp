//
// Created by Liao, Chang on 2020-09-07.
//

#include "subbasin.h"

namespace hexwatershed
{

  subbasin::subbasin()
  {
    iSubbasinIndex=-1;
  }
  subbasin::~subbasin()
  {
  }

  int subbasin::calculate_subbasin_characteristics(float dLength_stream_conceptual)
  {
    int error_code = 1;
    calculate_subbasin_total_area();
    calculate_subbasin_slope();
    calculate_subbasin_drainage_density(dLength_stream_conceptual);
    return error_code;
  }

  int subbasin::calculate_subbasin_total_area()
  {
    int error_code = 1;
    float dArea_total = 0.0;
    std::vector<hexagon>::iterator iIterator;
    nCell = vCell.size();

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

  int subbasin::calculate_subbasin_slope()
  {
    int error_code = 1;
    int iOption = 1;
    float dSlope_total = 0.0;
    std::vector<hexagon>::iterator iIterator;
    if (iOption == 1) // by cell
    {
      for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
      {
        dSlope_total = dSlope_total + (*iIterator).dSlope_max_downslope; // should mean slope?
      }
    }
    dSlope = dSlope_total / nCell;
    dSlope_mean = dSlope;
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
  int subbasin::calculate_travel_distance()
  {
    int error_code = 1;
    long lCellID_current;     
    long lCellIndex;
    float dDistance_to_subbasin_outlet;
    std::vector<hexagon>::iterator iIterator;
    for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
    {
      lCellID_current = (*iIterator).lCellID;
      if (lCellID_current !=lCellID_outlet)
      {
        dDistance_to_subbasin_outlet = (*iIterator).dDistance_to_downslope;         
        lCellID_current =  (*iIterator).lCellID_downslope_dominant;   
        while (lCellID_current != lCellID_outlet)
        {
          lCellIndex = subbasin_find_index_by_cellid(lCellID_current);
          lCellID_current = vCell.at(lCellIndex).lCellID_downslope_dominant;       
          dDistance_to_subbasin_outlet = dDistance_to_subbasin_outlet + vCell.at(lCellIndex).dDistance_to_downslope;  
        }

        (*iIterator).dDistance_to_subbasin_outlet = dDistance_to_subbasin_outlet;
      }
      else
      {
        (*iIterator).dDistance_to_subbasin_outlet = 0.0;
      }

      
    }

    return error_code;
  }
  long subbasin::subbasin_find_index_by_cellid(long lCellID_in)
  {
    long lCellIndex_subbasin = -1;
    std::vector<hexagon>::iterator iIterator;
    for (iIterator = vCell.begin(); iIterator != vCell.end(); iIterator++)
    {
      if ((*iIterator).lCellID == lCellID_in)
      {
        lCellIndex_subbasin = (*iIterator).lCellIndex_subbasin;
        break;
      }
    }

    return lCellIndex_subbasin;
  }
} // namespace hexwatershed