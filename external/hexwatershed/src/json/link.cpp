#include <string>
#include "link.h"

namespace jsonmodel
{
	link::link() 
	{
		
	}

	link::~link()
	{
		
	}	
	
	
	bool link::Deserialize(const rapidjson::Value & obj)
	{
		std::string sKey;
		
		
		sKey = "pCell_start";
		if (obj.HasMember(sKey.c_str()))
		{
			this->lCellID_start= obj[sKey.c_str()].GetInt64();
		}
		sKey = "pCell_end";
		if (obj.HasMember(sKey.c_str()))
		{
			this->lCellID_end= obj[sKey.c_str()].GetInt();
		}
		
		
        


		return true;
	}

	bool link::Serialize(rapidjson::Writer<rapidjson::StringBuffer> * writer) const
	{
		writer->StartObject();
		//writer->String("id");
		//writer->Int(_id);
		//writer->String("name");
		//writer->String(_name.c_str());
		//writer->String("category");
		//writer->String(_category.c_str());
		//writer->String("sales");
		//writer->Double(_sales);
		writer->EndObject();

		return true;
	}	
}