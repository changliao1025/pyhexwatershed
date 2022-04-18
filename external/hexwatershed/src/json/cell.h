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
    std::vector<long> aNeighbor;
    std::vector<long> aNeighbor_land;
    std::vector<long> aNeighbor_ocean;

    std::vector<float> aNeighbor_distance;  //list of neighbor local id
    std::vector<vertex> vVertex;
    
    float dElevation_mean;
    float dElevation_profile0;
    float dElevation_raw;
    float dLatitude_center_degree;
    float dLongitude_center_degree;
    //float dLatitude_center_radian;
    //float dLongitude_center_radian;
    //float dz;
    float dArea;
    float dAccumulation;
    float dSlope_between;
    float dSlope_within;
    float dSlope_profile;
    float dLength_flowline;
    float dLength;
   
    int nEdge;
    int nNeighbor;
    int nNeighbor_land;
    int nNeighbor_ocean;
    int nVertex;
    int iStream_segment_burned;
    int iStream_order_burned;
    long lCellID;
    long lCellID_downstream_burned;
    long lCellID_downslope;
    
  private:
    
  };	
}