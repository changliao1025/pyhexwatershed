#pragma once
#include "../../rapidjson/rapidjson.h"
#include "../../rapidjson/prettywriter.h"// for stringify JSON
#include "../../rapidjson/document.h"// rapidjson's DOM-style API
#include "../../rapidjson/writer.h"
#include "../../rapidjson/stringbuffer.h"	// wrapper of C stream for prettywriter as output
#include "../../rapidjson/istreamwrapper.h"
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
