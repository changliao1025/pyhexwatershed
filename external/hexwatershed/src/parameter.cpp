
/**
 * @file flowline.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief
 * @version 0.1
 * @date 2019-06-11Created by Chang Liao on 4/26/18.
 *
 * @copyright Copyright (c) 2019
 *
 */

#include "parameter.h"

namespace hexwatershed
{

  parameter::parameter()
  {
    iFlag_global = 0;
    iFlag_multiple_outlet=0;
    iFlag_elevation_profile = 0;
    dAccumulation_threshold = 0.01;
    dBreach_threshold = 5.0; //unit in meter
  }

  parameter::~parameter()
  {
  }



} // namespace hexwatershed
