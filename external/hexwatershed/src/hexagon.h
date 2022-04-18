/**
 * @file hexagon.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief The header file the hexagon class.
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

#include <string>
#include <vector>
#include <array>
#include "global.h"
#include "json/vertex.h"
#include "edge.h"
#include "flowline.h"
using namespace std;
using namespace jsonmodel;
namespace hexwatershed
{
  class hexagon
  {
  public:
    hexagon();

    ~hexagon();


    long lCellIndex;       //real id used when elevation is assigned
    long lCellID;   //this is the mesh id from the shapefile, it might be the same with Global ID,
    // this depends upon how mesh id was generated, it can be different from global id

    int iFlag_active;        //if it has elevation assigned
    int iFlag_watershed;     //whether it is inside a watershed
    int iFlag_stream;        //whether it is a stream grid
    int iFlag_stream_burned; //flag for burned stream grid
 
  //be careful, a stream grid maybe visited multiple if breaching is enabled

    int iFlag_stream_burning_treated;
    int iFlag_depression_filling_treated;//flag to indicate whether a cell is treated for elevation

    int iStream_segment_burned;
    int iStream_order_burned;
    int nFlowline_burned;
    int iFlag_confluence_burned;
    int iFlag_headwater_burned;

    int iFlag_first_reach; //whether it is the first reach of a stream
    int iFlag_last_reach;  //whether it is the last reach of a stream
    int iFlag_headwater;   //whether the stream segment is headwater, but we should set it to segment level?
    int iFlag_neighbor;    //this flag is used to check whether a hexagon is neighbor to another hexagon
    int iFlag_outlet;      //whether this hexagon is an outlet or not
    int iFlag_confluence;  //whether this hexagon is a stream confluence or not, confluence is where stream meets.

    int iSegment;       //the stream segment index
    int iSegment_order; //the stream order of segment, there are different type of definition
    int iSubbasin;      //the subbasin index, should be the same with the segment

    int nNeighbor; //number of neighbors, should be equal or less than nedge
    int nNeighbor_land;
    int nNeighbor_ocean;
    int nUpslope;  //all upslope including stream
    int nDownslope;
    int nUpstream;           //only consider stream upslope
    int iSegment_downstream; //if a hexagon is a stream, this is the downstream index, -1 for outlet

    int nVertex; //the vertex number from polygon, should always be constant for uniform resolution, for MPAS, this can be 5, 6, 7
    int nEdge; //total number of edge
    long lCellID_downslope_dominant; //the downslope hexagon local ID
    
    long lCellID_downstream_burned;//the downstream mesh ID

    float dAccumulation;             //the flow accumulation value. it does not consider area of hexagon in this version
    float dAspect; //maybe used for radiation
    float dSlope;

    float dSlope_within; //slope based on fine DEM

    float dSlope_max_downslope; //the maximum slope among all neighbors (unitless, it is a ratio)
    float dSlope_min_downslope;
    float dSlope_mean_downslope;

    float dSlope_max_upslope; //the maximum slope among all neighbors (unitless, it is a ratio)
    float dSlope_min_upslope;
    float dSlope_mean_upslope;

    float dSlope_mean_between;
    float dSlope_elevation_profile0;

    float dLength_edge_mean;          //the edge/face length of hexagon (unit:m)
    float dResolution_effective;
    float dx;                    //map projection, (unit:m)
    float dy;                    //map projection, (unit:m)
    float dz;                    //map projection, (unit:m)
    float dLongitude_center_degree;            //GCS, (unit:degree)
    float dLatitude_center_degree;             //GCS, (unit:degree)
    float dLongitude_center_radian;            //GCS, (unit:degree)
    float dLatitude_center_radian;             //GCS, (unit:degree)
    
    float dElevation_mean;            //from DEM, (unit:m)
    float dElevation_profile0;            //from DEM, (unit:m)
    float dElevation_raw;            //from DEM, (unit:m)
    float dElevation_downstream; //down stream elevation for breach algorithm
    float dArea;                 //the area of hexagon,  (unit:m2)
    float dTwi;                  //terrain wetness index
    float dLength_stream_conceptual;//conceptual length based on mesh
    float dLength_stream_burned; //the provided flowline length

    std::vector<long> vNeighbor;  //list of neighbor local id
    std::vector<float> vNeighbor_distance;  //list of neighbor local id

    std::vector<long> vNeighbor_land;  //list of neighbor local id
    std::vector<long> vUpslope;   //list of upslope local id
    std::vector<long> vDownslope; //list of downslope local id, new feature to support multiple downslope

    std::vector<long> vUpstream; //list of upslope local id

    std::vector<long> vVertex_index; //
    std::vector<vertex> vVertex;     //list of vertex
    std::vector<edge> vEdge;         //list of vertex
    std::vector<flowline> vFlowline; //list of vertex


    int calculate_average_edge_length();
    int calculate_effective_resolution();

    int update_location();
  };

} // namespace hexwatershed
