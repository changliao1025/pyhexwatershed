#pragma once

#include "link.h"
#include <vector>
#include <iostream>
namespace jsonmodel
{
  class links : public JSONBase
  {
  public:		
    virtual ~links() {};
    virtual bool Deserialize(const std::string& s);		

    std::vector<link> aLink;
  public:
    virtual bool Deserialize(const rapidjson::Value& obj) { return false; };
    virtual bool Serialize(rapidjson::Writer<rapidjson::StringBuffer>* writer) const;
  private:
    
  };
}