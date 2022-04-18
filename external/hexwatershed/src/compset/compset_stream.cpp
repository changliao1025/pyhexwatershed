/**
 * @file compset.cpp
 * @author Chang Liao (chang.liao@pnnl.gov)
 * @brief the realization of the compset class
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
   * @brief
   *
   * @param lCellIndex_center
   * @return int
   */
  int compset::compset_stream_burning_without_topology(long lCellID_center_in)
  {
    int error_code = 1;
    int iFlag_stream_burned;
    int iFlag_stream_burned_neighbor;
    int iFlag_stream_burning_treated;
    int iFlag_stream_burning_treated_neighbor;

    int untreated;
    long lCellID_neighbor;
    long lCellID_neighbor2;
    long lCellIndex_neighbor;
    long lCellIndex_neighbor2;
    float dBreach_threshold = cParameter.dBreach_threshold;
    float dElevation_mean_center;
    float dElevation_mean_neighbor;
    std::vector<long>::iterator iIterator_neighbor;
    std::vector<long> vNeighbor_land;

    long lCellIndex_center = compset_find_index_by_cellid(lCellID_center_in);

    vCell_active.at(lCellIndex_center).iFlag_stream_burning_treated = 1;
    vNeighbor_land = vCell_active.at(lCellIndex_center).vNeighbor_land;

    dElevation_mean_center = vCell_active.at(lCellIndex_center).dElevation_mean;

    // stream first
    for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor != vNeighbor_land.end(); iIterator_neighbor++)
    {
      lCellID_neighbor = (*iIterator_neighbor);
      lCellIndex_neighbor = compset_find_index_by_cellid(lCellID_neighbor);
      iFlag_stream_burning_treated_neighbor = vCell_active.at(lCellIndex_neighbor).iFlag_stream_burning_treated;
      iFlag_stream_burned_neighbor = vCell_active.at(lCellIndex_neighbor).iFlag_stream_burned;

      if (iFlag_stream_burned_neighbor == 1)
      {
        if (iFlag_stream_burning_treated_neighbor != 1)
        {
          dElevation_mean_neighbor = vCell_active.at(lCellIndex_neighbor).dElevation_mean;
          if (dElevation_mean_neighbor < dElevation_mean_center)
          {
            vCell_active[lCellIndex_neighbor].dElevation_mean = dElevation_mean_center + 0.1 + abs(dElevation_mean_center) * 0.001;
          }
          else
          {
            if ((dElevation_mean_neighbor - dElevation_mean_center) > dBreach_threshold)
            {
              vCell_active[lCellIndex_neighbor].dElevation_mean = dElevation_mean_center + dBreach_threshold;
            }
          }

          vCell_active.at(lCellIndex_neighbor).iFlag_stream_burning_treated = 1;
        }
      }
    }

    // go to the next iteration
    for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor != vNeighbor_land.end(); iIterator_neighbor++)
    {
      lCellID_neighbor = (*iIterator_neighbor);
      lCellIndex_neighbor = compset_find_index_by_cellid(lCellID_neighbor);
      iFlag_stream_burned_neighbor = vCell_active.at(lCellIndex_neighbor).iFlag_stream_burned;
      if (iFlag_stream_burned_neighbor == 1)
      {
        // recursive
        untreated = 0;
        for (int j = 0; j < vCell_active.at(lCellIndex_neighbor).nNeighbor_land; j++)
        {
          lCellID_neighbor2 = vCell_active.at(lCellIndex_neighbor).vNeighbor_land[j];
          lCellIndex_neighbor2 = compset_find_index_by_cellid(lCellID_neighbor2);

          if (vCell_active.at(lCellIndex_neighbor2).iFlag_stream_burned == 1)
          {
            if (vCell_active.at(lCellIndex_neighbor2).iFlag_stream_burning_treated != 1)
            {
              untreated = untreated + 1;
            }
          }
        }
        if (untreated > 0)
        {
          compset_stream_burning_without_topology(lCellIndex_neighbor);
        }
      }
    }
    // land second
    // for (int i = 0; i < vCell_active.at (lCellIndex_center).nNeighbor_land; i++)
    for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor != vNeighbor_land.end(); iIterator_neighbor++)
    {
      lCellID_neighbor = (*iIterator_neighbor);
      lCellIndex_neighbor = compset_find_index_by_cellid(lCellID_neighbor);
      iFlag_stream_burned_neighbor = vCell_active[lCellIndex_neighbor].iFlag_stream_burned;
      iFlag_stream_burning_treated_neighbor = vCell_active[lCellIndex_neighbor].iFlag_stream_burning_treated;
      if (iFlag_stream_burned_neighbor != 1)
      {
        if (iFlag_stream_burning_treated_neighbor != 1)
        {
          dElevation_mean_neighbor = vCell_active[lCellIndex_neighbor].dElevation_mean;
          if (dElevation_mean_neighbor < dElevation_mean_center)
          {
            vCell_active[lCellIndex_neighbor].dElevation_mean = dElevation_mean_center + abs(dElevation_mean_center) * 0.01 + 0.01;
            // we may increase the elevation again in the depression filling step
            vCell_active[lCellIndex_neighbor].iFlag_stream_burning_treated = 1;
          }
          else
          {
          }
        }
      }
    }

    return error_code;
  }

  /**
   * @brief
   *
   * @param lCellIndex_center
   * @return int
   */
  int compset::compset_stream_burning_with_topology(long lCellID_center_in)
  {
    int error_code = 1;
    int iFlag_elevation_profile = cParameter.iFlag_elevation_profile;
    int iOption_filling = 1;
    int iFlag_finished;

    int iFlag_stream_burned;
    int iFlag_stream_burned_neighbor;

    int iFlag_stream_burning_treated;
    int iFlag_stream_burning_treated_neighbor;

    int iStream_order_center;
    int iStream_order_neighbor;
    long lIndex_outlet;
    long lIndex_lowest;
    long lCellIndex_active;
    long lCellIndex_neighbor;
    long lIndex_current;
    long lIndex_center_next;
    long lCellID_current;
    long lCellID_downstream_burned;

    long lCellID_neighbor;
    float dBreach_threshold = cParameter.dBreach_threshold;
    float dElevation_mean_center;
    float dElevation_mean_neighbor;
    float dDifference_dummy;
    float dElevation_profile0_center;
    float dElevation_profile0_neighbor;
    std::vector<long> vNeighbor_land;

    std::vector<long>::iterator iIterator_neighbor;

    long lCellIndex_center = compset_find_index_by_cellid(lCellID_center_in);

    vCell_active.at(lCellIndex_center).iFlag_stream_burning_treated = 1;
    vNeighbor_land = vCell_active.at(lCellIndex_center).vNeighbor_land;
    dElevation_mean_center = vCell_active.at(lCellIndex_center).dElevation_mean;
    dElevation_profile0_center = vCell_active.at(lCellIndex_center).dElevation_profile0;

    // stream elevation
    iStream_order_center = vCell_active.at(lCellIndex_center).iStream_order_burned;
    lCellID_current = vCell_active.at(lCellIndex_center).lCellID;

    // stream first

    for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor < vNeighbor_land.end(); iIterator_neighbor++)
    {
      lCellIndex_neighbor = compset_find_index_by_cellid(*iIterator_neighbor);
      lCellID_downstream_burned = vCell_active.at(lCellIndex_neighbor).lCellID_downstream_burned;
      if (lCellID_downstream_burned == lCellID_current)
      {
        iStream_order_neighbor = vCell_active.at(lCellIndex_neighbor).iStream_order_burned;
        dElevation_mean_neighbor = vCell_active.at(lCellIndex_neighbor).dElevation_mean;
        vCell_active.at(lCellIndex_neighbor).dElevation_downstream = dElevation_mean_center; // need update after modification
        dDifference_dummy = dElevation_mean_neighbor - dElevation_mean_center;
        if (dDifference_dummy >= 0)
        {
          
        }
        else
        {
          // this is a depression, but should we fill or breaching depends on parameter
          if (abs(dDifference_dummy) < dBreach_threshold)
          {
            // if it is slight lower, we will increase  it
            if (iStream_order_neighbor == iStream_order_center)
            {
              vCell_active.at(lCellIndex_neighbor).dElevation_mean = dElevation_mean_center + abs(dElevation_mean_center) * 0.001 + 0.1;
            }
            else
            {
              vCell_active.at(lCellIndex_neighbor).dElevation_mean = dElevation_mean_center + abs(dElevation_mean_center) * 0.001 + 0.2;
            }
          }
          else
          {
            // breaching needed//we will use breach algorithm
            compset_breaching_stream_elevation(*iIterator_neighbor);
          }
        }

        // for elevation enabled case
        if (iFlag_elevation_profile == 1)
        {
          dElevation_profile0_neighbor = vCell_active.at(lCellIndex_neighbor).dElevation_profile0;
          if (dElevation_profile0_neighbor < dElevation_profile0_center)
          {
            vCell_active.at(lCellIndex_neighbor).dElevation_profile0 =
                dElevation_profile0_center + abs(dElevation_profile0_center) * 0.001 + 1.0;
          }
        }

        // update for next step
        vCell_active.at(lCellIndex_neighbor).iFlag_stream_burning_treated = 1; // this should be enough
        // burn recusively
        lIndex_center_next = lCellIndex_neighbor;

        //std::cout << vCell_active.at(lCellIndex_neighbor).lCellID << ": " << vCell_active.at(lCellIndex_neighbor).dElevation_mean << std::endl;
        // go to the new grid
        if (vCell_active.at(lIndex_center_next).iFlag_headwater_burned != 1)
        {
          compset_stream_burning_with_topology(vCell_active.at(lCellIndex_neighbor).lCellID);
        }
      }
    }

    // land second
    for (iIterator_neighbor = vNeighbor_land.begin(); iIterator_neighbor != vNeighbor_land.end(); iIterator_neighbor++)
    {
      lCellID_neighbor = (*iIterator_neighbor);
      lCellIndex_neighbor = compset_find_index_by_cellid(lCellID_neighbor);

      iFlag_stream_burned_neighbor = vCell_active[lCellIndex_neighbor].iFlag_stream_burned;
      iFlag_stream_burning_treated_neighbor = vCell_active[lCellIndex_neighbor].iFlag_stream_burning_treated;

      if (iFlag_stream_burned_neighbor != 1)
      {
        if (iFlag_stream_burning_treated_neighbor != 1)
        {
          dElevation_mean_neighbor = vCell_active[lCellIndex_neighbor].dElevation_mean;
          if (dElevation_mean_neighbor < dElevation_mean_center)
          {
            vCell_active.at(lCellIndex_neighbor).dElevation_mean =
                dElevation_mean_center + abs(dElevation_mean_center) * 0.001 + 1.0;
            // we may increase the elevation agin in the depression filling step
            vCell_active.at(lCellIndex_neighbor).iFlag_stream_burning_treated = 1;
          }

          // if elevation profile is turned on
          if (iFlag_elevation_profile == 1)
          {
            dElevation_profile0_neighbor = vCell_active[lCellIndex_neighbor].dElevation_profile0;
            if (dElevation_profile0_neighbor < dElevation_profile0_center)
            {
              vCell_active.at(lCellIndex_neighbor).dElevation_profile0 =
                  dElevation_profile0_center + abs(dElevation_profile0_center) * 0.001 + 1.0;
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
   * @param lCellID_active
   * @return int
   */
  int compset::compset_breaching_stream_elevation(long lCellID_active_in)
  {
    int error_code = 1;
    // int iStream_order_neighbor;
    // int iStream_order_center;
    long lCellID;
    long lCellIndex_active;
    long lCellID2, lCellID3;
    long lCellIndex2, lCellIndex3;
    float dElevation_upstream;
    float dElevation_downstream;

    long lCellID_downstream;
    long lCellID_downstream2;
    long lCellID_next;

    int iFlag_finished = 0;
    int iFlag_found;
    int iFlag_found1;
    float dDifference_dummy;
    float dElevation_before;
    float dElevation_after;
    float dElevation_dummy;
    // std::vector<hexagon>::iterator iIterator2;
    // std::vector<hexagon>::iterator iIterator3;
    lCellIndex_active = compset_find_index_by_cellid(lCellID_active_in);
    while (iFlag_finished != 1)
    {
      lCellID = vCell_active.at(lCellIndex_active).lCellID;
      lCellID_downstream = vCell_active.at(lCellIndex_active).lCellID_downstream_burned;
      dElevation_upstream = vCell_active.at(lCellIndex_active).dElevation_mean;
      // iStream_order_neighbor = vCell_active.at(lCellIndex_active).iStream_order_burned;
      if (lCellID_downstream != -1)
      {
        iFlag_found = 0;
        // for (iIterator2 = vCell_active.begin (); iIterator2 != vCell_active.end (); iIterator2++)
        for (long lIndex2 = 0; lIndex2 < vCell_active.size(); lIndex2++)
        {
          lCellIndex2 = vCell_active.at(lIndex2).lCellIndex;
          lCellID2 = vCell_active.at(lCellIndex2).lCellID;
          if (lCellID2 == lCellID_downstream)
          {
            iFlag_found = 1;
            dElevation_downstream = vCell_active.at(lCellIndex2).dElevation_mean;
            // dElevation_before = dElevation_downstream;
            //  iStream_order_center = (*iIterator2).iStream_order_burned;
            dDifference_dummy = dElevation_upstream - dElevation_downstream;
            if (dDifference_dummy < 0)
            {
              vCell_active.at(lCellIndex2).dElevation_mean = dElevation_upstream;
              vCell_active.at(lCellIndex_active).dElevation_mean = dElevation_downstream;
              //std::cout << "Breached: CellID " << lCellID_active_in << "->" << lCellID_downstream
              //          << ", before: "
              //          << "upstream: " << dElevation_upstream << "downstream: " << dElevation_downstream
              //          << ", After: "
              //          << "upstream: " << vCell_active.at(lCellIndex_active).dElevation_mean << "downstream: " << vCell_active.at(lCellIndex2).dElevation_mean << std::endl;
              // update
              vCell_active.at(lCellIndex_active).dElevation_downstream = dElevation_upstream;
              // find out the next downstream elevation
              lCellID_downstream2 = vCell_active.at(lCellIndex2).lCellID_downstream_burned;
              if (lCellID_downstream2 != -1)
              {
                iFlag_found1 = 0;
                // for (iIterator3 = vCell_active.begin (); iIterator3 != vCell_active.end (); iIterator3++)
                for (long lIndex3 = 0; lIndex3 < vCell_active.size(); lIndex3++)
                {
                  lCellIndex3 = vCell_active.at(lIndex3).lCellIndex;
                  lCellID3 = vCell_active.at(lCellIndex3).lCellID;
                  if (lCellID3 == lCellID_downstream2)
                  {
                    iFlag_found1 = 1;
                    dDifference_dummy = vCell_active.at(lCellIndex2).dElevation_mean - vCell_active.at(lCellIndex3).dElevation_mean;
                    if (dDifference_dummy < 0.0) // another depression
                    {
                      lCellID_next = lCellID_downstream;
                      compset_breaching_stream_elevation(lCellID_next);
                      //}
                    }
                    iFlag_finished = 1;
                    break;
                  }
                }
              }
              else
              {
                iFlag_finished = 1;
                break;
              }
            }
            else
            {
              // stop
              iFlag_finished = 1;
            }
          }
        }
      }
      else
      {
        iFlag_finished = 1;
        break;
      }
    }

    return error_code;
  }

}
