
/**
 * @file edge.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief 
 * @version 0.1
 * @date 2019-06-11 Created by Chang Liao on 4/26/18.
 * 
 * @copyright Copyright (c) 2019
 * 
 */

#include "edge.h"

namespace hexwatershed
{

    edge::edge()
    {
    }

    edge::~edge()
    {
    }
    

    /**
     * @brief calculate the arc length of an edge on a sphere
     * 
     * @return int 
     */
    int edge::calculate_length()
    {
        int error_code = 1;
        dLength = cVertex_end.calculate_distance(cVertex_start);
        if (dLength < 0.001)
        {
            //something is wrong
        }
        return error_code;
    }

    /**
     * @brief check whether a vertex is one the edge or not
     * 
     * @param pVertex_in 
     * @return int 
     */

    int edge::check_point_overlap(vertex pVertex_in)
    {
        int overlap = 0;
        float diff;
        float dDistance1, dDistance2;
        dDistance1 = pVertex_in.calculate_distance(this->cVertex_start);
        dDistance2 = pVertex_in.calculate_distance(this->cVertex_end);
        diff = this->dLength - (dDistance1 + dDistance2);
        if (abs(diff) < 0.01)
        {
            overlap = 1;
        }
        return overlap;
    }

    /**
     * @brief check whether an edge overlap with another edge, this algorithm has error
     * 
     * @param pVertex_start 
     * @param pVertex_end 
     * @return int 
     */
    int edge::check_overlap(vertex pVertex_start, vertex pVertex_end)
    {
        int error_code = 1;
        int overlap = 0;
        float diff;
        float dDistance1, dDistance2, dDistance3, dDistance4;
        dDistance4 = pVertex_start.calculate_distance(pVertex_end);
        dDistance1 = cVertex_start.calculate_distance(pVertex_start);
        dDistance2 = cVertex_start.calculate_distance(pVertex_end);

        if (dDistance1 < dDistance2)
        {
            dDistance2 = cVertex_end.calculate_distance(pVertex_end);
            //now we have all distance
            diff = dLength - (dDistance1 + dDistance2 + dDistance4);
            if (abs(diff) < 0.001)
            {
                //they are overlap
                overlap = 1;
            }
            else
            {
                overlap = 0;
            }
        }
        else
        {
            dDistance1 = cVertex_start.calculate_distance(pVertex_end);
            dDistance2 = cVertex_end.calculate_distance(pVertex_start);

            //now we have all distance
            diff = dLength - (dDistance1 + dDistance2 + dDistance4);
            if (abs(diff) < 1)
            {
                //they are overlap
                overlap = 1;
            }
            else
            {
                overlap = 0;
            }
        }

        return overlap;
    }

    /**
     * @brief check whether two edge are the same ignoring the direction
     * 
     * @param pEdge_in 
     * @return int 
     */
    int edge::check_shared(edge pEdge_in)
    {
        int iFlag_shared = 0;

        if (this->cVertex_start == pEdge_in.cVertex_start && this->cVertex_end == pEdge_in.cVertex_end)
        {
            iFlag_shared = 1;
            return iFlag_shared;
        }
        else
        {
            if (this->cVertex_start == pEdge_in.cVertex_end && this->cVertex_end == pEdge_in.cVertex_start)
            {
                iFlag_shared = 1;
                return iFlag_shared;
            }
            else
            {
                iFlag_shared = 0;
            }
        }

        return iFlag_shared;
    }
} // namespace hexwatershed