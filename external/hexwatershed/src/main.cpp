/**
 * @file depression.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief the main entrance
 * @version 0.1
 * @date 2019-08-02
 * @citation Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). 
 * Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 104702.
 * https://www.sciencedirect.com/science/article/pii/S1364815219308278
 * @github page https://github.com/changliao1025/hexwatershed
 * @copyright Copyright (c) 2019
 * 
 */
#include <iostream>
#include <string>
#include "domain/domain.h"

/*! \mainpage An introduction to the HexWatershed Model
 *
 * \section intro_sec Introduction
 *
 * This is the Doxygen page of the HexWatershed model.
 * 
 *
 * \section install_sec Installation
 *
 * \subsection step1 Step 1: Opening the box
 *
 * etc...
 */

/**
 *
 * @param argc
 * @param argv
 * @return
 */
int main(int argc, char *argv[])
{
  int error_code = 1;

  //initial program running status as success,
  //the status variable changes to 0 if any step fails to proceed.
  std::cout << "Start to run HexWatershed model!" << std::endl;
  int program_status = 1;
  std::string sConfiguration_file = "";
  if (argc == 2) //at least 2 arguments are needed
  {
    std::cout << "The following arguments are provided:" << std::endl;
    std::cout << argv[1] << std::endl; //print out all the arguments
    sConfiguration_file = argv[1];
  }
  else
  {
    std::cout << "No arguments are provided!" << std::endl;
    std::cout << "Please input the configuration file: " << std::endl;
  
  }
  //initialize the ecosystem model
  hexwatershed::domain cDomain(sConfiguration_file);
  //since the class initialization does not have a return value, we check it here directly
  if (cDomain.cCompset.cParameter.iFlag_configuration_file == 0) //the configuration file is effective.
  {
    std::cout << "The configuration file does not exit!" << "\n";
    exit(0);
  }
  else
  {
    //initialize the class member
    cDomain.domain_setup();
    error_code = cDomain.domain_read();
    if (error_code != 0)
    {
      error_code = cDomain.domain_initialize();
      if (error_code != 0)
      {
        error_code = cDomain.domain_run();
        if (error_code != 0)
        {
          error_code = cDomain.domain_save();
          if (error_code != 0)
          {
            error_code = cDomain.domain_cleanup();
          }
        }
      }
      std::cout << "Finished!" << "\n";
      program_status = 1;
    }
    else
    {
      program_status = 0;
    }

  }
  return program_status;

}

