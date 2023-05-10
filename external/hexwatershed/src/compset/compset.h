/**
 * @file edge.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Header file of the case class
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
#include <list>
#include <vector>
#include <map>
#include <algorithm>
#include <numeric>
#include <cmath> // abs, floor

#include "../system.h"
#include "../hexagon.h"
#include "../flowline.h"
#include "../conversion.h"
#include "../watershed.h"
#include "../parameter.h"


#include "../json/JSONBase.h"
#include "../json/mesh.h"
#include "../json/cell.h"
#include "../json/basin.h"
#include "../json/multibasin.h"

using namespace std;
using namespace rapidjson;
using namespace jsonmodel;

enum eMesh_type {
                 eM_hexagon,
                 eM_square,
                 eM_latlon,
                 eM_triangle,
                 eM_mpas,
};

enum eVariable {
                eV_elevation,
                eV_flow_direction,
                eV_flow_accumulation,
                eV_stream_grid,
                eV_confluence,
                eV_watershed,
                eV_subbasin,
                eV_segment,
                eV_slope_between,
                eV_slope_within,
                eV_stream_order,
                eV_wetness_index,
};

namespace hexwatershed
{


  class compset {
  public:
    compset ();

    ~compset ();    

    int nWatershed_total;
    int nSegment_total;            //the total number of stream segment
    int nConfluence_total;         //the total number of stream confluence
  
       
    std::string sWorkspace_input;
    std::string sWorkspace_output;

    std::string sWorkspace_output_pyflowline;
    std::string sWorkspace_output_hexwatershed;
    
    std::string sFilename_configuration;
    std::string sFilename_log;
    std::string sLog;
    std::string sFilename_mesh_info;    

    std::string sFilename_domain_json;
    std::string sFilename_json;
    std::string sFilename_animation_json;

    //vtk support
    std::string sFilename_vtk;
    std::string sFilename_vtk_debug;

    //others
    std::string sDate_default;
    std::string sDate;
  
    std::ofstream ofs_log; // used for IO starlog file

    //std::map <std::string, std::string> mParameter; //for input data and parameters
    std::vector <hexagon> vCell;                    //all the cells based on shapefile
    std::vector <hexagon> vCell_active;             //all calls has elevation (not missing value)
    std::vector <hexagon> vCell_priority_flood;             //all calls has elevation (not missing value)
    //watershed cWatershed;
    std::vector <watershed> vWatershed;
    std::vector<float> vElevation; //vector to store the DEM raster data
    std::vector <flowline> vFlowline;
    // this may be merged with global id
    std::vector <vertex> vVertex_active; //for vtk support, it store all the vertex in 3D

    std::string sFilename_netcdf_output; //if model use netcdf, we can put all results into one single netcdf file,
    // except the txt based results.
    std::string sFilename_hexagon_netcdf;
    parameter cParameter;
    std::vector<cell> aCell;
    std::vector<basin> aBasin;
    std::vector<hexagon> vContinent_boundary;
    //std::vector<instance> vInstance;

    int compset_initialize_model ();
    int compset_setup_model ();
    int compset_read_model();
    int compset_run_model ();
    int compset_save_model ();
    int compset_cleanup_model ();

    int compset_assign_stream_burning_cell();
    int compset_priority_flood_depression_filling ();
    int compset_stream_burning_with_topology (long lCellID_center);
    int compset_stream_burning_without_topology (long lCellID_center);
    int compset_breaching_stream_elevation (long lCellID_center);
    int compset_calculate_flow_direction ();
    int compset_calculate_flow_accumulation ();
    int compset_define_stream_grid ();
    int compset_define_watershed_boundary ();
    int compset_define_stream_confluence ();
    int compset_define_stream_segment ();
    int compset_tag_confluence_upstream (int iWatershed, long lCellID_confluence);

    int compset_build_stream_topology();
    int compset_define_stream_order();
    int compset_define_subbasin ();
    int compset_calculate_watershed_characteristics ();

    int compset_save_watershed_characteristics ();
  

    int compset_transfer_watershed_to_domain();

    int compset_save_vtk (std::string sFilename_in);
    int compset_save_json(std::string sFilename_in);
    int compset_save_domain_json(std::string sFilename_in);
    int compset_save_animation_json(std::string sFilename_in);
    std::vector <hexagon> compset_obtain_boundary (std::vector <hexagon> vCell_in);
    long compset_find_index_by_cell_id(long lCellID);
    

    int find_continent_boundary(long lCellID_in);
    int find_land_ocean_interface_neighbors(long lCellID_in);

    int priority_flood_depression_filling(std::vector <hexagon> vCell_in);
    int compset_update_cell_elevation();
    int compset_update_vertex_elevation();

    int compset_check_digital_elevation_model_depression (std::vector <hexagon> vCell_in);

    std::array<long, 3> compset_find_lowest_cell_in_priority_queue (std::vector <hexagon> vCell_in);

  };
} // namespace hexwatershed
