/**
 * @file domain.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Header file of the domain class
 * @version 0.1
 * @date 2019-08-02
 * @citation Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020).
 * Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 104702.
 * https://www.sciencedirect.com/science/article/pii/S1364815219308278
 * @github page https://github.com/changliao1025/hexwatershed
 * @copyright Copyright (c) 2019
 *
 */

 #pragma once
#include <cmath>
#include <ctime>
#include <string>
#include <fstream>
#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <queue>
#include <numeric>
#include <utility>

#include "../compset/compset.h"


#include "../../rapidjson/document.h"
#include "../../rapidjson/writer.h"
#include "../../rapidjson/stringbuffer.h"
#include "../../rapidjson/istreamwrapper.h"

#include "../json/JSONBase.h"
#include "../json/mesh.h"
#include "../json/cell.h"
#include "../json/basin.h"
#include "../json/multibasin.h"


using namespace std;
using namespace rapidjson;
using namespace jsonmodel;


namespace hexwatershed
{
  class domain {
  public:
    domain ();
    domain (std::string sFilename_configuration_in);
    ~domain ();

    std::string sWorkspace_input;
    std::string sWorkspace_output;
    std::string sWorkspace_output_pyflowline;
    std::string sWorkspace_output_hexwatershed;
    
    std::string sFilename_log;
    std::string sLog;

    std::string sFilename_mesh_info;
    std::string sFilename_flowline_info;
    //polygon vector filename
    std::string sFilename_elevation_polygon;
    std::string sFilename_elevation_polygon_debug;

    std::string sFilename_slope_between_polygon;
    std::string sFilename_slope_between_polygon_debug;
    std::string sFilename_slope_within_polygon;
    std::string sFilename_slope_within_polygon_debug;

    std::string sFilename_flow_accumulation_polygon;
    std::string sFilename_flow_accumulation_polygon_debug;

    std::string sFilename_watershed_polygon;
    std::string sFilename_stream_confluence_polygon;

    std::string sFilename_stream_grid_polygon;
    std::string sFilename_stream_grid_polygon_debug;

    std::string sFilename_subbasin_polygon;

    std::string sFilename_stream_segment_polygon;

    std::string sFilename_wetness_index_polygon;

    //polyline
    std::string sFilename_stream_segment_polyline;
    std::string sFilename_stream_segment_merge_polyline;
    std::string sFilename_flow_direction_polyline;
    std::string sFilename_flow_direction_polyline_debug;
    std::string sFilename_stream_order_polyline;

    std::string sFilename_basins;

    //vtk support
    std::string sFilename_vtk;
    std::string sFilename_vtk_debug;      



    //others
    std::string sDate_default;
    std::string sDate;
    
    std::string sFilename_mesh;

    std::string sExtension_json;

    std::ofstream ofs_log; // used for IO starlog file

    //std::map <std::string, std::string> mParameter; //for input data and parameters

    //rapidjson object
    jsonmodel::mesh cMesh;
    jsonmodel::multibasin cBasin;

    rapidjson::Document pConfigDoc;
    rapidjson::Document pConfigDoc_basin;

    //for global
    std::vector<long> lCellIndex_outlet;
    std::vector<long> lCellID_outlet;

    compset cCompset; //currently we only support one compset per run
    //function
    int domain_read ();
    int domain_read_configuration_file ();
    int domain_read_elevation_json(std::string sFilename_elevation_in);
    int domain_read_basin_json(std::string sFilename_basin_in);

    int domain_assign_parameter ();
    int domain_read_input_data();
    int domain_initialize ();
    int domain_retrieve_user_input();
    int domain_run ();
    int domain_save ();
    int domain_cleanup ();
    int domain_setup();


  };
} // namespace hexwatershed
