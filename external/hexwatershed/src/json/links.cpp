#include "links.h"

namespace jsonmodel
{
	

	bool links::Deserialize(const std::string& s)
	{
		rapidjson::Document doc;
		if (!InitDocument(s, doc))
			return false;

		if (!doc.IsArray())
			return false;

		for (rapidjson::Value::ConstValueIterator itr = doc.Begin(); itr != doc.End(); ++itr)
		{
			link pLink;
			pLink.Deserialize(*itr);
			aLink.push_back(pLink);
		}

		return true;
	}

	bool links::Serialize(rapidjson::Writer<rapidjson::StringBuffer>* writer) const
	{
		writer->StartArray();

		for (std::vector<link>::const_iterator it = aLink.begin(); it != aLink.end(); it++)
		{
			(*it).Serialize(writer);
		}
		writer->EndArray();

		return true;
	}
}