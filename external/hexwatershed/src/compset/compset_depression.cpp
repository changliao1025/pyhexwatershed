
/**
 * @file depression.h
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief The depression header file
 * @version 0.1
 * @date 2019-08-02
 * @citation Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020).
 * Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 104702.
 * https://www.sciencedirect.com/science/article/pii/S1364815219308278
 * @github page https://github.com/changliao1025/hexwatershed
 * @copyright Copyright (c) 2019
 *
 */
#include "./compset.h"

namespace hexwatershed
{

  /**
   * private functions. check whether there is local depression in the dem or not. in fact, a more rigorous method should pass in dem instead of the hexagon vector
   but because we will not change any member variable here, it should be safe to pass in the vector
   * @param vCell_in
   * @return
   */
  int compset::compset_check_digital_elevation_model_depression(std::vector<hexagon> vCell_in)
  {
    int error_code = 1;
    int iNeighbor;
    int nNeighbor_land;
    int nEdge;
    long lCellID_neighbor;
    long lCellIndex_self, lCelllIndex_search;
    float dElevation_min;
    float dElevation_self;
    std::vector<long> vNeighbor_land;
    std::vector<long>::iterator iIterator;
    std::vector<float> vElevation_neighbor;
    //std::vector<hexagon>::iterator iIterator1;
    //std::vector<hexagon>::iterator iIterator2;

    //#pragma omp parallel for private(lCellIndex_self, iIterator, iNeighbor, vNeighbor_land, \
    dElevation_self, vElevation_neighbor,  \
    lCellID_neighbor, dElevation_min, lCelllIndex_search)
    for (lCellIndex_self = 0; lCellIndex_self < vCell_in.size(); lCellIndex_self++)
      {
        if (error_code == 1)
          {
            nNeighbor_land = vCell_in.at(lCellIndex_self).nNeighbor_land;
            nEdge = vCell_in.at(lCellIndex_self).nEdge;
            if (nNeighbor_land == nEdge)
              {                
                vNeighbor_land = vCell_in.at(lCellIndex_self).vNeighbor_land;
                dElevation_self = vCell_in.at(lCellIndex_self).dElevation_mean;
                vElevation_neighbor.clear();
                for (iNeighbor = 0; iNeighbor < nNeighbor_land; iNeighbor++)
                  {
                    lCellID_neighbor = vNeighbor_land[iNeighbor];
                    //find it
                    for (lCelllIndex_search = 0; lCelllIndex_search < vCell_in.size(); lCelllIndex_search++)
                      {
                        if (vCell_in.at(lCelllIndex_search).lCellID == lCellID_neighbor)
                          {
                            vElevation_neighbor.push_back(vCell_in.at(lCelllIndex_search).dElevation_mean);
                          }
                        else
                          {
                            //continue;
                          }
                      }
                  }
                //if it is the lowest?
                dElevation_min = *(std::min_element(vElevation_neighbor.begin(), vElevation_neighbor.end()));
                if (dElevation_self < dElevation_min)
                  {
                    error_code = 0;
                  }
              }
            else
              {
                //edge do nothing
              }
          }
        else
          {
            //continue;
          }
      }
    return error_code;
  }

  /**
   * retrieve the boundary of the hexagon grid boundary
   * it is not ordered
   * @param vCell_in :the hexagon grid
   * @return
   */
  std::vector<hexagon> compset::compset_obtain_boundary(std::vector<hexagon> vCell_in)
  {
    int error_code = 1;
    int iMesh_type = this->cParameter.iMesh_type;
    std::vector<hexagon>::iterator iIterator1;

    std::vector<hexagon> vCell_out;

    for (iIterator1 = vCell_in.begin(); iIterator1 != vCell_in.end(); iIterator1++)
      {
        if (iMesh_type ==1 || iMesh_type ==4 )
        {
          if ((*iIterator1).nNeighbor_land < (*iIterator1).nVertex) //or vertex
          {
            vCell_out.push_back(*iIterator1);
          }
        }
        else
        {
          if ((*iIterator1).nNeighbor_land < 8) //
          {
            vCell_out.push_back(*iIterator1);
          }
        }
        
      }

    return vCell_out;
  }
  /**
   * find the hexagon with the lowest elevation
   * @param vCell_in :the hexagon grid
   * @return
   */
  std::array<long, 3> compset::compset_find_lowest_cell_in_priority_queue(std::vector<hexagon> vCell_in)
  {
    long lCellIndex_active = 0;
    long lCellID_global = -1;
    long lIndex = 0;
    long lCellIndex_boundary = 0;
    float dElevation_lowest;

    std::vector<hexagon>::iterator iIterator1;
    std::array<long, 3> aIndex_out;
    if (vCell_in.size() < 2)
      {
        //something is wrong
      }
    else
      {
        //set the first as lowest
        dElevation_lowest = vCell_in[0].dElevation_mean;
        lCellID_global = vCell_in[0].lCellID;
        lCellIndex_active = vCell_in[0].lCellIndex;
        lCellIndex_boundary = 0;
        for (iIterator1 = vCell_in.begin(); iIterator1 != vCell_in.end(); iIterator1++)
          {
            if ((*iIterator1).dElevation_mean < dElevation_lowest)
              {
                dElevation_lowest = (*iIterator1).dElevation_mean;
                lCellID_global = (*iIterator1).lCellID;
                lCellIndex_active = (*iIterator1).lCellIndex;
                lCellIndex_boundary = lIndex;
              }
            lIndex = lIndex + 1;
          }
        //be careful
        aIndex_out.at(0) = lCellIndex_boundary;
        aIndex_out.at(1) = lCellIndex_active;
        aIndex_out.at(2) = lCellID_global;
      }
    return aIndex_out;
  }

  /**
   * DEM depression filling
   * @return
   */
  int compset::compset_priority_flood_depression_filling()
  {
    int error_code = 1;
    int iFlag_finished = 0;
    int iFlag_has_stream;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    int iFlag_flowline = cParameter.iFlag_flowline;
    int iFlag_stream_burning_topology= cParameter.iFlag_stream_burning_topology;
    int iFlag_stream_burning_treated_neighbor;
    int nOutlet = cParameter.nOutlet;

    long lCellID_outlet  ;
    long lCellIndex_outlet;

    float dBreach_threshold = cParameter.dBreach_threshold;
    int iFlag_stream_burned;
    int iFlag_stream_burned_center;
    int iFlag_stream_burned_neighbor;
    int iFlag_depression_filling_treated;
    int iFlag_depression_filling_treated_neighbor;
    int iFlag_found;
    int iOption_filling = 1; //2 switch

    long lCellIndex_boundary;
    long lCellIndex_active;
    long lCellIndex_neighbor;
    long iAttempt = 0;
    long lCellID_center;
    long lCellID_neighbor;
    long lCellID_self;
    long lCellID_temp;
    long lCellID_next;
    long lCellIndex_next;

    long lCellID_downstream;
    long lCellID_downstream_neighbor;
    float dElevation_mean_center;
    float dElevation_mean_neighbor;
    float dElevation_history;
    float dDifference_dummy;
    std::array<long, 3> aIndex;

    std::vector<hexagon> vCell_boundary;
    std::vector<flowline>::iterator iIterator1;
    std::vector<hexagon>::iterator iIterator;
    std::vector<hexagon>::iterator iIterator_self;


    if (iFlag_global==0)
      {
        if (iFlag_multiple_outlet == 0)
          {
            std::cout<<"This is a local simulation with only one outlet."<<std::endl;
            vCell_boundary = compset_obtain_boundary(vCell_active);
          
            //set initial as true for boundary
            if (iFlag_flowline == 1)
              {
                //only one outlet is used
                lCellID_outlet = aBasin.at(0).lCellID_outlet;
                iFlag_found = 0;
                for (iIterator = vCell_boundary.begin(); iIterator != vCell_boundary.end(); iIterator++)
                  {
                    //the outlet must be on the boundary at the begining
                    if ((*iIterator).lCellID == lCellID_outlet)
                      {
                        lCellIndex_outlet = (*iIterator).lCellIndex;
                        iFlag_found = 1;
                        std::cout << " You have assigned the correct outlet mesh ID!" << std::endl;
                        break;
                      }
                  }
                if (iFlag_found == 1)
                  {
                    //set the stream as the lowest if possible
                    aIndex = compset_find_lowest_cell_in_priority_queue(vCell_boundary);
                    lCellIndex_boundary = aIndex[0]; //local index in boundary
                    lCellIndex_active = aIndex[1]; //local id
                    dElevation_mean_center = vCell_active.at(lCellIndex_active).dElevation_mean;
                
                    vCell_priority_flood.push_back(vCell_active.at(lCellIndex_outlet));

                    //new simplified approach
                    if (iFlag_stream_burning_topology == 0)
                      {
                        //rasterization based stream burning
                        //this will make sure the outlet is the lowest point in the begining
                        vCell_active.at(lCellIndex_outlet).dElevation_mean = dElevation_mean_center - 20 * dBreach_threshold; //deep reduction
                        //set boundary as treated
                        vCell_active.at(lCellIndex_outlet).iFlag_depression_filling_treated = 1;
                        compset_stream_burning_without_topology( vCell_active.at(lCellIndex_outlet).lCellID );
                      }
                    else
                      {
                        //topology based stream burning
                        vCell_active.at(lCellIndex_outlet).dElevation_mean = dElevation_mean_center-10;
                        //burn stream first, set flag as well
                        vCell_active.at(lCellIndex_outlet).iFlag_depression_filling_treated = 1;

                        compset_stream_burning_with_topology( vCell_active.at(lCellIndex_outlet).lCellID );
                      }
                    //the model requires the initial boundary to be modified already after stream burning
                    for (iIterator = vCell_boundary.begin(); iIterator != vCell_boundary.end(); iIterator++)
                      {
                        lCellIndex_active = (*iIterator).lCellIndex;                        
                        if ( vCell_active.at(lCellIndex_active).iFlag_stream_burning_treated !=1 )
                        {
                          vCell_priority_flood.push_back(vCell_active.at(lCellIndex_active));
                        }
                        vCell_active.at(lCellIndex_active).iFlag_depression_filling_treated = 1;
                      }

                    priority_flood_depression_filling(vCell_boundary);
                  }
                else
                  {
                    std::cout << " You failed to assign the correct outlet mesh ID!" << std::endl;
                    error_code = 0;
                    return error_code;
                  }
              }
            else
              {
                std::cout<<"This is a pure elevation based depression filling."<<std::endl;
                //pure elevation based, single watershed
                iFlag_finished = compset_check_digital_elevation_model_depression(vCell_active);
                if (iFlag_finished == 1)
                  {
                    //there is no depression at all
                  }
                else
                  {
                    //this is the case if no nhd flowline is provided
                    //set boundary as done first

                    for (iIterator = vCell_boundary.begin(); iIterator != vCell_boundary.end(); iIterator++)
                      {
                        lCellIndex_active = (*iIterator).lCellIndex;
                        vCell_active.at(lCellIndex_active).iFlag_depression_filling_treated = 1;
                      }

                    priority_flood_depression_filling(vCell_boundary);

                    //check again
                    iFlag_finished = compset_check_digital_elevation_model_depression(vCell_active);

                    if (iFlag_finished != 1)
                      {
                        //something is wrong
                      }
                  }
              }

            return error_code;
          }
        else
          {
            std::cout<<"This is a regional simulation with multiple outlets"<<std::endl;
            //global case
            if (iFlag_flowline == 1)//with stream burning
              {
                if (iFlag_stream_burning_topology == 0)
                  {
                    for (int i =0; i< nOutlet; i++)
                      {
                        lCellID_outlet = aBasin.at(i).lCellID_outlet;

                        lCellIndex_outlet = compset_find_index_by_cell_id(lCellID_outlet);
                        dElevation_mean_center =  vCell_active.at(lCellIndex_active).dElevation_mean;
                        //rasterization based stream burning
                        //this will make sure the outlet is the lowest point in the begining
                        vCell_active.at(lCellIndex_outlet).dElevation_mean = dElevation_mean_center - 20 * dBreach_threshold; //    deep reduction
                        //set boundary as treated
                        vCell_active.at(lCellIndex_outlet).iFlag_depression_filling_treated = 1;
                        compset_stream_burning_without_topology(vCell_active.at(lCellIndex_outlet).lCellID);
                      }
                  }
                else //topology is used
                  {
                    for (int i =0; i< nOutlet; i++)
                      {
                        //topology based stream burning
                        lCellID_outlet = aBasin.at(i).lCellID_outlet;

                        lCellIndex_outlet = compset_find_index_by_cell_id(lCellID_outlet);
                        dElevation_mean_center =  vCell_active.at(lCellIndex_active).dElevation_mean;

                        //burn stream first, set flag as well
                        vCell_active.at(lCellIndex_outlet).iFlag_depression_filling_treated = 1;
                        compset_stream_burning_with_topology( vCell_active.at(lCellIndex_outlet).lCellID );
                      }
                  }

                //depression filling
                //find each watershed
                for (iIterator_self = vCell_active.begin (); iIterator_self != vCell_active.end (); iIterator_self++)
                  {
                    if ((*iIterator_self).iFlag_depression_filling_treated != 1)
                      {
                        if ((*iIterator_self).nNeighbor_land < (*iIterator_self).nVertex)
                          {

                            vContinent_boundary.clear();
                            find_continent_boundary((*iIterator_self).lCellID);

                            for (iIterator = vContinent_boundary.begin(); iIterator != vContinent_boundary.end(); iIterator++)
                              {
                                lCellIndex_active = (*iIterator).lCellIndex;
                                vCell_active.at(lCellIndex_active).iFlag_depression_filling_treated = 1;
                              }

                            //start flooding
                            if (vContinent_boundary.size () >= 3)//careful
                              {
                                priority_flood_depression_filling (vContinent_boundary);
                              }

                            //reset to the next continent
                            vContinent_boundary.clear();

                          }
                      }
                  }

              }
            else //pure dem based
              {
                //find each watershed
                for (iIterator_self = vCell_active.begin (); iIterator_self != vCell_active.end (); iIterator_self++)
                  {
                    if ((*iIterator_self).iFlag_depression_filling_treated != 1)
                      {
                        if ((*iIterator_self).nNeighbor_land < (*iIterator_self).nVertex)
                          {

                            vContinent_boundary.clear();
                            find_continent_boundary((*iIterator_self).lCellID);

                            for (iIterator = vContinent_boundary.begin(); iIterator != vContinent_boundary.end(); iIterator++)
                              {
                                lCellIndex_active = (*iIterator).lCellIndex;
                                vCell_active.at(lCellIndex_active).iFlag_depression_filling_treated = 1;
                              }

                            //start flooding
                            if (vContinent_boundary.size () >= 3)//careful
                              {
                                priority_flood_depression_filling (vContinent_boundary);
                              }

                            //reset to the next continent
                            vContinent_boundary.clear();

                          }
                      }
                  }

              }

          }

      }
    else
      {
        std::cout<<"This is a global simulation"<<std::endl;
        //global case
        if (iFlag_flowline == 1)//with stream burning
          {
            if (iFlag_stream_burning_topology == 0)
              {
                for (int i =0; i< nOutlet; i++)
                  {
                    lCellID_outlet = aBasin.at(i).lCellID_outlet;

                    lCellIndex_outlet = compset_find_index_by_cell_id(lCellID_outlet);
                    dElevation_mean_center =  vCell_active.at(lCellIndex_active).dElevation_mean;
                    //rasterization based stream burning
                    //this will make sure the outlet is the lowest point in the begining
                    vCell_active.at(lCellIndex_outlet).dElevation_mean = dElevation_mean_center - 20 * dBreach_threshold; //    deep reduction
                    //set boundary as treated
                    vCell_active.at(lCellIndex_outlet).iFlag_depression_filling_treated = 1;
                    compset_stream_burning_without_topology(vCell_active.at(lCellIndex_outlet).lCellID);
                  }
              }
            else //topology is used
              {
                for (int i =0; i< nOutlet; i++)
                  {
                    //topology based stream burning
                    lCellID_outlet = aBasin.at(i).lCellID_outlet;

                    lCellIndex_outlet = compset_find_index_by_cell_id(lCellID_outlet);
                    dElevation_mean_center =  vCell_active.at(lCellIndex_active).dElevation_mean;

                    //burn stream first, set flag as well
                    vCell_active.at(lCellIndex_outlet).iFlag_depression_filling_treated = 1;
                    compset_stream_burning_with_topology(vCell_active.at(lCellIndex_outlet).lCellID);
                  }
              }

            //depression filling
            //find each watershed
            for (iIterator_self = vCell_active.begin (); iIterator_self != vCell_active.end (); iIterator_self++)
              {
                if ((*iIterator_self).iFlag_depression_filling_treated != 1)
                  {
                    if ((*iIterator_self).nNeighbor_land < (*iIterator_self).nVertex)
                      {

                        vContinent_boundary.clear();
                        find_continent_boundary((*iIterator_self).lCellID);

                        for (iIterator = vContinent_boundary.begin(); iIterator != vContinent_boundary.end(); iIterator++)
                          {
                            lCellIndex_active = (*iIterator).lCellIndex;
                            vCell_active.at(lCellIndex_active).iFlag_depression_filling_treated = 1;
                          }

                        //start flooding
                        if (vContinent_boundary.size () >= 3)//careful
                          {
                            priority_flood_depression_filling (vContinent_boundary);
                          }

                        //reset to the next continent
                        vContinent_boundary.clear();

                      }
                  }
              }

          }
        else //pure dem based
          {
            //find each watershed
            for (iIterator_self = vCell_active.begin (); iIterator_self != vCell_active.end (); iIterator_self++)
              {
                if ((*iIterator_self).iFlag_depression_filling_treated != 1)
                  {
                    if ((*iIterator_self).nNeighbor_land < (*iIterator_self).nVertex)
                      {

                        vContinent_boundary.clear();
                        find_continent_boundary((*iIterator_self).lCellID);

                        for (iIterator = vContinent_boundary.begin(); iIterator != vContinent_boundary.end(); iIterator++)
                          {
                            lCellIndex_active = (*iIterator).lCellIndex;
                            vCell_active.at(lCellIndex_active).iFlag_depression_filling_treated = 1;
                          }

                        //start flooding
                        if (vContinent_boundary.size () >= 3)//careful
                          {
                            priority_flood_depression_filling (vContinent_boundary);
                          }

                        //reset to the next continent
                        vContinent_boundary.clear();

                      }
                  }
              }

          }

      }

    return error_code;
  }

/**
 * @brief 
 * 
 * @param lCellID_in 
 * @return int 
 */
  int compset::find_land_ocean_interface_neighbors(long lCellID_in)
  {
    int error_code = 1;
    int iNeighbor;
    int iVertex;
    int iFlag_depression_filling_treated;
    std::vector<long> aNeighbor;
    //std::vector<hexagon>::iterator iIterator_self;
    std::vector<long> vNeighbor_land;
    long lCellIndex_neighbor;
    long lCellIndex = compset_find_index_by_cell_id(lCellID_in);
    long lCellID_neighbor;
    std::vector<long>::iterator iIterator;
    vNeighbor_land = vCell_active.at(lCellIndex).vNeighbor_land;
    for (iIterator = vNeighbor_land.begin (); iIterator != vNeighbor_land.end (); iIterator++)
      {
        lCellID_neighbor = *iIterator;
        lCellIndex_neighbor = compset_find_index_by_cell_id(lCellID_neighbor);
        iNeighbor = vCell_active.at(lCellIndex_neighbor).nNeighbor_land;
        iVertex = vCell_active.at(lCellIndex_neighbor).nVertex;
        iFlag_depression_filling_treated = vCell_active.at(lCellIndex_neighbor).iFlag_depression_filling_treated ;
        if ( iNeighbor <iVertex )
          {
            if(iFlag_depression_filling_treated != 1)
              {
                //aNeighbor.push_back(lCellID_neighbor);
                vCell_active.at(lCellIndex_neighbor).iFlag_depression_filling_treated = 1;

                vContinent_boundary.push_back(vCell_active.at(lCellIndex_neighbor));
                find_land_ocean_interface_neighbors(lCellID_neighbor);
              }
          }

      }

    return error_code;

  }

  int compset::find_continent_boundary(long lCellID_in)
  {
    int error_code=1;
    //std::vector<long> vCellID_boundary;
    std::vector<long> aNeighbor;
    int iFlag_finished = 0 ;
    int iFlag_found_starting_point =0 ;
    long lCellIndex_neighbor;
    long lCellID_current = lCellID_in;
    long lCellID_neighbor;
    std::vector<long>::iterator iIterator;
    std::vector<hexagon>::iterator iIterator1;

    lCellIndex_neighbor = compset_find_index_by_cell_id(lCellID_in);
    vCell_active.at(lCellIndex_neighbor).iFlag_depression_filling_treated = 1;
    vContinent_boundary.push_back(vCell_active.at(lCellIndex_neighbor));



    find_land_ocean_interface_neighbors(lCellID_current);




    return error_code;;

  }



  int compset::priority_flood_depression_filling(std::vector <hexagon> vCell_boundary_in)
  {
    int error_code= 1;
    int iFlag_stream_burning_treated_neighbor;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    int iFlag_elevation_profile = cParameter.iFlag_elevation_profile;
    long lCellID_lowest;
    long lCellIndex_neighbor;
    long lCellID_neighbor;
    long lCellIndex_boundary;
    long lCellIndex_active;
    float dElevation_mean_center;
    float dElevation_mean_neighbor;
    float dElevation_profile0_center;
    float dElevation_profile0_neighbor;
    int iFlag_depression_filling_treated_neighbor;
    std::array<long, 3> aIndex_search;

    while (vCell_boundary_in.size () > 3)
      {
        aIndex_search = compset_find_lowest_cell_in_priority_queue(vCell_boundary_in);
        lCellIndex_boundary = aIndex_search[0]; //local index in boundary
        lCellIndex_active = aIndex_search[1];
        lCellID_lowest = aIndex_search[2];
        dElevation_mean_center = (vCell_active.at (lCellIndex_active)).dElevation_mean;
        dElevation_profile0_center = (vCell_active.at (lCellIndex_active)).dElevation_profile0;
        //remove it from the table
        vCell_boundary_in.erase (vCell_boundary_in.begin () + lCellIndex_boundary);       

        for (int i = 0; i < (vCell_active.at (lCellIndex_active)).nNeighbor_land; i++)
          {
            lCellID_neighbor = (vCell_active.at (lCellIndex_active)).vNeighbor_land[i];
            lCellIndex_neighbor = compset_find_index_by_cell_id(lCellID_neighbor);
            iFlag_depression_filling_treated_neighbor = vCell_active.at(lCellIndex_neighbor).iFlag_depression_filling_treated;
            iFlag_stream_burning_treated_neighbor = vCell_active.at(lCellIndex_neighbor).iFlag_stream_burning_treated;
            dElevation_mean_neighbor = vCell_active[lCellIndex_neighbor].dElevation_mean;
           
            if (iFlag_depression_filling_treated_neighbor != 1)
              {
                if(iFlag_stream_burning_treated_neighbor ==1 )
                  {
                    vCell_active.at(lCellIndex_neighbor).iFlag_depression_filling_treated = 1;
                    vCell_boundary_in.push_back(vCell_active[lCellIndex_neighbor]);
                  }
                else
                  {
                    vCell_priority_flood.push_back( vCell_active.at(lCellIndex_neighbor) );

                    if (dElevation_mean_neighbor <= dElevation_mean_center)
                      {
                        vCell_active[lCellIndex_neighbor].dElevation_mean = dElevation_mean_center + 0.001 + abs(dElevation_mean_neighbor) * 0.0001;                        
                      }

                      //elevation profile case
                      if(iFlag_elevation_profile == 1)
                      {
                        dElevation_profile0_neighbor = vCell_active[lCellIndex_neighbor].dElevation_profile0;
                        if (dElevation_profile0_neighbor <= dElevation_profile0_center)
                          {
                            vCell_active[lCellIndex_neighbor].dElevation_profile0 =
                              dElevation_profile0_center + abs (dElevation_profile0_center) * 0.0001 + 0.0001;
                          }
                      }
                      
                    vCell_active.at(lCellIndex_neighbor).iFlag_depression_filling_treated = 1;
                    vCell_boundary_in.push_back(vCell_active[lCellIndex_neighbor]);
                  }
              }
            else
              {
                (vCell_active[lCellIndex_neighbor]).iFlag_depression_filling_treated =1;

              }
          }
      }
    return error_code;
  }




}
