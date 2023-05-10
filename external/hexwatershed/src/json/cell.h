#pragma once

#include "JSONBase.h"
#include "vertex.h"
#include "../conversion.h"
#include <list>
#include <vector>
namespace jsonmodel
{
  class cell : public JSONBase
  {
  public:
    cell();		    
    virtual ~cell();
    
    virtual bool Deserialize(const rapidjson::Value& obj);
    virtual bool Serialize(rapidjson::PrettyWriter<rapidjson::StringBuffer>* writer) const;

    //Getters/Setters.
    //std::vector<long> aEdge;
    std::vector<long> aNeighbor; /*!<neighbor ID*/
    std::vector<long> aNeighbor_land; /*!<land neighbor ID*/
    std::vector<long> aNeighbor_ocean;/*!<ocean neighbor ID*/
    std::vector<float> aNeighbor_distance;  /*!<neighbor distance*/
    std::vector<vertex> vVertex;
    
    float dElevation_mean; /*!<average elevation*/
    float dElevation_profile0; /*!<elevation profile*/
    float dElevation_raw;  /*!<original elevation*/
    float dLatitude_center_degree; /*!<latitude*/
    float dLongitude_center_degree; /*!<longitude*/

    //float dLatitude_center_radian;
    //float dLongitude_center_radian;
    //float dz;

    float dArea;  /*!<cell area*/
    float dAccumulation; /*!<flow accumulation*/
    float dSlope_between; /*!<slope between this cell and downslope cell*/
    float dSlope_within; /*!<slope based on high resolution DEM*/
    float dSlope_profile; /*!<slope based on elevation profile between downslope cell*/
    float dLength_flowline; /*!<flowline length*/
    float dLength; /*!<effective cell length*/

    float dDistance_to_downslope; /*!<distance to downsloe*/
    float dDistance_to_subbasin_outlet; /*!< distance to subbasin outlet*/
    float dDistance_to_watershed_outlet; /*!< distance to watershed outlet*/
   
    int nEdge;
    int nNeighbor;
    int nNeighbor_land;
    int nNeighbor_ocean;
    int nVertex; /*!<number of vertex*/
    int iStream_segment_burned;
    int iStream_order_burned;
    int iStream_segment;
    int iSubbasin;
    long lCellID; /*!<global cell ID*/
    long lCellID_downstream_burned;/*!<pre-descibed global downstream cell ID*/
    long lCellID_downslope;/*!<global downslope cell ID*/
    
  private:
    
  };	
}