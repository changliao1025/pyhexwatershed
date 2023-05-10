#pragma once

#include "JSONBase.h"
#include <list>
#include <vector>
namespace jsonmodel
{
  class link : public JSONBase
  {
  public:
    link();		    
    virtual ~link();		
    
    virtual bool Deserialize(const rapidjson::Value& obj);
    virtual bool Serialize(rapidjson::Writer<rapidjson::StringBuffer>* writer) const;

    long lCellID_start;
    long lCellID_end;
  private:
    
  };	
}