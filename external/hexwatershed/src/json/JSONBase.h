#pragma once
#include "../../external/rapidjson/rapidjson.h"
#include "../../external/rapidjson/prettywriter.h"// for stringify JSON
#include "../../external/rapidjson/document.h"// rapidjson's DOM-style API
#include "../../external/rapidjson/writer.h"
#include "../../external/rapidjson/stringbuffer.h"	// wrapper of C stream for prettywriter as output
#include "../../external/rapidjson/istreamwrapper.h"
#include <string>
#include <fstream>
#include <sstream>
using namespace std;
namespace jsonmodel
{
  class JSONBase
  {
  public:
    JSONBase();
    virtual ~JSONBase();
    bool DeserializeFromFile(const std::string& filePath);
    bool SerializeToFile(const std::string& filePath);

    virtual std::string Serialize() const;
    virtual bool Deserialize(const std::string& s);
    virtual bool Deserialize(const rapidjson::Value& obj) = 0;
    virtual bool Serialize(rapidjson::PrettyWriter<rapidjson::StringBuffer>* writer) const = 0;
  protected:
    bool InitDocument(const std::string & s, rapidjson::Document &doc);
  };
}
