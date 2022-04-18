#include <string>
#include "cell.h"

namespace jsonmodel
{
	cell::cell() 
	{
	iStream_segment_burned=-1;
	iStream_order_burned=-1;	

	dAccumulation=0.0;
	lCellID=-1;
	lCellID_downslope=-1;
	lCellID_downstream_burned=-1;
	dElevation_mean=-9999.0;
	dElevation_profile0=-9999.0;
	dElevation_raw = -9999.0;
	dLatitude_center_degree=-9999.0;
	dLongitude_center_degree=-9999.0;
	dArea=-9999.0;
	nEdge=0;
	nVertex=0;
	nNeighbor=0;
	nNeighbor_land=0;
	nNeighbor_ocean=0;

	dSlope_between =-9999.0;
	dSlope_within = -9999.0;
	}

	cell::~cell()
	{
		
	}	
	
	
	bool cell::Deserialize(const rapidjson::Value & obj)
	{
		std::string sKey;
		sKey = "dElevation_mean";
		if (obj.HasMember(sKey.c_str()))
		{
			this->dElevation_mean= obj[sKey.c_str()].GetFloat();			
			this->dElevation_raw = this->dElevation_mean;
		}
		sKey = "dElevation_profile0";
		if (obj.HasMember(sKey.c_str()))
		{			
			this->dElevation_profile0= obj[sKey.c_str()].GetFloat();			
		}
		sKey = "dLatitude_center_degree";
		if (obj.HasMember(sKey.c_str()))
		{
			this->dLatitude_center_degree= obj[sKey.c_str()].GetFloat();
		}
		
		sKey = "dLongitude_center_degree";
		if (obj.HasMember(sKey.c_str()))
		{
			this->dLongitude_center_degree= obj[sKey.c_str()].GetFloat();
		}

		sKey = "dLength";
		if (obj.HasMember(sKey.c_str()))
		{
			this->dLength= obj[sKey.c_str()].GetFloat();
		}

		sKey = "dLength_flowline";
		if (obj.HasMember(sKey.c_str()))
		{
			this->dLength_flowline= obj[sKey.c_str()].GetFloat();
		}

		sKey = "dArea";
		if (obj.HasMember(sKey.c_str()))
		{
			this->dArea= obj[sKey.c_str()].GetFloat();
		}
		
		sKey = "lCellID";
		if (obj.HasMember(sKey.c_str()))
		{
			this->lCellID= obj[sKey.c_str()].GetInt64();
		}
		sKey = "lCellID_downstream_burned";
		if (obj.HasMember(sKey.c_str()))
		{
			this->lCellID_downstream_burned= obj[sKey.c_str()].GetInt64();
		}
		sKey = "iStream_segment_burned";
		if (obj.HasMember(sKey.c_str()))
		{
			this->iStream_segment_burned= obj[sKey.c_str()].GetInt();
		}
		sKey = "iStream_order_burned";
		if (obj.HasMember(sKey.c_str()))
		{
			this->iStream_order_burned= obj[sKey.c_str()].GetInt();
		}
		sKey = "nEdge";
		if (obj.HasMember(sKey.c_str()))
		{
			this->nEdge= obj[sKey.c_str()].GetInt();
		}
		sKey = "nNeighbor";
		if (obj.HasMember(sKey.c_str()))
		{
			this->nNeighbor= obj[sKey.c_str()].GetInt();
		}
		sKey = "nNeighbor_land";
		if (obj.HasMember(sKey.c_str()))
		{
			this->nNeighbor_land= obj[sKey.c_str()].GetInt();
		}
		sKey = "nNeighbor_ocean";
		if (obj.HasMember(sKey.c_str()))
		{
			this->nNeighbor_ocean= obj[sKey.c_str()].GetInt();
		}
		sKey = "nVertex";
		if (obj.HasMember(sKey.c_str()))
		{
			this->nVertex= obj[sKey.c_str()].GetInt();
		}      
		//for (int i = 0; i < this->nEdge; i++)
		//{
     	//	this->aEdge.push_back(obj["aEdge"][i].GetInt64());
		//}
		for (int i = 0; i < this->nNeighbor; i++)
		{
	 		this->aNeighbor.push_back(obj["aNeighbor"][i].GetInt64());
			this->aNeighbor_distance.push_back(obj["aNeighbor_distance"][i].GetFloat());
		}
		for (int i = 0; i < this->nNeighbor_land; i++)
		{
     		this->aNeighbor_land.push_back(obj["aNeighbor_land"][i].GetInt64());
		}
		const rapidjson::Value& rVertex = obj["aVertex"];
		assert(rVertex.IsArray());
		for (int i = 0; i < this->nVertex; i++)
		{
			vertex pVertex;  
			pVertex.dLongitude_degree = rVertex[i]["dLongitude_degree"].GetFloat();
			pVertex.dLatitude_degree = rVertex[i]["dLatitude_degree"].GetFloat();
			pVertex.dLongitude_radian = convert_degree_to_radian(pVertex.dLongitude_degree);
			pVertex.dLatitude_radian = convert_degree_to_radian(pVertex.dLatitude_degree);
			pVertex.dElevation = this->dElevation_raw;
			pVertex.update_location();
			this->vVertex.push_back(pVertex);
		}        


		return true;
	}

	bool cell::Serialize(rapidjson::PrettyWriter<rapidjson::StringBuffer> * writer) const
	{
      	std::vector<vertex>::const_iterator iIterator;
		//writer->SetIndent('\n',2);
		writer->StartObject();
		writer->String("lCellID");
		writer->Int64(lCellID);		
		writer->String("lCellID_downstream_burned");
		writer->Int64(lCellID_downstream_burned);		
		writer->String("lCellID_downslope");
		writer->Int64(lCellID_downslope);	
		writer->String("dLongitude_center_degree");
		writer->Double(dLongitude_center_degree);
		writer->String("dLatitude_center_degree");
		writer->Double(dLatitude_center_degree);
		writer->String("Area");
		writer->Double(dArea);
		writer->String("Elevation_raw");
		writer->Double(dElevation_raw);
		writer->String("Elevation");
		writer->Double(dElevation_mean);
		writer->String("Elevation_profile");
		writer->Double(dElevation_profile0);
		writer->String("dSlope_between");
		writer->Double(dSlope_between);
		writer->String("dSlope_profile");
		writer->Double(dSlope_profile);
		//writer->String("dSlope_within");
		//writer->Double(dSlope_within);
		writer->String("DrainageArea");
		writer->Double(dAccumulation);
		
		//vertex information		
		writer->Key("vVertex");
		writer->StartArray();		
		for (iIterator = this->vVertex.begin(); iIterator != this->vVertex.end(); ++iIterator)    
		{	
			writer->StartObject();					
			writer->Key("dLongitude_degree");
			writer->Double((*iIterator).dLongitude_degree);
			writer->Key("dLatitude_degree");
			writer->Double((*iIterator).dLatitude_degree);	
			writer->EndObject();					
		}	
		
		writer->EndArray();
		
		writer->EndObject();

		return true;
	}	
}