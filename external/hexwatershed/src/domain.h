
/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * @file domain.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief Header file of the domain class
 * @version 0.1
 * @date 2019-08-02
 * 
 * @copyright Copyright (c) 2019
 * 
 */
#include <cmath>
#include <string>
#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <queue>
#include <numeric>
#include <utility>

#include "ogrsf_frmts.h"
#include "system.h"
#include "hexagon.h"
#include "segment.h"
#include "conversion.h"

using namespace std;

enum eVariable
{
  eV_elevation,
  eV_flow_direction,
  eV_flow_accumulation,
  eV_confluence,
  eV_watershed,
  eV_subbasin,
  eV_segment,
  eV_stream_order,
  eV_wetness_index,
};

namespace hexwatershed
{
class domain
{
public:
  domain();

  domain(std::string sFilename_configuration);

  ~domain();

  int iFlag_debug;
  int iFlag_merge;
  int iFlag_configuration_file;

  int iFlag_hexagon_point;   //user provided point hexagon
  int iFlag_hexagon_polygon; //user provided polygon hexagon

  int iMesh_type; //1: qgis; 2: dggrid; 3: MPAS

  int nColumn_elevation;
  int nRow_elevation;
  int nColumn_mesh;
  int nRow_mesh;

  int nSegment;
  int iSegment_current;
  int iCase;
  long lOutlet;
  long nRecord_shapefile;

  long lCell_count;
  double dResolution_elevation;
  double dX_origin;
  double dY_origin;

  double dArea_watershed;
  double dLength_stream;
  double dLongest_length_stream;
  double dArea_2_stream_ratio;
  double dSlope_mean;

  double dAccumulation_threshold;
  
  double missing_value;

  std::string sRegion;
  std::string sWorkspace_data;
  std::string sWorkspace_output;
  std::string sFilename_configuration;
  std::string sFilename_log;
  std::string sLog;

  std::string sFilename_hexagon_point_shapefile;
  std::string sFilename_hexagon_polygon_shapefile;

  std::string sFilename_elevation_raster;

  //point vector filenames
  std::string sFilename_elevation_point;
  std::string sFilename_elevation_point_debug;

  std::string sFilename_flow_accumulation_point;
  std::string sFilename_flow_accumulation_point_debug;

  std::string sFilename_watershed_point;
  std::string sFilename_stream_confluence_point;

  std::string sFilename_subbasin_point;
  std::string sFilename_stream_grid_point;
  std::string sFilename_stream_grid_point_debug;

  std::string sFilename_stream_segment_point;
  std::string sFilename_wetness_index_point;
  //polygon vector filename
  std::string sFilename_elevation_polygon;
  std::string sFilename_elevation_polygon_debug;

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

  //others

  std::string sFilename_watershed_characteristics;

  std::string sExtension_header;
  std::string sExtension_envi;
  std::string sExtension_text;

  std::ofstream ofs_log; // used for IO starlog file

  std::map<std::string, std::string> mParameter; //for input data and parameters
  std::vector<hexagon> vCell;                    //all the cells based on shapefile
  std::vector<hexagon> vCell_active;             //all calls has elevation (not missing value)
  std::vector<hexagon> vCell_watershed;
  std::vector<segment> vSegment;
  std::vector<float> vElevation;
  std::vector<hexagon> vConfluence;

  OGRSpatialReference *oSRS;

  //function
  //setup
  int domain_setup_model();

  //read
  int domain_read_data();

  int domain_read_configuration_file();

  int domain_retrieve_user_input();

  int domain_read_all_cell_information(std::string sFilename_hexagon_point_shapefile_in,
                                       std::string sFilename_hexagon_polygon_shapefile_in,
                                       std::string sFilename_elevation_in);

  int read_digital_elevation_model(std::string sFilename_elevation_in);

  int read_hexagon_point_shapefile(std::string sFilename_hexagon_point_shapefile_in);

  int read_hexagon_polygon_shapefile(std::string sFilename_hexagon_polygon_shapefile_in);

  int domain_calculate_hexagon_polygon_center_location();

  int domain_initialize_model();

  int domain_run_model();

  int domain_fill_depression();

  int domain_calculate_flow_direction();

  int domain_calculate_flow_accumulation();

  int domain_define_stream_grid();

  int domain_define_watershed_boundary();

  int domain_define_stream_confluence();

  int domain_define_stream_segment();
  int domain_build_stream_topology();
  int domain_define_stream_order();

  int domain_tag_confluence_upstream(long lID_confluence);

  int domain_define_subbasin();

  //the watershed characteristics for comparison
  int domain_calculate_watershed_characteristics();

  int domain_calculate_watershed_drainage_area();

  int domain_calculate_watershed_total_stream_length();

  int domain_calculate_watershed_longest_stream_length();

  int domain_calculate_watershed_area_to_stream_length_ratio();

  int domain_calculate_watershed_average_slope();
  int domain_calculate_topographic_wetness_index();
  int domain_save_watershed_characteristics();

  //we decided to not calculate the aspect here.
  //other indices?

  //save all the result
  int domain_save_result();

  int domain_save_variable(eVariable eV_in);

  int domain_save_point_vector(eVariable eV_in,
                               std::string sFieldname_in,
                               std::string sFilename_in,
                               std::string sLayer_name_in);

  int domain_save_polyline_vector(eVariable eV_in,
                                  std::string sFieldname_in,
                                  std::string sFilename_in,
                                  std::string sLayername_in);

  int domain_save_polygon_vector(eVariable eV_in,
                                 std::string sFieldname_in,
                                 std::string sFilename_in,
                                 std::string sLayer_name_in);

  int domain_cleanup();

  std::vector<hexagon> domain_get_boundary(std::vector<hexagon> vCell_in);

  int check_digital_elevation_model_depression(std::vector<hexagon> vCell_in);

  std::array<long, 3> find_lowest_cell(std::vector<hexagon> vCell_in);

  int find_all_neighbors();
};
} // namespace hexwatershed
