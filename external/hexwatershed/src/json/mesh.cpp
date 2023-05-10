#include "mesh.h"

namespace jsonmodel
{
	

	bool mesh::Deserialize(const std::string& s)
	{
		rapidjson::Document doc;
		if (!InitDocument(s, doc))
			return false;

		if (!doc.IsArray())
			return false;		

		for (rapidjson::Value::ConstValueIterator itr = doc.Begin(); itr != doc.End(); ++itr)
		{
			cell pCell;
			pCell.Deserialize(*itr);
			aCell.push_back(pCell);
		}

		return true;
	}

	bool mesh::Serialize(rapidjson::PrettyWriter<rapidjson::StringBuffer>* writer) const
	{
		writer->StartArray();

		for (std::list<cell>::const_iterator it = aCell.begin(); it != aCell.end(); it++)
		{
			(*it).Serialize(writer);
		}
		writer->EndArray();

		return true;
	}
}