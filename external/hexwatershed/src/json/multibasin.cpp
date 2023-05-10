#include "multibasin.h"

namespace jsonmodel
{
	

	bool multibasin::Deserialize(const std::string& s)
	{
		rapidjson::Document doc;
		if (!InitDocument(s, doc))
			return false;

		if (!doc.IsArray())
			return false;
		
		
		

		for (rapidjson::Value::ConstValueIterator itr = doc.Begin(); itr != doc.End(); ++itr)
		{
			basin pBasin;
			pBasin.Deserialize(*itr);
			aBasin.push_back(pBasin);
		}

		return true;
	}

	bool multibasin::Serialize(rapidjson::PrettyWriter<rapidjson::StringBuffer>* writer) const
	{
		writer->StartArray();

		for (std::list<basin>::const_iterator it = aBasin.begin(); it != aBasin.end(); it++)
		{
			(*it).Serialize(writer);
		}
		writer->EndArray();

		return true;
	}
}