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
#include "./compset.h"

namespace hexwatershed
{


  /**
   * calculate the flow accumulation based on flow direction
   * @return
   */
  int compset::compset_calculate_flow_accumulation()
  {
    int error_code = 1;
    int iFlag_has_upslope = 0;
    int iFlag_all_upslope_done; //assume all are done
    long lFlag_total = 0;
    long lCelllIndex_neighbor;
    long lCellID_downslope_neighbor;
    long lCellID_neighbor;

    std::vector<hexagon>::iterator iIterator_self;
    //std::vector<long>::iterator iIterator_neighbor;
    std::vector<int> vFlag(vCell_active.size());
    std::vector<int> vFinished(vCell_active.size());
    std::fill(vFlag.begin(), vFlag.end(), 0);
    std::fill(vFinished.begin(), vFinished.end(), 0);

    //the initial run

    lFlag_total = std::accumulate(vFlag.begin(), vFlag.end(), 0);

    while (lFlag_total != vCell_active.size())
      {
        for (iIterator_self = vCell_active.begin(); iIterator_self != vCell_active.end(); iIterator_self++)
          {

            if (vFlag.at((*iIterator_self).lCellIndex) == 1)
              {
                //this hexagon is finished
                continue;
              }
            else
              {
                //check whether one or more of the neighbors flow to itself
                iFlag_has_upslope = 0;
                iFlag_all_upslope_done = 1;
                for (int i = 0; i < (*iIterator_self).nNeighbor_land; i++)
                  {
                    lCellID_neighbor = (*iIterator_self).vNeighbor_land.at(i);

                    lCelllIndex_neighbor = compset_find_index_by_cellid(lCellID_neighbor);

                    lCellID_downslope_neighbor = (vCell_active.at(lCelllIndex_neighbor)).lCellID_downslope_dominant;

                    if (lCellID_downslope_neighbor == (*iIterator_self).lCellID)
                      {
                        //there is one upslope neighbor found
                        iFlag_has_upslope = 1;
                        if (vFlag.at(lCelllIndex_neighbor) == 1)
                          {
                            //std::cout << "==" << lCelllIndex_neighbor << std::endl;
                          }
                        else
                          {
                            iFlag_all_upslope_done = 0;
                          }
                      }
                    else
                      {
                      }
                  }
               
                //there are the ones have no upslope at all
             

                if (iFlag_has_upslope == 0)
                  {
                    vFlag.at((*iIterator_self).lCellIndex) = 1;
                  }
                else
                  {
                    //these ones have upslope,
                    if (iFlag_all_upslope_done == 1)
                      {
                        //and they are finished scanning
                        for (int i = 0; i < (*iIterator_self).nNeighbor_land; i++)
                          {
                            lCellID_neighbor = (*iIterator_self).vNeighbor_land.at(i);
                            lCelllIndex_neighbor = compset_find_index_by_cellid(lCellID_neighbor);
                            lCellID_downslope_neighbor = (vCell_active.at(lCelllIndex_neighbor)).lCellID_downslope_dominant;

                            if (lCellID_downslope_neighbor == (*iIterator_self).lCellID)
                              {
                                //std::cout << "===" << lCelllIndex_neighbor << std::endl;
                                //std::cout << "====" << lCellID_downslope_neighbor << std::endl;
                                //this one accepts upslope and the upslope is done
                                (*iIterator_self).dAccumulation =
                                  (*iIterator_self).dAccumulation + vCell_active.at(lCelllIndex_neighbor).dAccumulation;
                              }
                            else
                              {
                                //this neighbor does not flow here, sorry
                              }
                          }
                        vFlag.at((*iIterator_self).lCellIndex) = 1;
                      }
                    else
                      {
                        //we have wait temporally
                      }
                  }
              }
          }
        lFlag_total = std::accumulate(vFlag.begin(), vFlag.end(), 0);
      }
    return error_code;
  }




  /**
   * define the stream network using flow accumulation value
   * @return
   */
  int compset::compset_define_stream_grid()
  {
    int error_code = 1;
    long lCellIndex_self;

    //in watershed hydrology, a threshold is usually used to define the network
    //here we use similar method
    float  dAccumulation_threshold;
    long lCellID_outlet ;

    long lCellIndex_outlet ;
    std::vector<hexagon>::iterator iIterator_self;

    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    if (iFlag_global != 1)
      {

        //use outlet id as largest
        lCellID_outlet =  aBasin.at(0).lCellID_outlet;  
        lCellIndex_outlet = compset_find_index_by_cellid(lCellID_outlet);
        dAccumulation_threshold = 0.05 * vCell_active.at(lCellIndex_outlet).dAccumulation;

        //openmp may  not work for std container in earlier C++ 
//#pragma omp parallel for private(lCellIndex_self)
        for (lCellIndex_self = 0; lCellIndex_self < vCell_active.size(); lCellIndex_self++)
          {
            if ((vCell_active.at(lCellIndex_self)).dAccumulation >= dAccumulation_threshold)
              {
                (vCell_active.at(lCellIndex_self)).iFlag_stream = 1;  
                (vCell_active.at(lCellIndex_self)).dLength_stream_conceptual = (vCell_active.at(lCellIndex_self)).dResolution_effective;
              }
            else
              {
                (vCell_active.at(lCellIndex_self)).iFlag_stream = 0;
                //we still need its length for MOSART model.    
                (vCell_active.at(lCellIndex_self)).dLength_stream_conceptual =  (vCell_active.at(lCellIndex_self)).dResolution_effective;
              }
          }
      }
    else
      {
        //global scale simulation
      }


    return error_code;
  }




  /**
   * define the watershed boundary using outlet
   * @return
   */
  int compset::compset_define_watershed_boundary()
  {
    int error_code = 1;
    int iFound_outlet;
    long lCellIndex_self;
    long lCellIndex_current;
    long lCellIndex_downslope;
    long lCellIndex_outlet;
    long lCellID_downslope;
    long lCellID_outlet;
    std::vector<float> vAccumulation;
    std::vector<float>::iterator iterator_float;
    std::vector<hexagon>::iterator iIterator_self;

    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    if (iFlag_global != 1)
      {
        //find the max accumulation outlet

        for (iIterator_self = vCell_active.begin(); iIterator_self != vCell_active.end(); iIterator_self++)
          {
            vAccumulation.push_back((*iIterator_self).dAccumulation);
          }
        iterator_float = max_element(std::begin(vAccumulation), std::end(vAccumulation)); // c++11
        lCellIndex_outlet = std::distance(vAccumulation.begin(), iterator_float);
        vAccumulation.clear();


        lCellID_outlet = vCell_active.at(lCellIndex_outlet).lCellID;
        cWatershed.lCellID_outlet = lCellID_outlet;
        //we may check the mesh id as well

        vCell_active.at(lCellIndex_outlet).iFlag_outlet = 1;

        //#pragma omp parallel for private(lCellIndex_self, iFound_outlet, lIndex_downslope, lCellIndex_current)
        //can also use
        for (lCellIndex_self = 0; lCellIndex_self < vCell_active.size(); lCellIndex_self++)
          {            
            iFound_outlet = 0;
            lCellIndex_current = lCellIndex_self;
            while (iFound_outlet != 1)
              {
                lCellID_downslope = (vCell_active.at(lCellIndex_current)).lCellID_downslope_dominant;
                if (lCellID_outlet == lCellID_downslope)
                  {
                    iFound_outlet = 1;
                    (vCell_active.at(lCellIndex_self)).iFlag_watershed = 1;
                    //add this cell to the watershed
                    cWatershed.vCell.push_back(vCell_active.at(lCellIndex_self));
                  }
                else
                  {
                    lCellIndex_current =  compset_find_index_by_cellid(lCellID_downslope);
                    if (lCellIndex_current >= 0)
                      {
                        iFound_outlet=0;
                      }
                    else
                      {
                        //this one is going out, but it is not the one belong in this watershed
                        iFound_outlet = 1;
                        (vCell_active.at(lCellIndex_self)).iFlag_watershed = 0;
                      }
                  }
              }
          }
        //add the outout as well, this is important when there are two upstream at the outlet
        (vCell_active.at(lCellIndex_outlet)).iFlag_watershed = 1;
        cWatershed.vCell.push_back(vCell_active.at(lCellIndex_outlet));
      }
    else
      {

      }

    return error_code;
  }


  /**
   * define the stream confluence point
   * because we need to topology info, the vCell_active will be used
   * @return
   */
  int compset::compset_define_stream_confluence()
  {
    int error_code = 1;
    int iCount = 0;
    long lCellID_downstream;
    long lCellIndex_downstream;
    std::vector<hexagon>::iterator iIterator_self;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    if (iFlag_global != 1)
      {

        for (iIterator_self = vCell_active.begin(); iIterator_self != vCell_active.end(); iIterator_self++)
          {
            //we only consider cells within the watershed
            if ((*iIterator_self).iFlag_stream == 1 && (*iIterator_self).iFlag_watershed == 1)
              {
                lCellID_downstream =  (*iIterator_self).lCellID_downslope_dominant;
                lCellIndex_downstream = compset_find_index_by_cellid(lCellID_downstream);
                if (lCellIndex_downstream != -1)
                  {
                    (vCell_active.at(lCellIndex_downstream)).vUpstream.push_back((*iIterator_self).lCellID); //use id instead of index
                  }
                else
                  {
                    //this might be the outlet
                    //std::cout << (*iIterator_self).lCellIndex << ", outlet is: " << lCellIndex_downstream << std::endl;
                  }
              }
          }
        //sum up the size the upstream
        for (iIterator_self = vCell_active.begin(); iIterator_self != vCell_active.end(); iIterator_self++)
          {
            (*iIterator_self).nUpstream = ((*iIterator_self).vUpstream).size();
          }
        //calculate total segment
        vConfluence.clear();
        for (iIterator_self = vCell_active.begin(); iIterator_self != vCell_active.end(); iIterator_self++)
          {
            if ((*iIterator_self).nUpstream > 1 && (*iIterator_self).iFlag_watershed == 1 && (*iIterator_self).iFlag_stream == 1)
              {
                iCount = iCount + 1;
                (*iIterator_self).iFlag_confluence = 1;

                vConfluence.push_back((*iIterator_self));
              }
          }
        nConfluence = iCount;
        nSegment = 1;
        for (iIterator_self = vConfluence.begin(); iIterator_self != vConfluence.end(); iIterator_self++)
          {
            nSegment = nSegment + (*iIterator_self).vUpstream.size();
          }

        //sort cannot be used directly here
        cWatershed.nSegment = nSegment;
      }
    else
      {
        
      }

    return error_code;
  }



  /**
   * define the stream segment, must use vCell_active
   * @return
   */
  int compset::compset_define_stream_segment()
  {
    int error_code = 1;
    long lCellIndex_outlet ; //this is a local variable for each subbasin

    int iFlag_confluence ;
    int iUpstream;
    long lCellIndex_current;
    long lCellID_upstream;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    if (iFlag_global != 1)
      {

        lCellIndex_outlet =  compset_find_index_by_cellid(cWatershed.lCellID_outlet);
        iFlag_confluence = vCell_active.at(lCellIndex_outlet).iFlag_confluence;
        lCellIndex_current = vCell_active.at(lCellIndex_outlet).lCellIndex;
        segment cSegment;
        std::vector<hexagon> vReach_segment;
        vCell_active.at(lCellIndex_outlet).iFlag_last_reach = 1;
        iSegment_current = nSegment;
        vCell_active.at(lCellIndex_outlet).iSegment = iSegment_current;

        vReach_segment.push_back(vCell_active.at(lCellIndex_outlet));
        if (iFlag_confluence == 1) //the outlet is actually a confluence
          {

            cSegment.vReach_segment = vReach_segment;
            cSegment.nReach = 1;
            cSegment.cReach_start = vReach_segment.front();
            cSegment.cReach_end = vReach_segment.back();
            cSegment.iSegment = nSegment;
            cSegment.nSegment_upstream = cSegment.cReach_start.nUpstream;
            cSegment.iFlag_has_upstream = 1;
            cSegment.iFlag_has_downstream = 0;
            cWatershed.vSegment.push_back(cSegment);
          }
        else
          {
            while (iFlag_confluence != 1)
              {
                iUpstream = vCell_active.at(lCellIndex_current).nUpstream;
                if (iUpstream == 1) //
                  {
                    lCellID_upstream= (vCell_active.at(lCellIndex_current)).vUpstream[0];
                    lCellIndex_current = compset_find_index_by_cellid(lCellID_upstream);
                    vCell_active.at(lCellIndex_current).iSegment = iSegment_current;
                    vReach_segment.push_back(vCell_active.at(lCellIndex_current));
                  }
                else
                  {//headwater
                    vCell_active.at(lCellIndex_current).iSegment = iSegment_current;
                    vCell_active.at(lCellIndex_current).iFlag_first_reach = 1;
                    vReach_segment.push_back(vCell_active.at(lCellIndex_current));
                    iFlag_confluence = 1;
                  }
              }

            //this is the last reach of a segment
            std::reverse(vReach_segment.begin(), vReach_segment.end());
            cSegment.vReach_segment = vReach_segment;
            cSegment.nReach = vReach_segment.size();
            cSegment.cReach_start = vReach_segment.front();
            cSegment.cReach_end = vReach_segment.back();
            cSegment.iSegment = nSegment;
            cSegment.nSegment_upstream = cSegment.cReach_start.nUpstream;
            cSegment.iFlag_has_upstream = 1;
            cSegment.iFlag_has_downstream = 0;
            if (cSegment.cReach_start.iFlag_headwater == 1)
              {
                cSegment.iFlag_headwater = 1;
              }
            cWatershed.vSegment.push_back(cSegment);
          }

        //std::cout << iSegment_current << std::endl;
        iSegment_current = iSegment_current - 1;

        compset_tag_confluence_upstream(lCellIndex_current);

        //in fact the segment is ordered by default already, just reservely

        std::sort(cWatershed.vSegment.begin(), cWatershed.vSegment.end());
      }

    return error_code;
  }


  /**
   * find the confluence recursively from existing confluence point.
   * @param lCellIndex_confluence
   * @return
   */
  int compset::compset_tag_confluence_upstream(long lCellIndex_confluence)
  {
    int error_code = 1;

    int nUpstream;
    int iFlag_first_reach;
    int iFlag_confluence;
    int iSegment_confluence;
    long lCellID_upstream;
    long lCellIndex_upstream;
    segment cSegment; //be careful with the scope
    std::vector<long> vUpstream;
    std::vector<long>::iterator iterator_upstream;
    std::vector<hexagon> vReach_segment;

    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    if (iFlag_global != 1)
      {

        vUpstream = (vCell_active.at(lCellIndex_confluence)).vUpstream;
        iSegment_confluence = (vCell_active.at(lCellIndex_confluence)).iSegment;

        for (iterator_upstream = vUpstream.begin();
             iterator_upstream != vUpstream.end();
             iterator_upstream++)
          {
            lCellID_upstream = *iterator_upstream;
            lCellIndex_upstream =  compset_find_index_by_cellid(lCellID_upstream);
            iFlag_first_reach = 0;
            //remember that it is possible a segment only has one reach
            iFlag_confluence = vCell_active.at(lCellIndex_upstream).iFlag_confluence;

            vCell_active.at(lCellIndex_upstream).iFlag_last_reach = 1;
            //use last reach to find next stream segment

            vCell_active.at(lCellIndex_upstream).iSegment_downstream = vCell_active.at(lCellIndex_confluence).iSegment;

            vReach_segment.clear();

            //if the immediate upstream is also confluence: 1-1, we can quickly setup then move on
            //to the confluence
            if (iFlag_confluence == 1)
              {
                //continuous confluence, in this case, we need to set only one reach and move on
                nUpstream = (vCell_active.at(lCellIndex_upstream)).nUpstream;
                //we need to set 4 importnat attributes
                vCell_active.at(lCellIndex_upstream).iSegment = iSegment_current;
                (vCell_active.at(lCellIndex_upstream)).iFlag_first_reach = 1;
                //(vCell_active.at(lCellIndex_upstream)).iFlag_last_reach = 1;
                (vCell_active.at(lCellIndex_upstream)).iFlag_headwater = 0;

                vReach_segment.push_back(vCell_active.at(lCellIndex_upstream));
                //it has only one reach
                cSegment.vReach_segment = vReach_segment;
                cSegment.nReach = vReach_segment.size();
                cSegment.cReach_start = vReach_segment.front();
                cSegment.cReach_end = vReach_segment.back();
                cSegment.iSegment = iSegment_current;
                cSegment.iFlag_has_downstream = 1;
                cSegment.iFlag_has_upstream = 1;
                cSegment.iFlag_headwater = 0;
                cSegment.iSegment_downstream = iSegment_confluence;
                //add the segment to the watershed object
                cWatershed.vSegment.push_back(cSegment);
                //update segment index
                iSegment_current = iSegment_current - 1;
                compset_tag_confluence_upstream(lCellIndex_upstream);
              }
            else
              {
                //if there is at least one reach that is not a confluence: 1-0-1 or 1-0-2
                while (iFlag_confluence != 1) //1-0-1
                  {
                    //it has only one upstream
                    nUpstream = (vCell_active.at(lCellIndex_upstream)).nUpstream;
                    (vCell_active.at(lCellIndex_upstream)).iSegment = iSegment_current;
                    if (nUpstream == 0)
                      {
                        //this is the headwater, 1-0-2
                        iFlag_first_reach = 1;
                        (vCell_active.at(lCellIndex_upstream)).iFlag_first_reach = 1;
                        (vCell_active.at(lCellIndex_upstream)).iFlag_headwater = 1;
                        vReach_segment.push_back(vCell_active.at(lCellIndex_upstream));
                        break;
                      }
                    else
                      {
                        //1-0-0
                        (vCell_active.at(lCellIndex_upstream)).iFlag_last_reach = 0;
                        (vCell_active.at(lCellIndex_upstream)).iFlag_first_reach = 0;
                        (vCell_active.at(lCellIndex_upstream)).iFlag_headwater = 0;
                        vReach_segment.push_back(vCell_active.at(lCellIndex_upstream));
                        //we are on the stream segment and there is only one upstream
                        //move to upstream
                        lCellID_upstream = (vCell_active.at(lCellIndex_upstream)).vUpstream[0];
                        lCellIndex_upstream = compset_find_index_by_cellid(lCellID_upstream);
                        iFlag_confluence = vCell_active.at(lCellIndex_upstream).iFlag_confluence;
                        //should not add now
                      }
                  }
                //either we reach the headwater or we find the next confluence
                if (iFlag_first_reach == 1)
                  {
                    //it is already been pushed back
                    cSegment.iFlag_has_upstream = 0;
                    cSegment.iFlag_headwater = 1;
                  }
                else
                  {
                    //this is a new confluence, so we need to push it back
                    (vCell_active.at(lCellIndex_upstream)).iSegment = iSegment_current;
                    (vCell_active.at(lCellIndex_upstream)).iFlag_last_reach = 0;
                    (vCell_active.at(lCellIndex_upstream)).iFlag_first_reach = 1;
                    (vCell_active.at(lCellIndex_upstream)).iFlag_headwater = 0;
                    vReach_segment.push_back(vCell_active.at(lCellIndex_upstream));

                    cSegment.iFlag_has_upstream = 1;
                    cSegment.iFlag_headwater = 0;
                  }

                std::reverse(vReach_segment.begin(), vReach_segment.end());
                cSegment.vReach_segment = vReach_segment;
                cSegment.nReach = vReach_segment.size();
                cSegment.cReach_start = vReach_segment.front();
                cSegment.cReach_end = vReach_segment.back();
                cSegment.iSegment = iSegment_current;
                cSegment.iFlag_has_downstream = 1;
                cSegment.iSegment_downstream = iSegment_confluence;
                cWatershed.vSegment.push_back(cSegment);
                iSegment_current = iSegment_current - 1;

                if (iFlag_first_reach != 1)
                  {
                    compset_tag_confluence_upstream(lCellIndex_upstream);
                  }
              }
          }
      }

    return error_code;
  }

  /**
   * define subbasin boundary, it requires cell topology, so the vCell_active is used
   * @return
   */
  int compset::compset_define_subbasin()
  {
    int error_code = 1;
    int iFound_outlet;
    int iSubbasin;
    long lCellIndex_self;
    long lCellIndex_current;
    long lCellID_outlet;
    long lCellIndex_outlet; //local outlet
    long lCellID_downslope;
    long lCellIndex_downslope;
    long lCellIndex_accumulation;
    std::vector<long> vAccumulation;
    std::vector<long>::iterator iterator_accumulation;
    std::vector<hexagon> vConfluence_copy(vConfluence);
    std::vector<hexagon>::iterator iIterator_self;
    std::vector<long>::iterator iIterator_upstream;
    std::vector<hexagon>::iterator iIterator_current;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    if (iFlag_global != 1)
      {

        //the whole watershed first
        for (iIterator_self = vCell_active.begin(); iIterator_self != vCell_active.end(); iIterator_self++)
          {
            if ((*iIterator_self).iFlag_watershed == 1)
              {
                (*iIterator_self).iSubbasin = nSegment;
              }
          }

        for (iIterator_self = vConfluence.begin(); iIterator_self != vConfluence.end(); iIterator_self++)
          {
            vAccumulation.push_back((*iIterator_self).dAccumulation);
          }

        //now starting from the confluences loop
        while (vConfluence_copy.size() != 0)
          {
            iterator_accumulation = max_element(std::begin(vAccumulation), std::end(vAccumulation));
            lCellIndex_accumulation = std::distance(vAccumulation.begin(), iterator_accumulation);

            std::vector<long> vUpstream((vConfluence_copy.at(lCellIndex_accumulation)).vUpstream);

            for (iIterator_upstream = vUpstream.begin(); iIterator_upstream != vUpstream.end(); iIterator_upstream++)
              {
                //use the watershed method again here

                lCellID_outlet = *iIterator_upstream;
                lCellIndex_outlet = compset_find_index_by_cellid(lCellID_outlet);

                iSubbasin = (vCell_active.at(lCellIndex_outlet)).iSegment;
                (vCell_active.at(lCellIndex_outlet)).iSubbasin = iSubbasin;

                for (iIterator_self = vCell_active.begin(); iIterator_self != vCell_active.end(); iIterator_self++)           
                  {
                    iFound_outlet = 0;
                    lCellIndex_current =  (*iIterator_self).lCellIndex;      
                    while (iFound_outlet != 1)
                      {                        
                        lCellID_downslope = vCell_active.at(lCellIndex_current).lCellID_downslope_dominant;                        
                        if (lCellID_outlet == lCellID_downslope)
                          {
                            iFound_outlet = 1;
                            (*iIterator_self).iSubbasin = iSubbasin;
                          }
                        else
                          {
                            lCellIndex_current = compset_find_index_by_cellid(lCellID_downslope);
                            if (lCellIndex_current== -1)
                            {
                                //this one does not belong in this watershed
                                iFound_outlet = 1;
                            }
                            else
                            {
                              lCellID_downslope = vCell_active.at(lCellIndex_current).lCellID_downslope_dominant;
                              if (lCellID_downslope == -1)
                              {
                                //this is the outlet
                                iFound_outlet = 1;
                              }
                              else
                              {
                                //std::cout << lCellID_downslope << std::endl;
                              }
                            }
                            
                          }
                      }
                  }
              }

            //remove the confluence now
            vAccumulation.erase(iterator_accumulation);
            vConfluence_copy.erase(vConfluence_copy.begin() + lCellIndex_accumulation);
            //repeat
          }

        //assign watershed subbasin cell
        cWatershed.vSubbasin.clear();
        for (int iSubbasin = 1; iSubbasin <= nSegment; iSubbasin++)
          {
            subbasin cSubbasin;
            cSubbasin.iSubbasin = iSubbasin;
            cWatershed.vSubbasin.push_back(cSubbasin);
          }
        for (iIterator_self = vCell_active.begin(); iIterator_self != vCell_active.end(); iIterator_self++)
          {
            int iSubbasin = (*iIterator_self).iSubbasin;
            if (iSubbasin >= 1 && iSubbasin <= nSegment)
              {
                (cWatershed.vSubbasin[iSubbasin - 1]).vCell.push_back(*iIterator_self);
              }
            else
              {
                if (iSubbasin != -1)
                  {
                    std::cout << "Something is wrong" << std::endl;
                  }
              }
          }
      }
    return error_code;
  }

  /**
   * @brief 
   * 
   * @return int 
   */

  int compset::compset_calculate_watershed_characteristics()
  {
    int error_code = 1;
    int iFlag_global = cParameter.iFlag_global;
    int iFlag_multiple_outlet = cParameter.iFlag_multiple_outlet;
    if (iFlag_global != 1)
      {
        cWatershed.calculate_watershed_characteristics();
      }
    else
      {

      }
    return error_code;
  }

/**
 * @brief 
 * 
 * @return int 
 */
  int compset::update_cell_elevation()
  {
    int error_code = 1;
    std::vector<hexagon>::iterator iIterator1;
    for (iIterator1 = vCell_active.begin(); iIterator1 != vCell_active.end(); ++iIterator1)
      {
         (*iIterator1).update_location();
      }
    return error_code;
  }

  /**
   * @brief 
   * 
   * @return int 
   */
  int compset::update_vertex_elevation()
  {
    int error_code = 1;
    long lVertexIndex = 0;
    std::vector<hexagon>::iterator iIterator1;
    std::vector<vertex>::iterator iIterator2;
    std::vector<vertex>::iterator iIterator3;

    for (iIterator2 = vVertex_active.begin(); iIterator2 != vVertex_active.end(); ++iIterator2)
    {
    
      for (iIterator1 = vCell_active.begin(); iIterator1 != vCell_active.end(); ++iIterator1)
      {          
         iIterator3 = std::find((*iIterator1).vVertex.begin(), (*iIterator1).vVertex.end(), ( *iIterator2 ));

          if (iIterator3 != (*iIterator1).vVertex.end())
            {
              //found
              (*iIterator2).dElevation = (*iIterator1).dElevation_mean;
              //update location too
              (*iIterator2).update_location();
              break;
            }
            else
            {
            }
      }

    }
      
    
    return error_code;
  }

}
