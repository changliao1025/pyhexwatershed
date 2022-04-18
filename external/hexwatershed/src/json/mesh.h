#pragma once

#include "cell.h"
#include <list>
#include <iostream>
namespace jsonmodel
{
  class mesh : public JSONBase
  {
  public:		
   //mesh() {};
    virtual ~mesh() {};
    virtual bool Deserialize(const std::string& s);		

    std::list<cell> aCell;
  public:
    virtual bool Deserialize(const rapidjson::Value& obj) { return false; };
    virtual bool Serialize(rapidjson::PrettyWriter<rapidjson::StringBuffer>* writer) const;
  private:
    
  };
}