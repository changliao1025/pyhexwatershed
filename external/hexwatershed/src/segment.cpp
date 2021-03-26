
/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
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
      iSegment_order=-1;
      iSegment_downstream =-1;
      //iSegment_upstream=-1;
      iFlag_has_upstream = -1;
      iFlag_has_downstream=-1;
      nSegment_upstream =-1;

    }

    segment::~segment()
    {

    }
}
