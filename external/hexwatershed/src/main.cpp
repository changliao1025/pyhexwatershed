/**
 * HexWatershed, a hydrologic routing model based on the hexagon mesh framework.
 * Copyright (C) <2002> <Chang Liao>
 * Developer can be contacted by <chang.liao@pnnl.gov>
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 * Created by Chang Liao on 4/6/18.
 */
#include <iostream>
#include <string>
#include "domain.h"

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
  std::cout << "Start to run ecosystem model!" << std::endl;
  int program_status = 1;
  std::string sConfiguration_file = "";
  //sConfiguration_file = "./tinpan.meta";
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
  if (cDomain.iFlag_configuration_file == 0) //the configuration file is effective.
  {
    std::cout << "The configuration file does not exit!" << "\n";
    exit(0);
  }
  else
  {
    //initialize the class member
    cDomain.domain_setup_model();
    error_code = cDomain.domain_read_data();
    if (error_code != 0)
    {
      error_code = cDomain.domain_initialize_model();
      if (error_code != 0)
      {
        error_code = cDomain.domain_run_model();
        if (error_code != 0)
        {
          error_code = cDomain.domain_save_result();
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

