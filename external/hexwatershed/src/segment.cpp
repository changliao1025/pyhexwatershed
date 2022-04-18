
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
    iSegment_order = -1;
    iSegment_downstream = -1;

    iFlag_has_upstream = -1;
    iFlag_has_downstream = -1;
    nSegment_upstream = -1;
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
} // namespace hexwatershed
