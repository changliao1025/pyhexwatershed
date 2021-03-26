/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * @file segment.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Header file of the stream segment class
 * @version 0.1
 * @date 2019-08-02
 * 
 * @copyright Copyright (c) 2019
 * 
 */


#include <vector>

#include "hexagon.h"

using namespace std;
namespace hexwatershed
{
    class segment
    {
    public:
        segment();

        ~segment();

        int nReach;
        int iSegment;
        //int iSegment_upstream; do not use because one stream can have 2 upstream segment
        int iSegment_downstream;
        int iSegment_order;
        int iFlag_headwater;
        int iFlag_has_upstream;
        int iFlag_has_downstream;
        int nSegment_upstream;
        std::vector<int> vSegment_upstream;

        hexagon cReach_start;
        hexagon cReach_end;
        std::vector<hexagon> vReach_segment;

//sort 
        bool operator < (const segment& cSegment) const
    {
        return (iSegment < cSegment.iSegment);
    }


    };
}


