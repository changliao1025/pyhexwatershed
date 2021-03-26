
/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
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
        iFlag_first_reach =0;
        iFlag_last_reach = 0;
        iFlag_headwater =0;
        lIndex_downslope = -1;

        lAccumulation = 0;
        iSubbasin = -1;
        iSegment = -1;
        iSegment_order = -1;
        iSegment_downstream =-1;
        nUpslope = 0;

        nPtVertex = -1;
        //dLength_edge = 500; //this should be read from the user configuration
        dTwi =0.0;
      }

      hexagon::~hexagon()
      {

      }
  }