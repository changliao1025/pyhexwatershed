
/**
 * @file segment.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief
 * @version 0.1
 * @date 2019-08-02
 *
 * @copyright Copyright (c) 2019
 *
 */
#include "segment.h"

namespace hexwatershed
{
  segment::segment()
  {
    iFlag_headwater = 0;
    iSegment = 0;
    iSegmentIndex = -1;
    iSegment_order = -1;
    iSegment_downstream = -1;

    iFlag_has_upstream = -1;
    iFlag_has_downstream = -1;
    nSegment_upstream = -1;
    dDistance_to_watershed_outlet = 0.0;
  }

  segment::~segment()
  {
  }

  bool segment::operator<(const segment &cSegment)
  {
    return (this->iSegment < cSegment.iSegment);
  }

  /**
   * @brief
   *
   * @return int
   */
  int segment::calculate_stream_segment_characteristics()
  {
    int error_code = 1;
    calculate_stream_segment_length();
    calculate_stream_segment_slope();
    return error_code;
  }

  /**
   * @brief calculate stream segment length
   *
   * @return int
   */
  int segment::calculate_stream_segment_length()
  {
    int error_code = 1;
    float dLength_total = 0.0;

    std::vector<hexagon>::iterator iIterator;
    for (iIterator = vReach_segment.begin(); iIterator != vReach_segment.end(); iIterator++)
    {
      dLength_total = dLength_total + (*iIterator).dLength_stream_conceptual;
    }

    dLength = dLength_total;

    return error_code;
  }

  int segment::calculate_stream_segment_slope()
  {
    int error_code = 1;
    float dElevation_diff;
    float dElevation_min, dElevation_max;

    if (nReach == 1)
    {
      // there is only reach
      dSlope_mean = vReach_segment[0].dSlope_max_downslope;
      dElevation_drop = dSlope_mean * dLength;
    }
    else
    {
      dElevation_max = vReach_segment.front().dElevation_mean;
      dElevation_min = vReach_segment.back().dElevation_mean;
      dElevation_diff = dElevation_max - dElevation_min;
      dElevation_drop = dElevation_diff;
      dSlope_mean = dElevation_diff / dLength;
    }

    return error_code;
  }
  int segment::calculate_travel_distance()
  {
    int error_code = 1;
    return error_code;
  }
} // namespace hexwatershed
