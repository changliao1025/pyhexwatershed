
/**
 * @file flowline.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief
 * @version 0.1
 * @date 2019-06-11Created by Chang Liao on 4/26/18.
 *
 * @copyright Copyright (c) 2019
 *
 */

#include "./compset.h"

namespace hexwatershed
{

  compset::compset()
  {


  }

  compset::~compset()
  {
  }

  int compset::compset_read_model()
  {
    int error_code =1;
    return error_code;
  }
  int compset::compset_setup_model()
  {
    int error_code =1;
    return error_code;
  }

  int compset::compset_run_model()

  {
    int error_code =1;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    int iFlag_debug =cParameter.iFlag_debug;
    std::string sFilename;
    error_code = compset_priority_flood_depression_filling();
    if (error_code != 1)
    {
      return error_code;
    }
    sLog = "Finished depression filling";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;
    compset_calculate_flow_direction();
    sLog = "Finished flow direction";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::flush(std::cout);
    std::cout << sLog << std::endl;

    compset_calculate_flow_accumulation();
    sLog = "Finished flow accumulation";
    ofs_log << sLog << std::endl;
    ofs_log.flush();
    std::cout << sLog << std::endl;

    if (iFlag_global !=1)
      {
        if (iFlag_multiple_outlet != 1)
          {
            compset_define_stream_grid();
            sLog = "Finished defining stream grid";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;

            iFlag_debug = 0;
            compset_define_watershed_boundary();
            sLog = "Finished defining watershed boundary";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;

            //start from here, we can actually run all the algorithm using the watershed object
            compset_define_stream_confluence();
            sLog = "Finished defining confluence";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;

            compset_define_stream_segment();
            sLog = "Finished defining stream segment";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;
            
            compset_build_stream_topology();
            sLog = "Finished defining stream topology";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;

            compset_define_stream_order();     
            sLog = "Finished defining stream order";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;

            compset_define_subbasin();
            sLog = "Finished defining subbasin";
            ofs_log << sLog << std::endl;
            ofs_log.flush();            
            std::cout << sLog << std::endl;

            compset_calculate_watershed_characteristics();
            sLog = "Finished watershed characteristics";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;
            std::flush(std::cout);

            //now all the watersheds are processed, we can transfer back to main object
            compset_transfer_watershed_to_domain();            
            compset_update_cell_elevation();
            compset_update_vertex_elevation();
          }
        else
          {
            //multiple outlet case, do we need these information?
            compset_define_stream_grid();
            sLog = "Finished defining stream grid";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;
            iFlag_debug = 0;
            compset_define_watershed_boundary();
            sLog = "Finished defining watershed boundary";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;
            //start from here, we can actually run all the algorithm using the watershed object
            compset_define_stream_confluence();
            sLog = "Finished defining confluence";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;
            compset_define_stream_segment();
            sLog = "Finished defining stream segment";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;            
            compset_build_stream_topology();
            sLog = "Finished defining stream topology";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;
            compset_define_stream_order();     
            sLog = "Finished defining stream order";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;
            compset_define_subbasin();
            sLog = "Finished defining subbasin";
            ofs_log << sLog << std::endl;
            ofs_log.flush();            
            std::cout << sLog << std::endl;
            compset_calculate_watershed_characteristics();
            sLog = "Finished watershed characteristics";
            ofs_log << sLog << std::endl;
            ofs_log.flush();
            std::cout << sLog << std::endl;
            std::flush(std::cout);
            //now all the watersheds are processed, we can transfer back to main object
            compset_transfer_watershed_to_domain();            
            compset_update_cell_elevation();
            compset_update_vertex_elevation();
          }
      }
    else
      {
        //global simulation
      }

    std::flush(std::cout);


    return error_code;
  }

  int compset::compset_cleanup_model ()
  {
    int error_code =1;
    return error_code;
  }

} // namespace hexwatershed
