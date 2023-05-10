/**
 * @file flowline.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Header file of the flowline class
 * @version 0.1
 * @date 2019-08-02
 * @citation Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). 
 * Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 104702.
 * https://www.sciencedirect.com/science/article/pii/S1364815219308278
 * @github page https://github.com/changliao1025/hexwatershed
 * @copyright Copyright (c) 2019
 * 
 */
#pragma once
#include <vector>
#include <algorithm>
#include "json/vertex.h"

using namespace std;
using namespace jsonmodel;
namespace hexwatershed
{
    class flowline
    {
    public:
        flowline();

        ~flowline();

        long lCellID;
        int iFlag_merged;
        int iFlag_active;
        int iFlag_new; //this is a new flowline

        int iStream_segment;
        int iStream_order;
        float dLength;
        //int iFlag_multiLine;
        std::vector<vertex> vVertex; //store all the vertex of this line

        vertex cVertex_start;
        vertex cVertex_end;

       
        int share_vertex(flowline pFlowline_in);
        int share_vertex(flowline pFlowline_in, vertex pVertex_in);
        
    };
} // namespace hexwatershed
