
/**
 * @file flowline.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief 
 * @version 0.1
 * @date 2019-06-11 Created by Chang Liao on 4/26/18.
 * 
 * @copyright Copyright (c) 2019
 * 
 */

#include "flowline.h"

namespace hexwatershed
{

    flowline::flowline()
    {
        lCellID = -1;
        iFlag_merged = 0;
        iFlag_active = 1;
        iFlag_new = 0;
        iStream_segment = -1;
        iStream_order = -1;
    }

    flowline::~flowline()
    {
    }

    
    /**
     * @brief check whether two flowlines share a starting or ending vertex
     * 
     * @param pFlowline_in 
     * @return int 
     */
    int flowline::share_vertex(flowline pFlowline_in)
    {
        int iFlag_share = 0;
        vertex pVertex1, pVertex2;

      pVertex1 = pFlowline_in.cVertex_start;
      pVertex2 = pFlowline_in.cVertex_end;

        if (pVertex1 == cVertex_start || pVertex1 == cVertex_end || pVertex2 == cVertex_start || pVertex2 == cVertex_end)
        {
            iFlag_share = 1;
        }

        return iFlag_share;
    }

    /**
     * @brief check two flowlines share the specified vertex
     * 
     * @param pFlowline_in 
     * @param pVertex_shared 
     * @return int 
     */
    int flowline::share_vertex(flowline pFlowline_in, vertex pVertex_shared)
    {
        int iFlag_share = 0;
        std::vector<long> aOut;
        vertex pVertex1, pVertex2, pVertex3, pVertex4;

        pVertex1 = pFlowline_in.cVertex_start;
        pVertex2 = pFlowline_in.cVertex_end;
        pVertex3 = cVertex_start;
        pVertex4 = cVertex_end;

        if (pVertex3 == pVertex_shared || pVertex4 == pVertex_shared)
        {
            if (pVertex1 == pVertex_shared )
            {
                iFlag_share = 1;

            }
            else
            {
               if (pVertex2 == pVertex_shared)
               {
                    iFlag_share = 1;
               }

            }
            
        }

        return iFlag_share;
    }
} // namespace hexwatershed