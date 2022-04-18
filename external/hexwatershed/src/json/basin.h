#pragma once

#include "JSONBase.h"
#include <list>
#include <vector>
namespace jsonmodel
{
  class basin : public JSONBase
  {
  public:
    basin();		    
    virtual ~basin();
    
    virtual bool Deserialize(const rapidjson::Value& obj);
    virtual bool Serialize(rapidjson::PrettyWriter<rapidjson::StringBuffer>* writer) const;

    int iFlag_dam;
    
    
    float dLongitude_outlet_degree;
    float dLatitude_outlet_degree;
    
    long lCellID_outlet;
    long lBasinID;
    
    
  private:
    
  };	
}