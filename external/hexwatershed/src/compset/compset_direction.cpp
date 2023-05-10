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
#include "compset.h"

namespace hexwatershed
{

  /**
   * calculate the flow direction based on elevation, this step "should" only be run after the depression filling
   * @return
   */
  int compset::compset_calculate_flow_direction()
  {
    int error_code = 1;
    int iFlag_stream_burned;
    int iFlag_has_stream;
    int iMesh_type = cParameter.iMesh_type;

    int iFlag_flowline = cParameter.iFlag_flowline;
    int iFlag_stream_burning_topology = cParameter.iFlag_stream_burning_topology;
  
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    int iFlag_elevation_profile = cParameter.iFlag_elevation_profile;
    long iNeighborIndex;
    long lCellID_lowest;
    long lCellID_highest;
    long lCellIndex_self;
    long lCellID;
    float dElevation_mean;
    float dElevation_profile0;
    float dElevation_diff;
    float dDistance_neighbor;
    float dDistance_downslope;
    float dDistance_initial =0.0;
    float dSlope_initial = 0.0;
    float dSlope_downslope; // should be negative because downslope
    float dSlope_upslope;   // should be positive because upslope
    float dSlope_new;
    float dSlope_elevation_profile0;

    long lCellIndex_neighbor;
    long lCellIndex_neighbor_lowest;
    long lCellIndex_neighbor_highest;
    long lCellID_downstream;

    std::vector<float> vNeighbor_distance;
    std::vector<long> vNeighbor;
    std::vector<long> vNeighbor_land;

    std::vector<long>::iterator iIterator;
    std::vector<long>::iterator iIterator_neighbor;

    if (iFlag_flowline == 1) // use the existing
    {

      if (iFlag_stream_burning_topology == 0)
      {
        // rely on elevation
        for (lCellIndex_self = 0; lCellIndex_self < vCell_active.size(); lCellIndex_self++)
        {
          vNeighbor = (vCell_active.at(lCellIndex_self)).vNeighbor;
          vNeighbor_land = (vCell_active.at(lCellIndex_self)).vNeighbor_land;
          vNeighbor_distance = (vCell_active.at(lCellIndex_self)).vNeighbor_distance;
          lCellID_lowest = -1;
          lCellID_highest = -1;
          dElevation_mean = (vCell_active.at(lCellIndex_self)).dElevation_mean;
          dSlope_downslope = dSlope_initial;
          dSlope_upslope = dSlope_initial;
          dDistance_downslope = dDistance_initial;

          // iterate through all neighbors
          for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor != vNeighbor_land.end(); iIterator_neighbor++)
          {

            lCellIndex_neighbor = compset_find_index_by_cell_id(*iIterator_neighbor);
            dElevation_diff = dElevation_mean - vCell_active.at(lCellIndex_neighbor).dElevation_mean;
            // get distance
            iIterator = std::find(vNeighbor.begin(), vNeighbor.end(), *iIterator_neighbor);
            iNeighborIndex = std::distance(vNeighbor.begin(), iIterator);
            dDistance_neighbor = vNeighbor_distance.at(iNeighborIndex);
            dSlope_new = dElevation_diff / dDistance_neighbor;
            if (dSlope_new > 0.0)
            {
              // this is a downslope
              (vCell_active.at(lCellIndex_self)).vDownslope.push_back(*iIterator_neighbor);
              if (dSlope_new > dSlope_downslope)
              {
                // this maybe a dominant downslope
                dSlope_downslope = dSlope_new;
                dDistance_downslope = dDistance_neighbor;
                lCellID_lowest = *iIterator_neighbor;
              }
            }
            else
            {
              // this should be a upslope
              (vCell_active.at(lCellIndex_self)).vUpslope.push_back(*iIterator_neighbor);
              if (dSlope_new < dSlope_upslope)
              {
                // this maybe a dominant upslope
                dSlope_upslope = dSlope_new;
                lCellID_highest = *iIterator_neighbor;
              }
            }
          }
          // mark the direction as the largest elevation differences
          if (lCellID_lowest != -1)
          {
            (vCell_active.at(lCellIndex_self)).lCellID_downslope_dominant = lCellID_lowest;
            // before define stream, we cannot establish upslope relationship
            // calculate slope
            if (dSlope_downslope < 0.0)
            {
              std::cout << "Slope should be positive!" << std::endl;
            }
            (vCell_active.at(lCellIndex_self)).dSlope_max_downslope = dSlope_downslope;
            (vCell_active.at(lCellIndex_self)).dDistance_to_downslope = dDistance_downslope;
          }
          else
          {
            // outlet
            if (dSlope_upslope > 0.0)
            {
              std::cout << "Upslope should be positive!" << std::endl;
            }
            (vCell_active.at(lCellIndex_self)).dSlope_max_downslope = -1 * dSlope_upslope;
            //just use its own length
            (vCell_active.at(lCellIndex_self)).dDistance_to_downslope = (vCell_active.at(lCellIndex_self)).dLength_edge_mean;
          }
        }
      }
      else
      {
        //#pragma omp parallel for private(lCellIndex_self, vNeighbor_land, lCellID_lowest, dElevation_mean, dSlope_initial, dSlope_new, iIterator_neighbor)
        for (lCellIndex_self = 0; lCellIndex_self < vCell_active.size(); lCellIndex_self++)
        {
          vNeighbor = (vCell_active.at(lCellIndex_self)).vNeighbor;
          vNeighbor_distance = (vCell_active.at(lCellIndex_self)).vNeighbor_distance;
          iFlag_stream_burned = vCell_active[lCellIndex_self].iFlag_stream_burned;
          vNeighbor_land = (vCell_active.at(lCellIndex_self)).vNeighbor_land;
          lCellID_lowest = -1;
          lCellID_highest = -1;

          dElevation_mean = (vCell_active.at(lCellIndex_self)).dElevation_mean;
          dElevation_profile0 = (vCell_active.at(lCellIndex_self)).dElevation_profile0;
          lCellID_downstream = (vCell_active.at(lCellIndex_self)).lCellID_downstream_burned;
          lCellID = (vCell_active.at(lCellIndex_self)).lCellID;

          dSlope_downslope = dSlope_initial;
          dSlope_upslope = dSlope_initial;
          dDistance_downslope = dDistance_initial;

          iFlag_has_stream = 0;
          for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor != vNeighbor_land.end(); iIterator_neighbor++)
          {
            lCellIndex_neighbor = compset_find_index_by_cell_id(*iIterator_neighbor);
            if (vCell_active.at(lCellIndex_neighbor).iFlag_stream_burned == 1)
            {
              iFlag_has_stream = 1;
              break;
            }
          }

          if (iFlag_has_stream == 1)
          {
            // iterate through all neighbors
            for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor != vNeighbor_land.end(); iIterator_neighbor++)
            {
              lCellIndex_neighbor = compset_find_index_by_cell_id(*iIterator_neighbor);
              if (vCell_active.at(lCellIndex_neighbor).iFlag_stream_burned == 1)
              {
                // it has a neighboring stream
                dElevation_diff = dElevation_mean - vCell_active.at(lCellIndex_neighbor).dElevation_mean;
                // get distance
                iIterator = std::find(vNeighbor.begin(), vNeighbor.end(), (*iIterator_neighbor));
                iNeighborIndex = std::distance(vNeighbor.begin(), iIterator);
                dDistance_neighbor = vNeighbor_distance.at(iNeighborIndex);

                dSlope_new = dElevation_diff / dDistance_neighbor;
                if (dSlope_new > 0.0) // positive means stream elevation is lower
                {
                  if (dSlope_new > dSlope_downslope)
                  {
                    dSlope_downslope = dSlope_new;
                    lCellID_lowest = *iIterator_neighbor;
                    lCellIndex_neighbor_lowest = lCellIndex_neighbor;
                    dDistance_downslope = dDistance_neighbor;
                  }
                }
                else
                {
                  // this is an upslope stream grid, but may not the steepest one, so we can skip the lowest
                }
                (vCell_active.at(lCellIndex_self)).vDownslope.push_back(*iIterator_neighbor);
              }
              else
              {
                dElevation_diff = dElevation_mean - vCell_active.at(lCellIndex_neighbor).dElevation_mean;
                // get distance
                iIterator = std::find(vNeighbor.begin(), vNeighbor.end(), (*iIterator_neighbor));
                iNeighborIndex = std::distance(vNeighbor.begin(), iIterator);
                dDistance_neighbor = vNeighbor_distance.at(iNeighborIndex);
                dSlope_new = dElevation_diff / dDistance_neighbor;
                if (dSlope_new > 0.0) // positive, a lower neighbor
                {
                  // this is a downslope but not stream
                  (vCell_active.at(lCellIndex_self)).vDownslope.push_back(*iIterator_neighbor);
                }
                else
                {
                  // this should be a upslope land grid
                  (vCell_active.at(lCellIndex_self)).vUpslope.push_back(*iIterator_neighbor);
                  if (dSlope_new < dSlope_upslope)
                  {
                    // this maybe a dominant downslope
                    dSlope_upslope = dSlope_new;
                    lCellID_highest = *iIterator_neighbor;
                    dDistance_downslope = dDistance_neighbor;
                    lCellIndex_neighbor_highest = lCellIndex_self;
                  }
                }
              }
            }
          }
          else
          {
            // iterate through all neighbors
            for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor != vNeighbor_land.end(); iIterator_neighbor++)
            {
              lCellIndex_neighbor = compset_find_index_by_cell_id(*iIterator_neighbor);
              dElevation_diff = dElevation_mean - vCell_active.at(lCellIndex_neighbor).dElevation_mean;
              // get distance
              iIterator = std::find(vNeighbor.begin(), vNeighbor.end(), (*iIterator_neighbor));
              iNeighborIndex = std::distance(vNeighbor.begin(), iIterator);
              dDistance_neighbor = vNeighbor_distance.at(iNeighborIndex);
              dSlope_new = dElevation_diff / dDistance_neighbor;
              if (dSlope_new > 0.0)
              {
                // this is a downslope
                (vCell_active.at(lCellIndex_self)).vDownslope.push_back(*iIterator_neighbor);
                if (dSlope_new > dSlope_downslope) // downslope
                {
                  dSlope_downslope = dSlope_new;
                  lCellID_lowest = *iIterator_neighbor;
                  dDistance_downslope = dDistance_neighbor;
                  lCellIndex_neighbor_lowest = lCellIndex_neighbor;
                }
              }
              else
              {
                // this should be a upslope
                (vCell_active.at(lCellIndex_self)).vUpslope.push_back(*iIterator_neighbor);
                if (dSlope_new < dSlope_upslope)
                {
                  // this maybe a dominant upslope
                  dSlope_upslope = dSlope_new;
                  lCellID_highest = *iIterator_neighbor;
                  lCellIndex_neighbor_highest = lCellIndex_self;
                }
              }
            }
          }

          if (iFlag_stream_burned == 1)
          {
            if (lCellID_downstream != -1)
            {
              for (iIterator_neighbor = vNeighbor_land.begin();
                   iIterator_neighbor != vNeighbor_land.end();
                   iIterator_neighbor++)
              {

                lCellIndex_neighbor = compset_find_index_by_cell_id(*iIterator_neighbor);
                if (vCell_active.at(lCellIndex_neighbor).lCellID == lCellID_downstream) // thi is the downstream
                {
                  (vCell_active.at(lCellIndex_self)).lCellID_downslope_dominant = *iIterator_neighbor;
                  // only use this stream elevation to calcualte slope
                  dElevation_diff = dElevation_mean - vCell_active.at(lCellIndex_neighbor).dElevation_mean; // positive
                  // get distance
                  iIterator = std::find(vNeighbor.begin(), vNeighbor.end(), (*iIterator_neighbor));
                  iNeighborIndex = std::distance(vNeighbor.begin(), iIterator);
                  dDistance_neighbor = vNeighbor_distance.at(iNeighborIndex);
                  dSlope_new = dElevation_diff / dDistance_neighbor;
                  (vCell_active.at(lCellIndex_self)).dSlope_max_downslope = dSlope_new;
                  (vCell_active.at(lCellIndex_self)).dDistance_to_downslope = dDistance_neighbor;
                  // elevation profile
                  if (iFlag_elevation_profile == 1)
                  {
                    dElevation_diff = dElevation_profile0 - vCell_active.at(lCellIndex_neighbor).dElevation_profile0;
                    dSlope_elevation_profile0 = dElevation_diff / (vCell_active.at(lCellIndex_self)).dLength_stream_burned;
                    if (dSlope_elevation_profile0 <= 0.0001)
                    {
                      dSlope_elevation_profile0 = 0.0001;
                    }
                    (vCell_active.at(lCellIndex_self)).dSlope_elevation_profile0 = dSlope_elevation_profile0;
                  }
                  break;
                }
              }
            }
            else
            {
              // this is possibly outlet, and it has no downstream slope calculated
              for (iIterator_neighbor = vNeighbor_land.begin();
                   iIterator_neighbor != vNeighbor_land.end();
                   iIterator_neighbor++)
              {
                lCellIndex_neighbor = compset_find_index_by_cell_id(*iIterator_neighbor);

                if (vCell_active.at(lCellIndex_neighbor).lCellID_downstream_burned == lCellID) // reverse
                {
                  //=====================================
                  // special case because we flip it
                  //==================================
                  dElevation_diff = dElevation_mean - vCell_active.at(lCellIndex_neighbor).dElevation_mean;
                  // get distance
                  iIterator = std::find(vNeighbor.begin(), vNeighbor.end(), (*iIterator_neighbor));
                  iNeighborIndex = std::distance(vNeighbor.begin(), iIterator);
                  dDistance_neighbor = vNeighbor_distance.at(iNeighborIndex);
                  dSlope_new = dElevation_diff / dDistance_neighbor;
                  if (dSlope_new > 0.0)
                  {
                    std::cout << "Upslope should be negative!" << std::endl;
                  }
                  (vCell_active.at(lCellIndex_self)).dSlope_max_downslope = -1.0 * dSlope_new; // reverse
                  (vCell_active.at(lCellIndex_self)).dDistance_to_downslope = (vCell_active.at(lCellIndex_self)).dLength_edge_mean;

                  if (iFlag_elevation_profile == 1)
                  {
                    dElevation_diff = vCell_active.at(lCellIndex_neighbor).dElevation_profile0 - dElevation_profile0;
                    dSlope_elevation_profile0 = dElevation_diff / (vCell_active.at(lCellIndex_self)).dLength_stream_burned;
                    if (dSlope_elevation_profile0 <= 0.0001)
                    {
                      dSlope_elevation_profile0 = 0.0001;
                    }
                    (vCell_active.at(lCellIndex_self)).dSlope_elevation_profile0 = dSlope_elevation_profile0;
                  }

                  break;
                }
              }
            }
          }
          else
          {
            // normal land grid neighbor, this cell maybe on the edge, if so, we can set it mannually as beach
            if ( iMesh_type == 4) // this only apply to mpas that does not consider the vertex neighbors
            {
              if ((vCell_active.at(lCellIndex_self)).nNeighbor_land == (vCell_active.at(lCellIndex_self)).nVertex)
              {
                // mark the direction as the largest elevation differences
                if (lCellID_lowest != -1)
                {
                  (vCell_active.at(lCellIndex_self)).lCellID_downslope_dominant = lCellID_lowest;
                  // before define stream, we cannot establish upslope relationship
                  // calculate slope
                  if (dSlope_downslope < 0.0)
                  {
                    std::cout << "Downslope should be positive!" << std::endl;
                  }
                  (vCell_active.at(lCellIndex_self)).dSlope_max_downslope = dSlope_downslope;
                  (vCell_active.at(lCellIndex_self)).dDistance_to_downslope = dDistance_downslope;

                  // elevation profile
                  if (iFlag_elevation_profile == 1)
                  {
                    dElevation_diff = dElevation_profile0 - vCell_active.at(lCellIndex_neighbor_lowest).dElevation_profile0;
                    dSlope_elevation_profile0 = dElevation_diff / (vCell_active.at(lCellIndex_self)).dLength_stream_burned;
                    if (dSlope_elevation_profile0 <= 0.0001)
                    {
                      dSlope_elevation_profile0 = 0.0001;
                    }
                    (vCell_active.at(lCellIndex_self)).dSlope_elevation_profile0 = dSlope_elevation_profile0;
                  }
                }
                else
                {
                  // this cell is not on the edge, so it must has one
                  std::cout << "It should have one downslope!" << std::endl;
                }
              }
              else
              { // this is a edge node
                (vCell_active.at(lCellIndex_self)).lCellID_downslope_dominant = -1;
                if (dSlope_upslope > 0.0)
                {
                  std::cout << "Upslope should be negative!" << std::endl;
                }
                (vCell_active.at(lCellIndex_self)).dSlope_max_downslope = -1.0 * dSlope_upslope;
                (vCell_active.at(lCellIndex_self)).dDistance_to_downslope = (vCell_active.at(lCellIndex_self)).dLength_edge_mean;

                if (iFlag_elevation_profile == 1) // beach
                {
                  (vCell_active.at(lCellIndex_self)).dSlope_elevation_profile0 = 0.0001;
                }
              }
            }
            else // for latlon and square mesh type
            {
              //
              // mark the direction as the largest elevation differences
              if (lCellID_lowest != -1)
              {
                (vCell_active.at(lCellIndex_self)).lCellID_downslope_dominant = lCellID_lowest;
                // before define stream, we cannot establish upslope relationship
                // calculate slope
                if (dSlope_downslope < 0.0)
                {
                  std::cout << "Downslope should be positive!" << std::endl;
                }
                (vCell_active.at(lCellIndex_self)).dSlope_max_downslope = dSlope_downslope;
                (vCell_active.at(lCellIndex_self)).dDistance_to_downslope = dDistance_downslope;

                // elevation profile
                if (iFlag_elevation_profile == 1)
                {
                  dElevation_diff = dElevation_profile0 - vCell_active.at(lCellIndex_neighbor_lowest).dElevation_profile0;
                  dSlope_elevation_profile0 = dElevation_diff / (vCell_active.at(lCellIndex_self)).dLength_stream_burned;
                  if (dSlope_elevation_profile0 <= 0.0001)
                  {
                    dSlope_elevation_profile0 = 0.0001;
                  }
                  (vCell_active.at(lCellIndex_self)).dSlope_elevation_profile0 = dSlope_elevation_profile0;
                }
              }
              else
              {
                // this cell may be on the edge, so it must has one
                //std::cout << "It should have one downslope!" << std::endl;
              }
            }
          }
        }
      }
    }
    else
    {
      // pure dem based
      //#pragma omp parallel for private(lCellIndex_self, vNeighbor_land, lCellID_lowest, dElevation_mean, dSlope_initial, dSlope_new, iIterator_neighbor)
      for (lCellIndex_self = 0; lCellIndex_self < vCell_active.size(); lCellIndex_self++)
      {
        vNeighbor = (vCell_active.at(lCellIndex_self)).vNeighbor;
        vNeighbor_distance = (vCell_active.at(lCellIndex_self)).vNeighbor_distance;
        vNeighbor_land = (vCell_active.at(lCellIndex_self)).vNeighbor_land;
        lCellID_lowest = -1;
        lCellID_highest = -1;
        dElevation_mean = (vCell_active.at(lCellIndex_self)).dElevation_mean;
        dSlope_downslope = dSlope_initial;
        dSlope_upslope = dSlope_initial;
        dDistance_downslope = dDistance_initial;
        // iterate through all neighbors
        for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor != vNeighbor_land.end(); iIterator_neighbor++)
        {

          lCellIndex_neighbor = compset_find_index_by_cell_id(*iIterator_neighbor);
          dElevation_diff = dElevation_mean - vCell_active.at(lCellIndex_neighbor).dElevation_mean;
          // get distance
          iIterator = std::find(vNeighbor.begin(), vNeighbor.end(), (*iIterator_neighbor));
          iNeighborIndex = std::distance(vNeighbor.begin(), iIterator);
          dDistance_neighbor = vNeighbor_distance.at(iNeighborIndex);
          dSlope_new = dElevation_diff / dDistance_neighbor;
          if (dSlope_new > 0.0)
          {
            // this is a downslope
            (vCell_active.at(lCellIndex_self)).vDownslope.push_back(*iIterator_neighbor);
            if (dSlope_new > dSlope_downslope)
            {
              // this maybe a dominant downslope
              dSlope_downslope = dSlope_new;
              dDistance_downslope = dDistance_neighbor;
              lCellID_lowest = *iIterator_neighbor;
            }
          }
          else
          {
            // this should be a upslope
            (vCell_active.at(lCellIndex_self)).vUpslope.push_back(*iIterator_neighbor);

            if (dSlope_new < dSlope_upslope)
            {
              // this maybe a dominant downslope
              dSlope_upslope = dSlope_new;
              lCellID_highest = *iIterator_neighbor;
            }
          }
        }
        // mark the direction as the largest elevation differences
        if (lCellID_lowest != -1)
        {
          (vCell_active.at(lCellIndex_self)).lCellID_downslope_dominant = lCellID_lowest;
          
          // before define stream, we cannot establish upslope relationship
          if (dSlope_downslope < 0.0)
          {
            std::cout << "Slope should be positive!" << std::endl;
          }
          (vCell_active.at(lCellIndex_self)).dSlope_max_downslope = dSlope_downslope;
          (vCell_active.at(lCellIndex_self)).dDistance_to_downslope = dDistance_downslope;
        }
        else
        {
          // outlet
          // in this case, we will use the highest upslope as slope calculation
          if (dSlope_upslope > 0.0)
          {
            std::cout << "Upslope should be positive!" << std::endl;
          }
          (vCell_active.at(lCellIndex_self)).dSlope_max_downslope = -1 * dSlope_upslope;
          (vCell_active.at(lCellIndex_self)).dDistance_to_downslope = (vCell_active.at(lCellIndex_self)).dLength_edge_mean;
        }
      }
    }
    return error_code;
  } // namespace hexwatershed

}
