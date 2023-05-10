//
// Created by liao313 on 4/8/2021.
//


#pragma once
#include <vector>
#include <string>
using namespace std;

namespace hexwatershed
{

  class parameter {

  public:
    parameter();

    ~parameter();
    int iCase_index;
    int nOutlet;
    int iFlag_configuration_file;
    int iFlag_debug;
    int iFlag_elevation_profile;
    int iMesh_type;
    int iFlag_global;
    int iFlag_multiple_outlet; //multiple outlet in one simulation
    int iFlag_resample_method;
    int iFlag_flowline; //has stream burning or not
    int iFlag_stream_burning_topology;//whethet to use topology for stream burning
    int iFlag_stream_grid_option;

    int iFlag_slope_provided;

    int iFlag_merge_reach;

    

    //parameters
    float dAccumulation_threshold;
    float dBreach_threshold; //the threshold parameter for stream burning breaching algorithm

    float dMissing_value_dem;
    std::string sMesh_type;
    std::string sFilename_configuration;
    std::string sMissing_value_default;

  };
}


