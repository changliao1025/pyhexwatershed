/**
 * @file domain.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief the realization of the domain class
 * @version 0.1
 * @date 2019-08-02
 *
 * @copyright Copyright (c) 2019
 *
 */
#include "domain.h"

namespace hexwatershed
{

  domain::domain(){

  };

  domain::~domain(){};

  /**
   *
   * @param sFilename_configuration_in: user provided model configuration file
   * please refer to the user guide for I/O instruction
   */
  domain::domain(std::string sFilename_configuration_in)
  {

    // check the length of the configuration file
    std::size_t iLength = sFilename_configuration_in.length();
    if (iLength < 5)
      {
        cCompset.cParameter.iFlag_configuration_file = 0;
      }
    else
      {
        std::cout << "The configuration file is:" << sFilename_configuration_in
                  << std::endl;
        // check the existence of the configuration file
        if (1 != file_test(sFilename_configuration_in)) // the file does not even exist
          {
            cCompset.cParameter.iFlag_configuration_file = 0;
          }
        else
          {
            cCompset.cParameter.sFilename_configuration = sFilename_configuration_in;
            cCompset.cParameter.iFlag_configuration_file = 1;
          }
      }

    time_t now = time(0);
    tm *ltm = localtime(&now);




    int iYear = 1900 + ltm->tm_year;
    int iMonth = 1 + ltm->tm_mon;
    int iDay = ltm->tm_mday;
    sDate_default = convert_integer_to_string(iYear, 4) + convert_integer_to_string(iMonth, 2) + convert_integer_to_string(iDay, 2);
    sDate = "20200101";

    std::cout << "Finished set up model" << std::endl;
    std::flush(std::cout);
  }

  int domain::domain_setup()
  {
    int error_code=1;

    cCompset.compset_setup_model();
    return  error_code;
  }

  int domain::domain_initialize ()
  {
    int error_code=1;  
    
    cCompset.compset_initialize_model();
    //the last outlet need to be set

    return  error_code;
  }

  /**
   * run the model
   * @return
   */
  int domain::domain_run()
  {
    int error_code = 1;
    error_code = cCompset.compset_run_model();

    return error_code;
  }

  int domain::domain_save ()
  {
    int error_code=1;
    cCompset.compset_save_model();
    return  error_code;
  }


  /**
   * clean up the model status
   * @return
   */
  int domain::domain_cleanup()
  {
    int error_code = 1;
    cCompset.compset_cleanup_model ();
    std::cout << "Finished clean up memory!" << endl;

    return error_code;
  }

} // namespace hexwatershed
