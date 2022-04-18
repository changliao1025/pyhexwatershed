
/**
 * @file hexagon.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief 
 * @version 0.1
 * @date 2019-06-11Created by Chang Liao on 4/26/18.
 * 
 * @copyright Copyright (c) 2019
 * 
 */

#include "hexagon.h"

namespace hexwatershed
{

  hexagon::hexagon()
  {
    iFlag_confluence = 0;
    iFlag_active = 0;
    iFlag_watershed = 0;
    iFlag_first_reach = 0;
    iFlag_last_reach = 0;
    iFlag_headwater = 0;
    iFlag_stream = -1;
    iFlag_stream_burned = 0;

    iFlag_stream_burning_treated = 0;
    iFlag_depression_filling_treated = 0;

    iFlag_confluence_burned = 0;
    iFlag_headwater_burned =0;
    iStream_segment_burned = -1;
    lCellID_downstream_burned = -1;//only assign it if we found on
    iStream_order_burned = -1;
    iFlag_outlet = -1;
    lCellID_downslope_dominant = -1;

    dAccumulation = 0.0;
    iSubbasin = -1;
    iSegment = -1;
    iSegment_order = -1;
    iSegment_downstream = -1;
    nUpslope = 0;
    nUpstream = 0;

    nVertex = -1;
    dArea = -9999.0;
    dElevation_mean = 0.0;
    dElevation_downstream = -9999.0;


    dSlope = 0.0;   
    dSlope_within= 0.0;
    dSlope_max_downslope= 0.0;
    dSlope_min_downslope= 0.0;
    dSlope_mean_downslope= 0.0;
    dSlope_max_upslope= 0.0;
    dSlope_min_upslope= 0.0;
    dSlope_mean_upslope= 0.0;
    dSlope_mean_between= 0.0;
     
    dz = -9999.0;

    dTwi = 0.0;
    dLength_stream_conceptual = 0.0;
    dLength_stream_burned=0.0;
  }

  hexagon::~hexagon()
  {
  }

  
  
  /**
   * @brief calculate the mean edge length
   * 
   * @return int 
   */
  int hexagon::calculate_average_edge_length()
  {
    int error_code = 1;
    float dLength = 0.0;
    std::vector<edge>::iterator iIterator;
    for (iIterator = vEdge.begin(); iIterator != vEdge.end(); iIterator++)
    {
      dLength = dLength + (*iIterator).dLength;
    }
    dLength_edge_mean = dLength / (nEdge);
    return error_code;
  }

  /**
   * @brief calculate the effective resolution using area
   * 
   * @return int 
   */
  int hexagon::calculate_effective_resolution()
  {
    int error_code = 1;
    float dLength = 0.0;   
    dLength = sqrt( dArea );    
    dResolution_effective = dLength ;
    dLength_stream_conceptual = dResolution_effective;
    return error_code;
  }

 
  /**
   * @brief update the x y z location
   * 
   * @return int 
   */
  int hexagon::update_location()
  {
    int error_code =1;

    std::array<float, 3> aLocation = calculate_location_based_on_lon_lat_radian(dLongitude_center_radian, dLatitude_center_radian, dElevation_mean);
    dx = aLocation[0];
    dy = aLocation[1];
    dz = aLocation[2];

    return error_code;
  }

} // namespace hexwatershed